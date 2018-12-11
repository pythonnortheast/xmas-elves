from rest_framework import pagination


class ResultsPaginator(pagination.LimitOffsetPagination):
    """
    Only return the results themselves and no extra structure.

    Works like LimitOffsetPagination.
    """

    def get_paginated_response(self, data):
        """
        Return the results in data.
        """
        return data
