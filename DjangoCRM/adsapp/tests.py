"""
Модуль для тестирования функций приложения AdsApp
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
from productapp.models import Product


class AuthenticatedTestCase(TestCase):
    """Аутентификация пользователя и загрузка фикстур"""
    fixtures = [
        "fixtures/fixtures.xml",
    ]

    def setUp(self):
        """Логинимся от имени маркетолога"""
        self.client.login(username="Evgeniy", password="Abc9517850219")


class CreateAdTestCase(AuthenticatedTestCase):
    """Проверка создания рекламной компании"""

    def setUp(self):
        super().setUp()
        Product.objects.create(
            name="Product",
            description="Test product",
            price=1,
        )
        self.product = Product.objects.filter(price=1).first()

    def tearDown(self):
        """Удаляем рекламную компанию после теста"""
        Ad.objects.filter(advertising_budget=10 ** 6).delete()
        Product.objects.filter(price=1).delete()

    def test_create_ads(self) -> None:
        """
        Тест на создание и добавление в БД рекламной компании
        """
        response = self.client.post(
            reverse("adsapp:ads_create"),
            {
                "name": "Тестовая рекламная компания",
                "product": self.product.id,
                "promotion_channel": "Instagram",
                "advertising_budget": 10 ** 5,
            }
        )
        self.assertRedirects(response, reverse("adsapp:ads_list"))
        self.assertTrue(Ad.objects.filter(advertising_budget=10 ** 5).exists())

    def test_negative_create_ads(self) -> None:
        """
        Отрицательный тест на создание рекламной компании
        """

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username='Irina', password="Abc9002973474")

        # Пробуем создать компанию
        response = self.client.post(
            reverse("adsapp:ads_create"),
            {
                "name": "Тестовая рекламная компания",
                "product": self.product.id,
                "promotion_channel": "Instagram",
                "advertising_budget": 10 ** 5,
            }
        )
        self.assertEqual(response.status_code, 403)


class DetailAdTestCase(AuthenticatedTestCase):

    def test_get_detail_ads(self):
        """Тест на просмотр деталей рекламной компании"""
        response = self.client.get(
            reverse("adsapp:ads_detail",
                    kwargs={"pk": 1}
                    ),

        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Контекстная реклама 1")

    def test_negative_get_detail_ads(self):
        """Негативный тест на просмотр деталей рекламной компании"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username='Irina', password="Abc9002973474")

        # Отправляем запрос на просмотр рекламной компании
        response = self.client.get(
            reverse("adsapp:ads_detail",
                    kwargs={"pk": 1}
                    ),

        )
        self.assertNotEqual(response.status_code, 200)


class AdListTestCase(AuthenticatedTestCase):

    def test_list_ads(self):
        """Тест на просмотр списка услуг"""
        response = self.client.get(reverse("adsapp:ads_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "adsapp/ads_list.html")
        self.assertQuerysetEqual(
            qs=list(Ad.objects.all()),
            values=(p.pk for p in response.context["ads"]),
            transform=lambda p: p.pk,
        )

    def test_negative_list_ads(self):
        """Негативный тест на просмотр списка услуг"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username='Irina', password="Abc9002973474")

        # Отправляем запрос на просмотр услуг
        response = self.client.get(reverse("adsapp:ads_list"))
        self.assertEqual(response.status_code, 403)


class UpdateAdTestCase(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.filter(id=3).first()

    def test_update_ads(self):
        """Тест на обновление рекламной компании"""

        random_number = random.randint(1, 1000)
        response = self.client.post(
            reverse("adsapp:ads_update", kwargs={"pk": 1}),
            {
                "name": "Контекстная реклама 1",
                "product": self.product.id,
                "promotion_channel": "Яндекс, Google",
                "advertising_budget": random_number,
            }
        )
        self.assertRedirects(response, reverse("adsapp:ads_detail", kwargs={"pk": 1}))
        self.assertTrue(
            Ad.objects.filter(Q(pk=1) & Q(advertising_budget=random_number)).exists()
        )

    def test_negative_update_ads(self):
        """Негативный тест на обновление рекламной компании"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Оператора
        self.client.login(username='Irina', password="Abc9002973474")

        # Отправляем запрос на обновление рекламной компании
        response = self.client.post(
            reverse("adsapp:ads_update", kwargs={"pk": 1}),
            {
                "name": "Контекстная реклама 1",
                "product": self.product.id,
                "promotion_channel": "Яндекс, Google",
                "advertising_budget": 1,
            }
        )
        self.assertNotEqual(response.status_code, 200)


class DeleteAdTestCase(AuthenticatedTestCase):

    def setUp(self):
        """Добавляем новую рекламную компанию"""
        super().setUp()

        # создаём услугу
        Product.objects.create(
            name="Test product",
            description="None",
            price=0,
        )
        self.product = Product.objects.filter(price=0).first()

        # создаём компанию
        Ad.objects.create(
            name="Test Ad",
            product=self.product,
            promotion_channel="Instagram",
            advertising_budget=1,
        )
        self.ad = Ad.objects.filter(advertising_budget=1).first()

    def test_negative_delete_ads(self):
        """Негативный тест на удаление рекламной компании"""
        response = self.client.post(
            reverse("adsapp:ads_delete", kwargs={"pk": self.ad.pk}),
        )

        # Получаем ошибку удаления из-за нехватки прав
        self.assertEqual(response.status_code, 403)

    def test_delete_ads(self):
        """Тест на удаление рекламной компании"""

        # выполняем logout
        self.client.logout()

        # выполняем login от имени Администратора
        self.client.login(username='admin', password="admin")

        # Отправляем запрос на удаление рекламной компании
        response = self.client.post(
            reverse("adsapp:ads_delete", kwargs={"pk": self.ad.pk}),
        )
        self.assertRedirects(response, "/ads/")

        # Проверяем, что заказ удален
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())
