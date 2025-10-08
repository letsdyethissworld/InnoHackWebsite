import React from "react";
import "./DesktopTabs.css";

const DesktopTabs = ({ cases, activeTab, onTabChange }) => {
  return (
    <div className="desktop-tabs-container">
      <div className="tabs">
        <button
          className={`tab-btn ${activeTab === "all" ? "active" : ""}`}
          onClick={() => onTabChange("all")}
        >
          Все кейсы
        </button>
        
        <button
          className={`tab-btn ${activeTab === "schedule" ? "active" : ""}`}
          onClick={() => onTabChange("schedule")}
        >
          Расписание
        </button>
        
        {cases.map((caseItem) => (
          <button
            key={caseItem.id}
            className={`tab-btn ${activeTab === caseItem.id ? "active" : ""}`}
            onClick={() => onTabChange(caseItem.id)}
          >
            Кейс {caseItem.id}
          </button>
        ))}
      </div>
    </div>
  );
};

export default DesktopTabs;
