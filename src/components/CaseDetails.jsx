import React from "react";
import "../App.css";

const CaseDetails = ({ caseItem }) => {
  if (!caseItem) {
    return <div className="case-details">Кейс не найден</div>;
  }

  return (
    <div className="case-details">
      <div className="case-header">
        <div className="case-title-section">
          <span className="case-number">Кейс {caseItem.id}</span>
          <h1>{caseItem.title}</h1>
          <div className="case-meta">
            <span className="category">{caseItem.category}</span>
          </div>
        </div>
      </div>

      <div className="case-content">
        <div className="main-description">
          <h2>📖 Описание проекта</h2>
          <p>{caseItem.fullDescription}</p>
        </div>

        <div className="details-grid">
          <div className="detail-section">
            <h3>🎯 Цели проекта</h3>
            <ul>
              {caseItem.goals.map((goal, index) => (
                <li key={index}>{goal}</li>
              ))}
            </ul>
          </div>

          <div className="detail-section">
            <h3>📋 Основные требования</h3>
            <ul>
              {caseItem.requirements.map((req, index) => (
                <li key={index}>{req}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="case-footer">
          <div className="team-size">
            <h3>👥 Рекомендуемый размер команды</h3>
            <p>{caseItem.teamSize}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CaseDetails;
