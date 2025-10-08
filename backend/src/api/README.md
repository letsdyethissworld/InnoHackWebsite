# API Layer (`api/`)

HTTP API слой приложения, построенный на FastAPI с автоматической генерацией документации OpenAPI.

## 📁 Структура

```
api/
├── routers/           # Роутеры FastAPI по доменам
│   ├── registrations/ # API регистрации команд
│   └── telegram/      # API Telegram настроек
└── webserver.py       # Конфигурация веб-сервера
```

## 🚀 API Роутеры

### Регистрации (`routers/registrations/`)

Управление регистрацией команд на хакатон:

#### Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/registrations/` | Создать новую регистрацию команды |
| GET | `/api/registrations/` | Получить все регистрации |
| GET | `/api/registrations/{id}` | Получить регистрацию по ID |
| PUT | `/api/registrations/{id}` | Обновить регистрацию |
| GET | `/api/registrations/health` | Проверка здоровья сервиса |

#### Модели запросов/ответов

**Запрос регистрации:**
```python
class RegistrationRequest(BaseModel):
    teamName: str
    selectedCase: str
    captainName: str
    captainEmail: str
    teamMembers: List[str]
    event: str
    status: str = "pending"
    # registrationDate устанавливается автоматически
```

**Ответ регистрации:**
```python
class RegistrationResponse(BaseModel):
    status: str
    message: str
    registration_id: int | None = None
```

### Telegram (`routers/telegram/`)

Управление настройками Telegram уведомлений:

#### Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/settings/telegram/` | Получить статус Telegram сервиса |
| PUT | `/api/settings/telegram/` | Обновить настройки Telegram |
| POST | `/api/settings/telegram/test` | Отправить тестовое уведомление |

#### Модели

**Статус Telegram:**
```python
class TelegramSettingsResponse(BaseModel):
    bot_token_configured: bool
    admin_user_ids: List[int]
    initialized: bool
```

## 🔧 Конфигурация

### Валидация и обработка ошибок

**Автоматическая валидация:**
- Все запросы валидируются через Pydantic модели
- Обязательные поля проверяются автоматически
- Формат данных контролируется схемами

**Обработка ошибок:**
- `400 Bad Request` - Ошибки валидации
- `404 Not Found` - Ресурс не найден
- `422 Unprocessable Entity` - Ошибки обработки данных
- `500 Internal Server Error` - Внутренние ошибки сервера

### Документация

**Автоматическая генерация:**
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

Документация генерируется автоматически на основе:
- Типов данных в моделях
- Докстрингов функций
- Аннотаций параметров

## 🔄 Dependency Injection

Роутеры используют **зависимости** для доступа к сервисам:

```python
@router.post("/", response_model=RegistrationResponse)
async def create_registration(
    registration_data: RegistrationRequest,
    uow: UoW = Depends(get_uow),  # Unit of Work
    telegram_service = Depends(get_telegram_service)  # Telegram сервис
) -> RegistrationResponse:
    # Логика обработки...
```

**Доступные зависимости:**
- `get_uow()` - Unit of Work для работы с базой данных
- `get_telegram_service()` - Сервис Telegram уведомлений

## 🧪 Тестирование API

### Интеграционные тесты

Тестируют полные HTTP запросы:

```python
async def test_create_registration_integration(client):
    response = client.post("/api/registrations/", json={
        "teamName": "Test Team",
        "selectedCase": "AI Case",
        "captainName": "John Doe",
        "captainEmail": "john@example.com",
        "teamMembers": ["Alice", "Bob"],
        "event": "Hackathon 2025"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "registration_id" in data
```

### Моки для внешних зависимостей

```python
@pytest.fixture
def mock_telegram_service():
    """Мок сервиса Telegram для тестов"""
    # Настройка моков...
```

## 📊 Мониторинг

### Метрики запросов

Каждый запрос логируется с информацией:
- Метод и URL
- Статус код ответа
- Время обработки
- IP клиента

### Health Checks

- `/api/registrations/health` - Статус сервиса регистрации
- `/api/settings/telegram/` - Статус Telegram интеграции

## 🔒 Безопасность

### Валидация входных данных

- **Типы данных**: Строгая проверка типов через Pydantic
- **Обязательные поля**: Проверка наличия всех требуемых полей
- **Формат данных**: Валидация email, дат и других форматов

### Обработка ошибок

- Детальные сообщения об ошибках для разработки
- Обобщенные сообщения для продакшена
- Логирование всех ошибок для анализа

## 🚀 Производительность

### Оптимизации

- **Асинхронные операции**: Все БД операции асинхронны
- **Connection pooling**: Переиспользование соединений с БД
- **Кэширование**: На уровне инфраструктуры (при необходимости)

### Масштабирование

- **Горизонтальное**: Поддержка нескольких инстансов
- **База данных**: Отдельный сервер PostgreSQL
- **Внешние сервисы**: Асинхронные вызовы Telegram API

## 📚 Примеры использования

### Создание регистрации

```bash
curl -X POST "http://localhost:8080/api/registrations/" \
     -H "Content-Type: application/json" \
     -d '{
       "teamName": "Team Alpha",
       "selectedCase": "AI Innovation",
       "captainName": "John Doe",
       "captainEmail": "john@example.com",
       "teamMembers": ["Alice", "Bob"],
       "event": "Hackathon 2025"
     }'
```

### Получение всех регистраций

```bash
curl "http://localhost:8080/api/registrations/"
```

### Проверка здоровья

```bash
curl "http://localhost:8080/api/registrations/health"
```
