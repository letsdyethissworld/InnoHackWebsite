import React, { useState } from "react";
import "./RegistrationModal.css";

const RegistrationModal = ({ cases, onClose }) => {
  const [selectedCase, setSelectedCase] = useState("");
  const [captainName, setCaptainName] = useState("");
  const [teamMembers, setTeamMembers] = useState([]);
  const [teamName, setTeamName] = useState("");
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const MAX_TEAM_MEMBERS = 4;

  const addTeamMember = () => {
    if (teamMembers.length < MAX_TEAM_MEMBERS) {
      setTeamMembers([...teamMembers, ""]);
    }
  };

  const removeTeamMember = (index) => {
    // Удаляем участника без проверки на минимальное количество
    const newMembers = teamMembers.filter((_, i) => i !== index);
    setTeamMembers(newMembers);
  };

  const updateTeamMember = (index, value) => {
    const newMembers = [...teamMembers];
    newMembers[index] = value;
    setTeamMembers(newMembers);
  };

  // РЕАЛЬНЫЙ HTTP ЗАПРОС
  const submitRegistration = async (registrationData) => {
  const API_URL = "https://innohackwebsite-production.up.railway.app/api/registrations";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      mode: 'cors', // явно указываем режим CORS
      body: JSON.stringify(registrationData),
    });

    if (!response.ok) {
      // Более детальная информация об ошибке
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    const result = await response.json();
    return { success: true, data: result };
  } catch (error) {
    console.error("Ошибка при отправке данных:", error);
    
    // Проверяем, является ли ошибка CORS
    if (error.message.includes('Failed to fetch') || error.message.includes('CORS')) {
      return {
        success: false,
        error: "CORS ошибка: Бэкенд не разрешает запросы с этого домена. Нужно настроить CORS на сервере."
      };
    }
    
    return {
      success: false,
      error: error.message || "Не удалось подключиться к серверу"
    };
  }
};

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const registrationData = {
      teamName: teamName.trim(),
      selectedCase: selectedCase,
      captainName: captainName.trim(),
      captainEmail: email.trim(),
      teamMembers: teamMembers.filter((member) => member.trim() !== ""),
      registrationDate: new Date().toISOString(),
      // Дополнительные поля которые могут понадобиться
      event: "Лицейский Хакатон 2024",
      status: "pending",
    };

    try {
      // Отправляем реальный HTTP запрос
      const result = await submitRegistration(registrationData);

      if (result.success) {
        alert(
          "✅ Регистрация успешно отправлена! Мы свяжемся с вами в ближайшее время."
        );

        // Очищаем форму после успешной отправки
        setTeamName("");
        setSelectedCase("");
        setCaptainName("");
        setEmail("");
        setTeamMembers([""]);

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

  // Альтернативный вариант с axios (если предпочитаете)
  /*
  const submitRegistrationWithAxios = async (registrationData) => {
    try {
      const response = await axios.post('https://your-backend-api.com/api/registrations', registrationData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Ошибка при отправке данных:', error);
      return { success: false, error: error.message };
    }
  };
  */

  const selectedCaseData = cases.find(
    (caseItem) => caseItem.id === selectedCase
  );

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
                onChange={(e) => setTeamName(e.target.value)}
                required
                placeholder="Придумайте креативное название"
                className="form-input"
                disabled={isLoading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="caseSelect">
                Выберите кейс<span className="required-star">*</span>
              </label>
              <select
                id="caseSelect"
                value={selectedCase}
                onChange={(e) => setSelectedCase(e.target.value)}
                required
                className="form-select"
                disabled={isLoading}
              >
                <option value="">-- Выберите кейс для решения --</option>
                {cases.map((caseItem) => (
                  <option key={caseItem.id} value={caseItem.id}>
                    Кейс {caseItem.id}: {caseItem.title}
                  </option>
                ))}
              </select>

              {selectedCaseData && (
                <div className="case-preview">
                  <div className="case-preview-header">
                    <span
                      className={`case-difficulty ${selectedCaseData.difficulty.toLowerCase()}`}
                    >
                      {selectedCaseData.difficulty}
                    </span>
                    <span className="case-category">
                      {selectedCaseData.category}
                    </span>
                  </div>
                  <p className="case-description">
                    {selectedCaseData.shortDescription}
                  </p>
                </div>
              )}
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
                  onChange={(e) => setCaptainName(e.target.value)}
                  required
                  placeholder="Ваше полное имя"
                  className="form-input"
                  disabled={isLoading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">
                  Email<span className="required-star">*</span>
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="example@email.com"
                  className="form-input"
                  disabled={isLoading}
                />
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
                  {/* Всегда показываем кнопку удаления */}
                  <button
                    type="button"
                    className="remove-member-btn"
                    onClick={() => removeTeamMember(index)}
                    title="Удалить участника"
                    disabled={isLoading}
                  >
                    ✕
                  </button>
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
              * Максимальное количество участников (помимо капитана):{" "}
              {MAX_TEAM_MEMBERS}
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
            <button type="submit" className="submit-btn" disabled={isLoading}>
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
