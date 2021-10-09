from django.urls import re_path
from . import consumers

websockets_urls = [
    re_path(r'ws/social/(?P<room_name>\w+)/$', consumers.SocialConsumer),
]