# Backend - FastAPI Application

Основное серверное приложение системы регистрации хакатона, построенное на FastAPI с использованием Domain-Driven Design архитектуры.

## 🏗️ Архитектура Backend

```
backend/
├── src/                    # Исходный код приложения
│   ├── api/               # HTTP API слой
│   │   ├── routers/       # Роутеры по доменам
│   │   │   ├── registrations/  # Роутеры регистрации команд
│   │   │   └── telegram/       # Роутеры Telegram настроек
│   │   └── webserver.py   # Конфигурация веб-сервера
│   ├── domain/            # Доменная логика (DDD)
│   │   ├── models/        # Доменные модели
│   │   ├── services/      # Бизнес-логика
│   │   └── repositories/  # Абстракции репозиториев
│   ├── infrastructure/    # Инфраструктурный слой
│   │   ├── adapters/      # Адаптеры внешних сервисов
│   │   └── repositories/  # Реализации репозиториев
│   ├── settings/          # Конфигурация приложения
│   └── entrypoints/       # Точки входа приложения
├── db/                    # Миграции базы данных
│   └── migrations/        # SQL миграции
├── tests/                 # Тесты
│   ├── unit/             # Unit тесты
│   └── integration/      # Интеграционные тесты
└── pyproject.toml        # Зависимости и конфигурация
```

## 🚀 Запуск

### Предварительные требования

- Python 3.11+
- PostgreSQL (или Docker)
- Poetry (для управления зависимостями)

### Локальный запуск

1. **Установите зависимости:**
```bash
poetry install
```

2. **Настройте переменные окружения:**
```bash
cp .env.example .env
# Отредактируйте .env с вашими настройками
```

3. **Запустите базу данных:**
```bash
docker-compose -f docker-compose.local.yaml up postgres -d
```

4. **Выполните миграции:**
```bash
dbmate up
```

5. **Запустите сервер:**
```bash
poetry run python src/entrypoints/main.py
```

Сервер будет доступен на `http://localhost:8080`

## 📋 Основные компоненты

### API Роутеры (`src/api/routers/`)

#### Регистрации (`registrations/`)
- `POST /api/registrations/` - Создать регистрацию команды
- `GET /api/registrations/` - Получить все регистрации
- `GET /api/registrations/{id}` - Получить регистрацию по ID
- `PUT /api/registrations/{id}` - Обновить регистрацию
- `GET /api/registrations/health` - Проверка здоровья сервиса

#### Telegram (`telegram/`)
- `GET /api/settings/telegram/` - Статус Telegram сервиса
- `POST /api/settings/telegram/test` - Тестовое уведомление

### Доменные сервисы (`src/domain/services/`)

#### RegistrationService
Обрабатывает бизнес-логику регистрации команд:
- Валидация данных регистрации
- Создание доменных моделей
- Координация с репозиториями

#### TelegramService
Управляет интеграцией с Telegram Bot API:
- Инициализация бота
- Отправка уведомлений администраторам
- Обработка ошибок подключения

### Модели (`src/domain/models/`)

#### TeamRegistration
Доменная модель регистрации команды с автоматическим присвоением даты:
```python
@dataclass
class TeamRegistration:
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

### Репозитории (`src/infrastructure/repositories/`)

#### TeamRegistrationRepository
Реализация доступа к данным регистраций:
- CRUD операции с базой данных
- Обработка ошибок базы данных
- Логирование операций

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|--------|
| `DATABASE_URL` | URL подключения к PostgreSQL | `postgresql://user:pass@localhost:5432/hackathon` |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | `123456:ABC-DEF...` |
| `TELEGRAM_ADMIN_IDS` | ID администраторов через запятую | `123456789,987654321` |
| `HOST` | Хост сервера | `0.0.0.0` |
| `PORT` | Порт сервера | `8080` |
| `DEBUG` | Режим отладки | `true` |

### Файлы конфигурации

- `settings.toml` - Базовые настройки
- `settings.dev.toml` - Настройки разработки
- `settings.staging.toml` - Настройки staging среды

## 🧪 Тестирование

### Структура тестов

```
tests/
├── unit/                  # Unit тесты
│   ├── test_registration_service.py
│   ├── test_telegram_service.py
│   └── test_team_registration_repository.py
└── integration/           # Интеграционные тесты
    ├── test_registration_api.py
    └── test_telegram_api.py
```

### Запуск тестов

```bash
# Все тесты
poetry run pytest

# Unit тесты
poetry run pytest tests/unit/

# Интеграционные тесты
poetry run pytest tests/integration/

# С покрытием
poetry run pytest --cov=src --cov-report=html
```

## 🚢 Развертывание

### Docker

```bash
# Сборка образа
docker build -t hackathon-backend .

# Запуск с базой данных
docker-compose up -d
```

### Миграции

```bash
# Создание новой миграции
dbmate new create_users_table

# Применение миграций
dbmate up

# Статус миграций
dbmate status
```

## 🔍 Отладка

### Логи

Сервер логирует в консоль с уровнями:
- DEBUG - Подробная отладочная информация
- INFO - Общая информация о работе
- WARNING - Предупреждения
- ERROR - Ошибки

### Метрики и мониторинг

- Health check: `GET /api/registrations/health`
- Telegram статус: `GET /api/settings/telegram/`
- Метрики запросов логируются автоматически

## 📚 Дополнительные ресурсы

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Guide](https://sqlmodel.tutorial.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Domain-Driven Design](https://dddcommunity.org/)
