import logging
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from pydantic import BaseModel

from src.domain.models import TeamRegistration


class TelegramConfig(BaseModel):
    """Configuration for Telegram service"""
    bot_token: str
    admin_user_ids: List[int]
    parse_mode: ParseMode = ParseMode.HTML


class TelegramService:
    """Service for handling Telegram bot operations and notifications"""

    def __init__(self, config: TelegramConfig):
        self.config = config
        self.bot: Bot | None = None
        self.dispatcher: Dispatcher | None = None
        self._logger = logging.getLogger(__name__)

    async def initialize(self) -> None:
        """Initialize the Telegram bot"""
        try:
            self.bot = Bot(
                token=self.config.bot_token,
                default=DefaultBotProperties(parse_mode=self.config.parse_mode)
            )
            self.dispatcher = Dispatcher()

            # Test the connection
            await self.bot.get_me()
            self._logger.info("Telegram bot initialized successfully")

        except Exception as e:
            self._logger.error(f"Failed to initialize Telegram bot: {e}")
            raise

    async def shutdown(self) -> None:
        """Shutdown the Telegram bot"""
        if self.bot:
            await self.bot.session.close()
            self._logger.info("Telegram bot shut down successfully")

    async def send_registration_notification(self, registration: TeamRegistration) -> None:
        """Send registration notification to all admin users"""
        if not self.bot:
            self._logger.error("Telegram bot not initialized")
            return

        message = self._format_registration_message(registration)

        for admin_id in self.config.admin_user_ids:
            try:
                await self.bot.send_message(chat_id=admin_id, text=message)
                self._logger.info(f"Registration notification sent to admin {admin_id}")
            except Exception as e:
                self._logger.error(f"Failed to send message to admin {admin_id}: {e}")

    async def send_test_message(self, message: str = "Test message from hackathon backend") -> None:
        """Send a test message to all admin users"""
        if not self.bot:
            self._logger.error("Telegram bot not initialized")
            return

        for admin_id in self.config.admin_user_ids:
            try:
                await self.bot.send_message(chat_id=admin_id, text=message)
                self._logger.info(f"Test message sent to admin {admin_id}")
            except Exception as e:
                self._logger.error(f"Failed to send test message to admin {admin_id}: {e}")

    def _format_registration_message(self, registration: TeamRegistration) -> str:
        """Format registration data into a nice Telegram message"""
        # Handle team_members as comma-separated string
        if registration.team_members:
            members_list = [member.strip() for member in registration.team_members.split(",") if member.strip()]
            members_formatted = "\n".join([f"• {member}" for member in members_list])
        else:
            members_formatted = "• Нет дополнительных участников"

        return (
            "🎯 <b>Новая регистрация на хакатон</b>\n\n"
            f"🏷 <b>Команда:</b> {registration.team_name}\n"
            f"📚 <b>Кейс:</b> {registration.selected_case}\n"
            f"👑 <b>Капитан:</b> {registration.captain_name}\n"
            f"📧 <b>Email:</b> {registration.captain_email}\n"
            f"👥 <b>Участники:</b>\n{members_formatted}\n"
            f"📅 <b>Дата регистрации:</b> {registration.registration_date}"
        )

    def is_initialized(self) -> bool:
        """Check if the Telegram service is properly initialized"""
        return self.bot is not None and self.dispatcher is not None
