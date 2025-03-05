from django.contrib.auth.views import LogoutView
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse_lazy


class MyLogoutView(LogoutView):
    """Класс для разлогирования пользователя"""
    next_page = reverse_lazy("myauth:login")

    def dispatch(self, request, *args, **kwargs):
        """Метод для того чтобы пользователь мог разлогиниться по методу GET"""
        if request.method == "GET":
            return self.post(request, *args, **kwargs)
        return HttpResponseNotAllowed(["GET", "POST"])
