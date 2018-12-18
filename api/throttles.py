from rest_framework.throttling import UserRateThrottle


class PdfGenerationThrottle(UserRateThrottle):
    scope = 'pdf_generation'
