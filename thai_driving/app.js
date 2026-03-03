/**
 * ThaiDrive - Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // State Management
    const state = {
        view: 'home', // 'home', 'quiz', 'results'
        mode: 'exam', // 'exam', 'practice'
        currentQuestions: [],
        currentIndex: 0,
        userAnswers: [],
        timer: null,
        timeLeft: 3600, // 60 minutes in seconds
        startTime: null,
        results: null
    };

    // DOM Elements
    const views = {
        home: document.getElementById('hero'), // Use hero as home entry
        categories: document.getElementById('categories'),
        signs: document.getElementById('signs-section'),
        history: document.getElementById('history-section'),
        quiz: document.getElementById('quiz-view'),
        results: document.getElementById('results-view'),
        main: document.getElementById('main-content')
    };

    const questionCard = document.getElementById('question-card');
    const progressBar = document.getElementById('progress-bar-fill');
    const questionNumberLabel = document.getElementById('question-number');
    const timerLabel = document.getElementById('quiz-timer');
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');

    // Initialization
    function init() {
        setupEventListeners();
        renderHome();
    }

    function setupEventListeners() {
        // Navigation
        document.getElementById('nav-home').addEventListener('click', () => switchView('home'));
        document.getElementById('nav-signs').addEventListener('click', () => switchView('signs'));
        document.getElementById('nav-history').addEventListener('click', () => switchView('history'));

        document.getElementById('start-exam-btn').addEventListener('click', () => startQuiz('exam'));
        document.getElementById('practice-btn').addEventListener('click', () => startQuiz('practice'));
        document.getElementById('exit-quiz').addEventListener('click', () => {
            if (confirm('Are you sure you want to exit the quiz? Your progress will be lost.')) {
                switchView('home');
                stopTimer();
            }
        });

        // Quiz Actions
        nextBtn.addEventListener('click', handleNext);
        prevBtn.addEventListener('click', handlePrev);

        // Results Actions
        document.getElementById('restart-btn').addEventListener('click', () => {
            startQuiz(state.mode);
        });
        document.getElementById('back-home-btn').addEventListener('click', () => {
            switchView('home');
        });

        // Category Cards
        document.querySelectorAll('.category-card').forEach(card => {
            card.addEventListener('click', () => {
                const category = card.dataset.category;
                startQuiz('practice', category);
            });
        });
    }

    function switchView(viewName) {
        state.view = viewName;

        // Hide all quiz/results
        views.quiz.classList.add('hidden');
        views.results.classList.add('hidden');

        // Navigation logic for main content
        if (['home', 'signs', 'history'].includes(viewName)) {
            views.main.classList.remove('hidden');
            views.home.classList.toggle('hidden', viewName !== 'home');
            views.categories.classList.toggle('hidden', viewName !== 'home');
            views.signs.classList.toggle('hidden', viewName !== 'signs');
            views.history.classList.toggle('hidden', viewName !== 'history');

            if (viewName === 'signs') renderSigns();
            if (viewName === 'history') renderHistory();
        } else if (viewName === 'quiz') {
            views.main.classList.add('hidden');
            views.quiz.classList.remove('hidden');
        } else if (viewName === 'results') {
            views.main.classList.add('hidden');
            views.results.classList.remove('hidden');
        }

        // Update Nav UI
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.id === `nav-${viewName}`);
        });
    }

    function startQuiz(mode, category = null) {
        state.mode = mode;
        state.currentIndex = 0;
        state.userAnswers = [];
        state.timeLeft = 3600;

        let pool = [...window.questionsData];

        if (category) {
            pool = pool.filter(q => q.category === category);
        }

        // Shuffle and select
        pool = pool.sort(() => Math.random() - 0.5);

        if (mode === 'exam') {
            // For real exam take 50, for demo take all available but max 50
            state.currentQuestions = pool.slice(0, 50);
        } else {
            // Practice mode: take random 15 or all in category
            state.currentQuestions = pool.slice(0, 15);
        }

        state.userAnswers = new Array(state.currentQuestions.length).fill(null);

        switchView('quiz');
        renderQuestion();
        startTimer();
    }

    function renderQuestion() {
        const question = state.currentQuestions[state.currentIndex];
        const isLast = state.currentIndex === state.currentQuestions.length - 1;

        // Update UI
        questionNumberLabel.textContent = `Question ${state.currentIndex + 1}/${state.currentQuestions.length}`;
        progressBar.style.width = `${((state.currentIndex + 1) / state.currentQuestions.length) * 100}%`;

        nextBtn.textContent = isLast ? 'Finish Exam' : 'Next';
        prevBtn.disabled = state.currentIndex === 0;

        questionCard.innerHTML = `
            <div class="question-header">
                <span class="category-tag">${question.category.replace('-', ' ').toUpperCase()}</span>
                <h3 class="question-text">${question.question}</h3>
            </div>
            <div class="options-list">
                ${question.options.map((opt, idx) => `
                    <div class="option-item ${state.userAnswers[state.currentIndex] === idx ? 'selected' : ''}" data-index="${idx}">
                        <div class="option-marker">${String.fromCharCode(65 + idx)}</div>
                        <div class="option-text">${opt}</div>
                    </div>
                `).join('')}
            </div>
        `;

        // Add click events to options
        questionCard.querySelectorAll('.option-item').forEach(item => {
            item.addEventListener('click', () => {
                const idx = parseInt(item.dataset.index);
                state.userAnswers[state.currentIndex] = idx;

                // Highlight selected
                questionCard.querySelectorAll('.option-item').forEach(i => i.classList.remove('selected'));
                item.classList.add('selected');

                // Auto next in practice mode? Maybe not to keep it consistent
            });
        });
    }

    function handleNext() {
        if (state.userAnswers[state.currentIndex] === null) {
            alert('Please select an answer before continuing.');
            return;
        }

        if (state.currentIndex < state.currentQuestions.length - 1) {
            state.currentIndex++;
            renderQuestion();
        } else {
            finishQuiz();
        }
    }

    function handlePrev() {
        if (state.currentIndex > 0) {
            state.currentIndex--;
            renderQuestion();
        }
    }

    function startTimer() {
        state.startTime = Date.now();
        stopTimer(); // Clear existing

        state.timer = setInterval(() => {
            state.timeLeft--;
            if (state.timeLeft <= 0) {
                clearInterval(state.timer);
                alert('Time is up!');
                finishQuiz();
            }
            updateTimerDisplay();
        }, 1000);

        updateTimerDisplay();
    }

    function stopTimer() {
        if (state.timer) clearInterval(state.timer);
    }

    function updateTimerDisplay() {
        const mins = Math.floor(state.timeLeft / 60);
        const secs = state.timeLeft % 60;
        timerLabel.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

        if (state.timeLeft < 300) {
            timerLabel.style.color = 'var(--error)';
        } else {
            timerLabel.style.color = 'inherit';
        }
    }

    function finishQuiz() {
        stopTimer();
        calculateResults();
        showResults();
    }

    function calculateResults() {
        let correct = 0;
        state.currentQuestions.forEach((q, idx) => {
            if (state.userAnswers[idx] === q.answer) {
                correct++;
            }
        });

        const total = state.currentQuestions.length;
        const percentage = Math.round((correct / total) * 100);
        const timeSpent = Math.floor((Date.now() - state.startTime) / 1000);

        state.results = {
            correct,
            total,
            percentage,
            timeSpent,
            passed: percentage >= 90
        };

        // Save to history (Local Storage)
        const history = JSON.parse(localStorage.getItem('thai_drive_history') || '[]');
        history.unshift({
            date: new Date().toISOString(),
            mode: state.mode,
            score: `${correct}/${total}`,
            percentage: percentage,
            passed: state.results.passed
        });
        localStorage.setItem('thai_drive_history', JSON.stringify(history.slice(0, 10)));
    }

    function showResults() {
        const { correct, total, percentage, timeSpent, passed } = state.results;

        document.getElementById('result-title').textContent = passed ? 'Congratulations!' : 'Keep Practicing!';
        document.getElementById('result-message').textContent = passed
            ? 'You passed the mock exam with flying colors. You are ready for the real thing!'
            : 'You didn\'t reach the 90% pass mark. Review your mistakes and try again.';

        document.getElementById('status-icon').textContent = passed ? '🏆' : '📚';
        document.getElementById('final-score').textContent = `${correct}/${total}`;
        document.getElementById('final-percentage').textContent = `${percentage}%`;

        const mins = Math.floor(timeSpent / 60);
        const secs = timeSpent % 60;
        document.getElementById('result-time').textContent = `${mins}m ${secs}s`;
        document.getElementById('result-correct').textContent = correct;
        document.getElementById('result-incorrect').textContent = total - correct;

        // Apply pass/fail styles
        const scoreCircle = document.querySelector('.score-circle');
        scoreCircle.style.borderColor = passed ? 'var(--success)' : 'var(--error)';

        switchView('results');
    }

    function renderSigns(filter = 'all') {
        const signsGrid = document.getElementById('signs-grid');
        // Sample signs data (In a real app, this would be more extensive)
        const signs = [
            { title: "No Entry", type: "regulatory", icon: "⛔", desc: "No vehicles allowed to enter." },
            { title: "Stop", type: "regulatory", icon: "🛑", desc: "Must come to a complete stop." },
            { title: "Yield", type: "regulatory", icon: "▽", desc: "Give way to other traffic." },
            { title: "Speed Limit 60", type: "regulatory", icon: "60", desc: "Maximum speed limit 60 km/h." },
            { title: "Sharp Curve Left", type: "warning", icon: "↶", desc: "Warning of a sharp curve to the left ahead." },
            { title: "Slippery Road", type: "warning", icon: "⚠️", desc: "Road may be slippery when wet." },
            { title: "Go Straight Only", type: "mandatory", icon: "↑", desc: "You must proceed straight ahead only." },
            { title: "Turn Left only", type: "mandatory", icon: "←", desc: "You must turn left at intersection." }
        ];

        const filtered = filter === 'all' ? signs : signs.filter(s => s.type === filter);

        signsGrid.innerHTML = filtered.map(s => `
            <div class="sign-card glass fade-in">
                <div class="sign-image">${s.icon}</div>
                <div class="sign-title">${s.title}</div>
                <div class="sign-desc">${s.desc}</div>
            </div>
        `).join('');

        // Handle filters
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
            if (!btn.hasListener) {
                btn.addEventListener('click', () => renderSigns(btn.dataset.filter));
                btn.hasListener = true;
            }
        });
    }

    function renderHistory() {
        const historyList = document.getElementById('history-list');
        const history = JSON.parse(localStorage.getItem('thai_drive_history') || '[]');

        if (history.length === 0) {
            historyList.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 2rem;">No history yet. Take an exam to see your progress!</td></tr>';
            return;
        }

        historyList.innerHTML = history.map(item => `
            <tr>
                <td>${new Date(item.date).toLocaleDateString()}</td>
                <td>${item.mode.toUpperCase()}</td>
                <td>${item.score} (${item.percentage}%)</td>
                <td><span class="history-tag ${item.passed ? 'tag-pass' : 'tag-fail'}">${item.passed ? 'PASS' : 'FAIL'}</span></td>
            </tr>
        `).join('');
    }

    function renderHome() {
        // Initially show home
        switchView('home');
    }

    init();
});
