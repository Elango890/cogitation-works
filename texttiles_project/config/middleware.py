import logging
import traceback
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("app")


class ExceptionLoggingMiddleware(MiddlewareMixin):
    """
    Logs all unhandled exceptions with full request & user details
    """

    def process_exception(self, request, exception):
        user = getattr(request, "user", None)

        logger.error(
            "UNHANDLED EXCEPTION\n"
            f"User: {user if user and user.is_authenticated else 'Anonymous'}\n"
            f"Path: {request.path}\n"
            f"Method: {request.method}\n"
            f"IP: {self.get_client_ip(request)}\n"
            f"Exception: {str(exception)}\n"
            f"Traceback:\n{traceback.format_exc()}"
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
