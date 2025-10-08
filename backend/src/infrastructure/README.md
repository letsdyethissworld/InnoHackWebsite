# Infrastructure Layer (`infrastructure/`)

Инфраструктурный слой обеспечивает реализацию внешних зависимостей и конкретные технологии хранения данных.

## 📁 Структура

```
infrastructure/
├── adapters/         # Адаптеры внешних сервисов
└── repositories/     # Конкретные реализации репозиториев
```

## 🔗 Адаптеры (`adapters/`)

Адаптеры обеспечивают интеграцию с внешними сервисами и технологиями:

### SQLModelAdapter
Подключение к базе данных PostgreSQL через SQLModel:

```python
class SQLModelAdapter:
    """Адаптер для управления подключением к PostgreSQL"""

    def __init__(self, database_host, database_port, database_user,
                 database_password, database_name, application_name):
        # Создание асинхронного движка SQLAlchemy

    async def create_engine(self) -> None:
        """Создание пула соединений"""

    async def get_session(self) -> AsyncSession:
        """Получение сессии для работы с БД"""

    async def dispose_engine(self) -> None:
        """Закрытие пула соединений"""
```

**Особенности:**
- Асинхронное подключение через `asyncpg`
- Управление connection pool
- Обработка ошибок подключения
- Логирование операций

## 💾 Репозитории (`repositories/`)

Конкретные реализации абстрактных репозиториев доменного слоя:

### TeamRegistrationRepository
Реализация работы с регистрациями команд:

```python
class TeamRegistrationRepository(AbstractTeamRegistrationRepository):
    """Реализация репозитория регистраций с SQLModel"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, registration: TeamRegistration) -> int:
        """Добавление регистрации с возвратом ID"""
        self._session.add(registration)
        await self._session.flush()  # Получение ID без коммита
        return registration.id

    async def get_by_id(self, registration_id: int) -> Optional[TeamRegistration]:
        """Получение регистрации по ID"""
        result = await self._session.execute(
            select(TeamRegistration).where(TeamRegistration.id == registration_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[TeamRegistration]:
        """Получение всех регистраций"""
        result = await self._session.execute(
            select(TeamRegistration).order_by(TeamRegistration.created_at.desc())
        )
        return list(result.scalars().all())

    async def update(self, registration: TeamRegistration) -> None:
        """Обновление регистрации"""
        # Логика обновления...

    async def delete(self, registration_id: int) -> None:
        """Удаление регистрации"""
        # Логика удаления...
```

**Особенности:**
- Работа с асинхронными сессиями SQLModel
- Обработка ошибок базы данных
- Логирование всех операций
- Транзакционность операций

## 🔄 Unit of Work

Инфраструктурный слой реализует паттерн **Unit of Work** для управления транзакциями:

### UoW (Unit of Work)
Координирует работу с несколькими репозиториями в рамках одной транзакции:

```python
class UoW(AbstractUnitOfWork):
    """Реализация Unit of Work"""

    async def __aenter__(self) -> Self:
        # Создание сессии БД
        self.__sql_model_session = await self.sql_model_adapter.get_session()
        # Инициализация репозиториев
        self.team_registrations = TeamRegistrationRepository(self.__sql_model_session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # Автоматический коммит или роллбек
        if exc_type is not None:
            await self.__sql_model_session.rollback()
        else:
            await self.__sql_model_session.commit()
        await self.__sql_model_session.close()
```

**Использование в API:**
```python
async with uow:
    registration_id = await uow.team_registrations.add(registration)
    # Автоматический коммит при выходе из контекста
```

## 🗄️ Управление данными

### Миграции базы данных

Используется **dbmate** для управления схемой БД:

```bash
# Создание новой миграции
dbmate new create_users_table

# Применение миграций
dbmate up

# Откат миграции
dbmate down

# Статус миграций
dbmate status
```

### Структура таблиц

