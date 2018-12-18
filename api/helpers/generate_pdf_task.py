from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError, APIException
from weasyprint.urls import URLFetchingError


def get_task_result(task):
    """
    Tried to get celery generate pdf task results or return error using api.
    :param task: AsyncTaskResult instance
    :return: Filename of pdf file
    """
    try:
        task_result = task.get()
    except URLFetchingError:
        raise ValidationError({'common': _('Please check that site is available')})
    except Exception:
        raise APIException(
            {'common': _('Unfortunately we can`t generate pdf for you now, please try later or contact us')})
    return task_result
