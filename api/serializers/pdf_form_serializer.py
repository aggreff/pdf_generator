from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class PdfFormSerializer(serializers.Serializer):
    url = serializers.URLField(required=False)
    file = serializers.FileField(required=False)

    def validate(self, data):
        errors = dict()
        url, file = data.get('url'), data.get('file')
        if not url and not file:
            errors.update({'common': _('Please provide url or HTML file!')})
        elif url and file:
            errors.update({'common': _('Please choose only one!')})
        if errors:
            raise serializers.ValidationError(errors)
        return data
