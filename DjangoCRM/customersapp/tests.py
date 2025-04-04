"""
Модуль для тестирования функций приложения CustomersApp
Созданные роли:
    - admin - Админ
    - Svetlana - Менеджер
    - Irina - Operator
"""

import random

from adsapp.models import Ad
from contractsapp.models import Contract
from customersapp.models import Customer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from leadsapp.models import Lead
from productapp.models import Product


class AuthenticatedTestCase(TestCase):
    """Аутентификация пользователя и загрузка фикстур"""

    fixtures = [
        "fixtures/fixtures.xml",
    ]

    def setUp(self):
        """Логинимся от имени менеджера"""
        self.client.login(username="admin", password="admin")


class CreateCustomerTestCase(AuthenticatedTestCase):
    """Проверка создания клиента"""

    def setUp(self):
        super().setUp()
        self.ad = Ad.objects.filter(
            id=1
        ).first()  # получаем рекламную компанию для создания лида
        self.lead = Lead.objects.create(
            full_name="Станислав Ди Каприо",
            phone_number="+79008964532",
            email="stas.bezOskarat@yandex.ru",
            ad=self.ad,
        )  # создаём лида

        # загружаем файл для загрузки
        test_file = SimpleUploadedFile(
            "../requirements.txt", b"Test file content", content_type="text/plain"
        )
        self.product = Product.objects.filter(id=3).first()  # получаем услугу с id = 3
        self.contract = Contract.objects.create(
            title="Контракт для Ди каприо",
            product=self.product,
            document=test_file,  # Передаём файл
            date_signed="2025-03-12",
            valid_until="2025-03-23",
            cost=100,
        )  # создаём контракт
        self.client.logout()  # разлогиниваемся от имени админа
        self.client.login(username="Svetlana", password="Abc9517850219")

    def tearDown(self):
        """Удаляем после теста"""
        self.lead.delete()
        self.contract.delete()

    def test_create_customers(self) -> None:
        """
        Тест на создание и добавление в БД клиента
        """

        response = self.client.post(
            reverse("customersapp:customers_create"),
            {"lead": self.lead.id, "contract": self.contract.id},
        )
        self.assertRedirects(response, reverse("leadsapp:leads_list"))
        self.assertTrue(Customer.objects.filter(lead__id=self.lead.id).exists())

    def test_negative_create_customers(self) -> None:
        """
        Отрицательный тест на создание клиента
        """

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username="Irina", password="Abc9002973474")

        # Пробуем создать клиент
        response = self.client.post(
            reverse("customersapp:customers_create"),
            {"lead": self.lead.id, "contract": self.contract.id},
        )
        self.assertEqual(response.status_code, 403)


class DetailCustomerTestCase(AuthenticatedTestCase):
    """Проверка просмотра деталей клиента"""

    def test_get_detail_customers(self):
        """Тест на просмотр деталей клиента"""

        response = self.client.get(
            reverse("customersapp:customers_detail", kwargs={"pk": 1}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сигал Стивен Петрович")

    def test_negative_get_detail_customers(self):
        """Негативный тест на просмотр деталей клиента"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Менеджера
        self.client.login(username="Svetlana", password="Abc9517850219")

        # Отправляем запрос на просмотр клиента
        response = self.client.get(
            reverse("customersapp:customers_detail", kwargs={"pk": 1}),
        )
        self.assertNotEqual(response.status_code, 200)


class CustomerListTestCase(AuthenticatedTestCase):
    """Проверка просмотра списка клиентов"""

    def test_list_customers(self):
        """Тест на просмотр списка клиентов"""
        response = self.client.get(reverse("customersapp:customers_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customersapp/customers_list.html")
        self.assertQuerysetEqual(
            qs=list(Customer.objects.all()),
            values=(c.pk for c in response.context["customers"]),
            transform=lambda c: c.pk,
        )

    def test_negative_list_customers(self):
        """Негативный тест на просмотр списка клиентов"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Менеджера
        self.client.login(username="Svetlana", password="Abc9517850219")

        # Отправляем запрос на просмотр клиентов
        response = self.client.get(reverse("customersapp:customers_list"))
        self.assertEqual(response.status_code, 403)


class UpdateCustomerTestCase(AuthenticatedTestCase):
    """Проверка обновления клиента"""

    def setUp(self):
        super().setUp()
        self.lead = Lead.objects.filter(id=3).first()  # получаем лида с id = 3
        self.contract = Contract.objects.filter(
            id=10
        ).first()  # получаем контракт с id = 10

    def test_update_customers(self):
        """Тест на обновление клиента"""

        response = self.client.post(
            reverse("customersapp:customers_update", kwargs={"pk": 1}),
            {"lead": self.lead.id, "contract": self.contract.id},
        )
        self.assertRedirects(
            response, reverse("customersapp:customers_detail", kwargs={"pk": 1})
        )
        self.assertTrue(
            Customer.objects.filter(Q(pk=1) & Q(contract=self.contract.id)).exists()
        )

    def test_negative_update_customers(self):
        """Негативный тест на обновление клиента"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username="Irina", password="Abc9002973474")

        response = self.client.post(
            reverse("customersapp:customers_update", kwargs={"pk": 1}),
            {"lead": self.lead.id, "contract": self.contract.id},
        )
        self.assertNotEqual(response.status_code, 200)


class DeleteCustomerTestCase(AuthenticatedTestCase):
    """Проверка удаления клиента"""

    def test_delete_customers(self):
        """Тест на удаление клиента"""

        # Отправляем запрос на удаление клиента
        response = self.client.post(
            reverse("customersapp:customers_delete", kwargs={"pk": 7}),
        )
        self.assertRedirects(response, "/customers/")

        # Проверяем, что клиент удален
        self.assertFalse(Customer.objects.filter(pk=7).exists())

    def test_negative_delete_customers(self):
        """Негативный тест на удаление клиента"""

        self.client.logout()  # выполняем выход от администратора
        self.client.login(
            username="Svetlana", password="Abc9517850219"
        )  # выполняем вход от Менеджера
        response = self.client.post(
            reverse("customersapp:customers_delete", kwargs={"pk": 7}),
        )

        # Получаем ошибку удаления из-за нехватки прав
        self.assertEqual(response.status_code, 403)
