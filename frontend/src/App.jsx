import React, { useState } from "react";
import CaseCard from "./components/CaseCard";
import CaseDetails from "./components/CaseDetails";
import RegistrationModal from "./components/RegistrationModal";
import BurgerMenu from "./components/BurgerMenu";
import { Carousel } from "antd";
import { cases } from "./data/cases";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("all");
  const [showRegistration, setShowRegistration] = useState(false);

  // Функция для перехода к конкретному кейсу
  const handleCaseClick = (caseId) => {
    setActiveTab(caseId);
  };

  const handleLogoClick = () => {
    setActiveTab("all");
  };

  const carouselSettings = {
    dots: true,
    infinite: true, // было "infinte"
    autoplay: true,
    arrows: true, // было "arrow"
    autoplaySpeed: 6000,
    speed: 1000,
    slidesToShow: 1,
    draggable: false, // было "darggable"
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
      {/* Кнопка регистрации в правом верхнем углу */}
      <button
        className="registration-btn"
        onClick={() => setShowRegistration(true)}
      >
        📝 Зарегистрироваться
      </button>

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
          ) : (
            <CaseDetails
              caseItem={cases.find((caseItem) => caseItem.id === activeTab)}
            />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Лицейский Хакатон 2024 • Разработано с ❤️ для участников</p>
      </footer>

      {/* Модальное окно регистрации */}
      {showRegistration && (
        <RegistrationModal
          cases={cases}
          onClose={() => setShowRegistration(false)}
        />
      )}
    </div>
  );
}

export default App;
