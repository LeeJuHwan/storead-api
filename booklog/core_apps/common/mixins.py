import logging

from rest_framework import status
from rest_framework.response import Response

from .constants import FAILURE, SUCCESS

logger = logging.getLogger("django")


class APIViewResponseMixin:
    """
    Mixin to customize the response format
    """

    @classmethod
    def success_response(cls, data=None, message=None, status_code=status.HTTP_200_OK):
        """
        Returns Success Response
        """
        response_data = {"status_code": status_code, "status": SUCCESS, "results": {}}
        if message is not None:
            response_data["results"]["message"] = message
        if data is not None:
            response_data["results"]["data"] = data

        logger.info(f"Response: {response_data}")

        return Response(response_data, status=status_code)

    @classmethod
    def fail_response(cls, data=None, message=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Returns Failure Response
        """
        response_data = {
            "status_code": status_code,
            "status": FAILURE,
            "results": {},
        }
        if message is not None:
            response_data["results"]["message"] = message
        if data is not None:
            response_data["results"]["data"] = data

        print(f"message: {message}")
        print(f"response data: {response_data}")
        return Response(response_data, status=status_code)
