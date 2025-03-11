"""
Модуль для тестирования функций приложений
Приложения:
    - Product app - услуги
    - Ads app - рекламные компании
    - Leads app - лиды
    - Contracts app - контракты
    - Сustomers app - клиенты
    - Myauth - приложения для аутентификации
    - Statistics app - статистика

Созданные роли:
    -  Aleksandr - Администратор
    - Irina - Оператор
    - Evgeniy - Маркетолог
    - Svetlana - Менеджер
"""

from django.test import TestCase
from django.urls import reverse

from productapp.models import Product


class CreateProductTestCase(TestCase):
    """Проверка создания услуги"""
    fixtures = [
        "fixtures/fixtures.xml",
    ]

    def setUp(self):
        """Логинимся от имени маркетолога"""
        self.client.login(username="Evgeniy", password="Abc9517850219")

    def tearDown(self):
        """Удаляем услугу после теста"""
        Product.objects.filter(name="Тестовая услуга").delete()

    def test_create_product(self) -> None:
        """
        Тест на создание и добавление в БД услуги
        """
        response = self.client.post(
            reverse("productapp:products_create"),
            {
                "name": "Тестовая услуга",
                "description": "Тестовое описание",
                "price": 1000,
            }
        )
        self.assertRedirects(response, reverse("productapp:products_list"))
        self.assertTrue(Product.objects.filter(name="Тестовая услуга").exists())

    def test_negative_create_product(self) -> None:
        """
        Отрицательный тест на создание услуги
        """

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username='Irina', password="Abc9002973474")

        # Пробуем создать продукт
        response = self.client.post(
            reverse("productapp:products_create"),
            {
                "name": "Негативный тест",
                "description": "Тест",
                "price": 1000,
            }
        )
        self.assertEqual(response.status_code, 403)


class DetailProductTestCase(TestCase):
    fixtures = [
        "fixtures/fixtures.xml",
    ]

    def setUp(self):
        """Логинимся от имени маркетолога"""
        self.client.login(username="Evgeniy", password="Abc9517850219")

    def test_get_detail_product(self):
        """Тест на просмотр деталей услуги"""
        response = self.client.get(
            reverse("productapp:products_detail",
                    kwargs={"pk": 6}
                    ),

        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Услуга номер 4")

    def test_negative_get_detail_product(self):
        """Негативный тест на просмотр деталей услуги"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username='Irina', password="Abc9002973474")

        # Отправляем запрос на просмотр услуги
        response = self.client.get(
            reverse("productapp:products_detail",
                    kwargs={"pk": 6}
                    ),

        )
        self.assertNotEqual(response.status_code, 200)
