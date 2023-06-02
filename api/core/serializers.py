from rest_framework import serializers


class ExceptionMessageSerializer(serializers.Serializer):
    detail = serializers.CharField(allow_null=True)
    non_field_errors = serializers.ListField(
        child=serializers.CharField(),
        allow_null=True
    )
    field_errors = serializers.ListField(
        allow_null=True,
        child=serializers.CharField(),
        help_text=(
            'Errors can be generated for each field from the request (there can be several!). '
            'The field name will match the field from the request.'
        )
    )



class ExceptionSerializer(serializers.Serializer):
    message = ExceptionMessageSerializer(read_only=True)
    type = serializers.CharField(read_only=True)  # noqa: WPS125