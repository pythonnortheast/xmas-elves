from rest_framework import pagination, response


class ResultsPaginator(pagination.LimitOffsetPagination):
    """
    Only return the results themselves and no extra structure.

    Works like LimitOffsetPagination.
    """

    default_limit = 100
    max_limit = 200

    def get_paginated_response(self, data):
        """
        Return the results in data.
        """
        return response.Response(data)
