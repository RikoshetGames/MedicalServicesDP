# MedicalServicesDP

## Структура проекта 🧑‍💻:

### Модели (Models) 🗃️
### Файл users/models.py:
#### Модель User (Пользователь):
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

##### Методы:
- `save()` - Переопределенный метод сохранения модели для генерации токена подтверждения email.

### Файл medical_services/models.py:
### Модель Category (Категория):
Модель `Category` представляет собой категорию услуг.

#### Поля:
- `category_title`: CharField с максимальной длиной 100 символов.
- `category_description`: TextField для описания категории.
- `category_image`: ImageField для изображения категории (может быть пустым).


### Модель Service (Услуга):
Модель `Service` описывает предоставляемые услуги.

#### Поля:
- `services_title`: CharField с максимальной длиной 100 символов.
- `services_description`: TextField для описания услуги.
- `price`: PositiveIntegerField для указания цены.
- `category`: ForeignKey на модель `Category`.
- `deadline`: CharField для указания срока выполнения.


### Модель Cart (Корзина):
Модель `Cart` представляет собой корзину покупок.

#### Поля:
- `client`: OneToOneField на модель пользователя.
- `services`: ManyToManyField на модель `Service`.
- `date`: DateTimeField для указания даты и времени (может быть пустым).


### Описание Представлений (Views) 🖥️
### Файл users/views.py 🖥:
#### RegisterView (Класс CreateView)
- URL: `/register/`
- Создает нового пользователя с установленным флагом `is_active` в False и генерирует токен подтверждения email, отправляет письмо со ссылкой для подтверждения регистрации пользователя.
#### ProfileView (Класс UpdateView)
- URL: `/profile/`
- Позволяет аутентифицированным пользователям просматривать и обновлять информацию своего профиля для редактирования.

#### confirm_registration (Функциональное Представление)
- URL: `/confirm-registration/<str:token>/`
- Подтверждает регистрацию пользователя, используя предоставленный токен, проверяет токен и активирует пользователя, если токен действителен.

#### invalid_token_view (Функциональное Представление)
- URL: `/invalid-token/`
- Отображает сообщение об ошибке при недействительном токене при подтверждении регистрации.

#### generate_new_password (Функциональное Представление)
- URL: `/profile/genpassword`
- Генерирует новый случайный пароль для пользователя и отправляет его по электронной почте, новый пароль устанавливается для пользователя, и отправляется письмо с подтверждением.

#### reset_password (Функциональное Представление)
- URL: `/reset_password/`
- Позволяет пользователям сбросить пароль, отправив новый случайный пароль по электронной почте, обрабатывает отправку формы для сброса пароля пользователя.

#### logout_view (Функциональное Представление)
- URL: `/logout/`
- Выходит из учетной записи текущего пользователя и перенаправляет на страницу входа.


### Файл medical_services/views.py 🖥:
#### CategoryCreateView (Класс CreateView, PermissionRequiredMixin)
- URL: `/create-category/`
- Создает новую категорию услуг, проверяет разрешения пользователя на добавление категории.
- Доступ: `medical_services.add_category`.

#### CategoryListView (Класс ListView)
- Отображает список категорий услуг.
- URL: `/categories/`.

#### CategoryUpdateView (Класс UpdateView, PermissionRequiredMixin)
- URL: `/update-category/<int:pk>/`
- Обновляет информацию о категории услуг, проверяет разрешения пользователя на изменение категории.
- Доступ: `medical_services.update_category`.

#### CategoryDeleteView (Класс DeleteView, PermissionRequiredMixin)
- Удаляет выбранную категорию услуг, проверяет разрешения пользователя на удаление категории.
- Доступ: `medical_services.delete_category`.

#### CategoryServiceListView (Класс ListView)
- Отображает список услуг в определенной категории.
- URL: `/category/<int:pk>/services/`.

#### ServiceCreateView (Класс CreateView, PermissionRequiredMixin)
- URL: `/create-service/`
- Создает новую услугу, проверяет разрешения пользователя на добавление услуги.
- Доступ: `medical_services.add_service`.

#### ServiceListView (Класс ListView)
- Отображает список всех доступных услуг.
- URL: `/services/`.

#### ServiceDetailView (Класс DetailView)
- Отображает подробную информацию об услуге.
- URL: `/service/<int:pk>/`.

#### ServiceUpdateView (Класс UpdateView, PermissionRequiredMixin)
- URL: `/update-service/<int:pk>/`
- Обновляет информацию о выбранной услуге, проверяет разрешения пользователя на изменение услуги.
- Доступ: `medical_services.update_service`.

#### ServiceDeleteView (Класс DeleteView, PermissionRequiredMixin)
- Удаляет выбранную услугу, проверяет разрешения пользователя на удаление услуги.
- Доступ: `medical_services.delete_service`.

#### ContactView (Класс View)
- Отображает страницу контактов.
- URL: `/contacts/`.

#### ServiceCartView (Класс View)
- Управляет корзиной услуг пользователя.

#### AddToCartView (Класс View)
- Добавляет выбранную услугу в корзину.
- URL: `/add-to-cart/`.

#### home (Функция)
- Отображает главную страницу проекта.
- URL: `/`.

#### remove_service (Функция)
- Удаляет определенную услугу из корзины пользователя.
- URL: `/remove-service/<int:service_id>/`.

#### clear_service (Функция)
- Очищает корзину пользователя.
- URL: `/clear-service/`.