import json
import logging

from django.conf import settings
from django.template.response import TemplateResponse
from rest_framework.response import Response


class CustomLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(getattr(settings, "loggers", ""))

    def __call__(self, request):
        path = f"{request.scheme}://{request.META['HTTP_HOST']}{request.path}"
        path_list = path.split("/")
        if all(["__debug__" in path_list, "history_sidebar" in path_list]):
            response = self.get_response(request)
        else:
            if request.content_type == "application/json":
                self.logger.info(
                    "REQUEST////////////////////////////////////////////////////////"
                )
                self.logger.info(f"Request USER: {request.user}")
                self.process_request(request=request, path=path)
                self.logger.info(
                    "RESPONSE////////////////////////////////////////////////////////"
                )
                response = self.get_response(request)
                self.process_response(response=response)
            else:
                self.logger.info(
                    "REQUEST////////////////////////////////////////////////////////"
                )
                self.logger.info(f"Request USER: {request.user}")
                self.process_request(request=request, path=path)
                self.logger.info(
                    "RESPONSE////////////////////////////////////////////////////////"
                )
                response = self.get_response(request)
                if isinstance(response, TemplateResponse):
                    self.logger.info(response.rendered_content)
                if isinstance(response, Response):
                    self.logger.info(json.dumps(response.data, indent=2))
        return response

    def process_response(self, response):  # noqa
        self.logger.info(f"Response STATUS: {response.status_code}")
        self.logger.info(f"Response SERIALIZE: {response.serialize}")
        self.logger.info(f"Response MEDIA_TYPE: {response.accepted_media_type}")
        self.logger.info(f"Response _MEDIA_TYPE: {response.charset}")
        self.logger.info(f"Response DATA: {response.data}")
        self.logger.info(f"Response COOKIES: {response.cookies}")
        self.logger.info(f"Response HEADERS: {response.headers}")

    def process_request(self, request, path=None):
        self.logger.info(f"Request URL: {path}")
        self.logger.info(f"Request METHOD: {request.method}")
        self.logger.info(f"Request GET: {request.GET}")
        self.logger.info(f"Request POST: {request.POST}")
        self.logger.info(f"Request FILES: {request.FILES}")
        self.logger.info(f"Request COOKIES: {request.COOKIES}")
        self.logger.info(f"Request HEADERS: {request.headers}")