**team_registrations:**
- `id` - SERIAL PRIMARY KEY
- `team_name` - VARCHAR(255) NOT NULL
- `selected_case` - VARCHAR(255) NOT NULL
- `captain_name` - VARCHAR(255) NOT NULL
- `captain_email` - VARCHAR(255) NOT NULL
- `team_members` - TEXT NOT NULL
- `registration_date` - VARCHAR(255) NOT NULL DEFAULT CURRENT_TIMESTAMP
- `event` - VARCHAR(255) NOT NULL
- `status` - VARCHAR(50) NOT NULL DEFAULT 'pending'
- `created_at` - TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `updated_at` - TIMESTAMPTZ NOT NULL DEFAULT NOW()

**Индексы:**
- `idx_team_registrations_captain_email` - для поиска по email
- `idx_team_registrations_event` - для фильтрации по событию
- `idx_team_registrations_status` - для фильтрации по статусу
- `idx_team_registrations_created_at` - для сортировки по дате создания

## 🔧 Конфигурация подключений

### База данных

**PostgreSQL через asyncpg:**
```python
# Создание движка
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@host:port/db",
    connect_args={"server_settings": {"application_name": "hackathon-backend"}}
)
```

**Особенности:**
- Асинхронное подключение
- Connection pooling (мин 5, макс 20 соединений)
- Автоматическое переподключение при ошибках
- Логирование медленных запросов

### Внешние сервисы

**Telegram Bot API:**
- Асинхронные HTTP запросы
- Обработка ошибок сети
- Автоматическая повторная отправка
- Логирование всех операций

## 🧪 Тестирование инфраструктуры

### Моки для внешних зависимостей

```python
@pytest.fixture
async def mock_database():
    """Мок базы данных для тестов"""
    # Настройка in-memory SQLite для тестов
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # ... настройка моков
```

### Тестирование репозиториев

```python
async def test_repository_crud():
    """Тестирование CRUD операций репозитория"""
    async with AsyncSession(engine) as session:
        repo = TeamRegistrationRepository(session)

        # Создание
        registration = TeamRegistration(...)
        registration_id = await repo.add(registration)

        # Чтение
        found = await repo.get_by_id(registration_id)
        assert found.id == registration_id

        # Обновление
        found.team_name = "Updated Team"
        await repo.update(found)

        # Удаление
        await repo.delete(registration_id)
```

## 📊 Мониторинг и логирование

### Метрики производительности

- Время выполнения запросов к БД
- Количество активных соединений
- Ошибки подключения и таймауты

### Логирование операций

**Уровни логирования:**
- DEBUG - Подробная информация о запросах
- INFO - Успешные операции
- WARNING - Предупреждения о потенциальных проблемах
- ERROR - Ошибки, требующие внимания

### Мониторинг здоровья

- Проверка доступности базы данных
- Статус подключения к внешним сервисам
- Метрики производительности API

## 🚀 Производительность

### Оптимизации БД

- **Индексы** на часто используемые поля
- **Connection pooling** для повторного использования соединений
- **Асинхронные операции** для неблокирующего I/O
- **Запросы с LIMIT** для пагинации результатов

### Масштабирование

- **Read replicas** для распределения нагрузки чтения
- **Connection pooling** на уровне приложения
- **Кэширование** часто запрашиваемых данных
- **Горизонтальное масштабирование** через load balancer

## 🔒 Безопасность

### Подключение к БД

- Использование SSL/TLS для продакшена
- Валидация сертификатов
- Ограничение доступа по IP
- Регулярная смена учетных данных

### Обработка ошибок

- Graceful degradation при недоступности сервисов
- Детальное логирование для отладки
- Обобщенные сообщения об ошибках для пользователей

## 📚 Дополнительные ресурсы

- [SQLModel Documentation](https://sqlmodel.tutorial.com/)
- [AsyncPG Guide](https://magicstack.github.io/asyncpg/)
- [Database Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- [PostgreSQL Performance](https://www.postgresql.org/docs/current/performance-tips.html)
