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
        response_data = {
            "status": SUCCESS,
            "status_code": status_code,
            "results": {
                "message": message,
                "data": data or None,
                # **(data or {"data": None})
            },
        }
        return Response(response_data, status=status_code)

    @classmethod
    def fail_response(cls, data=None, message=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Returns Failure Response
        """
        response_data = {
            "status": FAILURE,
            "status_code": status_code,
            "data": {"message": message, **(data or {"data": None})},
        }
        return Response(response_data, status=status_code)


class SerializerErrorMessageMixin:
    """
    Serializer의 Validator error내용 언패킹
    """

    @property
    def errors(self) -> str:
        error_dict = super().errors

        error_messages = []
        for error_message in error_dict.values():
            if isinstance(error_message, list):
                for error in error_message:
                    error_messages.append(error)
            else:
                error_messages.append(error_message)

        error_string = ". ".join(error_messages)

        return error_string
