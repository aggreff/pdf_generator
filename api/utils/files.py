from urllib.parse import urlparse

from django.utils.crypto import get_random_string

from common.constants import TYPE_FILE


def generate_filename(file_or_url, data_type):
    uuid = get_random_string(8).lower()
    if data_type == TYPE_FILE:
        filename = file_or_url.name.replace('.html', '.pdf')
        return "{0}_{2}.{1}".format(*filename.rsplit('.', 1), uuid)
    else:
        return "{}_{}.pdf".format(urlparse(file_or_url).hostname, uuid)
