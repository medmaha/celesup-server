from django.urls import path
from .thread_list import ThreadList
from .thread_retrieve import ThreadRetrieve
from .message_list import MessageList
from .message_create import MessageCreate


messenging_url_patterns = [
    path("threads", ThreadList.as_view(), name="thread_list"),
    path("threads/retrieve", ThreadRetrieve.as_view(), name="thread_retrieve"),
    path("messages", MessageList.as_view(), name="message_list"),
    path("messages/create", MessageCreate.as_view(), name="message_create"),
]
