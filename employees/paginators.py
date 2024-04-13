from rest_framework.pagination import PageNumberPagination


class EmployeePaginator(PageNumberPagination):
    """
        Пагинатор для списка сотрудников.

        Параметры:
        - page_size: Количество элементов на странице.
        - page_size_query_param: Параметр запроса, который определяет количество элементов на странице.
        - max_page_size: Максимальное количество элементов на странице, которое можно указать в параметре запроса.
        """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15
