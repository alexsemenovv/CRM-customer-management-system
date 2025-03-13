"""
Модуль для тестирования функций приложения ContractsApp
Созданные роли:
    - admin - Админ
    - Svetlana - Менеджер
    - Irina - Operator
"""

import random

from contractsapp.models import Contract
from django.core.files.uploadedfile import SimpleUploadedFile
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
        """Логинимся от имени менеджера"""
        self.client.login(username="Svetlana", password="Abc9517850219")


class CreateContractTestCase(AuthenticatedTestCase):
    """Проверка создания контракта"""

    def setUp(self):
        super().setUp()
        self.product = Product.objects.filter(id=3).first()  # получаем услугу с id = 3

    def tearDown(self):
        """Удаляем контракт после теста"""
        Contract.objects.filter(title="Новый контракт").delete()

    def test_create_contracts(self) -> None:
        """
        Тест на создание и добавление в БД контракта
        """

        test_file = SimpleUploadedFile(
            "../requirements.txt", b"Test file content", content_type="text/plain"
        )

        response = self.client.post(
            reverse("contractsapp:contracts_create"),
            {
                "title": "Новый контракт",
                "product": self.product.id,
                "document": test_file,  # Передаём файл
                "date_signed": "2025-03-12",
                "valid_until": "2025-03-23",
                "cost": 99,
            },
            format="multipart",  # указываем для загрузки файлов
        )
        self.assertRedirects(response, reverse("contractsapp:contracts_list"))
        self.assertTrue(Contract.objects.filter(title="Новый контракт").exists())

    def test_negative_create_contracts(self) -> None:
        """
        Отрицательный тест на создание контракта
        """

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username="Irina", password="Abc9002973474")

        # загружаем файл для загрузки
        test_file = SimpleUploadedFile(
            "../requirements.txt", b"Test file content", content_type="text/plain"
        )

        # Пробуем создать контракт
        response = self.client.post(
            reverse("contractsapp:contracts_create"),
            {
                "title": "Новый контракт",
                "product": self.product.id,
                "document": test_file,  # Передаём файл
                "date_signed": "2025-03-12",
                "valid_until": "2025-03-23",
                "cost": 99,
            },
            format="multipart",  # указываем для загрузки файлов
        )
        self.assertEqual(response.status_code, 403)


class DetailContractTestCase(AuthenticatedTestCase):
    """Проверка просмотра деталей контракта"""

    def test_get_detail_contracts(self):
        """Тест на просмотр деталей контракта"""
        response = self.client.get(
            reverse("contractsapp:contracts_detail", kwargs={"pk": 6}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Для Александры")

    def test_negative_get_detail_contracts(self):
        """Негативный тест на просмотр деталей контракта"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username="Irina", password="Abc9002973474")

        # Отправляем запрос на просмотр контракта
        response = self.client.get(
            reverse("contractsapp:contracts_detail", kwargs={"pk": 6}),
        )
        self.assertNotEqual(response.status_code, 200)


class ContractListTestCase(AuthenticatedTestCase):
    """Проверка просмотра списка контрактов"""

    def test_list_contracts(self):
        """Тест на просмотр списка контрактов"""
        response = self.client.get(reverse("contractsapp:contracts_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contractsapp/contracts_list.html")
        self.assertQuerysetEqual(
            qs=list(Contract.objects.all()),
            values=(c.pk for c in response.context["contracts"]),
            transform=lambda c: c.pk,
        )

    def test_negative_list_contracts(self):
        """Негативный тест на просмотр списка контрактов"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username="Irina", password="Abc9002973474")

        # Отправляем запрос на просмотр контрактов
        response = self.client.get(reverse("contractsapp:contracts_list"))
        self.assertEqual(response.status_code, 403)


class UpdateContractTestCase(AuthenticatedTestCase):
    """Проверка обновления контракта"""

    def setUp(self):
        super().setUp()
        self.product = Product.objects.filter(id=3).first()  # получаем услугу с id = 3

    def test_update_contracts(self):
        """Тест на обновление контракта"""

        # загружаем файл для загрузки
        test_file = SimpleUploadedFile(
            "../requirements.txt", b"Test file content", content_type="text/plain"
        )

        random_number = random.randint(100, 999)
        response = self.client.post(
            reverse("contractsapp:contracts_update", kwargs={"pk": 7}),
            {
                "title": "Новый контракт",
                "product": self.product.id,
                "document": test_file,  # Передаём файл
                "date_signed": "2025-03-12",
                "valid_until": "2025-03-23",
                "cost": random_number,
            },
            format="multipart",  # указываем для загрузки файлов
        )
        self.assertRedirects(
            response, reverse("contractsapp:contracts_detail", kwargs={"pk": 7})
        )
        self.assertTrue(
            Contract.objects.filter(Q(pk=7) & Q(cost=random_number)).exists()
        )

    def test_negative_update_contracts(self):
        """Негативный тест на обновление контракта"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username="Irina", password="Abc9002973474")

        # загружаем файл для загрузки
        test_file = SimpleUploadedFile(
            "../requirements.txt", b"Test file content", content_type="text/plain"
        )

        random_number = random.randint(100, 999)
        response = self.client.post(
            reverse("contractsapp:contracts_update", kwargs={"pk": 7}),
            {
                "title": "Новый контракт",
                "product": self.product.id,
                "document": test_file,  # Передаём файл
                "date_signed": "2025-03-12",
                "valid_until": "2025-03-23",
                "cost": random_number,
            },
            format="multipart",  # указываем для загрузки файлов
        )
        self.assertNotEqual(response.status_code, 200)


class DeleteContractTestCase(AuthenticatedTestCase):
    """Проверка удаления контракта"""

    def test_delete_contracts(self):
        """Тест на удаление контракта"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Администратора
        self.client.login(username="admin", password="admin")

        # Отправляем запрос на удаление контракта
        response = self.client.post(
            reverse("contractsapp:contracts_delete", kwargs={"pk": 7}),
        )
        self.assertRedirects(response, "/contracts/")

        # Проверяем, что контракт удален
        self.assertFalse(Contract.objects.filter(pk=7).exists())

    def test_negative_delete_contracts(self):
        """Негативный тест на удаление контракта"""
        response = self.client.post(
            reverse("contractsapp:contracts_delete", kwargs={"pk": 7}),
        )

        # Получаем ошибку удаления из-за нехватки прав
        self.assertEqual(response.status_code, 403)
