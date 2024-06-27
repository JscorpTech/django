from django import shortcuts
from django import views as django_views


class HomeView(django_views.View):
    def get(self, request):
        return shortcuts.render(request, "user/home.html")
