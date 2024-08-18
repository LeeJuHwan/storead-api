import logging
import time

from django.utils.deprecation import MiddlewareMixin
from django.db import connection
from django.conf import settings


log = logging.getLogger("django")


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        self.start_time = time.time()  # noqa
        log.info(f"Request: {request.get_full_path()} request {request.META.get('REMOTE_ADDR')}")

    def process_response(self, request, response):
        try:
            remote_addr = request.META.get("REMOTE_ADDR")
            response_tag = "FAIL" if response.status_code >= 400 else "SUCCESS"
            user_name = "-"
            extra_log = ""
            err_msg = ""
            response_data = getattr(response, "data", {})

            if hasattr(request, "user"):
                user_name = getattr(request.user, "username", "-")

            if err_detail := response_data.get("data", {}).get("message"):
                err_msg += f"error message: {err_detail}"

            req_time = time.time() - self.start_time

            if settings.DEBUG:
                sql_time = sum(float(q["time"]) for q in connection.queries) * 1000
                extra_log += f"({len(connection.queries)} SQL queries, {sql_time} ms)"

            log_content = {
                "message": f"Response: [{response_tag}] -",
                "api_domain": f"{remote_addr}{request.get_full_path()} ({request.method}|{response.status_code})",
                "result": f"- response time: {req_time:.2f} seconds{extra_log} {err_msg} / user: {user_name}",
            }

            self._display_log(response_tag)(" ".join([log_data for log_data in log_content.values()]))

        except Exception as e:
            log.error(f"LoggingMiddleware Error: {e}")
        return response

    @staticmethod
    def _display_log(response_status_name):
        if response_status_name == "FAIL":
            return log.error

        return log.info
