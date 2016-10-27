import logging
import math

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.utils import timezone, dateformat
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from hashids import Hashids

from codeclub.mixins import CachedModelMixin
from tg_utils.files import random_path
from tg_utils.hashmodels import ModelHashIdMixin

logger = logging.getLogger(__name__)


class SolutionEstimateField(models.IntegerField):
    description = _("Solution estimate integer")

    def formfield(self, **kwargs):
        defaults = {'min_value': 1, 'max_value': 100}
        defaults.update(kwargs)
        return super(SolutionEstimateField, self).formfield(**defaults)


class LowerHashIdsMixin(ModelHashIdMixin):

    @classmethod
    def get_hashids_object(cls):
        salt = cls.__name__ + settings.SECRET_KEY[:20]
        return Hashids(salt=salt, min_length=12, alphabet='abcdefghijklmnopqrstuvwxyz0123456789')


class Event(models.Model):
    title = models.CharField(max_length=64)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time,
            'public': self.public,
        }


class Challenge(CachedModelMixin, models.Model):
    event = models.ForeignKey(Event)

    title = models.CharField(max_length=32)
    description = models.TextField()
    public = models.BooleanField(default=True)
    author = models.ForeignKey("accounts.User")

    golf = models.BooleanField(default=False)
    network_allowed = models.BooleanField(default=False)

    tester = models.FileField(upload_to=random_path)
    requirements = models.FileField(upload_to=random_path, null=True, blank=True)
    timeout = models.FloatField(default=10)
    points = models.PositiveIntegerField()

    order = models.IntegerField(help_text="In ascending order")

    def __str__(self):
        return "{}: {}".format(self.event.title, self.title)

    def get_absolute_url(self):
        return reverse('challenge_detail', kwargs={'pk': self.id})

    @property
    def calculated_points(self):
        key_hash, created = self.get_cache_hash()
        cache_key = "calculated-points-%s-%s" % (self.id, key_hash)

        if not created:
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

        solutions = Solution.objects.filter(
            status=Solution.STATUS_CORRECT,
            estimated_points__isnull=False,
            challenge=self,
        ).order_by('user', '-timestamp').distinct('user')

        estimated_points = [s.estimated_points for s in solutions]

        if estimated_points:
            calculated_points = math.floor(sum(estimated_points) / float(len(estimated_points)))
        else:
            calculated_points = self.points

        cache.set(cache_key, calculated_points)
        return calculated_points

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author.get_display_name(),
            'public': self.public,
            'description': self.description,
            'calculated_points': self.calculated_points,
            'golf': self.golf,
        }


