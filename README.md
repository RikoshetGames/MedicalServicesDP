# MedicalServicesDP

## Структура проекта 🧑‍💻:

## Модели (Models) 🗃️
## Файл users/models.py:
### Модель User (Пользователь):
Модель `User` представляет собой расширение базовой модели пользователя (`AbstractUser`) в Django для управления пользователями в приложении.

#### Поля модели:

- `email` - Email пользователя (обязательное поле, уникальное)
- `patronymic` - Отчество (дополнительное поле, макс. длина 100 символов)
- `birth_date` - Дата рождения (дополнительное поле)
- `phone` - Номер телефона (дополнительное поле, макс. длина 35 символов)
- `avatar` - Аватар пользователя (дополнительное поле, загружается в папку 'users/')

- `verify_code` - Код верификации (длина до 12 символов)
- `email_confirmation_token` - Токен подтверждения email (макс. длина 64 символа)

Имя пользователя (`username`) не используется в данной модели, вместо этого в качестве идентификатора используется Email.

#### Методы:

- `save()` - Переопределенный метод сохранения модели для генерации токена подтверждения email.

## Файл medical_services/models.py:
### Модель Category (Категория):
Модель `Category` представляет собой категорию услуг.

#### Поля:
- `category_title`: CharField с максимальной длиной 100 символов.
- `category_description`: TextField для описания категории.
- `category_image`: ImageField для изображения категории (может быть пустым).
  
#### Методы:
- `__str__()`: Возвращает название категории.

### Модель Service (Услуга)
Модель `Service` описывает предоставляемые услуги.

#### Поля:
- `services_title`: CharField с максимальной длиной 100 символов.
- `services_description`: TextField для описания услуги.
- `price`: PositiveIntegerField для указания цены.
- `category`: ForeignKey на модель `Category`.
- `deadline`: CharField для указания срока выполнения.

#### Методы:
- `__str__()`: Возвращает название услуги.

### Модель Cart (Корзина)
Модель `Cart` представляет собой корзину покупок.

#### Поля:
- `client`: OneToOneField на модель пользователя.
- `services`: ManyToManyField на модель `Service`.
- `date`: DateTimeField для указания даты и времени (может быть пустым).

#### Методы:
- `__str__()`: Возвращает информацию о клиенте и услугах в корзине.

### Общее
- `verbose_name`: Имя модели для административного интерфейса Django.
- `verbose_name_plural`: Множественное имя модели для административного интерфейса Django.

