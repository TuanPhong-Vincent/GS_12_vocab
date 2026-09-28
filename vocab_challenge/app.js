/**
 * GLOBAL SUCCESS 12 - SPICED REPETITION VOCABULARY CHALLENGE
 * Core Application Engine: Leitner SRS, Due Date Tracker, 3D Flashcards, Quiz Mode, Time Simulator
 */

(function () {
  'use strict';

  // ==========================================
  // CONFIGURATION & CONSTANTS
  // ==========================================
  const STORAGE_KEY = 'GS12_SRS_DATA_V1';
  const START_DATE_KEY = 'GS12_SRS_START_DATE';
  const SOUND_ENABLED_KEY = 'GS12_SRS_SOUND_ENABLED';

  function getAllDaysData() {
    return window.GS12_50_DAYS_DATA || window.IELTS_50_DAYS_DATA || [];
  }

  const LEVEL_CONFIG = {
    1: { 
      id: 1, 
      name: 'Hộp 1: Từ Mới (Khởi Đầu)', 
      intervalDays: 0, 
      nextIntervalDays: 3, 
      color: '#f97316', 
      desc: 'Học 5 từ mới mỗi ngày theo lộ trình. Học xong chuyển sang Hộp +3 Ngày.' 
    },
    2: { 
      id: 2, 
      name: 'Hộp 2: +3 Ngày', 
      intervalDays: 3, 
      nextIntervalDays: 7, 
      color: '#38bdf8', 
      desc: 'Ôn lại sau 3 ngày kể từ bài học theo tag ngày của từ vựng.' 
    },
    3: { 
      id: 3, 
      name: 'Hộp 3: +7 Ngày', 
      intervalDays: 7, 
      nextIntervalDays: 14, 
      color: '#818cf8', 
      desc: 'Ôn lại sau 7 ngày theo tag ngày của từ vựng.' 
    },
    4: { 
      id: 4, 
      name: 'Hộp 4: +14 Ngày', 
      intervalDays: 14, 
      nextIntervalDays: 30, 
      color: '#c084fc', 
      desc: 'Ôn lại sau 14 ngày theo tag ngày của từ vựng.' 
    },
    5: { 
      id: 5, 
      name: 'Hộp 5: +30 Ngày (Master)', 
      intervalDays: 30, 
      nextIntervalDays: 0, 
      color: '#34d399', 
      desc: 'Khắc sâu vào trí nhớ dài hạn (Master).' 
    }
  };

  // ==========================================
  // STATE MANAGEMENT
  // ==========================================
  let state = {
    userCards: {}, // cardId -> { id, word, day, unit, level, learnedDate, lastReviewed, nextReviewDate, streak, reviewCount, mastered, history: [] }
    learnedDays: {}, // dayNumber -> true
    startDate: null, // Ngày bắt đầu thử thách học tập (ISO string)
    soundEnabled: true,
    currentTab: 'folders', // 'folders' | 'roadmap' | 'arena' | 'analytics'
    currentFolderId: 1,
    reviewQueue: [],
    reviewIndex: 0,
    isCardFlipped: false,
    arenaMode: 'flashcard', // 'flashcard' | 'quiz' | 'fillblank' | 'scramble'
    sessionType: 'practice', // 'srs' or 'practice' (chỉ học & luyện tập, không nhảy hộp lung tung)
    sessionDayNum: null,
    sessionTitle: '',
    activeQuizQuestion: null
  };

  // ==========================================
  // SOUND EFFECTS (Web Audio API)
  // ==========================================
  let audioCtx = null;
  function getAudioContext() {
    if (!audioCtx && (window.AudioContext || window.webkitAudioContext)) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioCtx;
  }

  function playSound(type) {
    if (!state.soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      if (ctx.state === 'suspended') {
        ctx.resume();
      }

      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      if (type === 'flip') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(320, now);
        osc.frequency.exponentialRampToValueAtTime(540, now + 0.08);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
        osc.start(now);
        osc.stop(now + 0.08);
      } else if (type === 'good') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(523.25, now); // C5
        osc.frequency.setValueAtTime(659.25, now + 0.08); // E5
        osc.frequency.setValueAtTime(783.99, now + 0.16); // G5
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
        osc.start(now);
        osc.stop(now + 0.28);
      } else if (type === 'again') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(240, now);
        osc.frequency.exponentialRampToValueAtTime(160, now + 0.15);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
        osc.start(now);
        osc.stop(now + 0.15);
      }
    } catch (e) {
      console.warn('Audio playback error', e);
    }
  }

  // ==========================================
  // TEXT TO SPEECH (Web Speech API)
  // ==========================================
  function speakText(text) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 0.9;
    const voices = window.speechSynthesis.getVoices();
    const enVoice = voices.find(v => (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Samantha') || v.name.includes('David')) && v.lang.startsWith('en'));
    if (enVoice) utterance.voice = enVoice;
    window.speechSynthesis.speak(utterance);
  }

  // ==========================================
  // DATE HELPER UTILITIES
  // ==========================================
  function normalizeDate(d) {
    const date = new Date(d);
    date.setHours(0, 0, 0, 0);
    return date;
  }

  function addDays(date, days) {
    const res = new Date(date);
    res.setDate(res.getDate() + days);
    return res;
  }

  function formatDateDisplay(d) {
    const date = new Date(d);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  }

  function formatDateISO(d) {
    const date = new Date(d);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  function getRemainingDays(nextDate, refDate) {
    const d1 = normalizeDate(refDate);
    const d2 = normalizeDate(nextDate);
    const diffTime = d2.getTime() - d1.getTime();
    return Math.round(diffTime / (1000 * 3600 * 24));
  }

  // ==========================================
  // LOCAL STORAGE PERSISTENCE & REAL-TIME PROGRESS
  // ==========================================
  function getToday() {
    return normalizeDate(new Date());
  }

  function getStartDateKey() {
    return currentUser ? `${START_DATE_KEY}_${currentUser.id}` : `${START_DATE_KEY}_LOCAL`;
  }

  function getChallengeCurrentDay() {
    const today = getToday();
    const completedCount = Object.keys(state.learnedDays).filter(k => state.learnedDays[k]).length;
    // Nếu học viên mới bắt đầu (chưa hoàn thành ngày nào và chưa có thẻ nào tăng cấp), khởi đầu tại Ngày 1
    if (completedCount === 0 && (!state.userCards || Object.values(state.userCards).every(c => (c.streak || 0) === 0))) {
      state.startDate = today.toISOString();
      saveState();
      return 1;
    }

    if (!state.startDate) {
      state.startDate = today.toISOString();
      saveState();
    }
    const start = normalizeDate(new Date(state.startDate));
    const diffTime = today.getTime() - start.getTime();
    const diffDays = Math.floor(diffTime / (1000 * 3600 * 24));
    // Ngày 1 = diffDays 0, Ngày 2 = diffDays 1,... giới hạn 1 đến 50
    return Math.max(1, Math.min(50, diffDays + 1));
  }

  function loadState() {
    try {
      // Dọn dẹp cache ngày ảo cũ nếu có
      localStorage.removeItem('GS12_SRS_VIRTUAL_DATE');

      const savedStart = localStorage.getItem(getStartDateKey());
      if (savedStart) {
        state.startDate = savedStart;
      } else {
        state.startDate = getToday().toISOString();
      }

      const savedSound = localStorage.getItem(SOUND_ENABLED_KEY);
      if (savedSound !== null) {
        state.soundEnabled = savedSound === 'true';
      }

      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        state.userCards = parsed.userCards || {};
        state.learnedDays = parsed.learnedDays || {};
        if (parsed.startDate && !savedStart) {
          state.startDate = parsed.startDate;
        }

        // Kiểm tra tính toàn vẹn: Đảm bảo có learnedDate và đồng bộ chính xác learnedDays
        const todayIso = getToday().toISOString();
        Object.values(state.userCards).forEach(c => {
          if (!c.learnedDate) c.learnedDate = c.lastReviewed || state.startDate || todayIso;
          if (c.level === undefined || c.level === null) c.level = 1;
        });

        // Chỉ công nhận Day hoàn thành khi đủ từ của Day đó đã thăng cấp lên Hộp >= 2
        const allDays = getAllDaysData();
        if (allDays.length > 0) {
          allDays.forEach(d => {
            if (d.vocab && d.vocab.length > 0) {
              const dayCards = d.vocab.map(v => state.userCards[v.id]).filter(Boolean);
              if (dayCards.length === d.vocab.length && dayCards.every(c => c.level >= 2)) {
                state.learnedDays[d.day] = true;
              } else {
                delete state.learnedDays[d.day];
              }
            }
          });
        }
        // Sắp xếp Hộp chuẩn xác theo tag ngày của từ vựng
        calibrateCardsByDayTag();
      } else {
        initializeDefaultDay1();
      }
    } catch (err) {
      console.error('Failed to load state from localStorage', err);
      initializeDefaultDay1();
    }
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        userCards: state.userCards,
        learnedDays: state.learnedDays,
        startDate: state.startDate
      }));
      if (state.startDate) {
        localStorage.setItem(getStartDateKey(), state.startDate);
      }
      localStorage.setItem(SOUND_ENABLED_KEY, String(state.soundEnabled));
    } catch (err) {
      console.error('Failed to save state to localStorage', err);
    }
  }

  function initializeDefaultDay1() {
    const day1 = getAllDaysData()[0] || null;
    if (day1 && day1.vocab) {
      enrollDay(1, false);
    }
  }

  // ==========================================
  // QUẢN LÝ TIẾN ĐỘ THỬ THÁCH 50 NGÀY & CỘNG DỒN THÔNG MINH
  // ==========================================
  function getChallengeDaysStatus() {
    const targetDay = getChallengeCurrentDay();
    const allDaysWithVocab = getAllDaysData().filter(d => d.vocab && d.vocab.length > 0);

    const completedDays = [];
    const pendingDays = [];

    allDaysWithVocab.forEach(d => {
      if (d.day <= targetDay) {
        const dayCards = d.vocab.map(v => state.userCards[v.id]).filter(Boolean);
        const isDone = state.learnedDays[d.day] || (dayCards.length === d.vocab.length && dayCards.every(c => c.level >= 2));
        if (isDone) {
          state.learnedDays[d.day] = true;
          completedDays.push(d.day);
        } else {
          pendingDays.push(d);
        }
      }
    });

    const isTodayLearned = !pendingDays.some(d => d.day === targetDay);
    const todayDayData = allDaysWithVocab.find(d => d.day === targetDay);

    return {
      targetDay,
      completedDays,
      pendingDays, // Các Day cần học (Hôm nay + các ngày bỏ lỡ chưa vào học)
      todayDayData,
      isTodayLearned
    };
  }

  function syncDailyAccumulation() {
    const { targetDay, pendingDays } = getChallengeDaysStatus();
    const today = getToday();
    let newlyEnrolledCards = [];

    // Chỉ nạp từ của ngày đang học (hoặc ngày tiếp theo cần học trong pendingDays[0]),
    // TUYỆT ĐỐI KHÔNG nạp dồn một lúc 20-50 ngày làm cho học viên bị ngợp 88 từ!
    const activeDayToEnroll = pendingDays.length > 0 ? pendingDays[0] : (getAllDaysData().find(d => d.day === targetDay) || getAllDaysData()[0]);

    if (activeDayToEnroll && activeDayToEnroll.vocab && activeDayToEnroll.vocab.length > 0) {
      activeDayToEnroll.vocab.forEach(item => {
        if (!state.userCards[item.id]) {
          const newCard = {
            id: item.id,
            word: item.word,
            day: activeDayToEnroll.day,
            unit: activeDayToEnroll.unit,
            module: activeDayToEnroll.module,
            level: 1, // Bắt đầu ở Hộp 1: Từ Mới (Khởi Đầu)
            learnedDate: today.toISOString(),
            lastReviewed: today.toISOString(),
            nextReviewDate: today.toISOString(),
            streak: 0,
            reviewCount: 0,
            mastered: false,
            history: []
          };
          state.userCards[item.id] = newCard;
          newlyEnrolledCards.push(newCard);
        }
      });
    }

    // DỌN DẸP CÁC THẺ CỦA CÁC NGÀY TƯƠNG LAI BỊ TỰ ĐỘNG NẠP NHẦM TRƯỚC ĐÓ:
    // Nếu có thẻ ở level 1 chưa từng học (streak === 0 && reviewCount === 0) thuộc về các ngày > activeDayToEnroll.day
    // và ngày đó chưa từng được hoàn thành: loại bỏ để trả lại số lượng 5-6 từ chuẩn mực cho học viên!
    let cleanedCount = 0;
    const currentActiveDayNum = activeDayToEnroll ? activeDayToEnroll.day : 1;
    Object.keys(state.userCards).forEach(cardId => {
      const c = state.userCards[cardId];
      if (c && c.level === 1 && (c.streak || 0) === 0 && (c.reviewCount || 0) === 0 && c.day > currentActiveDayNum && !state.learnedDays[c.day]) {
        delete state.userCards[cardId];
        cleanedCount++;
      }
    });

    if (newlyEnrolledCards.length > 0 || cleanedCount > 0) {
      saveState();
      if (currentUser && window.SupabaseService) {
        window.SupabaseService.saveBulkCardsProgress(currentUser.id, Object.values(state.userCards));
      }
    }
  }

  function startDailyStudySession(dayNum) {
    const dayData = getAllDaysData().find(d => d.day === dayNum);
    if (!dayData || !dayData.vocab || dayData.vocab.length === 0) {
      showToast(`Day ${dayNum} là ngày ôn tập tổng hợp (không có từ mới).`);
      return;
    }

    const today = getToday();
    const cardsToStudy = [];

    dayData.vocab.forEach(item => {
      if (!state.userCards[item.id]) {
        state.userCards[item.id] = {
          id: item.id,
          word: item.word,
          day: dayNum,
          unit: dayData.unit,
          module: dayData.module,
          level: 1,
          learnedDate: today.toISOString(),
          lastReviewed: today.toISOString(),
          nextReviewDate: today.toISOString(),
          streak: 0,
          reviewCount: 0,
          mastered: false,
          history: []
        };
      }
      cardsToStudy.push(state.userCards[item.id]);
    });

    state.sessionDayNum = dayNum;
    state.sessionType = 'srs';
    state.arenaMode = 'flashcard';
    startReviewSession(cardsToStudy, `Học 5 Từ Mới: Day ${dayNum}`, 'srs');
  }

  function checkDayCompletion(dayNum) {
    if (!dayNum) return false;
    const dayData = getAllDaysData().find(d => d.day === dayNum);
    if (!dayData || !dayData.vocab || dayData.vocab.length === 0) return false;

    const dayCards = dayData.vocab.map(v => state.userCards[v.id]).filter(Boolean);
    if (dayCards.length === dayData.vocab.length && dayCards.every(c => c.level >= 2)) {
      state.learnedDays[dayNum] = true;
      saveState();
      return true;
    }
    return false;
  }

  // ==========================================
  // ENROLL DAY INTO SRS
  // ==========================================
  function enrollDay(dayNum, shouldSave = true) {
    const dayData = getAllDaysData().find(d => d.day === dayNum);
    if (!dayData) return;

    const today = getToday();

    if (dayData.vocab && dayData.vocab.length > 0) {
      dayData.vocab.forEach(item => {
        if (!state.userCards[item.id]) {
          state.userCards[item.id] = {
            id: item.id,
            word: item.word,
            day: dayNum,
            unit: dayData.unit,
            module: dayData.module,
            level: 1, // Start in Box 1
            learnedDate: today.toISOString(),
            lastReviewed: today.toISOString(),
            nextReviewDate: today.toISOString(),
            streak: 0,
            reviewCount: 0,
            mastered: false,
            history: []
          };
        }
      });
    }

    if (shouldSave) {
      saveState();
      renderAll();
      showToast(`Đã nạp thành công 5 thẻ Day ${dayNum} vào Hộp 1: Từ Mới!`);
      if (currentUser && window.SupabaseService) {
        const enrolledCards = Object.values(state.userCards).filter(c => c.day === dayNum);
        window.SupabaseService.saveBulkCardsProgress(currentUser.id, enrolledCards);
      }
    }
  }

  // ==========================================
  // CARD RATING (HỌC & LUYỆN TẬP - KHÔNG NHẢY HỘP LUNG TUNG)
  // Sắp xếp đúng ô theo tag ngày của từ vựng
  // ==========================================
  function getBoxLevelByDayTag(card) {
    if (!card || !card.day) return 1;
    const currentDay = getChallengeCurrentDay();
    const diff = currentDay - card.day;

    if (diff <= 0) {
      if (state.learnedDays[card.day] || (card.reviewCount && card.reviewCount > 0) || (card.level && card.level >= 2)) {
        return 2;
      }
      return 1;
    }

    if (diff < 3) return 2;
    if (diff < 7) return 3;
    if (diff < 14) return 4;
    return 5;
  }

  function calibrateCardsByDayTag() {
    if (!state.userCards) return;
    let changed = false;
    Object.values(state.userCards).forEach(card => {
      if (card && card.day) {
        const correctLevel = getBoxLevelByDayTag(card);
        if (card.level !== correctLevel) {
          card.level = correctLevel;
          changed = true;
        }
      }
    });
    if (changed) {
      saveState();
    }
  }

  function rateCard(cardId, rating) {
    const card = state.userCards[cardId];
    if (!card) return;

    const today = getToday();

    if (!card.learnedDate) {
      card.learnedDate = formatDateISO(today);
    }

    if (rating === 'again') {
      // Đánh dấu cần ôn lại trong phiên học
      card.streak = 0;
      card.lastReviewed = formatDateISO(today);
      playSound('again');
      showToast(`Từ "${card.word || card.id}" sẽ được ôn lại ở cuối buổi học.`);
    } else if (rating === 'good') {
      // "Đã thuộc": Ghi nhận kết quả học/luyện tập, KHÔNG nhảy hộp lung tung!
      card.streak = (card.streak || 0) + 1;
      card.reviewCount = (card.reviewCount || 0) + 1;
      card.lastReviewed = formatDateISO(today);

      // Nếu từ này ở Hộp 1 (từ mới), học xong buổi đầu sẽ chuyển vào Hộp 2 (+3 Ngày)
      if (card.level === 1) {
        card.level = 2;
        card.nextReviewDate = formatDateISO(addDays(today, 3));
      }
      // Các từ ở Hộp 2, 3, 4, 5: giữ nguyên Hộp theo tag ngày, KHÔNG nhảy hộp lung tung!

      playSound('good');

      // Kiểm tra xem đã hoàn thành toàn bộ từ của Day này chưa
      if (card.day) {
        checkDayCompletion(card.day);
      }
    }

    // Ghi lịch sử ôn tập
    if (!card.history) card.history = [];
    card.history.push({
      date: formatDateISO(today),
      rating: rating,
      level: card.level,
      nextReviewDate: card.nextReviewDate
    });

    saveState();
    updateHeaderStats();
    if (currentUser && window.SupabaseService) {
      window.SupabaseService.saveCardProgress(currentUser.id, card);
    }
  }

  // ==========================================
  // DUE CARDS COMPUTATION (DỰA TRÊN NGÀY THỰC TẾ)
  // ==========================================
  function getDueCards(levelFilter = null) {
    const cur = getToday();
    return Object.values(state.userCards).filter(card => {
      if (levelFilter !== null && card.level !== levelFilter) return false;
      const nextD = normalizeDate(new Date(card.nextReviewDate));
      return nextD <= cur;
    });
  }

  function getAllCardsInLevel(level) {
    return Object.values(state.userCards).filter(c => c.level === level);
  }

  function getCardFullData(cardId) {
    for (const day of getAllDaysData()) {
      if (day.vocab) {
        const found = day.vocab.find(v => v.id === cardId);
        if (found) {
          return {
            ...found,
            grammar: day.grammar,
            unit: day.unit,
            module: day.module,
            day: day.day
          };
        }
      }
    }
    return null;
  }

  // ==========================================
  // REVIEW ARENA SESSION
  // ==========================================
  function startReviewSession(cards, title = 'Phiên Ôn Tập', sessionType = 'srs') {
    if (!cards || cards.length === 0) {
      showToast('Không có thẻ nào trong danh sách!');
      return;
    }

    // Shuffle cards for healthy recall
    state.reviewQueue = [...cards].sort(() => Math.random() - 0.5);
    state.reviewIndex = 0;
    state.isCardFlipped = false;
    state.sessionType = sessionType; // 'srs' or 'practice'
    state.sessionTitle = title;

    // Switch tab to Review Arena
    switchTab('arena');
    renderCurrentReviewCard();
  }

  function renderCurrentReviewCard() {
    const container = document.getElementById('arena-content-area');
    if (!container) return;

    if (state.reviewIndex >= state.reviewQueue.length) {
      // Completed session!
      playSound('good');
      const finishedDay = state.sessionDayNum;
      const today = getToday();
      let dayCongratHtml = '';
      if (finishedDay) {
        dayCongratHtml = `
          <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;">
            <div style="font-weight: 700; color: #34d399; font-size: 1.05rem;">🎉 Hoàn thành bài học Day ${finishedDay}!</div>
            <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 4px;">
              Các từ vựng đã được học và sắp xếp vào <strong>Hộp 2 (+3 Ngày)</strong> theo đúng tag ngày của bài học!
            </div>
          </div>
        `;
        state.sessionDayNum = null;
      }

      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">🎉</div>
          <h2 class="empty-title">Tuyệt vời! Đã hoàn thành phiên học & ôn tập!</h2>
          ${dayCongratHtml}
          <p class="empty-sub">Tất cả ${state.reviewQueue.length} thẻ đã được sắp xếp lịch ôn tập tự động chuẩn xác theo Spaced Repetition (SRS Leitner).</p>
          <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 16px;">
            <button class="btn-primary" id="btn-back-folders">
              <span>🗂️</span> Xem 5 Hộp SRS
            </button>
            <button class="btn-day-action" id="btn-restart-due" style="padding: 12px 20px;">
              <span>⚡</span> Kiểm tra lượt ôn tiếp theo
            </button>
          </div>
        </div>
      `;

      document.getElementById('btn-back-folders')?.addEventListener('click', () => switchTab('folders'));
      document.getElementById('btn-restart-due')?.addEventListener('click', () => {
        const due = getDueCards();
        if (due.length > 0) {
          startReviewSession(due, 'Ôn tập thẻ đến hạn', 'srs');
        } else {
          switchTab('folders');
        }
      });

      updateHeaderStats();
      return;
    }

    const currentCardStub = state.reviewQueue[state.reviewIndex];
    const cardData = getCardFullData(currentCardStub.id);
    const userCard = state.userCards[currentCardStub.id] || currentCardStub;

    // Update progress bar
    const progressPercent = Math.round((state.reviewIndex / state.reviewQueue.length) * 100);
    const progressFill = document.getElementById('arena-progress-fill');
    const progressText = document.getElementById('arena-progress-text');
    if (progressFill) progressFill.style.width = `${progressPercent}%`;
    if (progressText) progressText.innerText = `${state.reviewIndex + 1} / ${state.reviewQueue.length}`;

    if (state.arenaMode === 'quiz') {
      renderQuizMode(container, cardData, userCard);
    } else if (state.arenaMode === 'fillblank') {
      renderFillBlankMode(container, cardData, userCard);
    } else if (state.arenaMode === 'scramble') {
      renderScrambleSentenceMode(container, cardData, userCard);
    } else {
      renderFlashcardMode(container, cardData, userCard);
    }
  }

  function renderFlashcardMode(container, cardData, userCard) {
    const levelInfo = LEVEL_CONFIG[userCard.level] || LEVEL_CONFIG[1];
    const today = getToday();
    const nextD = normalizeDate(new Date(userCard.nextReviewDate || today));
    const isDue = (userCard.level === 1) || (nextD <= today);
    const remaining = getRemainingDays(nextD, today);
    const learnedDateStr = formatDateDisplay(userCard.learnedDate || userCard.lastReviewed || today);
    const nextReviewStr = formatDateDisplay(userCard.nextReviewDate || today);

    let statusTagHtml = '';
    if (userCard.level === 1) {
      statusTagHtml = `<span class="card-tag-chip tag-new-pill">✨ Cần học hôm nay</span>`;
    } else if (userCard.mastered) {
      statusTagHtml = `<span class="card-tag-chip tag-upcoming-pill" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">🏆 Đã thuộc dài hạn (Master)</span>`;
    } else if (isDue) {
      statusTagHtml = `<span class="card-tag-chip tag-due-pill">🔴 Đến hạn ôn hôm nay</span>`;
    } else {
      statusTagHtml = `<span class="card-tag-chip tag-upcoming-pill">⏳ Ôn sau ${remaining} ngày (${nextReviewStr})</span>`;
    }

    const tagsHtml = `
      <div class="card-tags-cloud">
        <span class="card-tag-chip tag-day">🏷️ Day ${cardData.day}</span>
        <span class="card-tag-chip tag-box" style="background: ${levelInfo.color}20; color: ${levelInfo.color}; border-color: ${levelInfo.color}60;">
          📦 ${levelInfo.name}
        </span>
        <span class="card-tag-chip tag-date">📅 Ngày học: ${learnedDateStr}</span>
        <span class="card-tag-chip tag-next">⏰ Lịch ôn: ${nextReviewStr}</span>
        ${statusTagHtml}
      </div>
    `;

    container.innerHTML = `
      ${state.sessionTitle ? `<div class="session-info-badge">⚡ ${state.sessionTitle}</div>` : ''}
      <div class="flashcard-wrapper ${state.isCardFlipped ? 'flipped' : ''}" id="flashcard-click-area">
        <div class="flashcard-inner">
          <!-- CARD FRONT -->
          <div class="card-face card-face-front">
            <div class="card-top-meta">
              ${tagsHtml}
            </div>

            <div class="card-center-front">
              <h1 class="card-word-title">${cardData.word}</h1>
              <div class="card-phonetics-row">
                <span class="card-ipa">${cardData.phonetics}</span>
                <button class="btn-speaker" id="btn-speak-word" title="Nghe phát âm">
                  🔊
                </button>
              </div>
              <span class="card-pos-tag">${cardData.pos}</span>
            </div>

            <div class="card-bottom-hint">
              <span>👆 Nhấn chuột hoặc phím <kbd class="kbd">Space</kbd> để lật thẻ</span>
            </div>
          </div>

          <!-- CARD BACK -->
          <div class="card-face card-face-back">
            <div class="card-top-meta">
              ${tagsHtml}
            </div>

            <div class="back-meaning-box">
              <div style="font-size: 0.82rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Ý nghĩa tiếng Việt</div>
              <div class="back-vietnamese-meaning">${cardData.meaning}</div>
            </div>

            <div class="back-section">
              <div class="back-section-title">Collocation đặc trưng:</div>
              <div class="back-section-text" style="color: #67e8f9; font-weight: 600;">${cardData.collocation}</div>
            </div>

            <div class="back-section">
              <div class="back-section-title">Câu ví dụ minh họa:</div>
              <div class="back-section-text back-example-sentence">"${cardData.example}"</div>
            </div>

            ${cardData.grammar ? `
              <div class="back-section grammar-box">
                <div class="back-section-title" style="color: #fbbf24;">Cấu trúc ngữ pháp áp dụng:</div>
                <div class="back-section-text" style="font-size: 0.88rem; color: #fde68a;">
                  <strong>${cardData.grammar.structure}</strong>
                  <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 2px;">${cardData.grammar.note}</div>
                </div>
              </div>
            ` : ''}

            <div class="card-bottom-hint">
              <span>Đánh giá mức độ nhớ của bạn bên dưới</span>
            </div>
          </div>
        </div>
      </div>

      <!-- REVISE CONTROLS -->
      <div class="srs-controls" style="${state.isCardFlipped ? '' : 'opacity: 0.45; pointer-events: none; filter: grayscale(0.6);'}">
        <button class="srs-btn again" data-rating="again" style="flex: 1;">
          <span class="srs-label">🔁 Cần ôn lại</span>
          <span class="srs-sub">Luyện thêm ở cuối buổi học</span>
        </button>
        <button class="srs-btn good" data-rating="good" style="flex: 1;">
          <span class="srs-label">✅ Đã thuộc từ này</span>
          <span class="srs-sub">Đã ghi nhớ nghĩa và cách dùng</span>
        </button>
      </div>

      <div class="keyboard-shortcut-hint">
        Phím tắt: <kbd class="kbd">Space</kbd> Lật thẻ | <kbd class="kbd">1</kbd> Cần ôn lại | <kbd class="kbd">2</kbd> Đã thuộc
      </div>
    `;

    // Event listeners
    const flipArea = document.getElementById('flashcard-click-area');
    flipArea?.addEventListener('click', (e) => {
      if (e.target.closest('#btn-speak-word')) return;
      toggleFlipCard();
    });

    document.getElementById('btn-speak-word')?.addEventListener('click', (e) => {
      e.stopPropagation();
      speakText(cardData.word);
    });

    // Rating buttons
    container.querySelectorAll('.srs-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const rating = btn.getAttribute('data-rating');
        submitCardReview(userCard.id, rating);
      });
    });
  }

  function toggleFlipCard() {
    state.isCardFlipped = !state.isCardFlipped;
    playSound('flip');
    const wrapper = document.getElementById('flashcard-click-area');
    const controls = document.querySelector('.srs-controls');
    if (wrapper) {
      if (state.isCardFlipped) {
        wrapper.classList.add('flipped');
        if (controls) {
          controls.style.opacity = '1';
          controls.style.pointerEvents = 'auto';
          controls.style.filter = 'none';
        }
      } else {
        wrapper.classList.remove('flipped');
        if (controls) {
          controls.style.opacity = '0.45';
          controls.style.pointerEvents = 'none';
          controls.style.filter = 'grayscale(0.6)';
        }
      }
    }
  }

  function submitCardReview(cardId, rating) {
    if (state.sessionType === 'srs') {
      if (rating === 'again') {
        state.reviewQueue.push(state.reviewQueue[state.reviewIndex]);
      }
      rateCard(cardId, rating);
    } else {
      if (rating === 'again') {
        playSound('again');
        state.reviewQueue.push(state.reviewQueue[state.reviewIndex]);
      } else {
        playSound('good');
      }
    }
    state.reviewIndex++;
    state.isCardFlipped = false;
    renderCurrentReviewCard();
    renderFoldersGrid();
  }

  // Helper: Tìm từ vựng (kể cả dạng chia số nhiều, quá khứ, v-ing, cụm nhiều từ...) trong câu ví dụ để ẩn đi chuẩn xác
  function findWordInSentence(word, sentence) {
    if (!sentence) return null;
    const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const patterns = [];

    // Hỗ trợ cụm từ nhiều chữ (multi-word phrase, e.g. "attend school", "drop out", "carry out attacks")
    if (word.includes(' ')) {
      const parts = word.split(/\s+/);
      const first = parts[0];
      
      let firstVariants = [first];
      if (first === 'have') firstVariants.push('had', 'having', 'has');
      else if (first === 'be') firstVariants.push('was', 'were', 'is', 'are', 'been', 'being');
      else if (first.endsWith('y')) {
        const stem = first.slice(0, -1);
        firstVariants.push(`${stem}ied`, `${stem}ying`, `${stem}ies`);
      } else if (first.endsWith('e')) {
        const stem = first.slice(0, -1);
        firstVariants.push(`${stem}ed`, `${stem}ing`, `${stem}es`);
      } else {
        firstVariants.push(`${first}ed`, `${first}ped`, `${first}ted`, `${first}ing`, `${first}ping`, `${first}ting`, `${first}s`, `${first}es`);
      }

      const firstGroup = `(?:${firstVariants.join('|')})`;
      const remainingPattern = parts.slice(1).map(p => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('(?:\\s+[a-zA-Z]+)?\\s+');
      patterns.push(`\\b${firstGroup}\\s+(?:[a-zA-Z\\s]{0,20}\\s+)?${remainingPattern}\\b`);
      patterns.push(`\\b${firstGroup}\\s+${remainingPattern}\\b`);
    }

    // Các biến thể từ đuôi phổ biến trong tiếng Anh
    if (word.endsWith('y')) {
      const stemY = word.slice(0, -1);
      patterns.push(`\\b${stemY.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(y|ies|ied|ying)\\b`);
    }
    if (word.endsWith('e')) {
      const stemE = word.slice(0, -1);
      patterns.push(`\\b${stemE.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(e|es|ed|ing)\\b`);
    }
    if (word.endsWith('is')) {
      const stemIs = word.slice(0, -2);
      patterns.push(`\\b${stemIs.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(is|es)\\b`);
    }
    if (word.includes('-')) {
      const spaceVer = word.replace(/-/g, '[-\\s]');
      patterns.push(`\\b${spaceVer}[a-z]*\\b`);
    }
    patterns.push(`\\b${escaped}[a-z]*\\b`);

    for (const p of patterns) {
      const reg = new RegExp(p, 'i');
      const m = sentence.match(reg);
      if (m) return { match: m[0], regex: reg };
    }
    return null;
  }

  // Quiz Mode Implementation (Chỉ ôn tập - Giữ nguyên Hộp & KHÔNG LỘ ĐÁP ÁN TRƯỚC KHI CHỌN)
  function renderQuizMode(container, cardData, userCard) {
    const allWords = [];
    getAllDaysData().forEach(d => {
      if (d.vocab) allWords.push(...d.vocab);
    });

    const distractors = allWords
      .filter(w => w.id !== cardData.id && w.meaning !== cardData.meaning)
      .sort(() => Math.random() - 0.5)
      .slice(0, 3);

    const options = [
      { text: cardData.meaning, isCorrect: true, word: cardData.word },
      ...distractors.map(d => ({ text: d.meaning, isCorrect: false, word: d.word }))
    ].sort(() => Math.random() - 0.5);

    const letters = ['A', 'B', 'C', 'D'];

    // KHÔNG đưa Collocation vào câu hỏi vì collocation chứa nghĩa tiếng Việt và làm lộ đáp án
    // KHÔNG gán data-correct trực tiếp vào DOM HTML để tránh học sinh Inspect Element
    container.innerHTML = `
      <div class="quiz-container">
        <div class="quiz-question-header">
          <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 6px;">Day ${cardData.day} • Chọn nghĩa tiếng Việt chính xác nhất:</div>
          <h2 class="quiz-question-word">${cardData.word} <span style="font-size: 1.1rem; color: #38bdf8; font-weight: normal;">${cardData.phonetics}</span></h2>
          <p class="quiz-question-sub">Từ loại: <strong style="color: #a5b4fc;">${cardData.pos || 'từ vựng'}</strong> • <em>${cardData.unit || ''}</em></p>
        </div>

        <div class="quiz-options-grid">
          ${options.map((opt, idx) => `
            <button class="quiz-opt-btn" data-idx="${idx}">
              <span class="quiz-opt-badge">${letters[idx]}</span>
              <span>${opt.text}</span>
            </button>
          `).join('')}
        </div>

        <div class="quiz-feedback-box" id="quiz-feedback">
          <span style="color: var(--text-muted);">Hãy chọn một trong 4 phương án trên</span>
        </div>
      </div>
    `;

    const optionBtns = container.querySelectorAll('.quiz-opt-btn');
    const feedbackBox = document.getElementById('quiz-feedback');

    optionBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        optionBtns.forEach(b => b.disabled = true);
        const optIdx = parseInt(btn.getAttribute('data-idx'), 10);
        const selectedOpt = options[optIdx];
        const isCorrect = selectedOpt ? selectedOpt.isCorrect : false;

        // Sau khi học sinh chọn, mới hiển thị Collocation đầy đủ làm phần giải thích học tập
        const collocationHtml = cardData.collocation 
          ? `<div style="font-size: 0.84rem; color: #93c5fd; margin-top: 4px;">💡 <strong>Collocation ghi điểm:</strong> <em>${cardData.collocation}</em></div>` 
          : '';

        if (isCorrect) {
          btn.classList.add('correct');
          playSound('good');
          feedbackBox.innerHTML = `
            <div>
              <div style="color: #6ee7b7; font-weight: 700;">🎉 Rất chính xác! Bạn đã ghi nhớ chuẩn nghĩa từ này.</div>
              ${collocationHtml}
            </div>
          `;
          // Luyện tập: KHÔNG gọi rateCard (không làm thay đổi Hộp của từ)
        } else {
          btn.classList.add('wrong');
          playSound('again');
          optionBtns.forEach(b => {
            const bIdx = parseInt(b.getAttribute('data-idx'), 10);
            if (options[bIdx]?.isCorrect) b.classList.add('correct');
          });
          feedbackBox.innerHTML = `
            <div>
              <div style="color: #fda4af; font-weight: 700;">Chưa chính xác! Nghĩa đúng là: <u>${cardData.meaning}</u></div>
              ${collocationHtml}
            </div>
          `;
          state.reviewQueue.push(state.reviewQueue[state.reviewIndex]);
          // Luyện tập: KHÔNG gọi rateCard
        }

        setTimeout(() => {
          state.reviewIndex++;
          renderCurrentReviewCard();
          renderFoldersGrid();
        }, 1600);
      });
    });
  }

  // ==========================================
  // DẠNG BÀI 3: ĐIỀN TỪ CÒN THIẾU (FILL IN THE BLANK - TUYỆT ĐỐI KHÔNG LỘ COLLOCATION TRƯỚC KHI TRẢ LỜI)
  // ==========================================
  function renderFillBlankMode(container, cardData, userCard) {
    const word = cardData.word;
    const example = cardData.example || '';
    
    // Tìm và ẩn từ trong câu ví dụ bằng smart matcher
    const matchResult = findWordInSentence(word, example);
    let sentenceWithBlank = example;
    let targetAnswer = word.toLowerCase();

    if (matchResult) {
      targetAnswer = matchResult.match.toLowerCase();
      sentenceWithBlank = example.replace(matchResult.regex, `<span class="fillblank-blank-word">[ ????? ]</span>`);
    } else {
      // Trường hợp dự phòng nếu câu ví dụ không chứa từ
      sentenceWithBlank = `<span class="fillblank-blank-word">[ ????? ]</span>`;
    }

    const firstLetter = word.charAt(0).toUpperCase();

    // TUYỆT ĐỐI KHÔNG hiển thị Collocation ở hint pill trước khi trả lời
    // vì Collocation thường chứa từ khóa hoặc phần dịch tiếng Việt trong ngoặc làm lộ đáp án
    container.innerHTML = `
      <div class="fillblank-container">
        <div class="fillblank-header">
          <div class="fillblank-meta-tags">
            <span class="tag-badge tag-day">Day ${cardData.day}</span>
            <span class="tag-badge tag-pos">${cardData.pos || 'v/n'}</span>
            <span class="tag-badge" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8;">${cardData.unit}</span>
          </div>
          <h3 style="font-size: 1.15rem; color: #fff; margin-bottom: 4px;">Điền từ vựng còn thiếu vào chỗ trống:</h3>
          <p style="font-size: 0.85rem; color: #94a3b8; margin: 0;">Đọc câu ví dụ bên dưới và gõ từ cần điền.</p>
        </div>

        <div class="fillblank-sentence-box" id="fillblank-sentence">
          ${sentenceWithBlank}
        </div>

        <div class="fillblank-hint-pill">
          <span>💡 <strong>Nghĩa tiếng Việt:</strong> ${cardData.meaning}</span>
          <span style="opacity: 0.4;">•</span>
          <span><strong>Chữ cái đầu:</strong> <code style="color: #38bdf8; font-weight: 800; font-size: 0.95rem;">${firstLetter}...</code> <small style="color: #94a3b8;">(${word.length} ký tự)</small></span>
        </div>

        <div class="fillblank-input-row">
          <input type="text" class="fillblank-input" id="fillblank-input" placeholder="Gõ từ vựng vào đây..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
          <button class="btn-primary" id="btn-fillblank-check" style="padding: 12px 20px;">
            ✅ Kiểm tra
          </button>
          <button class="btn-secondary" id="btn-fillblank-speak" title="Nghe câu mẫu sau khi trả lời" style="padding: 12px 14px;">
            🔊
          </button>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div class="quiz-feedback-box" id="fillblank-feedback" style="flex: 1; margin-right: 12px; min-height: 48px; padding: 10px 14px;">
            <span style="color: var(--text-muted); font-size: 0.85rem;">Nhập từ và bấm Kiểm tra (hoặc nhấn phím Enter)</span>
          </div>
          <button class="btn-secondary" id="btn-fillblank-skip" style="font-size: 0.8rem; padding: 8px 12px;">
            👁️ Xem đáp án
          </button>
        </div>
      </div>
    `;

    const input = document.getElementById('fillblank-input');
    const checkBtn = document.getElementById('btn-fillblank-check');
    const speakBtn = document.getElementById('btn-fillblank-speak');
    const skipBtn = document.getElementById('btn-fillblank-skip');
    const feedback = document.getElementById('fillblank-feedback');
    const sentenceEl = document.getElementById('fillblank-sentence');

    setTimeout(() => input?.focus(), 100);

    let answered = false;

    // Chặn lộ đáp án qua nút nghe: chỉ phát âm câu khi đã trả lời hoặc khi bấm xem đáp án
    speakBtn?.addEventListener('click', () => {
      if (!answered) {
        showToast('💡 Hãy thử điền từ trước hoặc bấm "Xem đáp án" để nghe phát âm cả câu!');
      } else {
        speakText(cardData.example || cardData.word);
      }
    });

    function showRevealedSentence(highlightWord) {
      if (matchResult) {
        sentenceEl.innerHTML = example.replace(matchResult.regex, `<strong style="color: #34d399; text-decoration: underline;">${highlightWord}</strong>`);
      } else {
        sentenceEl.innerHTML = `Từ đúng: <strong style="color: #34d399;">${highlightWord}</strong>`;
      }
    }

    function checkAnswer() {
      if (answered) return;
      const userVal = (input.value || '').trim().toLowerCase();
      if (!userVal) {
        input.focus();
        return;
      }

      const isMatch = (userVal === word.toLowerCase()) || (userVal === targetAnswer);

      if (isMatch) {
        answered = true;
        playSound('good');
        input.style.borderColor = '#10b981';
        input.style.color = '#34d399';
        showRevealedSentence(targetAnswer || word);
        // Sau khi trả lời, hiển thị Collocation đầy đủ làm phần giải thích nâng cao
        feedback.innerHTML = `
          <div>
            <span style="color: #6ee7b7; font-weight: 700;">🎉 Chính xác! Bạn đã điền đúng từ "${word}"!</span>
            ${cardData.collocation ? `<div style="font-size: 0.84rem; color: #93c5fd; margin-top: 4px;">💡 <strong>Collocation ghi điểm:</strong> <em>${cardData.collocation}</em></div>` : ''}
          </div>
        `;
        // Luyện tập: KHÔNG gọi rateCard
        speakText(cardData.example || word);

        setTimeout(() => {
          state.reviewIndex++;
          renderCurrentReviewCard();
          renderFoldersGrid();
        }, 1800);
      } else {
        playSound('again');
        input.style.borderColor = '#ef4444';
        feedback.innerHTML = `<span style="color: #fda4af; font-weight: 700;">Chưa chính xác! Thử lại hoặc bấm 'Xem đáp án'.</span>`;
      }
    }

    checkBtn?.addEventListener('click', checkAnswer);
    input?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') checkAnswer();
    });

    skipBtn?.addEventListener('click', () => {
      if (answered) return;
      answered = true;
      showRevealedSentence(word);
      feedback.innerHTML = `
        <div>
          <span style="color: #93c5fd; font-weight: 700;">Đáp án đúng là: <u>${word}</u></span>
          ${cardData.collocation ? `<div style="font-size: 0.84rem; color: #93c5fd; margin-top: 4px;">💡 <strong>Collocation ghi điểm:</strong> <em>${cardData.collocation}</em></div>` : ''}
        </div>
      `;
      input.value = word;
      state.reviewQueue.push(state.reviewQueue[state.reviewIndex]);
      speakText(cardData.example || word);
      setTimeout(() => {
        state.reviewIndex++;
        renderCurrentReviewCard();
        renderFoldersGrid();
      }, 2200);
    });
  }

  // ==========================================
  // DẠNG BÀI 4: SẮP XẾP CÂU (SENTENCE SCRAMBLE - CHẶN SPOIL AUDIO, RANDOM TOKEN ID & CHỈ HIỆN COLLOCATION SAU KHI XONG)
  // ==========================================
  function renderScrambleSentenceMode(container, cardData, userCard) {
    const rawSentence = (cardData.example || '').trim();
    if (!rawSentence) {
      renderFlashcardMode(container, cardData, userCard);
      return;
    }

    const originalTokens = rawSentence.split(/\s+/);
    // Dùng random ID cho từng chip để tránh lộ thứ tự ban đầu qua data-id
    const tokenObjects = originalTokens.map(tok => ({
      id: 'tok_' + Math.random().toString(36).substring(2, 9),
      text: tok
    }));
    const shuffled = [...tokenObjects].sort(() => Math.random() - 0.5);

    let selectedTokens = [];

    container.innerHTML = `
      <div class="scramble-container">
        <div class="scramble-prompt-box">
          <div class="fillblank-meta-tags">
            <span class="tag-badge tag-day">Day ${cardData.day}</span>
            <span class="tag-badge" style="background: rgba(192, 132, 252, 0.15); color: #c084fc;">Sắp Xếp Câu Tiếng Anh</span>
            <span class="tag-badge" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8;">${cardData.word}</span>
          </div>
          <h3 style="font-size: 1.15rem; color: #fff; margin-bottom: 4px;">Sắp xếp các mảnh từ thành câu ví dụ hoàn chỉnh:</h3>
          <p style="font-size: 0.85rem; color: #94a3b8; margin: 0;">Từ vựng trọng tâm trong câu: <strong style="color: #38bdf8;">${cardData.word}</strong> <em>(${cardData.meaning})</em></p>
          ${cardData.grammar ? `<div style="font-size: 0.8rem; color: #fbbf24; margin-top: 6px;">Cấu trúc áp dụng: <strong>${cardData.grammar.structure}</strong></div>` : ''}
        </div>

        <div class="scramble-target-zone empty" id="scramble-target"></div>

        <div class="scramble-pool" id="scramble-pool">
          ${shuffled.map(t => `
            <div class="scramble-chip" data-id="${t.id}">${t.text}</div>
          `).join('')}
        </div>

        <div class="scramble-actions">
          <button class="btn-secondary" id="btn-scramble-speak" title="Nghe câu mẫu sau khi kiểm tra">🔊 Nghe</button>
          <button class="btn-secondary" id="btn-scramble-reset">🔄 Xếp lại từ đầu</button>
          <button class="btn-secondary" id="btn-scramble-solution">👁️ Xem đáp án</button>
          <button class="btn-primary" id="btn-scramble-check">✅ Kiểm tra câu</button>
        </div>

        <div class="scramble-feedback" id="scramble-feedback"></div>
      </div>
    `;

    const targetEl = document.getElementById('scramble-target');
    const poolEl = document.getElementById('scramble-pool');
    const feedback = document.getElementById('scramble-feedback');
    const checkBtn = document.getElementById('btn-scramble-check');
    const resetBtn = document.getElementById('btn-scramble-reset');
    const solutionBtn = document.getElementById('btn-scramble-solution');
    const speakBtn = document.getElementById('btn-scramble-speak');

    function updateTargetView() {
      targetEl.innerHTML = '';
      if (selectedTokens.length === 0) {
        targetEl.classList.add('empty');
      } else {
        targetEl.classList.remove('empty');
        selectedTokens.forEach((tok, idx) => {
          const chip = document.createElement('div');
          chip.className = 'scramble-chip in-target';
          chip.innerText = tok.text;
          chip.title = 'Bấm để gỡ từ này';
          chip.addEventListener('click', () => {
            selectedTokens.splice(idx, 1);
            const poolChip = poolEl.querySelector(`[data-id="${tok.id}"]`);
            if (poolChip) poolChip.classList.remove('used');
            updateTargetView();
          });
          targetEl.appendChild(chip);
        });
      }
    }

    poolEl.querySelectorAll('.scramble-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        if (chip.classList.contains('used')) return;
        const id = chip.getAttribute('data-id');
        const tok = tokenObjects.find(t => t.id === id);
        if (tok) {
          selectedTokens.push(tok);
          chip.classList.add('used');
          updateTargetView();
        }
      });
    });

    let completed = false;

    // Chặn lộ đáp án qua nút nghe: chỉ phát âm câu khi đã ghép đúng hoặc khi bấm xem đáp án
    speakBtn?.addEventListener('click', () => {
      if (!completed) {
        showToast('💡 Hãy sắp xếp câu trước hoặc bấm "Xem đáp án" để nghe phát âm toàn bộ câu nhé!');
      } else {
        speakText(rawSentence);
      }
    });

    resetBtn?.addEventListener('click', () => {
      selectedTokens = [];
      poolEl.querySelectorAll('.scramble-chip').forEach(c => c.classList.remove('used'));
      feedback.style.display = 'none';
      updateTargetView();
    });

    checkBtn?.addEventListener('click', () => {
      if (completed) return;
      if (selectedTokens.length === 0) {
        feedback.className = 'scramble-feedback wrong';
        feedback.innerText = 'Vui lòng chọn các từ để ghép thành câu trước khi kiểm tra!';
        return;
      }

      const assembled = selectedTokens.map(t => t.text).join(' ').trim().toLowerCase();
      const targetClean = originalTokens.map(t => t).join(' ').trim().toLowerCase();

      const clean1 = assembled.replace(/[.,/#!$%^&*;:{}=\-_`~()?"']/g, '');
      const clean2 = targetClean.replace(/[.,/#!$%^&*;:{}=\-_`~()?"']/g, '');

      if (clean1 === clean2) {
        completed = true;
        playSound('good');
        feedback.className = 'scramble-feedback correct';
        feedback.innerHTML = `
          <div>
            🎉 <strong>Chính xác xuất sắc!</strong> Câu hoàn chỉnh: <em>"${rawSentence}"</em>
            ${cardData.collocation ? `<div style="font-size: 0.85rem; margin-top: 4px; color: #a5b4fc;">💡 Collocation: <strong>${cardData.collocation}</strong></div>` : ''}
          </div>
        `;
        // Luyện tập: KHÔNG gọi rateCard
        speakText(rawSentence);

        setTimeout(() => {
          state.reviewIndex++;
          renderCurrentReviewCard();
          renderFoldersGrid();
        }, 1800);
      } else {
        playSound('again');
        feedback.className = 'scramble-feedback wrong';
        feedback.innerHTML = `Chưa đúng thứ tự câu. Hãy thử xem lại vị trí các từ hoặc cấu trúc câu nhé!`;
      }
    });

    solutionBtn?.addEventListener('click', () => {
      completed = true;
      feedback.className = 'scramble-feedback correct';
      feedback.innerHTML = `
        <div>
          💡 Câu mẫu chính xác: <strong>"${rawSentence}"</strong>
          ${cardData.collocation ? `<div style="font-size: 0.85rem; margin-top: 4px; color: #a5b4fc;">💡 Collocation: <strong>${cardData.collocation}</strong></div>` : ''}
        </div>
      `;
      speakText(rawSentence);
    });
  }

  // ==========================================
  // VIEW RENDERING: 5 SRS FOLDERS
  // ==========================================
  function renderFoldersGrid() {
    const grid = document.getElementById('folders-grid');
    if (!grid) return;

    grid.innerHTML = '';
    const { pendingDays } = getChallengeDaysStatus();

    Object.values(LEVEL_CONFIG).forEach(lvl => {
      const allInLevel = getAllCardsInLevel(lvl.id);
      const dueInLevel = getDueCards(lvl.id);

      const folderEl = document.createElement('div');
      folderEl.className = `folder-card ${state.currentFolderId === lvl.id ? 'active-folder' : ''}`;
      folderEl.style.setProperty('--folder-accent', lvl.color);

      let statusBadgeHtml = '';
      if (lvl.id === 1) {
        if (pendingDays.length > 0) {
          statusBadgeHtml = `<div class="folder-due-pill" style="background: rgba(249, 115, 22, 0.2); color: #fdba74; border-color: rgba(249, 115, 22, 0.45);">⚡ Cần học: ${pendingDays.length * 5} từ</div>`;
        } else if (allInLevel.length > 0) {
          statusBadgeHtml = `<div class="folder-due-pill" style="background: rgba(249, 115, 22, 0.2); color: #fdba74; border-color: rgba(249, 115, 22, 0.45);">🔄 Cần học lại: ${allInLevel.length}</div>`;
        } else {
          statusBadgeHtml = `<div class="folder-due-pill zero">✓ Đã hoàn thành</div>`;
        }
      } else {
        if (dueInLevel.length > 0) {
          statusBadgeHtml = `<div class="folder-due-pill">🔴 Đến hạn: ${dueInLevel.length}</div>`;
        } else {
          statusBadgeHtml = `<div class="folder-due-pill zero">✓ Đã xong hôm nay</div>`;
        }
      }

      let actionBtnText = 'Xem chi tiết';
      if (lvl.id === 1) {
        if (pendingDays.length > 0) {
          actionBtnText = `Học Day ${pendingDays[0].day} (5 từ)`;
        } else if (allInLevel.length > 0) {
          actionBtnText = `Học lại (${allInLevel.length})`;
        }
      } else {
        if (dueInLevel.length > 0) {
          actionBtnText = `Ôn ngay (${dueInLevel.length})`;
        }
      }

      folderEl.innerHTML = `
        <div class="folder-top">
          <div class="folder-icon-wrap" style="color: ${lvl.color}">
            📁
          </div>
          ${statusBadgeHtml}
        </div>
        <h3 class="folder-name">${lvl.name}</h3>
        <p class="folder-interval">${lvl.desc}</p>
        <div class="folder-stats-row">
          <div>
            <div class="folder-total-count">${allInLevel.length}</div>
            <div class="folder-total-label">Tổng thẻ trong hộp</div>
          </div>
          <button class="folder-btn-review" data-folder-id="${lvl.id}">
            ${actionBtnText}
          </button>
        </div>
      `;

      folderEl.addEventListener('click', (e) => {
        if (e.target.classList.contains('folder-btn-review')) {
          if (lvl.id === 1 && pendingDays.length > 0) {
            startDailyStudySession(pendingDays[0].day);
            return;
          }
          if (dueInLevel.length > 0) {
            startReviewSession(dueInLevel, `Ôn tập ${lvl.name}`, 'srs');
            return;
          }
        }
        state.currentFolderId = lvl.id;
        renderFoldersGrid();
        renderFolderDetailPane(lvl.id);
      });

      grid.appendChild(folderEl);
    });

    renderFolderDetailPane(state.currentFolderId);
    updateHeaderStats();
  }

  function renderFolderDetailPane(levelId) {
    const pane = document.getElementById('folder-detail-pane');
    if (!pane) return;

    const lvl = LEVEL_CONFIG[levelId];
    const cards = getAllCardsInLevel(levelId);
    const dueCards = getDueCards(levelId);
    const today = getToday();
    const { targetDay, pendingDays } = getChallengeDaysStatus();

    let specialSectionHtml = '';

    // Nếu đang ở Hộp 1: Hiển thị danh sách các Day cần học (hôm nay + các ngày cộng dồn)
    if (levelId === 1) {
      if (pendingDays.length > 0) {
        specialSectionHtml = `
          <div style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px;">
                <span>📚</span> Danh Sách Bài Học 5 Từ Cần Hoàn Thành:
              </h3>
              ${pendingDays.length > 1 ? `
                <span class="pdc-badge badge-accumulated">
                  ⚠️ Có ${pendingDays.length - 1} ngày chưa học được cộng dồn (${(pendingDays.length - 1) * 5} từ)
                </span>
              ` : ''}
            </div>
            <div class="pending-days-section">
              ${pendingDays.map(pDay => {
                const isToday = (pDay.day === targetDay);
                return `
                  <div class="pending-day-card ${isToday ? 'is-today' : 'is-accumulated'}">
                    <div class="pdc-left">
                      <div style="display: flex; align-items: center; gap: 8px;">
                        <span class="pdc-badge ${isToday ? 'badge-today' : 'badge-accumulated'}">
                          ${isToday ? '🎯 Bài học hôm nay' : '⚠️ Cộng dồn do chưa học'}
                        </span>
                        <span style="font-size: 0.8rem; color: var(--text-muted);">5 từ mới</span>
                      </div>
                      <h4 class="pdc-title">DAY ${pDay.day}: ${pDay.subtopic}</h4>
                      <p class="pdc-sub">${pDay.unit} • ${pDay.module}</p>
                    </div>
                    <div class="pdc-right">
                      <button class="btn-primary btn-study-day" data-day="${pDay.day}">
                        <span>📖</span> Bắt đầu học 5 từ này
                      </button>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }
    }

    pane.innerHTML = `
      <div class="folder-details-header">
        <div>
          <h2 style="font-size: 1.4rem; font-weight: 800; display: flex; align-items: center; gap: 10px;">
            <span style="color: ${lvl.color};">📁</span> ${lvl.name} (${cards.length} thẻ)
          </h2>
          <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 4px;">${lvl.desc}</p>
        </div>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
          ${levelId === 1 ? `
            ${pendingDays.length > 0 ? `
              <button class="btn-primary" id="btn-quick-study-day1" style="background: ${lvl.color}; color: #000; font-weight: 700;">
                📖 Học 5 từ Day ${pendingDays[0].day}
              </button>
            ` : ''}
            ${cards.length > 0 ? `
              <button class="btn-day-action" id="btn-review-box1-cards">
                ⚡ Học lại thẻ trong Hộp 1 (${cards.length})
              </button>
            ` : ''}
          ` : `
            ${dueCards.length > 0 ? `
              <button class="btn-primary" id="btn-review-this-folder" style="background: ${lvl.color}; color: #000; font-weight: 700;">
                ⚡ Ôn tập thẻ đến hạn (${dueCards.length})
              </button>
            ` : ''}
            <button class="btn-day-action" id="btn-practice-all-in-folder">
              🎮 Luyện tập hộp này (${cards.length})
            </button>
          `}
        </div>
      </div>

      ${specialSectionHtml}

      ${cards.length === 0 && (levelId !== 1 || pendingDays.length === 0) ? `
        <div class="empty-state" style="padding: 40px 20px;">
          <div class="empty-icon">📭</div>
          <h3 class="empty-title">Chưa có thẻ nào trong ${lvl.name}</h3>
          <p class="empty-sub">Hãy hoàn thành các bài học hoặc ôn luyện theo đúng chu kỳ để thăng cấp thẻ lên đây.</p>
        </div>
      ` : `
        ${cards.length > 0 ? `
          <h4 style="font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 12px;">
            ${levelId === 1 ? `Danh Sách Thẻ Cần Học / Củng Cố Lại (${cards.length} thẻ):` : `Danh Sách Thẻ Đang Ở ${lvl.name} (${cards.length} thẻ):`}
          </h4>
          <div class="cards-table-list">
            ${cards.map(card => {
              const cardFull = getCardFullData(card.id);
              if (!cardFull) return '';
              const nextD = normalizeDate(new Date(card.nextReviewDate));
              const isDue = (card.level === 1) || (nextD <= today);
              const remaining = getRemainingDays(nextD, today);
              const learnedDateStr = formatDateDisplay(card.learnedDate || card.lastReviewed || today);
              const nextReviewStr = formatDateDisplay(card.nextReviewDate);

              let dueStatusHtml = '';
              if (card.level === 1) {
                dueStatusHtml = `✨ Cần học (Bấm Tốt -> Hộp +3d)`;
              } else if (card.mastered) {
                dueStatusHtml = `🏆 Đã thuộc dài hạn (Master)`;
              } else if (isDue) {
                if (remaining < 0) {
                  dueStatusHtml = `🔴 Quá hạn ${Math.abs(remaining)} ngày (Cần ôn ngay)`;
                } else {
                  dueStatusHtml = `🔴 Đến hạn ôn hôm nay`;
                }
              } else {
                dueStatusHtml = `⏳ Sau ${remaining} ngày (${nextReviewStr})`;
              }

              return `
                <div class="card-item-pill ${isDue ? 'due-item' : ''}">
                  <div class="cip-top">
                    <span class="cip-word">${cardFull.word}</span>
                    <span class="cip-pos">${cardFull.pos}</span>
                  </div>
                  <div class="cip-meaning">${cardFull.meaning}</div>
                  ${cardFull.collocation ? `<div style="font-size: 0.8rem; color: #67e8f9; margin-top: 2px;">💡 ${cardFull.collocation}</div>` : ''}
                  
                  <div class="card-tags-cloud" style="margin-top: 8px; margin-bottom: 0;">
                    <span class="card-tag-chip tag-day">🏷️ Day ${cardFull.day}</span>
                    <span class="card-tag-chip tag-box" style="color: ${lvl.color}; border-color: ${lvl.color}50; background: ${lvl.color}15;">
                      📦 ${lvl.name}
                    </span>
                    <span class="card-tag-chip tag-date">📅 Học: ${learnedDateStr}</span>
                    <span class="card-tag-chip tag-next">⏰ Lịch ôn: ${nextReviewStr}</span>
                  </div>

                  <div class="cip-bottom">
                    <span>${cardFull.unit}</span>
                    <span class="cip-due-status ${isDue ? 'due-now' : 'upcoming'}">
                      ${dueStatusHtml}
                    </span>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        ` : ''}
      `}
    `;

    // Event listeners
    pane.querySelectorAll('.btn-study-day').forEach(btn => {
      btn.addEventListener('click', () => {
        const dayNum = parseInt(btn.getAttribute('data-day'), 10);
        startDailyStudySession(dayNum);
      });
    });

    document.getElementById('btn-quick-study-day1')?.addEventListener('click', () => {
      if (pendingDays.length > 0) {
        startDailyStudySession(pendingDays[0].day);
      }
    });

    document.getElementById('btn-review-box1-cards')?.addEventListener('click', () => {
      startReviewSession(cards, `Học lại Hộp 1: Từ Mới`, 'srs');
    });

    document.getElementById('btn-review-this-folder')?.addEventListener('click', () => {
      startReviewSession(dueCards, `Ôn tập ${lvl.name}`, 'srs');
    });

    document.getElementById('btn-practice-all-in-folder')?.addEventListener('click', () => {
      startReviewSession(cards, `Luyện tập ${lvl.name}`, 'practice');
    });
  }

  // ==========================================
  // VIEW RENDERING: 50-DAY ROADMAP
  // ==========================================
  let activeModuleFilter = 'ALL';
  let activeSearchTerm = '';

  function renderRoadmap() {
    const grid = document.getElementById('roadmap-grid');
    if (!grid) return;

    grid.innerHTML = '';

    const filtered = getAllDaysData().filter(day => {
      if (activeModuleFilter !== 'ALL' && !day.module.includes(`MODULE ${activeModuleFilter}`)) {
        return false;
      }
      if (activeSearchTerm.trim() !== '') {
        const term = activeSearchTerm.toLowerCase();
        const matchTitle = day.subtopic.toLowerCase().includes(term) || day.unit.toLowerCase().includes(term);
        const matchVocab = day.vocab && day.vocab.some(v => v.word.toLowerCase().includes(term) || v.meaning.toLowerCase().includes(term));
        return matchTitle || matchVocab;
      }
      return true;
    });

    const currentChallengeDay = getChallengeCurrentDay();

    filtered.forEach(day => {
      const isEnrolled = !!state.learnedDays[day.day];
      const isTodayDay = (day.day === currentChallengeDay);
      const cardEl = document.createElement('div');
      cardEl.className = `day-card ${day.isReview ? 'review-card' : ''} ${isEnrolled ? 'is-active-srs' : ''} ${isTodayDay ? 'is-today-card' : ''}`;

      let wordsHtml = '';
      if (day.vocab && day.vocab.length > 0) {
        wordsHtml = `
          <div class="day-words-preview">
            ${day.vocab.map(v => `<span class="word-preview-pill">${v.word}</span>`).join('')}
          </div>
        `;
      } else if (day.isReview) {
        wordsHtml = `
          <div style="font-size: 0.82rem; color: #fcd34d; margin: 4px 0;">
            📝 ${day.subtopic}
          </div>
        `;
      }

      cardEl.innerHTML = `
        <div class="day-card-header">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span class="day-number-tag">DAY ${day.day}</span>
            ${isTodayDay ? '<span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff; font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; font-weight: 700; box-shadow: 0 0 8px rgba(99,102,241,0.5);">🎯 Hôm nay</span>' : ''}
          </div>
          <span class="day-unit-name">${day.unit}</span>
        </div>
        <h4 class="day-topic-title">${day.subtopic}</h4>
        ${wordsHtml}
        <div class="day-card-footer">
          <span class="tag-badge ${isEnrolled ? 'tag-role-student' : 'tag-day'}" style="font-size: 0.76rem;">
            ${isEnrolled ? '✓ Đang trong lộ trình' : `Khóa học Day ${day.day}`}
          </span>
          <button class="icon-btn btn-view-day-modal" data-day-num="${day.day}" title="Xem chi tiết nội dung & ngữ pháp">
            👁️ Xem chi tiết
          </button>
        </div>
      `;

      cardEl.querySelector('.btn-view-day-modal')?.addEventListener('click', (e) => {
        e.stopPropagation();
        openDayModal(day);
      });

      cardEl.addEventListener('click', () => {
        openDayModal(day);
      });

      grid.appendChild(cardEl);
    });
  }

  // Day Detail Modal (Chế độ xem nội dung chuẩn - không can thiệp lộ trình)
  function openDayModal(day) {
    const modal = document.getElementById('day-modal');
    const modalBody = document.getElementById('day-modal-body');
    const modalTitle = document.getElementById('day-modal-title');
    if (!modal || !modalBody || !modalTitle) return;

    modalTitle.innerText = `DAY ${day.day}: ${day.subtopic} (${day.unit})`;

    let html = `
      <div style="font-size: 0.88rem; color: var(--text-secondary); margin-bottom: 16px;">
        <strong>Lịch trình ôn tập tham khảo:</strong> ${day.reviewInfo}
      </div>
    `;

    if (day.grammar) {
      html += `
        <div class="modal-day-grammar">
          <div style="font-size: 0.78rem; font-weight: 700; color: #818cf8; text-transform: uppercase;">Cấu trúc câu chủ đạo (Global Success 12)</div>
          <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin: 4px 0;">${day.grammar.structure}</div>
          <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 6px;">${day.grammar.note}</div>
          <div style="font-size: 0.88rem; font-style: italic; color: #93c5fd;">Ví dụ: "${day.grammar.example}"</div>
        </div>
      `;
    }

    if (day.isReview) {
      html += `
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 18px; margin-bottom: 16px;">
          <h4 style="color: #fbbf24; margin-bottom: 10px;">📌 Ghi chú trọng tâm ôn tập:</h4>
          <ul style="padding-left: 20px; line-height: 1.6; color: #fde68a;">
            ${day.reviewNotes.map(n => `<li>${n}</li>`).join('')}
          </ul>
          ${day.integratedExample ? `
            <div style="margin-top: 12px; font-size: 0.9rem; color: #e2e8f0; font-style: italic; border-top: 1px dashed rgba(245, 158, 11, 0.3); padding-top: 8px;">
              <strong>Ví dụ tích hợp đa chủ đề:</strong> "${day.integratedExample}"
            </div>
          ` : ''}
        </div>
      `;
    }

    if (day.vocab && day.vocab.length > 0) {
      html += `
        <h4 style="font-size: 1.05rem; font-weight: 700; margin: 20px 0 12px 0;">Danh sách 5 Thẻ Từ Vựng:</h4>
        <div class="modal-vocab-list">
          ${day.vocab.map(v => {
            const uCard = state.userCards[v.id];
            let cardTagBadge = '';
            if (uCard) {
              const uLvl = LEVEL_CONFIG[uCard.level] || LEVEL_CONFIG[1];
              cardTagBadge = `<span class="card-tag-chip tag-box" style="font-size: 0.72rem; color: ${uLvl.color}; border-color: ${uLvl.color}50; background: ${uLvl.color}15;">📦 ${uLvl.name}</span>`;
            } else {
              cardTagBadge = `<span class="card-tag-chip tag-new-pill" style="font-size: 0.72rem;">✨ Chưa nạp</span>`;
            }

            return `
              <div class="modal-word-row">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; flex-wrap: wrap; gap: 6px;">
                  <div>
                    <strong style="font-size: 1.15rem; color: #ffffff;">${v.word}</strong>
                    <span style="color: #38bdf8; font-family: serif; margin-left: 8px;">${v.phonetics}</span>
                    <span style="font-size: 0.75rem; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; margin-left: 6px;">${v.pos}</span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 6px;">
                    ${cardTagBadge}
                    <button class="btn-speaker modal-tts" data-word="${v.word}" style="width: 32px; height: 32px; font-size: 14px;">🔊</button>
                  </div>
                </div>
                <div style="color: #34d399; font-weight: 600; font-size: 0.95rem; margin-bottom: 4px;">${v.meaning}</div>
                <div style="font-size: 0.85rem; color: #67e8f9; margin-bottom: 2px;"><strong>Collocation:</strong> ${v.collocation}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; font-style: italic;"><strong>Ví dụ:</strong> "${v.example}"</div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    html += `
      <div style="margin-top: 24px; display: flex; justify-content: flex-end; gap: 10px; flex-wrap: wrap;">
        ${(day.vocab && day.vocab.length > 0) ? `
          <button class="btn-primary" id="btn-modal-study-action" style="padding: 8px 18px;">
            📖 Bắt đầu học 5 từ này (SRS)
          </button>
        ` : ''}
        <button class="btn-secondary" id="btn-modal-close-action" style="padding: 8px 18px;">
          Đóng cửa sổ
        </button>
      </div>
    `;

    modalBody.innerHTML = html;

    // Attach TTS
    modalBody.querySelectorAll('.modal-tts').forEach(btn => {
      btn.addEventListener('click', () => {
        speakText(btn.getAttribute('data-word'));
      });
    });

    document.getElementById('btn-modal-study-action')?.addEventListener('click', () => {
      closeDayModal();
      startDailyStudySession(day.day);
    });

    document.getElementById('btn-modal-close-action')?.addEventListener('click', closeDayModal);

    modal.classList.add('active');
  }

  function closeDayModal() {
    const modal = document.getElementById('day-modal');
    modal?.classList.remove('active');
  }

  // ==========================================
  // VIEW RENDERING: ANALYTICS & SETTINGS
  // ==========================================
  function renderAnalytics() {
    const totalCards = Object.keys(state.userCards).length;
    const dueCards = getDueCards();
    const masteredCards = getAllCardsInLevel(5).length;
    const learnedDaysCount = Object.keys(state.learnedDays).length;

    const elTotal = document.getElementById('stat-total-cards');
    const elDue = document.getElementById('stat-due-cards');
    const elMastered = document.getElementById('stat-mastered-cards');
    const elDays = document.getElementById('stat-learned-days');

    if (elTotal) elTotal.innerText = totalCards;
    if (elDue) elDue.innerText = dueCards.length;
    if (elMastered) elMastered.innerText = masteredCards;
    if (elDays) elDays.innerText = `${learnedDaysCount} / 50`;

    // Retention distribution bar
    const bar = document.getElementById('retention-bar');
    if (bar && totalCards > 0) {
      bar.innerHTML = Object.values(LEVEL_CONFIG).map(lvl => {
        const count = getAllCardsInLevel(lvl.id).length;
        const pct = ((count / totalCards) * 100).toFixed(1);
        return `<div class="retention-seg" style="width: ${pct}%; background: ${lvl.color};" title="${lvl.name}: ${count} thẻ (${pct}%)"></div>`;
      }).join('');
    }
  }

  // ==========================================
  // HEADER STATS & DUE BANNER
  // ==========================================
  function updateHeaderStats() {
    const dueCards = getDueCards();
    const masteredCount = getAllCardsInLevel(5).length;

    const headerDue = document.getElementById('header-due-count');
    const headerMastered = document.getElementById('header-mastered-count');
    const navDueBadge = document.getElementById('nav-due-badge');

    if (headerDue) headerDue.innerText = `${dueCards.length} đến hạn`;
    if (headerMastered) headerMastered.innerText = `${masteredCount} từ dài hạn`;
    if (navDueBadge) {
      navDueBadge.innerText = dueCards.length;
      navDueBadge.style.display = dueCards.length > 0 ? 'inline-block' : 'none';
    }

    // Hero Due Banner
    const dueBanner = document.getElementById('due-banner');
    const dueBannerText = document.getElementById('due-banner-text');
    if (dueBanner && dueBannerText) {
      if (dueCards.length > 0) {
        dueBanner.style.display = 'flex';
        dueBannerText.innerText = `Bạn có ${dueCards.length} từ vựng đã đến lịch ôn tập hôm nay theo chu kỳ Spaced Repetition!`;
      } else {
        dueBanner.style.display = 'none';
      }
    }

    // Real date & Challenge Day display
    const realDateEl = document.getElementById('current-real-date-text');
    if (realDateEl) {
      realDateEl.innerText = formatDateDisplay(getToday());
    }

    const challengeDayBadge = document.getElementById('challenge-day-badge');
    if (challengeDayBadge) {
      challengeDayBadge.innerText = `🏆 Thử thách: Ngày ${getChallengeCurrentDay()}/50`;
    }

    const challengeStartBadge = document.getElementById('challenge-start-badge');
    if (challengeStartBadge && state.startDate) {
      challengeStartBadge.style.display = 'inline-flex';
      challengeStartBadge.innerText = `Khởi đầu: ${formatDateDisplay(state.startDate)}`;
    }
  }

  // ==========================================
  // TAB NAVIGATION
  // ==========================================
  function switchTab(tabName) {
    state.currentTab = tabName;
    document.querySelectorAll('.nav-tab').forEach(tab => {
      tab.classList.toggle('active', tab.getAttribute('data-tab') === tabName);
    });

    document.querySelectorAll('.tab-content').forEach(view => {
      view.classList.toggle('active', view.id === `view-${tabName}`);
    });

    if (tabName === 'folders') {
      renderFoldersGrid();
    } else if (tabName === 'roadmap') {
      renderRoadmap();
    } else if (tabName === 'arena') {
      if (state.reviewQueue.length === 0) {
        const due = getDueCards();
        if (due.length > 0) {
          startReviewSession(due, 'Ôn tập thẻ đến hạn');
        } else {
          // If none due, offer all cards or empty state
          const all = Object.values(state.userCards);
          if (all.length > 0) {
            startReviewSession(all, 'Ôn tập toàn bộ thẻ đã học');
          } else {
            renderCurrentReviewCard();
          }
        }
      } else {
        renderCurrentReviewCard();
      }
    } else if (tabName === 'analytics') {
      renderAnalytics();
    }
  }

  // ==========================================
  // TOAST NOTIFICATIONS
  // ==========================================
  function showToast(message) {
    let toast = document.getElementById('app-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'app-toast';
      toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: rgba(19, 27, 46, 0.95);
        color: #ffffff;
        border: 1px solid rgba(99, 102, 241, 0.4);
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        backdrop-filter: blur(12px);
        z-index: 9999;
        transform: translateY(100px);
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        display: flex;
        align-items: center;
        gap: 8px;
      `;
      document.body.appendChild(toast);
    }
    toast.innerHTML = `<span>✨</span> ${message}`;
    toast.style.transform = 'translateY(0)';
    toast.style.opacity = '1';

    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
      toast.style.transform = 'translateY(100px)';
      toast.style.opacity = '0';
    }, 3000);
  }

  // ==========================================
  // EXPORT & IMPORT DATA
  // ==========================================
  function exportDataJSON() {
    const data = {
      userCards: state.userCards,
      learnedDays: state.learnedDays,
      startDate: state.startDate,
      exportDate: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `gs12_srs_backup_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Đã xuất tệp dữ liệu sao lưu thành công!');
  }

  function importDataJSON(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        if (data.userCards) {
          state.userCards = data.userCards;
          state.learnedDays = data.learnedDays || {};
          if (data.startDate) state.startDate = data.startDate;
          saveState();
          renderAll();
          showToast('Đã khôi phục dữ liệu học tập thành công!');
        } else {
          alert('Tệp dữ liệu không hợp lệ.');
        }
      } catch (err) {
        alert('Lỗi đọc tệp JSON: ' + err.message);
      }
    };
    reader.readAsText(file);
  }

  function enrollAll50Days() {
    if (!confirm('Bạn có muốn kích hoạt toàn bộ 50 ngày học vào hệ thống Spaced Repetition không?')) return;
    getAllDaysData().forEach(d => {
      enrollDay(d.day, false);
    });
    saveState();
    renderAll();
    showToast('Đã kích hoạt toàn bộ 50 ngày học vào Spaced Repetition!');
    if (currentUser && window.SupabaseService) {
      window.SupabaseService.saveBulkCardsProgress(currentUser.id, Object.values(state.userCards));
    }
  }

  function resetAllData() {
    if (!confirm('CẢNH BÁO: Thao tác này sẽ xoá toàn bộ lịch sử học tập và đặt lại về Day 1. Bạn có chắc chắn không?')) return;
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem('GS12_SRS_VIRTUAL_DATE');
    localStorage.removeItem(getStartDateKey());
    state.userCards = {};
    state.learnedDays = {};
    state.startDate = getToday().toISOString();
    initializeDefaultDay1();
    saveState();
    renderAll();
    showToast('Đã đặt lại dữ liệu học tập về ban đầu.');
  }

  // ==========================================
  // KEYBOARD SHORTCUTS
  // ==========================================
  function setupKeyboardShortcuts() {
    window.addEventListener('keydown', (e) => {
      // Ignore if typing in input
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

      if (state.currentTab === 'arena' && state.arenaMode === 'flashcard') {
        if (e.code === 'Space') {
          e.preventDefault();
          toggleFlipCard();
        } else if (state.isCardFlipped) {
          const currentCard = state.reviewQueue[state.reviewIndex];
          if (!currentCard) return;
          if (e.key === '1') {
            submitCardReview(currentCard.id, 'again');
          } else if (e.key === '2') {
            submitCardReview(currentCard.id, 'good');
          }
        }
      }
    });
  }

  // ==========================================
  // INITIALIZATION & EVENT BINDINGS
  // ==========================================
  function renderAll() {
    updateHeaderStats();
    if (state.currentTab === 'folders') renderFoldersGrid();
    else if (state.currentTab === 'roadmap') renderRoadmap();
    else if (state.currentTab === 'arena') renderCurrentReviewCard();
    else if (state.currentTab === 'analytics') renderAnalytics();
  }

  function bindEvents() {
    // Navigation tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        switchTab(tab.getAttribute('data-tab'));
      });
    });

    // Hero Due Banner Review Button
    document.getElementById('btn-hero-review')?.addEventListener('click', () => {
      const due = getDueCards();
      startReviewSession(due, 'Ôn tập tất cả thẻ đến hạn');
    });

    // 4 Chế độ phòng ôn tập (Flashcard, Quiz, Điền từ, Sắp xếp câu)
    const modeKeys = ['flashcard', 'quiz', 'fillblank', 'scramble'];
    modeKeys.forEach(m => {
      document.getElementById(`mode-${m}`)?.addEventListener('click', () => {
        state.arenaMode = m;
        modeKeys.forEach(other => {
          const btn = document.getElementById(`mode-${other}`);
          if (btn) {
            if (other === m) btn.classList.add('active');
            else btn.classList.remove('active');
          }
        });
        renderCurrentReviewCard();
      });
    });

    // Sound toggle
    const soundBtn = document.getElementById('btn-toggle-sound');
    soundBtn?.addEventListener('click', () => {
      state.soundEnabled = !state.soundEnabled;
      soundBtn.innerText = state.soundEnabled ? '🔊' : '🔇';
      localStorage.setItem(SOUND_ENABLED_KEY, String(state.soundEnabled));
      showToast(state.soundEnabled ? 'Đã bật hiệu ứng âm thanh' : 'Đã tắt âm thanh');
    });

    // Roadmap filters
    document.querySelectorAll('.module-pill-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.module-pill-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeModuleFilter = btn.getAttribute('data-module');
        renderRoadmap();
      });
    });

    const searchInput = document.getElementById('roadmap-search');
    searchInput?.addEventListener('input', (e) => {
      activeSearchTerm = e.target.value;
      renderRoadmap();
    });

    // Modal close events
    document.getElementById('day-modal-close')?.addEventListener('click', closeDayModal);
    document.getElementById('day-modal')?.addEventListener('click', (e) => {
      if (e.target.id === 'day-modal') closeDayModal();
    });
  }

  // ==========================================
  // SUPABASE AUTH & CLOUD PROGRESS SYNC
  // ==========================================
  let currentUser = null;
  let currentProfile = null;

  async function initSupabaseAuth() {
    if (!window.SupabaseService) return;

    // Luôn luôn gắn sự kiện mở modal và form
    bindAuthUI();

    // Kiểm tra cấu hình API Key
    const banner = document.getElementById('supabase-config-banner');
    if (!window.SupabaseService.isConfigured()) {
      if (banner) banner.style.display = 'flex';
      document.getElementById('btn-prompt-api-key')?.addEventListener('click', openAuthModal);
      return;
    } else {
      if (banner) banner.style.display = 'none';
    }

    // Kiểm tra phiên đăng nhập hiện tại
    try {
      const session = await window.SupabaseService.getSession();
      if (session?.user) {
        currentUser = session.user;
        currentProfile = await window.SupabaseService.getProfile(currentUser.id);
        updateAuthHeader(true);
        closeAuthModal();
        await syncProgressFromCloud();
      } else {
        updateAuthHeader(false);
        // Yêu cầu 4: Chưa đăng nhập/đăng ký thì xuất hiện bảng Yêu cầu
        openAuthModal(true);
      }

      // Lắng nghe sự thay đổi trạng thái đăng nhập
      const client = window.SupabaseService.getClient();
      if (client && client.auth) {
        client.auth.onAuthStateChange(async (event, newSession) => {
          if (event === 'SIGNED_IN' && newSession?.user) {
            currentUser = newSession.user;
            currentProfile = await window.SupabaseService.getProfile(currentUser.id);
            updateAuthHeader(true);
            closeAuthModal();
            await syncProgressFromCloud();
          } else if (event === 'SIGNED_OUT') {
            currentUser = null;
            currentProfile = null;
            updateAuthHeader(false);
            openAuthModal(true);
          }
        });
      }

      // Kiểm tra nếu URL có tham số ?auth=open
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('auth') === 'open') {
        openAuthModal();
      }
    } catch (err) {
      console.warn('Lỗi kiểm tra session:', err);
    }
  }

  function updateAuthHeader(isLoggedIn) {
    const loginBtn = document.getElementById('btn-open-auth-modal');
    const userBox = document.getElementById('user-menu-box');
    const userNameEl = document.getElementById('user-name-display');
    const userAvatarEl = document.getElementById('user-avatar');
    const adminBtn = document.getElementById('btn-header-admin');

    if (isLoggedIn && currentUser) {
      if (loginBtn) loginBtn.style.display = 'none';
      if (userBox) userBox.style.display = 'flex';
      
      const displayName = currentProfile?.full_name || currentUser.email?.split('@')[0] || 'Học viên';
      if (userNameEl) userNameEl.innerText = displayName;
      if (userAvatarEl) userAvatarEl.innerText = displayName.charAt(0).toUpperCase();

      if (adminBtn) {
        adminBtn.style.display = (currentProfile?.role === 'admin') ? 'inline-flex' : 'none';
      }
    } else {
      if (loginBtn) loginBtn.style.display = 'inline-block';
      if (userBox) userBox.style.display = 'none';
      if (adminBtn) adminBtn.style.display = 'none';
    }
  }

  // Helper tìm thông tin thẻ từ ID
  function getCardMetaById(cardId) {
    const allDays = getAllDaysData();
    if (allDays.length > 0) {
      for (const d of allDays) {
        if (d.vocab) {
          const found = d.vocab.find(v => v.id === cardId);
          if (found) {
            return {
              word: found.word,
              phonetics: found.phonetics,
              meaning: found.meaning,
              day: d.day,
              unit: d.unit,
              module: d.module
            };
          }
        }
      }
    }
    return null;
  }

  async function syncProgressFromCloud() {
    if (!currentUser || !window.SupabaseService) return;
    try {
      // 1. Đồng bộ Start Date từ Supabase (chỉ lấy nếu có start_date được chỉ định cụ thể, không lấy created_at)
      const cloudStartDate = currentUser.user_metadata?.start_date || currentProfile?.start_date;
      const localStartDate = localStorage.getItem(getStartDateKey());

      if (cloudStartDate) {
        state.startDate = cloudStartDate;
        localStorage.setItem(getStartDateKey(), cloudStartDate);
      } else if (localStartDate) {
        state.startDate = localStartDate;
        if (window.SupabaseService.updateUserStartDate) {
          window.SupabaseService.updateUserStartDate(localStartDate);
        }
      } else {
        state.startDate = getToday().toISOString();
        localStorage.setItem(getStartDateKey(), state.startDate);
        if (window.SupabaseService.updateUserStartDate) {
          window.SupabaseService.updateUserStartDate(state.startDate);
        }
      }

      // 2. Đồng bộ danh sách thẻ học tập
      const cloudCards = await window.SupabaseService.loadUserProgress(currentUser.id);
      if (cloudCards && cloudCards.length > 0) {
        let changed = false;
        cloudCards.forEach(item => {
          const meta = getCardMetaById(item.card_id) || {};

          if (!state.userCards[item.card_id]) {
            state.userCards[item.card_id] = {
              id: item.card_id,
              word: meta.word || item.card_id,
              day: meta.day || 1,
              unit: meta.unit || '',
              module: meta.module || '',
              level: item.level,
              streak: item.streak,
              lastReviewed: item.last_reviewed,
              learnedDate: (item.last_reviewed ? item.last_reviewed.split('T')[0] : getToday().toISOString().split('T')[0]),
              nextReviewDate: item.next_review_date,
              reviewCount: item.streak || 1,
              history: []
            };
            changed = true;
          } else {
            state.userCards[item.card_id].level = item.level;
            state.userCards[item.card_id].streak = item.streak;
            state.userCards[item.card_id].nextReviewDate = item.next_review_date;
            state.userCards[item.card_id].lastReviewed = item.last_reviewed;
            if (item.last_reviewed && !state.userCards[item.card_id].learnedDate) {
              state.userCards[item.card_id].learnedDate = item.last_reviewed.split('T')[0];
            }
            if (!state.userCards[item.card_id].word && meta.word) {
              state.userCards[item.card_id].word = meta.word;
              state.userCards[item.card_id].day = meta.day;
              state.userCards[item.card_id].unit = meta.unit;
              state.userCards[item.card_id].module = meta.module;
            }
            changed = true;
          }
        });

        // Chỉ đánh dấu hoàn thành nếu toàn bộ 5 từ trong ngày đạt level >= 2
        state.learnedDays = {};
        for (let d = 1; d <= 50; d++) {
          if (checkDayCompletion(d)) {
            state.learnedDays[d] = true;
          }
        }

        if (changed) {
          saveState();
        }
      } else {
        const localCards = Object.values(state.userCards);
        if (localCards.length > 0) {
          await window.SupabaseService.saveBulkCardsProgress(currentUser.id, localCards);
        }
      }

      // 3. Tự động cộng dồn bài học đến ngày hiện tại theo lịch thực tế
      syncDailyAccumulation();
      renderAll();
      showToast('Đã đồng bộ tiến độ học tập từ Đám Mây!');
    } catch (err) {
      console.warn('Lỗi đồng bộ đám mây:', err);
    }
  }

  function bindAuthUI() {
    const modal = document.getElementById('auth-modal');
    const openBtn = document.getElementById('btn-open-auth-modal');
    const closeBtn = document.getElementById('auth-modal-close');
    const tabLogin = document.getElementById('tab-login-btn');
    const tabRegister = document.getElementById('tab-register-btn');
    const formLogin = document.getElementById('form-login');
    const formRegister = document.getElementById('form-register');
    const feedback = document.getElementById('auth-feedback');
    const logoutBtn = document.getElementById('btn-header-logout');
    const saveKeyBtn = document.getElementById('btn-save-modal-key');

    openBtn?.addEventListener('click', () => openAuthModal(false));
    closeBtn?.addEventListener('click', closeAuthModal);
    modal?.addEventListener('click', (e) => {
      if (e.target.id === 'auth-modal') {
        if (modal?.classList.contains('compulsory-lock') && !currentUser) return;
        closeAuthModal();
      }
    });

    saveKeyBtn?.addEventListener('click', () => {
      const input = document.getElementById('modal-api-key-input');
      const val = (input?.value || '').trim();
      if (!val || val.length < 10) {
        alert('Vui lòng dán khóa API Key hợp lệ.');
        return;
      }
      window.SupabaseService.setApiKey(val);
    });

    tabLogin?.addEventListener('click', () => {
      tabLogin.classList.add('active');
      tabRegister.classList.remove('active');
      formLogin.style.display = 'block';
      formRegister.style.display = 'none';
      document.getElementById('auth-title').innerText = 'Đăng Nhập Tài Khoản';
      feedback.style.display = 'none';
    });

    tabRegister?.addEventListener('click', () => {
      tabRegister.classList.add('active');
      tabLogin.classList.remove('active');
      formRegister.style.display = 'block';
      formLogin.style.display = 'none';
      document.getElementById('auth-title').innerText = 'Đăng Ký Tài Khoản Mới';
      feedback.style.display = 'none';
    });

    formLogin?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();
      const pass = document.getElementById('login-password').value;
      feedback.className = 'auth-msg';
      feedback.style.display = 'none';

      try {
        await window.SupabaseService.signIn(email, pass);
        feedback.className = 'auth-msg success';
        feedback.innerText = 'Đăng nhập thành công!';
        const modal = document.getElementById('auth-modal');
        if (modal) modal.classList.remove('compulsory-lock');
        setTimeout(closeAuthModal, 600);
      } catch (err) {
        feedback.className = 'auth-msg error';
        let msg = err.message || '';
        if (msg.includes('Invalid login credentials')) {
          msg = 'Email hoặc mật khẩu chưa đúng, HOẶC bạn chưa tạo tài khoản trong dự án mới này. Vui lòng bấm sang tab "Đăng Ký Mới" bên cạnh để tạo tài khoản!';
        } else if (msg.includes('Email not confirmed')) {
          msg = 'Tài khoản chưa được kích hoạt email. Bạn hãy vào Supabase -> Authentication -> Providers -> Email -> Tắt "Confirm email" để đăng nhập ngay mà không cần kích hoạt!';
        }
        feedback.innerText = 'Lỗi đăng nhập: ' + msg;
      }
    });

    formRegister?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const pass = document.getElementById('reg-password').value;
      feedback.className = 'auth-msg';
      feedback.style.display = 'none';

      try {
        const res = await window.SupabaseService.signUp(email, pass, name);
        if (res?.session) {
          feedback.className = 'auth-msg success';
          feedback.innerText = 'Đăng ký và đăng nhập thành công!';
          const modal = document.getElementById('auth-modal');
          if (modal) modal.classList.remove('compulsory-lock');
          setTimeout(closeAuthModal, 600);
        } else {
          feedback.className = 'auth-msg success';
          feedback.innerText = 'Đăng ký tài khoản thành công! Đang chuyển sang đăng nhập...';
          setTimeout(() => {
            tabLogin?.click();
            document.getElementById('login-email').value = email;
            document.getElementById('login-password').value = pass;
          }, 800);
        }
      } catch (err) {
        feedback.className = 'auth-msg error';
        let msg = err.message || '';
        if (msg.includes('rate limit')) {
          msg = 'Giới hạn gửi email của Supabase đã vượt quá. Bạn hãy vào Supabase -> Authentication -> Providers -> Email -> Tắt "Confirm email" để tạo tài khoản ngay lập tức!';
        }
        feedback.innerText = 'Lỗi đăng ký: ' + msg;
      }
    });

    logoutBtn?.addEventListener('click', async () => {
      if (confirm('Bạn có muốn đăng xuất khỏi tài khoản không?')) {
        await window.SupabaseService.signOut();
        currentUser = null;
        currentProfile = null;
        updateAuthHeader(false);
        showToast('Đã đăng xuất tài khoản.');
        openAuthModal(true);
      }
    });
  }

  function openAuthModal(isCompulsory = false) {
    const modal = document.getElementById('auth-modal');
    if (!modal) return;

    const keySection = document.getElementById('auth-key-prompt-section');
    const formsContainer = document.getElementById('auth-forms-container');
    const titleEl = document.getElementById('auth-title');
    const compulsoryBanner = document.getElementById('auth-compulsory-banner');

    if (isCompulsory) {
      modal.classList.add('compulsory-lock');
      if (compulsoryBanner) compulsoryBanner.style.display = 'block';
    } else {
      modal.classList.remove('compulsory-lock');
      if (compulsoryBanner) compulsoryBanner.style.display = 'none';
    }

    // Kiểm tra đã cấu hình API Key chưa
    if (!window.SupabaseService || !window.SupabaseService.isConfigured()) {
      if (keySection) keySection.style.display = 'block';
      if (formsContainer) formsContainer.style.display = 'none';
      if (titleEl) titleEl.innerText = 'Kết Nối Supabase';
    } else {
      if (keySection) keySection.style.display = 'none';
      if (formsContainer) formsContainer.style.display = 'block';
      if (titleEl) titleEl.innerText = isCompulsory ? 'Yêu Cầu Đăng Nhập / Đăng Ký' : 'Đăng Nhập Tài Khoản';
    }

    modal.classList.add('active');
  }

  function closeAuthModal() {
    const modal = document.getElementById('auth-modal');
    if (modal) {
      if (!currentUser && modal.classList.contains('compulsory-lock')) {
        return;
      }
      modal.classList.remove('active');
      modal.classList.remove('compulsory-lock');
    }
  }

  // App bootstrap
  function init() {
    loadState();
    syncDailyAccumulation();
    bindEvents();
    setupKeyboardShortcuts();
    renderAll();
    renderFoldersGrid();
    initSupabaseAuth();

    // Set initial sound button icon
    const soundBtn = document.getElementById('btn-toggle-sound');
    if (soundBtn) soundBtn.innerText = state.soundEnabled ? '🔊' : '🔇';
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
