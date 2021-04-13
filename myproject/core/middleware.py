from myproject import urls
from django.shortcuts import redirect
import re

pattern = re.compile('^/admin/.*?')
custom_admin_urls = urls.urlpatterns[1]


class CustomAdminPermissionMiddleWare:

    def __init__(self, get_response):
        self.response = get_response

    def __call__(self, request):
        return self.response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser and pattern.match(request.path_info):
                return redirect('/custom-admin')