from pdf_generator.settings import MEDIA_ROOT


def get_pdf_file_path(filename):
    return MEDIA_ROOT + filename
