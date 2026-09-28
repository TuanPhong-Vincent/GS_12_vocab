/**
 * GLOBAL SUCCESS 12 VOCAB CHALLENGE - SUPABASE CLIENT INTEGRATION
 * Manages Supabase Auth, Cloud Database Sync, and Admin Operations.
 */

(function () {
  'use strict';

  // 1. SUPABASE PROJECT CONFIGURATION
  const DEFAULT_URL = 'https://wjyahmlrkcvtohvxjtil.supabase.co';
  
  // Khóa Publishable Key dự án GS12
  const DEFAULT_KEY = 'sb_publishable_0jYw3-iaOTT6zQefnAucxw_9mK6itql'; 

  // Lấy key cấu hình
  const activeUrl = DEFAULT_URL;
  const activeKey = DEFAULT_KEY;

  let supabase = null;
  let isReady = false;

  if (window.supabase && activeUrl && activeKey && activeKey.trim().length > 10) {
    try {
      supabase = window.supabase.createClient(activeUrl, activeKey);
      isReady = true;
      console.log('⚡ Supabase Client initialized successfully!');
    } catch (err) {
      console.error('❌ Failed to initialize Supabase client:', err);
    }
  }

  // 2. SUPABASE SERVICE INTERFACE
  const SupabaseService = {
    isConfigured: () => isReady,
    getClient: () => supabase,
    getUrl: () => activeUrl,
    getKey: () => activeKey,

    setApiKey: (newKey) => {
      if (!newKey || newKey.trim().length < 10) return false;
      localStorage.setItem('SUPABASE_CUSTOM_KEY', newKey.trim());
      location.reload();
      return true;
    },

    clearApiKey: () => {
      localStorage.removeItem('SUPABASE_CUSTOM_KEY');
      location.reload();
    },

    // AUTHENTICATION
    signUp: async (email, password, fullName) => {
      if (!supabase) throw new Error('Supabase chưa được cấu hình API Key.');
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName,
            role: 'student',
            start_date: new Date().toISOString()
          }
        }
      });
      if (error) throw error;
      return data;
    },

    signIn: async (email, password) => {
      if (!supabase) throw new Error('Supabase chưa được cấu hình API Key.');
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      });
      if (error) throw error;
      return data;
    },

    signOut: async () => {
      if (!supabase) return;
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
    },

    getSession: async () => {
      if (!supabase) return null;
      const { data: { session } } = await supabase.auth.getSession();
      return session;
    },

    updateUserStartDate: async (startDateIso) => {
      if (!supabase) return null;
      try {
        const { data, error } = await supabase.auth.updateUser({
          data: { start_date: startDateIso }
        });
        if (error) console.warn('Could not update start_date in user metadata:', error.message);
        return data;
      } catch (err) {
        console.warn('Error updating start_date:', err);
        return null;
      }
    },

    getProfile: async (userId) => {
      if (!supabase || !userId) return null;
      try {
        const { data, error } = await supabase
          .from('profiles')
          .select('*')
          .eq('id', userId)
          .single();
        if (error) {
          console.warn('Could not load profile from profiles table:', error.message);
          return { id: userId, role: 'student', error: error.message };
        }
        return data;
      } catch (err) {
        return { id: userId, role: 'student', error: err.message };
      }
    },

    // USER PROGRESS SYNC (SRS LEITNER)
    loadUserProgress: async (userId) => {
      if (!supabase || !userId) return [];
      const { data, error } = await supabase
        .from('user_progress')
        .select('*')
        .eq('user_id', userId);
      if (error) {
        console.warn('Failed to load user progress:', error.message);
        return [];
      }
      return data || [];
    },

    saveCardProgress: async (userId, card) => {
      if (!supabase || !userId || !card) return;
      try {
        await supabase.from('user_progress').upsert({
          user_id: userId,
          card_id: card.id,
          level: card.level || 1,
          streak: card.streak || 0,
          next_review_date: card.nextReviewDate,
          last_reviewed: card.lastReviewed || new Date().toISOString()
        }, { onConflict: 'user_id, card_id' });
      } catch (err) {
        console.warn('Failed to sync card to cloud:', err);
      }
    },

    saveBulkCardsProgress: async (userId, cardsArray) => {
      if (!supabase || !userId || !cardsArray || cardsArray.length === 0) return;
      try {
        const rows = cardsArray.map(c => ({
          user_id: userId,
          card_id: c.id,
          level: c.level || 1,
          streak: c.streak || 0,
          next_review_date: c.nextReviewDate,
          last_reviewed: c.lastReviewed || new Date().toISOString()
        }));
        await supabase.from('user_progress').upsert(rows, { onConflict: 'user_id, card_id' });
      } catch (err) {
        console.warn('Failed to bulk sync cards to cloud:', err);
      }
    },

    // VOCABULARY CRUD (FOR ALL USERS & ADMIN)
    fetchVocabCards: async () => {
      if (!supabase) return null;
      try {
        const { data, error } = await supabase
          .from('vocab_cards')
          .select('*')
          .order('day', { ascending: true });
        if (error) throw error;
        return data && data.length > 0 ? data : null;
      } catch (err) {
        console.warn('Could not fetch cloud vocab cards, falling back to local:', err.message);
        return null;
      }
    },

    // ADMIN OPERATIONS
    adminSaveVocabCard: async (card) => {
      if (!supabase) throw new Error('Supabase client chưa sẵn sàng.');
      const { data, error } = await supabase
        .from('vocab_cards')
        .upsert(card, { onConflict: 'id' })
        .select();
      if (error) throw error;
      return data;
    },

    adminDeleteVocabCard: async (cardId) => {
      if (!supabase) throw new Error('Supabase client chưa sẵn sàng.');
      const { error } = await supabase
        .from('vocab_cards')
        .delete()
        .eq('id', cardId);
      if (error) throw error;
      return true;
    },

    adminGetStudentCards: async (userId) => {
      if (!supabase) throw new Error('Supabase client chưa sẵn sàng.');
      const { data, error } = await supabase
        .from('user_progress')
        .select('*')
        .eq('user_id', userId);
      if (error) throw error;
      return data || [];
    },

    adminGetAllStudents: async () => {
      if (!supabase) throw new Error('Supabase client chưa sẵn sàng.');
      // Lấy danh sách profiles kèm theo thống kê tiến độ
      const { data: profiles, error: profileErr } = await supabase
        .from('profiles')
        .select('*')
        .order('created_at', { ascending: false });
      if (profileErr) throw profileErr;

      const { data: progress, error: progErr } = await supabase
        .from('user_progress')
        .select('user_id, level, card_id');
      
      const statsMap = {};
      if (progress) {
        progress.forEach(p => {
          if (!statsMap[p.user_id]) {
            statsMap[p.user_id] = { total: 0, box1: 0, box2: 0, box3: 0, box4: 0, box5: 0 };
          }
          statsMap[p.user_id].total++;
          const boxKey = 'box' + p.level;
          if (statsMap[p.user_id][boxKey] !== undefined) {
            statsMap[p.user_id][boxKey]++;
          }
        });
      }

      return (profiles || []).map(u => ({
        ...u,
        stats: statsMap[u.id] || { total: 0, box1: 0, box2: 0, box3: 0, box4: 0, box5: 0 }
      }));
    },

    adminSetUserRole: async (userId, newRole) => {
      if (!supabase) throw new Error('Supabase client chưa sẵn sàng.');
      const { data, error } = await supabase
        .from('profiles')
        .update({ role: newRole })
        .eq('id', userId)
        .select();
      if (error) throw error;
      return data;
    },

    adminImportAllCardsFromDataJs: async () => {
      if (!supabase) throw new Error('Supabase client chưa sẵn sàng.');
      const dataList = window.GS12_50_DAYS_DATA || window.IELTS_50_DAYS_DATA;
      if (!dataList) throw new Error('Không tìm thấy dữ liệu gốc GS12_50_DAYS_DATA trong data.js.');

      const allCards = [];
      dataList.forEach(dayItem => {
        if (dayItem.vocab && Array.isArray(dayItem.vocab)) {
          dayItem.vocab.forEach(v => {
            allCards.push({
              id: v.id,
              day: dayItem.day,
              module: dayItem.module || '',
              unit: dayItem.unit || '',
              subtopic: dayItem.subtopic || '',
              word: v.word,
              phonetics: v.phonetics || '',
              pos: v.pos || '',
              meaning: v.meaning || '',
              collocation: v.collocation || '',
              example: v.example || ''
            });
          });
        }
      });

      // Upload in chunks of 50
      const chunkSize = 50;
      let insertedCount = 0;
      for (let i = 0; i < allCards.length; i += chunkSize) {
        const chunk = allCards.slice(i, i + chunkSize);
        const { error } = await supabase.from('vocab_cards').upsert(chunk, { onConflict: 'id' });
        if (error) throw error;
        insertedCount += chunk.length;
      }
      return insertedCount;
    },

    // QUẢN TRỊ ĐIỀU CHỈNH TIẾN ĐỘ & HỌC VIÊN
    adminUpdateStudentCardLevel: async (userId, cardId, newLevel) => {
      if (!supabase) throw new Error('Supabase client chưa sẵn sàng.');
      const intervals = { 1: 1, 2: 3, 3: 7, 4: 14, 5: 30 };
      const days = intervals[newLevel] || 1;
      const nextDate = new Date();
      nextDate.setDate(nextDate.getDate() + days);

      const { data, error } = await supabase
        .from('user_progress')
        .upsert({
          user_id: userId,
          card_id: cardId,
          level: parseInt(newLevel, 10),
          next_review_date: nextDate.toISOString(),
          last_reviewed: new Date().toISOString()
        }, { onConflict: 'user_id, card_id' })
        .select();

      if (error) throw error;
      return data;
    },

    adminDeleteStudent: async (userId) => {
      if (!supabase) throw new Error('Supabase client chưa sẵn sàng.');
      try {
        const { error: rpcErr } = await supabase.rpc('admin_delete_student', { target_user_id: userId });
        if (!rpcErr) return true;
        console.warn('RPC admin_delete_student:', rpcErr.message);
      } catch (e) {
        console.warn('Fallback to table delete:', e);
      }

      const { error: progErr } = await supabase.from('user_progress').delete().eq('user_id', userId);
      if (progErr) console.warn('Lỗi xóa user_progress:', progErr.message);

      const { error: profErr } = await supabase.from('profiles').delete().eq('id', userId);
      if (profErr) throw profErr;
      return true;
    },

    adminEnrollAllDaysForStudent: async (userId) => {
      if (!supabase || !userId) throw new Error('Supabase client hoặc userId chưa sẵn sàng.');
      const allCards = [];
      const now = new Date().toISOString();
      const dataList = window.GS12_50_DAYS_DATA || window.IELTS_50_DAYS_DATA;
      if (dataList) {
        dataList.forEach(d => {
          if (d.vocab && Array.isArray(d.vocab)) {
            d.vocab.forEach(v => {
              allCards.push({
                user_id: userId,
                card_id: v.id,
                level: 1,
                streak: 0,
                next_review_date: now,
                last_reviewed: now
              });
            });
          }
        });
      }
      if (allCards.length === 0) throw new Error('Không có dữ liệu từ vựng để nạp.');
      const chunkSize = 50;
      for (let i = 0; i < allCards.length; i += chunkSize) {
        const chunk = allCards.slice(i, i + chunkSize);
        const { error } = await supabase.from('user_progress').upsert(chunk, { onConflict: 'user_id, card_id' });
        if (error) throw error;
      }
      return allCards.length;
    },

    adminResetStudentProgress: async (userId) => {
      if (!supabase || !userId) throw new Error('Supabase client hoặc userId chưa sẵn sàng.');
      const { error } = await supabase.from('user_progress').delete().eq('user_id', userId);
      if (error) throw error;
      return true;
    },

    // CHUẨN HÓA HỘP LEITNER SRS THEO NGÀY BẮT ĐẦU (HỘP 1, 2, 3, 4, 5)
    // - Ngày hôm nay: Nằm ở Hộp 1 (Từ mới), cần học hôm nay
    // - Các ngày trước hôm nay:
    //   + Bắt đầu: Lên Hộp 2, hẹn ôn sau +3 ngày
    //   + Nếu mốc +3 ngày đã qua trong quá khứ (< today): Đã ôn -> Lên Hộp 3 (+7 ngày)
    //   + Nếu mốc +7 ngày đã qua trong quá khứ (< today): Đã ôn -> Lên Hộp 4 (+14 ngày)
    //   + Nếu mốc +14 ngày đã qua trong quá khứ (< today): Đã ôn -> Lên Hộp 5 (+30 ngày)
    //   + Nếu mốc +30 ngày đã qua trong quá khứ (< today): Đã ôn -> Giữ Hộp 5 Master (+60 ngày)
    adminCalibrateStudentCards: async (userId, startDateStr) => {
      if (!supabase || !userId) throw new Error('Supabase client hoặc userId chưa sẵn sàng.');
      const dataList = window.GS12_50_DAYS_DATA || window.IELTS_50_DAYS_DATA;
      if (!dataList) throw new Error('Không tìm thấy dữ liệu từ vựng gốc GS12_50_DAYS_DATA.');

      let start = new Date(startDateStr || '2026-09-10');
      if (isNaN(start.getTime())) start = new Date('2026-09-10');
      start.setHours(0, 0, 0, 0);

      const today = new Date();
      today.setHours(0, 0, 0, 0);

      const diffDays = Math.floor((today.getTime() - start.getTime()) / (1000 * 3600 * 24));
      const currentDayNum = Math.max(1, Math.min(50, diffDays + 1));

      // Hàm tính toán trạng thái Hộp SRS (1 -> 5) chuẩn theo dòng thời gian
      // Tính luôn cả ngày hôm nay vào chuẩn hoá (xem như buổi học/ôn của ngày hôm nay đã hoàn thành)
      function computeSRSState(learnedDate) {
        // Nếu ngày học ở tương lai (> today): Giữ ở Hộp 1 (chưa học)
        if (learnedDate.getTime() > today.getTime()) {
          const t = new Date(learnedDate);
          t.setHours(8, 0, 0, 0);
          return {
            level: 1,
            streak: 0,
            lastReviewed: t.toISOString(),
            nextReviewDate: t.toISOString()
          };
        }

        // Các mốc chuyển Hộp Leitner:
        // Học xong lần đầu -> Hộp 2 (+3 ngày)
        // Ôn xong mốc 3 ngày -> Hộp 3 (+7 ngày)
        // Ôn xong mốc 7 ngày -> Hộp 4 (+14 ngày)
        // Ôn xong mốc 14 ngày -> Hộp 5 (+30 ngày)
        const steps = [
          { toLevel: 2, addDays: 3 },
          { toLevel: 3, addDays: 7 },
          { toLevel: 4, addDays: 14 },
          { toLevel: 5, addDays: 30 }
        ];

        // Học xong từ mới (kể cả hôm nay): Vào Hộp 2, hẹn ôn sau +3 ngày
        let level = 2;
        let streak = 1;
        let lastRev = new Date(learnedDate);
        lastRev.setHours(8, 0, 0, 0);

        let nextRev = new Date(learnedDate);
        nextRev.setDate(nextRev.getDate() + 3);
        nextRev.setHours(8, 0, 0, 0);

        // Duyệt các mốc thăng cấp tiếp theo (Hộp 3, 4, 5)
        // Tính luôn cả ngày hôm nay: nếu mốc hẹn ôn <= today,
        // coi như học viên đã hoàn thành buổi ôn tập hôm nay -> thăng cấp lên Hộp tiếp theo!
        for (let i = 1; i < steps.length; i++) {
          const nextRevDateOnly = new Date(nextRev);
          nextRevDateOnly.setHours(0, 0, 0, 0);

          if (nextRevDateOnly.getTime() <= today.getTime()) {
            lastRev = new Date(nextRev);
            level = steps[i].toLevel;
            streak++;
            nextRev = new Date(lastRev);
            nextRev.setDate(nextRev.getDate() + steps[i].addDays);
            nextRev.setHours(8, 0, 0, 0);
          } else {
            // Mốc ôn là tương lai (> today) -> dừng lại ở Hộp hiện tại
            break;
          }
        }

        // Nếu đã ở Hộp 5 (Master) và mốc ôn tiếp theo cũng <= today:
        const nextRevDateOnly = new Date(nextRev);
        nextRevDateOnly.setHours(0, 0, 0, 0);
        if (level === 5 && nextRevDateOnly.getTime() <= today.getTime()) {
          lastRev = new Date(nextRev);
          streak++;
          nextRev = new Date(lastRev);
          nextRev.setDate(nextRev.getDate() + 60);
          nextRev.setHours(8, 0, 0, 0);
        }

        return {
          level,
          streak,
          lastReviewed: lastRev.toISOString(),
          nextReviewDate: nextRev.toISOString()
        };
      }

      const rowsToUpsert = [];

      for (let d = 1; d <= currentDayNum; d++) {
        const dataList = window.GS12_50_DAYS_DATA || window.IELTS_50_DAYS_DATA;
        const dayData = dataList ? dataList.find(item => item.day === d) : null;
        if (!dayData || !dayData.vocab || dayData.vocab.length === 0) continue;

        // Ngày học thực tế của Day d
        const learnedDate = new Date(start);
        learnedDate.setDate(start.getDate() + (d - 1));
        learnedDate.setHours(0, 0, 0, 0);

        const srs = computeSRSState(learnedDate);

        dayData.vocab.forEach(v => {
          rowsToUpsert.push({
            user_id: userId,
            card_id: v.id,
            level: srs.level,
            streak: srs.streak,
            last_reviewed: srs.lastReviewed,
            next_review_date: srs.nextReviewDate
          });
        });
      }

      if (rowsToUpsert.length === 0) return 0;

      // Cố gắng cập nhật start_date vào profile học viên (nếu bảng profiles có cột này)
      try {
        const { error: updErr } = await supabase.from('profiles').update({ start_date: start.toISOString() }).eq('id', userId);
        if (updErr) {
          console.warn('Cột start_date có thể chưa tồn tại trong bảng profiles, bỏ qua cập nhật bảng profiles:', updErr.message);
        }
      } catch (e) {
        console.warn('Không thể lưu start_date vào bảng profiles:', e);
      }

      // Upsert theo từng chunk 50 thẻ
      const chunkSize = 50;
      for (let i = 0; i < rowsToUpsert.length; i += chunkSize) {
        const chunk = rowsToUpsert.slice(i, i + chunkSize);
        const { error } = await supabase.from('user_progress').upsert(chunk, { onConflict: 'user_id, card_id' });
        if (error) throw error;
      }

      return rowsToUpsert.length;
    },

    // Chuẩn hóa toàn bộ học viên: Tự động dựa theo Ngày Đăng Ký Lần Đầu (created_at) của từng học viên
    adminCalibrateAllStudents: async () => {
      if (!supabase) throw new Error('Supabase client chưa sẵn sàng.');
      // Dùng select('*') để tương thích an toàn nếu bảng profiles chưa có cột start_date
      const { data: profiles, error } = await supabase
        .from('profiles')
        .select('*');
      if (error) throw error;
      if (!profiles || profiles.length === 0) return { studentCount: 0, cardCount: 0, details: [] };

      let totalCards = 0;
      let studentCount = 0;
      const details = [];

      for (const p of profiles) {
        // Lấy chính xác Ngày Đăng Ký Lần Đầu của học viên (ưu tiên start_date nếu có, fallback về created_at)
        const studentRegDate = p.start_date || p.created_at || new Date().toISOString();
        const cardsCount = await SupabaseService.adminCalibrateStudentCards(p.id, studentRegDate);
        totalCards += cardsCount;
        studentCount++;
        details.push({
          name: p.full_name || p.email,
          registeredAt: new Date(studentRegDate).toLocaleDateString('vi-VN'),
          cards: cardsCount
        });
      }

      return { studentCount, cardCount: totalCards, details };
    },

    adminUpdateStudentStartDate: async (userId, startDateStr) => {
      if (!supabase || !userId) throw new Error('Supabase client hoặc userId chưa sẵn sàng.');
      const start = new Date(startDateStr);
      if (isNaN(start.getTime())) throw new Error('Ngày không hợp lệ');
      try {
        const { data, error } = await supabase
          .from('profiles')
          .update({ start_date: start.toISOString() })
          .eq('id', userId)
          .select();
        if (error) {
          console.warn('Không thể cập nhật start_date trong profiles:', error.message);
          return null;
        }
        return data;
      } catch (err) {
        console.warn('Lỗi adminUpdateStudentStartDate:', err);
        return null;
      }
    }
  };

  window.SupabaseService = SupabaseService;
})();
