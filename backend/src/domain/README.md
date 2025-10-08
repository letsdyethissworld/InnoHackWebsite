# Domain Layer (`domain/`)

Доменный слой содержит бизнес-логику приложения, организованную по принципам **Domain-Driven Design (DDD)**.

## 📁 Структура

```
domain/
├── models/           # Доменные модели данных
├── services/         # Бизнес-логика доменов
└── repositories/     # Абстракции репозиториев
```

## 🎯 Домены системы

### Регистрации (`registrations`)
Управление регистрацией команд на хакатон:
- Создание и обновление регистраций
- Валидация данных команды
- Автоматическое присвоение дат регистрации

### Telegram (`telegram`)
Интеграция с Telegram Bot API:
- Отправка уведомлений администраторам
- Управление настройками бота
- Обработка ошибок подключения

## 📋 Компоненты

### Модели (`models/`)

Доменные модели представляют бизнес-сущности системы:

#### TeamRegistration
```python
@dataclass
class TeamRegistration:
    """Доменная модель регистрации команды"""
    id: int | None = None
    team_name: str = ""
    selected_case: str = ""
    captain_name: str = ""
    captain_email: str = ""
    team_members: List[str] = None
    registration_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    event: str = ""
    status: str = "pending"
```

**Особенности:**
- Автоматическое присвоение даты регистрации
- Валидация обязательных полей
- Сериализация в JSON для API

### Сервисы (`services/`)

Бизнес-логика доменов инкапсулирована в сервисах:

#### RegistrationService
Обрабатывает процесс регистрации команд:
- Валидация входных данных
- Создание доменных моделей
- Координация с репозиториями
- Отправка уведомлений через Telegram

**Методы:**
- `create_registration_from_request()` - Создание модели из запроса
- `process_registration()` - Обработка полной регистрации
- `get_registration_by_id()` - Получение регистрации по ID
- `get_all_registrations()` - Получение всех регистраций

#### TelegramService
Управляет интеграцией с Telegram Bot API:
- Инициализация бота с токеном
- Отправка форматированных уведомлений
- Обработка ошибок подключения
- Тестирование подключения

**Методы:**
- `initialize()` - Инициализация бота
- `send_registration_notification()` - Отправка уведомления о регистрации
- `send_test_message()` - Тестовое сообщение
- `is_initialized()` - Проверка статуса инициализации

### Репозитории (`repositories/`)

Абстракции для доступа к данным:

#### AbstractTeamRegistrationRepository
Определяет интерфейс для работы с регистрациями:
```python
class AbstractTeamRegistrationRepository(ABC):
    @abstractmethod
    async def add(self, registration: TeamRegistration) -> int:
        """Добавить регистрацию и вернуть ID"""

    @abstractmethod
    async def get_by_id(self, registration_id: int) -> Optional[TeamRegistration]:
        """Получить регистрацию по ID"""

    @abstractmethod
    async def get_all(self) -> List[TeamRegistration]:
        """Получить все регистрации"""

    @abstractmethod
    async def update(self, registration: TeamRegistration) -> None:
        """Обновить регистрацию"""

    @abstractmethod
    async def delete(self, registration_id: int) -> None:
        """Удалить регистрацию"""
```

## 🔄 Взаимодействие компонентов

```
API Router → RegistrationService → AbstractTeamRegistrationRepository → Database
     ↓              ↓                        ↓
Validation ← TeamRegistration ← TeamRegistrationRepository ← SQLModel
```

1. **Запрос** валидируется роутером
2. **Сервис** обрабатывает бизнес-логику
3. **Репозиторий** обеспечивает доступ к данным
4. **Инфраструктура** реализует конкретное хранение

## 🧪 Тестирование

### Unit тесты домена
Тестируют бизнес-логику в изоляции:
- Валидация моделей
- Логика сервисов
- Контракты репозиториев

### Примеры тестов
```python
# Тестирование модели
def test_team_registration_creation():
    registration = TeamRegistration(
        team_name="Test Team",
        captain_name="John Doe"
    )
    assert registration.registration_date is not None

# Тестирование сервиса
async def test_registration_service_process():
    service = RegistrationService()
    request = RegistrationRequest(...)
    result = await service.process_registration(request)
    assert result.status == "success"
```

## 🔧 Разработка

### Добавление нового домена

1. **Определите модель** в `models/`
2. **Создайте сервис** в `services/`
3. **Определите репозиторий** в `repositories/`
4. **Добавьте роутеры** в `../api/routers/`

### Соглашения именования

- **Файлы**: `snake_case.py`
- **Классы**: `PascalCase`
- **Методы**: `snake_case`
- **Домены**: Нижний регистр с дефисами для многословных названий

### Зависимости

Доменный слой **не зависит** от:
- Конкретных технологий хранения (БД)
- Внешних API (Telegram)
- HTTP фреймворков (FastAPI)

Зависит только от:
- Стандартной библиотеки Python
- Внутренних доменных контрактов
