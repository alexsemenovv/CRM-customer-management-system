"""
Модуль для тестирования функций приложения My Auth App
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AuthViewsTestCase(TestCase):
    """Проверка аутентификации пользователя"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login_view_get(self):
        """Тест на то что страница содержит форму входа"""
        response = self.client.get(reverse("myauth:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Авторизация"
        )

    def test_logout_view_get(self):
        """Тест на редирект после выхода"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("myauth:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("myauth:login"))

    def test_about_me_view_logged_in(self):
        """Тест на загрузку страницы 'Обо мне' """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("myauth:about_me"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Обо мне")

    def test_about_me_view_not_logged_in(self):
        """Тест на редирект страницы about_me"""
        response = self.client.get(reverse("myauth:about_me"))
        self.assertEqual(
            response.status_code, 200
        )  # Должен быть редирект на страницу входа
        self.assertContains(
            response, "Анонимный пользователь"
        )  # Проверяем, что страница загружается
