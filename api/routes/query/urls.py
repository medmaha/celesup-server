from .search_query import Searching
from django.urls import path


query_url_patterns = [path("search_query", Searching.as_view())]
