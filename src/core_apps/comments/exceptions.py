from rest_framework import status
from rest_framework.exceptions import APIException


class CommentPermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"


class CommentNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Comment not found"
    default_code = "not_found"
