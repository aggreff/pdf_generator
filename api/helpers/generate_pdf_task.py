from rest_framework.exceptions import ValidationError
from weasyprint.urls import URLFetchingError
from django.utils.translation import ugettext_lazy as _


def get_task_result(task):
    try:
        task_result = task.get()
    except URLFetchingError:
        raise ValidationError({'common': _('Please check that site is available')})
    except Exception:
        raise ValidationError(
            {'common': _('Unfortunately we can`t generate pdf for you now, please try later or contact us')})
    return task_result
