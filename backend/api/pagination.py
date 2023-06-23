from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class FoodgramPagination(PageNumberPagination):
    page_size = settings.PAGINATION_PAGE_SIZE
    page_query_param = 'limit'
    page_size_query_param = page_query_param
