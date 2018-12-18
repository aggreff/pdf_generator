from urllib.parse import urlparse

from django.utils.crypto import get_random_string

from common.constants import TYPE_FILE


def generate_filename(file_or_url, data_type):
    """
    Generate unique pdf filename based on html filename or giving url.Generated filename includes uuid.
    :param file_or_url: Uploaded file or web url
    :param data_type: Describe type of first param.
    :return:
    """
    uuid = get_random_string(8).lower()
    if data_type == TYPE_FILE:
        return file_or_url.name.replace('.html', '_{}.pdf'.format(uuid))
    else:
        return "{}_{}.pdf".format(urlparse(file_or_url).hostname, uuid)
