"""
Модуль для тестирования функций приложения LeadsApp
Созданные роли:
    - admin - Админ
    - Irina - Оператор
    - Evgeniy - Маркетолог
"""
import random

from django.db.models import Q
from django.test import TestCase
from django.urls import reverse

from adsapp.models import Ad
from leadsapp.models import Lead


class AuthenticatedTestCase(TestCase):
    """Аутентификация пользователя и загрузка фикстур"""
    fixtures = [
        "fixtures/fixtures.xml",
    ]

    def setUp(self):
        """Логинимся от имени оператора"""
        self.client.login(username="Irina", password="Abc9002973474")


class CreateLeadTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.ad = Ad.objects.filter(id=1).first()

    def tearDown(self):
        """Удаляем потенциального клиента после теста"""
        Lead.objects.filter(email="PetrNotFirst@gmail.com").delete()

    def test_create_leads(self) -> None:
        """
        Тест на создание и добавление в БД потенциального клиента
        """
        response = self.client.post(
            reverse("leadsapp:leads_create"),
            {
                "full_name": "Петр МакКонахи Средний",
                "phone_number": "+79518564321",
                "email": "PetrNotFirst@gmail.com",
                "ad": self.ad.id,
            }
        )
        self.assertRedirects(response, reverse("leadsapp:leads_list"))
        self.assertTrue(Lead.objects.filter(email="PetrNotFirst@gmail.com").exists())

    def test_negative_create_leads(self) -> None:
        """
        Отрицательный тест на создание потенциального клиента
        """

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Маркетолога
        self.client.login(username='Evgeniy', password="Abc9517850219")

        # Пробуем создать лида
        response = self.client.post(
            reverse("leadsapp:leads_create"),
            {
                "full_name": "Петр МакКонахи Средний",
                "phone_number": "+79518564321",
                "email": "PetrNotFirst@gmail.com",
                "ad": self.ad,
            }
        )
        self.assertEqual(response.status_code, 403)


class DetailLeadTestCase(AuthenticatedTestCase):

    def test_get_detail_leads(self):
        """Тест на просмотр деталей потенциального клиента"""
        response = self.client.get(
            reverse("leadsapp:leads_detail",
                    kwargs={"pk": 2}
                    ),

        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сигал Стивен Петрович")

    def test_negative_get_detail_leads(self):
        """Негативный тест на просмотр деталей потенциального клиента"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Маркетолога
        self.client.login(username='Evgeniy', password="Abc9517850219")

        # Отправляем запрос на просмотр потенциального клиента
        response = self.client.get(
            reverse("leadsapp:leads_detail",
                    kwargs={"pk": 2}
                    ),

        )
        self.assertNotEqual(response.status_code, 200)


class LeadListTestCase(AuthenticatedTestCase):

    def test_list_leads(self):
        """Тест на просмотр списка потенциальных клиентов"""
        response = self.client.get(reverse("leadsapp:leads_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leadsapp/leads_list.html")
        self.assertQuerysetEqual(
            qs=list(Lead.objects.all()),
            values=(l.pk for l in response.context["leads"]),
            transform=lambda l: l.pk,
        )

    def test_negative_list_leads(self):
        """Негативный тест на просмотр списка потенциальных клиентов"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Маркетолога
        self.client.login(username='Evgeniy', password="Abc9517850219")

        # Отправляем запрос на просмотр услуг
        response = self.client.get(reverse("leadsapp:leads_list"))
        self.assertEqual(response.status_code, 403)


class UpdateLeadTestCase(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.ad = Ad.objects.filter(id=1).first()

    def test_update_leads(self):
        """Тест на обновление потенциального клиента"""

        random_number = random.randint(100, 999)
        response = self.client.post(
            reverse("leadsapp:leads_update", kwargs={"pk": 2}),
            {
                "full_name": "Сигал Стивен Петрович",
                "phone_number": str(random_number),
                "email": "stiven.cool@gmail.com",
                "ad": self.ad.id,
            }
        )
        self.assertRedirects(response, reverse("leadsapp:leads_detail", kwargs={"pk": 2}))
        self.assertTrue(
            Lead.objects.filter(Q(pk=2) & Q(phone_number=random_number)).exists()
        )

    def test_negative_update_leads(self):
        """Негативный тест на обновление потенциального клиента"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username='Evgeniy', password="Abc9517850219")

        # Отправляем запрос на обновление потенциального клиента
        response = self.client.post(
            reverse("leadsapp:leads_update", kwargs={"pk": 2}),
            {
                "full_name": "Сигал Стивен Петрович",
                "phone_number": str(1),
                "email": "stiven.cool@gmail.com",
                "ad": self.ad.id,
            }
        )
        self.assertNotEqual(response.status_code, 200)


class DeleteLeadTestCase(AuthenticatedTestCase):

    def test_delete_leads(self):
        """Тест на удаление потенциального клиента"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Администратора
        self.client.login(username='admin', password="admin")

        # Отправляем запрос на удаление потенциального клиента
        response = self.client.post(
            reverse("leadsapp:leads_delete", kwargs={"pk": 7}),
        )
        self.assertRedirects(response, "/leads/")

        # Проверяем, что лид удален
        self.assertFalse(Lead.objects.filter(pk=7).exists())

    def test_negative_delete_leads(self):
        """Негативный тест на удаление потенциального клиента"""
        response = self.client.post(
            reverse("leadsapp:leads_delete", kwargs={"pk": 7}),
        )

        # Получаем ошибку удаления из-за нехватки прав
        self.assertEqual(response.status_code, 403)
