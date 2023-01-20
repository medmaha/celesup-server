from django.urls import path
from .notifications_list import NotificationList
from .notification_viewed import NotificationViewed


notifications_url_patterns = [
    path("notifications", NotificationList.as_view()),
    path("notifications/viewed", NotificationViewed.as_view()),
]
