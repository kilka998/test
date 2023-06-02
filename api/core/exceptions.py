import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .errors import BaseIntegrationError

logger = logging.getLogger(__name__)


def rest_framework_exception_handler(exc, context):
    """Обработчик ошибок по-умолчанию для rest framework."""
    response = exception_handler(exc, context)

    logger.exception(exc)

    if not response:
        if isinstance(exc, IntegrityError):
            error_msg = """
            Кажется, существует конфликт между данными, которые вы пытаетесь сохранить,
            и вашими текущими данными. Пожалуйста, просмотрите ваши записи и попробуйте снова.
            """
            return Response(
                {
                    'message': error_msg,
                    'type': type(exc).__name__,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif isinstance(exc, BaseIntegrationError):
            error_msg = f'Ошибка при интеграции. Обратитесь к администратору. {str(exc)}'
            return Response(
                {
                    'message': {'detail': error_msg},
                    'type': type(exc).__name__,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif isinstance(exc, ValidationError):
            error_msg = exc.messages
            return Response(
                {
                    'message': {'non_field_errors': error_msg},
                    'type': type(exc).__name__,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    if response is not None and response.data:
        old_response_data = response.data
        response.data = {
            'message': old_response_data,
        }
    return response
