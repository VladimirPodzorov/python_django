from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
import time

from requestdataapp.views import error_req_count


def set_useragent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print(f'got {self.exceptions_count} exceptions so far')


class ThrottlingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0
        self.first_time = 0
        self.ip_log = {}

    def __call__(self, request: HttpRequest):
        self.count += 1
        ip = request.META.get('REMOTE_ADDR')
        if ip not in self.ip_log.keys():
            self.first_time = time.time()
            self.ip_log[ip] = {'first_time': self.first_time, 'count': self.count}
        else:
            self.ip_log[ip]['count'] = self.count
            if self.count > 5:
                last_time = time.time()
                if last_time - self.first_time < 180:
                    return error_req_count(request)
                else:
                    self.count = 0
                    self.first_time = last_time

        response = self.get_response(request)

        return response
