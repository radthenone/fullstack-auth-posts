import logging

from django.conf import settings


class CustomLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(
            getattr(settings, "loggers", "django.request-response")
        )

    def __call__(self, request):
        if (
            request.content_type == "application/json"
            or request.content_type == "text/html"
        ):
            self.logger.info(
                f"""
                Incoming request: {request.method} {request.META["HTTP_HOST"]}{request.path}\n
                Headers: {request.headers}\n
                GET: {request.GET}\n
                POST: {request.POST}\n
                Content type: {request.content_type}\n
                Cookies: {request.COOKIES}\n
                Files: {request.FILES}\n
                """
            )
            response = self.get_response(request)
            self.logger.info(
                f"""
                Outgoing response: {response.status_code}\n
                Serialize: {response.serialize}\n
                Headers: {response.headers}\n
                Render: {response.render}\n
                Content type: {response.content_type}\n
                Cookies: {response.cookies}\n
                Data: {response.data}\n
                """
            )
        else:
            self.logger.info(
                f"""
                Incoming request: {request.method} {request.META["HTTP_HOST"]}{request.path}\n
                Headers: {request.headers}\n
                GET: {request.GET}\n
                POST: {request.POST}\n
                Content type: {request.content_type}\n
                Cookies: {request.COOKIES}\n
                Files: {request.FILES}\n
                """
            )
            response = self.get_response(request)
        return response

    def process_view(self, view_func, view_args, view_kwargs):
        self.logger.info(
            f"Processing view: {view_func.__module__}.{view_func.__name__} \
             with {view_args} and {view_kwargs}"
        )
        return None

    def process_response(self, response):
        self.logger.info(
            f"""
            Processing response: {response.status_code}\n
            Serialize: {response.serialize}\n
            Headers: {response.headers}\n
            Content type: {response.content_type}\n
            Cookies: {response.cookies}\n
            Data: {response.data}\n
            """
        )
        return response

    def process_request(self, request):
        self.logger.info(
            f"""
            Incoming request: {request.method} {request.path}\n
            Headers: {request.headers}\n
            GET: {request.GET}\n
            POST: {request.POST}\n
            Content type: {request.content_type}\n
            Cookies: {request.COOKIES}\n
            Files: {request.FILES}\n
            """
        )
        return request

    def process_exception(self, exception):
        self.logger.exception(exception)
        return None
