import React, { useState } from "react";
import "./RegistrationModal.css";

const RegistrationModal = ({ cases, onClose }) => {
  const [selectedCase, setSelectedCase] = useState("");
  const [captainName, setCaptainName] = useState("");
  const [teamMembers, setTeamMembers] = useState([""]);
  const [teamName, setTeamName] = useState("");
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const MAX_TEAM_MEMBERS = 4;

  // Фильтруем кейсы - убираем кейс с id 5 (регистрация закрыта)
  const availableCases = cases.filter(caseItem => caseItem.id !== 5);

  const addTeamMember = () => {
    if (teamMembers.length < MAX_TEAM_MEMBERS) {
      setTeamMembers([...teamMembers, ""]);
      if (errors.teamMembers) {
        setErrors(prev => ({ ...prev, teamMembers: "" }));
      }
    }
  };

  const removeTeamMember = (index) => {
    const newMembers = teamMembers.filter((_, i) => i !== index);
    setTeamMembers(newMembers);
    
    if (newMembers.length === 0) {
      setErrors(prev => ({ ...prev, teamMembers: "Добавьте хотя бы одного участника" }));
    } else {
      setErrors(prev => ({ ...prev, teamMembers: "" }));
    }
  };

  const updateTeamMember = (index, value) => {
    const newMembers = [...teamMembers];
    newMembers[index] = value;
    setTeamMembers(newMembers);
    
    const hasValidMember = newMembers.some(member => member.trim() !== "");
    if (hasValidMember && errors.teamMembers) {
      setErrors(prev => ({ ...prev, teamMembers: "" }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!teamName.trim()) {
      newErrors.teamName = "Введите название команды";
    }
    
    if (!selectedCase) {
      newErrors.selectedCase = "Выберите кейс";
    }
    
    if (!captainName.trim()) {
      newErrors.captainName = "Введите имя капитана";
    }
    
    if (!email.trim()) {
      newErrors.email = "Введите email";
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = "Введите корректный email";
    }
    
    const hasValidMember = teamMembers.some(member => member.trim() !== "");
    if (!hasValidMember) {
      newErrors.teamMembers = "Добавьте хотя бы одного участника помимо капитана";
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const submitRegistration = async (registrationData) => {
    const API_URL = "https://innohackwebsite-production.up.railway.app/api/registrations";

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(registrationData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return { success: true, data: result };
    } catch (error) {
      console.error("Ошибка при отправке данных:", error);
      return {
        success: false,
        error: error.message || "Не удалось подключиться к серверу",
      };
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      const firstErrorElement = document.querySelector('.error-message');
      if (firstErrorElement) {
        firstErrorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      return;
    }
    
    setIsLoading(true);

    const registrationData = {
      teamName: teamName.trim(),
      selectedCase: selectedCase,
      captainName: captainName.trim(),
      captainEmail: email.trim(),
      teamMembers: teamMembers.filter((member) => member.trim() !== ""),
      registrationDate: new Date().toISOString(),
      event: "Лицейский Хакатон 2024",
      status: "pending",
    };

    try {
      const result = await submitRegistration(registrationData);

      if (result.success) {
        alert("✅ Регистрация успешно отправлена! Мы свяжемся с вами в ближайшее время.");

        setTeamName("");
        setSelectedCase("");
        setCaptainName("");
        setEmail("");
        setTeamMembers([""]);
        setErrors({});

        onClose();
      } else {
        alert(`❌ Ошибка при регистрации: ${result.error}`);
      }
    } catch (error) {
      console.error("Ошибка:", error);
      alert("❌ Произошла непредвиденная ошибка при отправке формы.");
    } finally {
      setIsLoading(false);
    }
  };

  const selectedCaseData = availableCases.find(
    (caseItem) => caseItem.id === selectedCase
  );

  const canSubmit = teamName.trim() && 
                   selectedCase && 
                   captainName.trim() && 
                   email.trim() && 
                   teamMembers.some(member => member.trim() !== "");

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>🎯 Регистрация на хакатон</h2>
          <button className="close-btn" onClick={onClose}>
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="registration-form">
          <div className="form-section">
            <h3>👥 Информация о команде</h3>
            <div className="form-group">
              <label htmlFor="teamName">
                Название команды<span className="required-star">*</span>
              </label>
              <input
                type="text"
                id="teamName"
                value={teamName}
                onChange={(e) => {
                  setTeamName(e.target.value);
                  if (errors.teamName) {
                    setErrors(prev => ({ ...prev, teamName: "" }));
                  }
                }}
                required
                placeholder="Придумайте креативное название"
                className={`form-input ${errors.teamName ? 'error' : ''}`}
                disabled={isLoading}
              />
              {errors.teamName && <span className="error-message">{errors.teamName}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="caseSelect">
                Выберите кейс<span className="required-star">*</span>
              </label>
              <select
                id="caseSelect"
                value={selectedCase}
                onChange={(e) => {
                  setSelectedCase(e.target.value);
                  if (errors.selectedCase) {
                    setErrors(prev => ({ ...prev, selectedCase: "" }));
                  }
                }}
                required
                className={`form-select ${errors.selectedCase ? 'error' : ''}`}
                disabled={isLoading}
              >
                <option value="">-- Выберите кейс для решения --</option>
                {availableCases.map((caseItem) => (
                  <option key={caseItem.id} value={caseItem.id}>
                    Кейс {caseItem.id}: {caseItem.title}
                  </option>
                ))}
              </select>
              {errors.selectedCase && <span className="error-message">{errors.selectedCase}</span>}

              {selectedCaseData && (
                <div className="case-preview">
                  <div className="case-preview-header">
                    <span className="case-category">
                      {selectedCaseData.category}
                    </span>
                  </div>
                  <p className="case-description">
                    {selectedCaseData.shortDescription}
                  </p>
                </div>
              )}

              {/* Сообщение о закрытой регистрации на кейс 5 */}
              <div className="registration-closed-notice">
                <p>ℹ️ <strong>Регистрация на Кейс 5 временно закрыта</strong></p>
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>👑 Капитан команды</h3>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="captainName">
                  Имя капитана<span className="required-star">*</span>
                </label>
                <input
                  type="text"
                  id="captainName"
                  value={captainName}
                  onChange={(e) => {
                    setCaptainName(e.target.value);
                    if (errors.captainName) {
                      setErrors(prev => ({ ...prev, captainName: "" }));
                    }
                  }}
                  required
                  placeholder="Ваше полное имя"
                  className={`form-input ${errors.captainName ? 'error' : ''}`}
                  disabled={isLoading}
                />
                {errors.captainName && <span className="error-message">{errors.captainName}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="email">
                  Email<span className="required-star">*</span>
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    if (errors.email) {
                      setErrors(prev => ({ ...prev, email: "" }));
                    }
                  }}
                  required
                  placeholder="example@email.com"
                  className={`form-input ${errors.email ? 'error' : ''}`}
                  disabled={isLoading}
                />
                {errors.email && <span className="error-message">{errors.email}</span>}
              </div>
            </div>
          </div>

          <div className="form-section">
            <div className="section-header">
              <h3>🧑‍💻 Участники команды</h3>
              <span className="members-count">
                {teamMembers.filter((m) => m.trim() !== "").length}/
                {MAX_TEAM_MEMBERS}
              </span>
            </div>

            {errors.teamMembers && (
              <div className="error-message team-members-error">
                {errors.teamMembers}
              </div>
            )}

            <div className="team-members">
              {teamMembers.map((member, index) => (
                <div key={index} className="member-input-group">
                  <div className="member-number">#{index + 1}</div>
                  <input
                    type="text"
                    value={member}
                    onChange={(e) => updateTeamMember(index, e.target.value)}
                    placeholder={`Имя участника ${index + 1}`}
                    className="form-input"
                    disabled={isLoading}
                  />
                  {teamMembers.length > 1 && (
                    <button
                      type="button"
                      className="remove-member-btn"
                      onClick={() => removeTeamMember(index)}
                      title="Удалить участника"
                      disabled={isLoading}
                    >
                      ✕
                    </button>
                  )}
                </div>
              ))}
            </div>

            {teamMembers.length === 0 && (
              <div className="no-members-message">
                <p>
                  Участники не добавлены. Нажмите «Добавить участника», чтобы
                  включить кого-то в команду.
                </p>
              </div>
            )}

            {teamMembers.length < MAX_TEAM_MEMBERS && (
              <button
                type="button"
                className="add-member-btn"
                onClick={addTeamMember}
                disabled={isLoading}
              >
                <span>+</span>
                Добавить участника
              </button>
            )}

            <div className="members-note">
              * Обязательно добавьте хотя бы одного участника помимо капитана
            </div>
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="cancel-btn"
              onClick={onClose}
              disabled={isLoading}
            >
              Отмена
            </button>
            <button 
              type="submit" 
              className="submit-btn" 
              disabled={isLoading || !canSubmit}
            >
              {isLoading ? (
                <>
                  <div className="loading-spinner"></div>
                  Отправка...
                </>
              ) : (
                "🚀 Зарегистрировать команду"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegistrationModal;
