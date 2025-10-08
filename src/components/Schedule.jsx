import React from "react";
import "./Schedule.css";

const Schedule = () => {
  const scheduleData = [
    {
      date: "10 октября 2025",
      events: [
        { time: "8:00", description: "Открытие хакатона, представление кейсов" },
        { time: "8:40", description: "Завтрак" },
        { time: "9:00", description: "Начало работы над кейсами" },
        { time: "12:30", description: "Обед" },
        { time: "13:00", description: "Продолжение решения кейсов" },
        { time: "15:30", description: "Полдник" },
        { time: "17:30", description: "Ужин" },
        { time: "до 22:00", description: "Продолжение работы по желанию команд" }
      ]
    },
    {
      date: "11 октября 2025", 
      events: [
        { time: "8:00", description: "Продолжение работы над проектами" },
        { time: "8:40", description: "Завтрак" },
        { time: "9:00", description: "Финальные доработки и подготовка к защите" },
        { time: "10:00", description: "Защита проектов перед жюри" },
        { time: "11:00", description: "Обед и отъезд участников" }
      ]
    },
    {
      date: "13 октября 2025",
      events: [
        { time: "На линейке", description: "Торжественное награждение победителей" }
      ]
    }
  ];

  return (
    <div className="schedule">
      <div className="schedule-header">
        <h1>Расписание хакатона</h1>
        <p className="schedule-subtitle">
          Ознакомьтесь с программой мероприятий на все дни соревнований
        </p>
      </div>

      <div className="schedule-timeline">
        {scheduleData.map((day, dayIndex) => (
          <div key={dayIndex} className="schedule-day">
            <div className="day-header">
              <div className="day-date">{day.date}</div>
              <div className="day-divider"></div>
            </div>
            
            <div className="events-list">
              {day.events.map((event, eventIndex) => (
                <div key={eventIndex} className="event-item">
                  <div className="event-time">
                    {event.time}
                  </div>
                  <div className="event-content">
                    <div className="event-dot"></div>
                    <div className="event-description">
                      {event.description}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="schedule-notes">
        <h3>💡 Важная информация</h3>
        <ul>
          <li>Все временные слоты являются ориентировочными</li>
          <li>Расписание может меняться со временем!</li>
          <li>Питание предоставляется для всех участников</li>
          <li>Рабочее пространство доступно до 22:00 в первый день</li>
        </ul>
      </div>
    </div>
  );
};

export default Schedule;
