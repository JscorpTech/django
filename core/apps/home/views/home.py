from django import views
from django import shortcuts


class HomeView(views.View):
    def get(self, request):
        return shortcuts.render(request, "user/home.html")
