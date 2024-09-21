from rest_framework.pagination import PageNumberPagination


class ViewPagination(PageNumberPagination):
    """
    Пагинация при выводе списка уроков и курсов
    """
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 5
