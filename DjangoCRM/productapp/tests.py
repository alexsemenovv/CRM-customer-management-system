"""
Модуль для тестирования функций приложения ProductApp
Созданные роли:
    - admin - Админ
    - Irina - Оператор
    - Evgeniy - Маркетолог
"""

import random

from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from productapp.models import Product


class AuthenticatedTestCase(TestCase):
    """Аутентификация пользователя и загрузка фикстур"""

    fixtures = [
        "fixtures/fixtures.xml",
    ]

    def setUp(self):
        """Логинимся от имени маркетолога"""
        self.client.login(username="Evgeniy", password="Abc9517850219")


class CreateProductTestCase(AuthenticatedTestCase):
    """Проверка создания услуги"""

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
            },
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
        self.client.login(username="Irina", password="Abc9002973474")

        # Пробуем создать продукт
        response = self.client.post(
            reverse("productapp:products_create"),
            {
                "name": "Негативный тест",
                "description": "Тест",
                "price": 1000,
            },
        )
        self.assertEqual(response.status_code, 403)


class DetailProductTestCase(AuthenticatedTestCase):
    """Проверка просмотра деталей услуги"""

    def test_get_detail_product(self):
        """Тест на просмотр деталей услуги"""
        response = self.client.get(
            reverse("productapp:products_detail", kwargs={"pk": 6}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Услуга номер 4")

    def test_negative_get_detail_product(self):
        """Негативный тест на просмотр деталей услуги"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username="Irina", password="Abc9002973474")

        # Отправляем запрос на просмотр услуги
        response = self.client.get(
            reverse("productapp:products_detail", kwargs={"pk": 6}),
        )
        self.assertNotEqual(response.status_code, 200)


class ProductListTestCase(AuthenticatedTestCase):
    """Проверка просмотра списка услуг"""
    def test_list_product(self):
        """Тест на просмотр списка услуг"""
        response = self.client.get(reverse("productapp:products_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "productapp/products_list.html")
        self.assertQuerysetEqual(
            qs=list(Product.objects.all()),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )

    def test_negative_list_product(self):
        """Негативный тест на просмотр списка услуг"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username="Irina", password="Abc9002973474")

        # Отправляем запрос на просмотр услуг
        response = self.client.get(reverse("productapp:products_list"))
        self.assertEqual(response.status_code, 403)


class UpdateProductTestCase(AuthenticatedTestCase):
    """Проверка обновления услуг"""

    def test_update_product(self):
        """Тест на обновление услуги"""
        random_number = random.randint(1, 10000)
        response = self.client.post(
            reverse("productapp:products_update", kwargs={"pk": 6}),
            {"name": "Test", "price": random_number},
        )
        self.assertRedirects(
            response, reverse("productapp:products_detail", kwargs={"pk": 6})
        )
        self.assertTrue(
            Product.objects.filter(Q(pk=6) & Q(price=random_number)).exists()
        )

    def test_negative_update_product(self):
        """Негативный тест на обновление услуги"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username="Irina", password="Abc9002973474")

        # Отправляем запрос на обновление услуги
        response = self.client.post(
            reverse("productapp:products_update", kwargs={"pk": 6}),
            {"name": "Test", "price": 1},
        )
        self.assertNotEqual(response.status_code, 200)


class DeleteProductTestCase(AuthenticatedTestCase):
    """Проверка удаления услуги"""

    def setUp(self):
        """Добавляем новую услугу"""
        super().setUp()
        Product.objects.create(
            name="Test for delete",
            description="None",
            price=0,
        )
        self.product = Product.objects.filter(price=0).first()

    def test_negative_delete_product(self):
        """Негативный тест на удаление услуги"""
        response = self.client.post(
            reverse("productapp:products_delete", kwargs={"pk": self.product.pk}),
        )

        # Получаем ошибку удаления из-за нехватки прав
        self.assertEqual(response.status_code, 403)

    def test_delete_product(self):
        """Тест на удаление услуги"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Администратора
        self.client.login(username="admin", password="admin")

        # Отправляем запрос на удаление услуги
        response = self.client.post(
            reverse("productapp:products_delete", kwargs={"pk": self.product.pk}),
        )
        self.assertRedirects(response, "/products/")

        # Проверяем, что заказ удален
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
