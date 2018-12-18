from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _
from pydash import at
from rest_framework import serializers


class PdfFormSerializer(serializers.Serializer):
    url = serializers.URLField(required=False)
    file = serializers.FileField(required=False, validators=[FileExtensionValidator(allowed_extensions=['html'])])

    def validate(self, data):
        errors = dict()
        url, file = at(data, 'url', 'file')
        if not url and not file:
            errors.update({'common': _('Please provide url or HTML file!')})
        elif url and file:
            errors.update({'common': _('Please choose only one!')})
        if errors:
            raise serializers.ValidationError(errors)
        return data
