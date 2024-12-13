from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = "page_size"  # Allow client to set page size
    max_page_size = 100  # Maximum page size allowed

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "previous": self.get_previous_link(),
                    "next": self.get_next_link(),
                },
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "page_size": self.page.paginator.per_page,
                "current_page": self.page.number,
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        return {
            "type": "object",
            "required": [
                "links",
                "total_items",
                "total_pages",
                "page_size",
                "current_page",
                "results",
            ],
            "properties": {
                "links": {
                    "type": "object",
                    "required": ["previous", "next"],
                    "properties": {
                        "previous": {
                            "type": "string",
                            "nullable": True,
                            "format": "uri",
                            "example": "http://api.example.org/accounts/?{page_query_param}=2".format(
                                page_query_param=self.page_query_param
                            ),
                        },
                        "next": {
                            "type": "string",
                            "nullable": True,
                            "format": "uri",
                            "example": "http://api.example.org/accounts/?{page_query_param}=4".format(
                                page_query_param=self.page_query_param
                            ),
                        },
                    },
                },
                "total_items": {
                    "type": "integer",
                    "example": 10,
                },
                "total_pages": {
                    "type": "integer",
                    "example": 1,
                },
                "page_size": {
                    "type": "integer",
                    "example": 10,
                },
                "current_page": {
                    "type": "integer",
                    "example": 1,
                },
                "results": schema,
            },
        }
