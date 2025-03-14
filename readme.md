# CRM Django Project

## Описание
### Общая информация
CRM-система разрабатывается в виде веб-приложения, предназначенного для управления клиентами, рекламными кампаниями и контрактами.
Система предоставляет функциональность для работы с потенциальными и активными клиентами, а также анализирует эффективность маркетинговых мероприятий.

### Функциональные возможности

- **Авторизация пользователей с разграничением ролей.**

- **Управление предоставляемыми услугами (создание, редактирование, просмотр, удаление).**

- **Управление рекламными кампаниями (создание, редактирование, просмотр, удаление).**

- **Ведение базы потенциальных клиентов (создание, редактирование, просмотр, удаление, перевод в активные клиенты).**

- **Оформление контрактов с клиентами (создание, редактирование, просмотр, удаление).**

- **Ведение базы активных клиентов.**

- **Подсчёт и отображение статистики по рекламным кампаниям.**

### Роли пользователей и их возможности

1) Администратор (управляет пользователями и их правами)

   - **Создание, редактирование и удаление пользователей.**

   - **Назначение ролей и разрешений.**

   - **Доступ к административной панели Django.**

2) Оператор (работает с потенциальными клиентами)

   - **Создание, редактирование и просмотр потенциальных клиентов.**

   - **Перевод потенциальных клиентов в активных.**

3) Маркетолог (отвечает за услуги и рекламу)

    - **Создание, редактирование и просмотр предоставляемых услуг.**

    - **Создание, редактирование и просмотр рекламных кампаний.**

4) Менеджер (работает с контрактами и клиентами)

    - **Создание, редактирование и просмотр контрактов.**

    - **Просмотр потенциальных клиентов.**

    - **Перевод потенциальных клиентов в активных.**

5) Все роли

    - **Просмотр статистики рекламных кампаний.**

### Создание и управление объектами

1) Услуги

    - **Название**

    - **Описание**

    - **Стоимость**

2) Рекламные кампании

    - **Название**

    - **Рекламируемая услуга**

    - **Канал продвижения**

    - **Бюджет на рекламу**

3) Потенциальные клиенты

    - **Ф. И. О.**

    - **Телефон**

    - **Email**

    - **Рекламная кампания, из которой клиент узнал об услуге**

4) Контракты

    - **Название**

    - **Предоставляемая услуга**

    - **Файл с документом**

    - **Дата заключения**

    - **Период действия**

    - **Сумма**

5) Активные клиенты

    - **Данные о потенциальном клиенте**

    - **Данные о контракте**

6) Статистика рекламных кампаний

    - **Количество привлечённых потенциальных клиентов.**

    - **Количество клиентов, перешедших в активные.**

    - **Соотношение дохода от контрактов и расходов на рекламу.**

### Технические требования

  - **Django и стандартный административный интерфейс для управления пользователями и ролями.**

  - **PostgreSQL в качестве СУБД.**

  - **Проверка кода с помощью Pylint.**

  - **Линтеры: black, isort**

  - **Тестирование с помощью Django TestCase**


## Структура проекта
```
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .env.template
├── DjangoCRM/
│   ├── DjangoCRM/
│   │── adsapp/
│   │── contractsapp/
│   │── customersapp/
│   │── leadsapp/
│   │── myauth/
│   │── productapp/
│   │── statisticsapp/
│   │── fixtires/
│   │── logs/
```

### Основные компоненты:
- **Dockerfile** — файл для сборки Docker-образа проекта.
- **docker-compose.yaml** — конфигурация для запуска контейнеров с сервисами.
- **requirements.txt** — список зависимостей для проекта.
- **.env** — файл с переменными окружения.
- **DjangoCRM/** — директория с исходным кодом проекта.
  - **DjangoCRM/** — основная папка проекта Django.
  - **logs/** — файлы логирования.
  - **manage.py** — управляющий скрипт Django.
  - **adsapp/** — приложение для работы с рекламными компаниями
  - **contractsapp/** — приложение для работы с контрактами
  - **customersapp/** — приложение для работы с активными клиентами
  - **leadsapp/** — приложение для работы с потенциальными клиентами (лидами)
  - **myauth/** — приложение для авторизации пользователей
  - **productapp/** — приложение для работы с услугами
  - **statisticsapp/** — приложение для работы со статистикой
  - **fixtures/** - фикстуры для тестов
  - **logs** - логи приложения

## Установка и запуск
### Для работы приложения требуется Docker
1. Настройка переменных окружения.  
Для работы приложения необходимо создать файл ".env", с указанием переменных, по шаблону ".env.template"
2. Соберите и запустите контейнеры:
   ```sh
   docker-compose up --build
   ```
3. Docker автоматически создаст и подключит PostgreSQL для работы с данными,
а также выполнит миграции и создаст суперпользователя, которого вы передадите, согласно шаблону
4. Приложение будет доступно по адресу: `http://127.0.0.1:8000/`

## Тестирование
Для запуска тестов используйте команду:
```sh
python manage.py test
```

## Оценка кода
Для проверки оценки кода, перейдите в папку с проектом и наберите команду
```sh
pylint --rcfile .pylintrc DjangoCRM/*
```

## Авторы
- Разработчик: Semyonov Aleksandr
- Контакты: aleksandrsemeonow@yandex.ru

