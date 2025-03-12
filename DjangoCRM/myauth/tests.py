"""
Модуль для тестирования функций приложения My Auth App
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view_get(self):
        response = self.client.get(reverse('myauth:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Авторизация')  # Проверяем, что страница содержит форму входа

    def test_logout_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('myauth:logout'))
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после выхода
        self.assertEqual(response.url, reverse('myauth:login'))

    def test_about_me_view_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('myauth:about_me'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Обо мне')  # Проверяем, что страница загружается

    def test_about_me_view_not_logged_in(self):
        response = self.client.get(reverse('myauth:about_me'))
        self.assertEqual(response.status_code, 200)  # Должен быть редирект на страницу входа
        self.assertContains(response, 'Анонимный пользователь')  # Проверяем, что страница загружается
