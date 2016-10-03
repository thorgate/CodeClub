from __future__ import absolute_import

from celery import shared_task

from challenges.models import Solution


@shared_task
def validate_solution(solution_id):
    try:
        solution = Solution.objects.get(id=solution_id, status=Solution.STATUS_SUBMITTED)
    except Solution.DoesNotExist:
        return None

    solution.status = Solution.STATUS_IN_PROGRESS
    solution.save()

    status, output = solution.check_solution()
    solution.status = status
    solution.output = output
    solution.save()
    solution.challenge.clear_cache_hash()

    return solution
