from logging import getLogger

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from {{cookiecutter.project_slug}}.libs.views import (
    handle_api_errors, pick_request_data, respond, respond_json
)

LOGGER = getLogger(__name__)


class MyView(View):

    def get(self, request, *args, **kwargs):
        return respond('Hello world!')


@method_decorator(csrf_exempt, name='dispatch')
class MyApiView(View):

    @method_decorator(
        [handle_api_errors,
         pick_request_data('title', 'content')]
    )
    def post(self, request, app_name, title, content):
        return respond_json(
            {'app': {
                'name': app_name,
                'title': title,
                'content': content
            }},
            status=201
        )
