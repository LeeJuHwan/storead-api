from rest_framework.pagination import CursorPagination


class CommonCursorPagination(CursorPagination):
    page_size = 10
    ordering = "created_at"
    cursor_query_param = "cursor"

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "required": ["results"],
            "properties": {
                "status_code": {
                    "type": "integer",
                },
                "status": {
                    "type": "boolean",
                },
                "results": schema,
                "message": {
                    "type": "string",
                },
            },
        }
