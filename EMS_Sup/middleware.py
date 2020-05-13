#This file makes all pages except the login page get redirected to the login page

from django.conf import settings
from django.shortcuts import redirect
import re

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LogInRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        print(path)

        if not request.user.is_authenticated:
            if not any(url.match(path) for url in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)