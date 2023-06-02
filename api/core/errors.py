class BaseIntegrationError(Exception):
    pass


class ValidateResponseError(BaseIntegrationError):
    pass


class RestClientError(BaseIntegrationError):
    def __init__(self, message, response=None, request_kwargs=None):
        self.message = message
        self.response = response
        self.request_kwargs = request_kwargs

    def __str__(self):
        return """
        Message: {message}
        Response: code={code} content={content}
        Request: request_kwargs={request_kwargs}
        """.format(
            message=self.message,
            code=self.response.status_code if self.response else 'Нет ответа',
            content=self.response.content if self.response else 'Нет ответа',
            request_kwargs=self.request_kwargs,
        )

    __repr__ = __str__
