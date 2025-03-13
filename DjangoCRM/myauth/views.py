from django.contrib.auth.views import LogoutView
from django.http import HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class MyLogoutView(LogoutView):
    """Класс для разлогирования пользователя"""

    next_page = reverse_lazy("myauth:login")

    def dispatch(self, request, *args, **kwargs):
        """Метод для того чтобы пользователь мог разлогиниться по методу GET"""
        if request.method == "GET":
            return self.post(request, *args, **kwargs)
        return HttpResponseNotAllowed(["GET", "POST"])


class AboutMe(TemplateView):
    """Класс для отображения информации о пользователе"""

    template_name = "myauth/about_me.html"
