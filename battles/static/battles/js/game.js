document.addEventListener('DOMContentLoaded', function() {
    const startBattleBtn = document.getElementById('start-battle');
    const battleContainer = document.getElementById('battle-container');
    const battleResult = document.getElementById('battle-result');
    
    let currentBattleId = null;
    let currentQuestionNum = 1;
    let totalQuestions = 5;
    
    startBattleBtn.addEventListener('click', function() {
        startBattleBtn.disabled = true;
        
        fetch('/battles/start-battle/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            currentBattleId = data.battle_id;
            battleContainer.style.display = 'block';
            loadQuestion(currentBattleId, 1);
        })
        .catch(error => {
            console.error('Error:', error);
            startBattleBtn.disabled = false;
        });
    });
    
    function loadQuestion(battleId, questionNum) {
        fetch(`/battles/battle/${battleId}/question/${questionNum}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('question-subject').textContent = data.subject;
                document.getElementById('question-text').textContent = data.question;
                document.getElementById('current-question').textContent = questionNum;
                document.getElementById('total-questions').textContent = data.total_questions;
                
                const answersContainer = document.getElementById('answers-container');
                answersContainer.innerHTML = '';
                
                data.answers.forEach(answer => {
                    const answerBtn = document.createElement('button');
                    answerBtn.className = 'answer-btn';
                    answerBtn.textContent = answer.text;
                    answerBtn.dataset.answerId = answer.id;
                    
                    answerBtn.addEventListener('click', function() {
                        submitAnswer(battleId, questionNum, answer.id);
                    });
                    
                    answersContainer.appendChild(answerBtn);
                });
            })
            .catch(error => console.error('Error:', error));
    }
    
    function submitAnswer(battleId, questionNum, answerId) {
        const formData = new FormData();
        formData.append('answer_id', answerId);
        
        fetch(`/battles/battle/${battleId}/question/${questionNum}/submit/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('battle-score').textContent = data.score;
            
            if (questionNum < totalQuestions) {
                currentQuestionNum++;
                loadQuestion(battleId, currentQuestionNum);
            } else {
                completeBattle(battleId);
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    function completeBattle(battleId) {
        fetch(`/battles/battle/${battleId}/complete/`)
            .then(response => response.json())
            .then(data => {
                battleContainer.style.display = 'none';
                battleResult.style.display = 'block';
                
                document.getElementById('final-score').textContent = data.score;
                document.getElementById('experience-gained').textContent = data.experience_gained;
                document.getElementById('coins-gained').textContent = data.coins_gained;
                
                if (data.leveled_up) {
                    document.getElementById('level-up-message').style.display = 'block';
                }
            })
            .catch(error => console.error('Error:', error));
    }
    
    document.getElementById('back-to-arena').addEventListener('click', function() {
        battleResult.style.display = 'none';
        startBattleBtn.disabled = false;
        currentQuestionNum = 1;
        location.reload(); // Yeniləyib statistikaları yeniləmək üçün
    });
    
    // CSRF token üçün köməkçi funksiya
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});