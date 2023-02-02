from rest_framework import pagination


class LimitPageNumberPagination(pagination.PageNumberPagination):
    "Кастомный класс пагинации."

    page_size_query_param = 'limit'
