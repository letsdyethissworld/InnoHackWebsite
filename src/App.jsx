import React, { useState } from "react";
import CaseCard from "./components/CaseCard";
import CaseDetails from "./components/CaseDetails";
import BurgerMenu from "./components/BurgerMenu";
import DesktopTabs from "./components/DesktopTabs";
import { Carousel } from "antd";
import { cases } from "./data/cases";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("all");
  
  // Регистрация закрыта - убираем состояние для модального окна

  const handleCaseClick = (caseId) => {
    setActiveTab(caseId);
  };

  const handleLogoClick = () => {
    setActiveTab("all");
  };

  const carouselSettings = {
    dots: true,
    infinite: true,
    autoplay: true,
    arrows: true,
    autoplaySpeed: 6000,
    speed: 1000,
    slidesToShow: 1,
    draggable: false,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };

  return (
    <div className="App">
      {/* Убираем кнопку регистрации и добавляем сообщение о закрытии */}
      <div className="registration-closed-header">
        <div className="closed-message">
          <span className="closed-icon">🚫</span>
          <div className="closed-text">
            <strong>Регистрация закрыта</strong>
            <span>Набор команд на хакатон завершен</span>
          </div>
        </div>
      </div>

      <header className="app-header">
        <div className="logo" onClick={handleLogoClick}>
          <h1>Кейсы InnoHackathon</h1>
        </div>
        <p>
          Изучите предложенные кейсы и выберите наиболее интересный для
          реализации
        </p>
      </header>

      <main className="cases-container">
        {/* Вкладки */}
        <DesktopTabs
          cases={cases}
          activeTab={activeTab}
          onTabChange={setActiveTab}
        />
        <BurgerMenu
          cases={cases}
          activeTab={activeTab}
          onTabChange={setActiveTab}
        />
        
        {/* Контент вкладок */}
        <div className="tab-content">
          {activeTab === "all" ? (
            <div className="all-cases">
              <h2>Все доступные кейсы</h2>
              <p className="subtitle">
                Нажмите на карточку кейса для просмотра детальной информации
              </p>
              <div className="cases-carousel">
                <Carousel {...carouselSettings} className="carousel-container">
                  {cases.map((caseItem) => (
                    <div key={caseItem.id} className="carousel-slide">
                      <CaseCard
                        caseItem={caseItem}
                        onClick={() => handleCaseClick(caseItem.id)}
                      />
                    </div>
                  ))}
                </Carousel>
              </div>
            </div>
          ) : activeTab === "schedule" ? (
            <Schedule />
          ) : (
            <CaseDetails
              caseItem={cases.find((caseItem) => caseItem.id === activeTab)}
            />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Лицейский Хакатон 2025 • Разработано с ❤️ для участников</p>
      </footer>
    </div>
  );
}

export default App;
