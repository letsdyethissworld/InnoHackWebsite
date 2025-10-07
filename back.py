import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from pydantic import BaseModel
from typing import List
import uvicorn
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import pysqlite3
import sys
sys.modules['sqlite3'] = pysqlite3
port = int(os.environ.get("PORT", 8000))

BOT_TOKEN = "8350542451:AAG_fJx9JzJOnLjJxcFGR4JWd_w1k6mBT2s"
ADMINS = [907136578]
DATABASE_URL = "sqlite:///registrations.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class TeamRegistration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    teamName = Column(String, nullable=False)
    selectedCase = Column(String, nullable=False)
    captainName = Column(String, nullable=False)
    captainEmail = Column(String, nullable=False)
    teamMembers = Column(Text, nullable=False)
    registrationDate = Column(String, nullable=False)
    event = Column(String, nullable=False)
    status = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

app = FastAPI(title="Registration Bot API")

# Добавьте CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Registration(BaseModel):
    teamName: str
    selectedCase: str
    captainName: str
    captainEmail: str
    teamMembers: List[str]
    registrationDate: str
    event: str
    status: str

async def notify_admins(reg_data: Registration):
    members_formatted = "\n".join([f"• {member}" for member in reg_data.teamMembers if member.strip()])
    text = (
        f"🎯 <b>Новая регистрация на хакатон</b>\n\n"
        f"🏷 <b>Команда:</b> {reg_data.teamName}\n"
        f"📚 <b>Кейс:</b> {reg_data.selectedCase}\n"
        f"👑 <b>Капитан:</b> {reg_data.captainName}\n"
        f"📧 <b>Email:</b> {reg_data.captainEmail}\n"
        f"👥 <b>Участники:</b>\n{members_formatted}\n"
        f"📅 <b>Дата регистрации:</b> {reg_data.registrationDate}"
    )

    for admin_id in ADMINS:
        try:
            await bot.send_message(chat_id=admin_id, text=text)
        except Exception as e:
            print(f"Failed to send message to admin {admin_id}: {e}")

def save_registration_to_db(reg_data: Registration):
    db = SessionLocal()
    try:
        new_entry = TeamRegistration(
            teamName=reg_data.teamName,
            selectedCase=reg_data.selectedCase,
            captainName=reg_data.captainName,
            captainEmail=reg_data.captainEmail,
            teamMembers=",".join(reg_data.teamMembers),
            registrationDate=reg_data.registrationDate,
            event=reg_data.event,
            status=reg_data.status,
        )
        db.add(new_entry)
        db.commit()
        return new_entry.id
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@app.post("/api/registrations")
async def registration_endpoint(registration: Registration):
    try:
        # Сохраняем в базу данных
        registration_id = save_registration_to_db(registration)
        
        # Уведомляем админов (асинхронно, не блокируя ответ)
        asyncio.create_task(notify_admins(registration))

        return {
            "status": "success", 
            "message": "Registration saved and admins notified.",
            "registration_id": registration_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Hackathon Registration API is running"}

if __name__ == "__main__":
    uvicorn.run("back:app", host="0.0.0.0", port=port, reload=True)
