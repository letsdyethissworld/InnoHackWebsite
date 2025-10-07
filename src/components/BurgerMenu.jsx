import React, { useState } from "react";
import "./BurgerMenu.css"; // Стили мы добавим ниже

const BurgerMenu = ({ cases, activeTab, onTabChange }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleTabClick = (caseId) => {
    onTabChange(caseId);
    setIsOpen(false); // Закрываем меню после выбора
  };

  return (
    <div className="burger-menu">
      {/* Кнопка-бургер */}
      <button
        className={`burger-button ${isOpen ? "open" : ""}`}
        onClick={toggleMenu}
        aria-label="Открыть меню"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Затемнение фона */}
      {isOpen && <div className="menu-overlay" onClick={toggleMenu}></div>}

      {/* Боковое меню */}
      <nav className={`menu-sidebar ${isOpen ? "open" : ""}`}>
        <button
          className={`menu-item ${activeTab === "all" ? "active" : ""}`}
          onClick={() => handleTabClick("all")}
        >
          Все кейсы
        </button>

        {cases.map((caseItem) => (
          <button
            key={caseItem.id}
            className={`menu-item ${activeTab === caseItem.id ? "active" : ""}`}
            onClick={() => handleTabClick(caseItem.id)}
          >
            Кейс {caseItem.id}: {caseItem.title}
          </button>
        ))}
      </nav>
    </div>
  );
};

export default BurgerMenu;
