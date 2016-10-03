from django.core.management.base import BaseCommand
from challenges.models import Solution


class Command(BaseCommand):
    help = 'Checks all the solutions'

#    def add_arguments(self, parser):
#        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        solutions = Solution.objects.filter(status=Solution.STATUS_SUBMITTED)
        self.stdout.write('There are %d solutions with submitted status' % solutions.count())
        for solution in solutions:
            self.stdout.write('Checking solution %d - %s' % (solution.id, solution.user.email))
            status, output = solution.check_solution()
            solution.status = status
            solution.output = output
            solution.save()
            self.stdout.write('Done - %d' % solution.status)
