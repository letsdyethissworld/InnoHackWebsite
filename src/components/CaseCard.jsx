import React from "react";

const CaseCard = ({ caseItem, onClick }) => {
  return (
    <div className="case-card" onClick={onClick}>
      <div className="case-header">
        <span className="case-number">Кейс {caseItem.id}</span>
      </div>

      <h3>{caseItem.title}</h3>
      <p className="category">{caseItem.category}</p>

      <p className="short-description">{caseItem.shortDescription}</p>

      <div className="card-footer">
        <div className="team-info">
          <span>👥 {caseItem.teamSize}</span>
        </div>
      </div>

      {/* Подсказка что карточка кликабельна */}
      <div className="click-hint">Нажмите для подробностей →</div>
    </div>
  );
};

export default CaseCard;
