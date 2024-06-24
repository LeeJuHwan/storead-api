from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView

from .mixins import APIViewResponseMixin
from .paginations import CommonCursorPagination


class BaseAPIView(APIView, APIViewResponseMixin):
    """
    Create a base API view that combines APIView and APIViewResponseMixin
    Custom API View to handle all the common logic for all APIs
    """


class BaseGenericView(GenericAPIView, APIViewResponseMixin):
    """
    Base API view that inherits from GenericAPIView and includes custom response mixins.
    """


class BaseListAPIView(BaseAPIView, ListAPIView):
    """
    Base List API view that inherits from BaseAPIView and ListAPIView.
    Includes cursor pagination using CommonCursorPagination.
    """

    pagination_class: CursorPagination = CommonCursorPagination

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Custom list view method to handle list requests.
        Args:
            request (Request): The incoming request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Response: {
                "status_code": int,
                "status": bool,
                "message": Optional[str],
                "data": Any
            }
        """
        queryset: QuerySet = self.filter_queryset(self.get_queryset())
        page: Response = self.paginate_queryset(queryset)

        serializer: Serializer | ModelSerializer = self.get_serializer(page, many=True)
        pagenated_response: Response = self.get_paginated_response(serializer.data)
        return self.success_response(data=pagenated_response.data, status_code=status.HTTP_200_OK)