class Solution(LowerHashIdsMixin, models.Model):

    STATUS_SUBMITTED = 0
    STATUS_IN_PROGRESS = 10
    STATUS_TIMEOUT = 15
    STATUS_WRONG = 20
    STATUS_CORRECT = 30
    STATUS_CHOICES = (
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_TIMEOUT, 'Timed out'),
        (STATUS_WRONG, 'Wrong'),
        (STATUS_CORRECT, 'Correct'),
    )

    user = models.ForeignKey("accounts.User")
    challenge = models.ForeignKey(Challenge)

    solution = models.FileField(upload_to=random_path)
    solution_size = models.PositiveIntegerField(null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_SUBMITTED)
    timestamp = models.DateTimeField(default=timezone.now)
    output = models.TextField(blank=True)

    estimated_points = SolutionEstimateField(null=True, blank=True)

    def __str__(self):
        return "Solution for {} by {}{}".format(self.challenge, self.user, " [CORRECT]" if self.is_correct else "")

    @property
    def is_correct(self):
        return self.status == Solution.STATUS_CORRECT

    @property
    def bootstrap_class(self):
        bootstrap_classes = {
            Solution.STATUS_IN_PROGRESS: "info",
            Solution.STATUS_TIMEOUT: "warning",
            Solution.STATUS_WRONG: "danger",
            Solution.STATUS_CORRECT: "success",
        }
        return bootstrap_classes.get(self.status)

    @property
    def filename(self):
        if self.solution and hasattr(self.solution, "url"):
            filename = str(self.solution).split("/")[-1]
            return filename
        else:
            return None

    def check_solution(self):
        logger.info("Checking solution {} from user {}".format(self.id, self.user.id))
        import os
        import subprocess
        import shutil

        from django.conf import settings

        tmp_docker_root = os.path.join(os.path.dirname(settings.SITE_ROOT), 'docker_tmp', self.hashid)
        dockerfile_path = os.path.join(os.path.dirname(settings.SITE_ROOT), 'docker/Dockerfile')
        if not os.path.exists(tmp_docker_root):
            try:
                os.makedirs(tmp_docker_root)
            except OSError as e:
                solution_message = "Solution - docker dir creation failed\n{}".format(e)
                logger.error(solution_message)
                return Solution.STATUS_SUBMITTED, solution_message

        logger.info("Copying files")
        try:
            shutil.copy(dockerfile_path, os.path.join(tmp_docker_root, 'Dockerfile'))
            shutil.copy(os.path.join(settings.MEDIA_ROOT, self.challenge.tester.file.name), os.path.join(tmp_docker_root, 'tester.py'))
            shutil.copy(os.path.join(settings.MEDIA_ROOT, self.solution.file.name), os.path.join(tmp_docker_root, 'solution.py'))

            requirements_path = os.path.join(tmp_docker_root, 'requirements.txt')
            if self.challenge.requirements:
                shutil.copy(os.path.join(settings.MEDIA_ROOT, self.challenge.requirements.file.name), requirements_path)
            else:
                if os.path.isfile(requirements_path):
                    os.remove(requirements_path)
                open(requirements_path, 'a').close()
        except IOError as e:
            solution_message = "Solution - file copying failed\n{}".format(e)
            logger.error(solution_message)
            return Solution.STATUS_SUBMITTED, solution_message
        else:
            logger.info("Building image")
            solution_status = Solution.STATUS_CORRECT
            solution_message = "Correct"
            image_hash = "image{}".format(self.hashid)
            container_hash = "container{}".format(self.hashid)

            build_cmd = "docker build -t {} {}".format(image_hash, tmp_docker_root)
            try:
                output = subprocess.check_output(build_cmd, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError as e:
                solution_message = "Solution - image building failed\n{}\n{}".format(e, e.output)
                logger.error(solution_message)
                return Solution.STATUS_SUBMITTED, solution_message

            logger.info("Running container")
            run_cmd = "docker run --rm{network} --log-driver=none --name={name} {image}".format(
                network=' --network=none' if not self.challenge.network_allowed else '',
                name=container_hash,
                image=image_hash,
            )

            try:
                output = subprocess.check_output(
                    run_cmd.split(), timeout=self.challenge.timeout, stderr=subprocess.STDOUT, shell=False,
                )
            except subprocess.TimeoutExpired as e:
                try:
                    subprocess.check_output("docker stop {}".format(container_hash), stderr=subprocess.STDOUT, shell=True)
                except subprocess.CalledProcessError as f:
                    error_message = "Docker container {} stopping failed\n{}".format(container_hash, force_text(f.output))
                    logger.error(error_message)
                    solution_message += "\n{}".format(error_message)

                try:
                    subprocess.check_output("docker rm -v -f {}".format(container_hash), stderr=subprocess.STDOUT, shell=True)
                except subprocess.CalledProcessError as f:
                    error_message = "Docker container {} removing failed\n{}".format(container_hash, force_text(f.output))
                    logger.error(error_message)
                    solution_message += "\n{}".format(error_message)

                logger.info("Solution - timeout")
                # logger.info(e.output)
                solution_status = Solution.STATUS_TIMEOUT
                solution_message = "Timeout\n{}".format(force_text(e.output)[:1024])
            except subprocess.CalledProcessError as e:
                logger.info("Solution - wrong")
                logger.info(e.output)
                solution_status = Solution.STATUS_WRONG
                solution_message = "Wrong\n{}".format(force_text(e.output)[:1024])
            else:
                logger.info("Solution - correct")
                logger.info(force_text(output))
                solution_message = "Correct\n{}".format(force_text(output)[:1024])

            try:
                subprocess.check_output("docker rmi {}".format(image_hash), stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError:
                pass

            if os.path.exists(tmp_docker_root):
                try:
                    shutil.rmtree(tmp_docker_root)
                except OSError as e:
                    pass

            return solution_status, solution_message

    def serialize(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'filesize': self.solution_size,
            'url': self.solution.url,
            'timestamp': dateformat.format(self.timestamp.astimezone(timezone.get_default_timezone()), 'd. F - H:i'),
            'bootstrap_class': self.bootstrap_class,
            'status_title': self.get_status_display(),
        }
