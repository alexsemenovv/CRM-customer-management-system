"""
Модуль для тестирования приложения Statistics App
"""
from django.test import TestCase
from django.urls import reverse


class StatisticTestCase(TestCase):
    fixtures = [
        "fixtures/fixtures.xml",
    ]

    def setUp(self):
        self.client.login(username="admin", password="admin")  # логинимся от имени админ

    def test_statistics_view_authenticated(self):
        """Тест на доступ к статистике для авторизованного пользователя"""
        response = self.client.get(reverse("statisticsapp:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statisticsapp/index.html")
        self.assertIn("products", response.context)
        self.assertIn("ads", response.context)
        self.assertIn("leads", response.context)
        self.assertIn("customers", response.context)

    def test_statistics_view_unauthenticated(self):
        """Тест редиректа на логин при неавторизованном доступе"""
        self.client.logout()
        response = self.client.get(reverse("statisticsapp:index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("myauth:login"))

    def test_check_amount_products(self):
        """Тест на кол-во услуг"""
        response = self.client.post(
            reverse("statisticsapp:index")
        )
        self.assertEqual(response.status_code, 200)
        amount_products = len(response.context['products'])  # получаем кол-во услуг в БД

        new_product = self.client.post(
            reverse("productapp:products_create"),
            {
                "name": "Тестовая услуга",
                "description": "Тестовое описание",
                "price": 1000,
            }
        )  # создаём еще одну услугу
        self.assertRedirects(new_product, reverse('productapp:products_list'))

        response = self.client.post(
            reverse("statisticsapp:index")
        )  # обновляем новые данные
        amount_products_plus_one = len(response.context['products'])  # получаем кол-во услуг в БД
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(amount_products, amount_products_plus_one)

    def test_check_amount_leads(self):
        """Тест на кол-во лидов"""
        response = self.client.post(
            reverse("statisticsapp:index")
        )
        self.assertEqual(response.status_code, 200)
        amount_leads = len(response.context['leads'])  # получаем кол-во лидов в БД

        new_lead = self.client.post(
            reverse("leadsapp:leads_create"),
            {
                "full_name": "Петр МакКонахи Средний",
                "phone_number": "+79518564321",
                "email": "PetrNotFirst@gmail.com",
                "ad": 1,
            }
        )  # создаём еще одного лида
        self.assertRedirects(new_lead, reverse('leadsapp:leads_list'))

        response = self.client.post(
            reverse("statisticsapp:index")
        )  # обновляем новые данные
        amount_leads_plus_one = len(response.context['leads'])  # получаем кол-во услуг в БД
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(amount_leads, amount_leads_plus_one)

    def test_check_amount_customers(self):
        """Тест на кол-во клиентов"""
        response = self.client.post(
            reverse("statisticsapp:index")
        )
        self.assertEqual(response.status_code, 200)
        amount_customers = len(response.context['customers'])  # получаем кол-во клиентов в БД

        new_customer = self.client.post(
            reverse("customersapp:customers_create"),
            {
                "lead": 8,
                "contract": 10
            }
        )  # создаём еще одного клиента
        self.assertRedirects(new_customer, reverse('leadsapp:leads_list'))

        response = self.client.post(
            reverse("statisticsapp:index")
        )  # обновляем новые данные
        amount_customers_plus_one = len(response.context['customers'])  # получаем кол-во услуг в БД
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(amount_customers, amount_customers_plus_one)
