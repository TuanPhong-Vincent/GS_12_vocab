/**
 * GLOBAL SUCCESS 12 VOCAB CHALLENGE - ADMIN MANAGEMENT LOGIC
 * Handles Vocab CMS, Student Monitoring, and Supabase Database Operations.
 */

(function () {
  'use strict';

  let currentAdmin = null;
  let adminProfile = null;
  let allVocabCards = [];
  let allStudents = [];

  // ==========================================
  // INITIALIZATION & AUTH GUARD
  // ==========================================
  async function initAdmin() {
    if (!window.SupabaseService) {
      alert('Không tìm thấy SupabaseService. Hãy kiểm tra kết nối mạng.');
      return;
    }

    // Kiểm tra cấu hình API Key
    if (!window.SupabaseService.isConfigured()) {
      showGateScreen('Chưa Cấu Hình Khóa API Supabase', 'Vui lòng nhập API Key của Supabase để hệ thống có thể kết nối với cơ sở dữ liệu đám mây.');
      return;
    }

    // Kiểm tra phiên đăng nhập
    try {
      const session = await window.SupabaseService.getSession();
      if (!session || !session.user) {
        showGateScreen('Chưa Đăng Nhập', 'Vui lòng đăng nhập với tài khoản có quyền Quản trị viên (Admin) để tiếp tục.');
        return;
      }

      currentAdmin = session.user;
      adminProfile = await window.SupabaseService.getProfile(currentAdmin.id);

      // Kiểm tra quyền role admin
      if (!adminProfile || adminProfile.role !== 'admin') {
        const isRecurErr = adminProfile?.error && adminProfile.error.includes('recursion');
        const descHtml = `
          <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 18px; margin: 18px 0; text-align: left; font-size: 0.88rem;">
            <div style="margin-bottom: 8px;"><strong>Tài khoản đang đăng nhập:</strong> <span style="color: #38bdf8;">${currentAdmin.email}</span></div>
            <div style="margin-bottom: 12px;"><strong>Vai trò hiện tại:</strong> <span style="color: #f97316; font-weight: 700;">${adminProfile?.role || 'Chưa xác định (Lỗi RLS)'}</span></div>
            
            ${isRecurErr ? `
              <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.3); padding: 10px; border-radius: 8px; color: #fca5a5; font-size: 0.82rem; margin-bottom: 12px;">
                ⚠️ <strong>Lỗi cơ sở dữ liệu Supabase:</strong> Bảng profiles đang bị lỗi đệ quy RLS (Error 500). Bạn cần chạy lại mã trong file <code>supabase_schema.sql</code> trên Supabase SQL Editor.
              </div>
            ` : `
              <p style="color: #94a3b8; font-size: 0.82rem; margin-bottom: 10px;">
                Tài khoản của bạn vừa đăng ký mặc định là <em>Học viên (Student)</em>. Để cấp quyền Quản trị (Admin) cho tài khoản này, hãy vào <strong>Supabase ➔ SQL Editor</strong> và chạy lệnh sau:
              </p>
            `}

            <div style="background: #020617; border: 1px solid rgba(255,255,255,0.1); padding: 10px; border-radius: 6px; font-family: monospace; font-size: 0.8rem; color: #34d399; margin-bottom: 10px; word-break: break-all;">
              update public.profiles set role = 'admin' where email = '${currentAdmin.email}';
            </div>
          </div>
        `;
        showGateScreen('Chưa Có Quyền Quản Trị', descHtml, true);
        return;
      }

      // Đã xác thực quyền admin thành công!
      setupAdminUI();
      bindAdminEvents();
      populateDayFilter();
      await loadDashboardData();

    } catch (err) {
      console.error('Lỗi khởi tạo Admin:', err);
      showGateScreen('Lỗi Kết Nối', err.message);
    }
  }

  function showGateScreen(title, descOrHtml, isHtml = false) {
    document.getElementById('admin-main-content').style.display = 'none';
    const gate = document.getElementById('admin-gate-screen');
    gate.style.display = 'flex';
    document.getElementById('gate-title').innerText = title;
    
    const descEl = document.getElementById('gate-desc');
    if (isHtml) {
      descEl.innerHTML = descOrHtml;
    } else {
      descEl.innerText = descOrHtml;
    }

    const loginBtn = document.getElementById('btn-gate-login');
    if (currentAdmin) {
      loginBtn.innerText = '🚪 Đăng xuất tài khoản này';
      loginBtn.onclick = async () => {
        await window.SupabaseService.signOut();
        location.reload();
      };
    } else {
      loginBtn.innerText = '🔑 Đăng nhập ngay';
      loginBtn.onclick = () => {
        location.href = 'index.html?auth=open';
      };
    }
  }

  function setupAdminUI() {
    document.getElementById('admin-gate-screen').style.display = 'none';
    document.getElementById('admin-main-content').style.display = 'block';

    const nameEl = document.getElementById('admin-user-name');
    const avatarEl = document.getElementById('admin-avatar');
    const displayName = adminProfile.full_name || currentAdmin.email.split('@')[0];

    nameEl.innerText = displayName;
    avatarEl.innerText = displayName.charAt(0).toUpperCase();
  }

  function populateDayFilter() {
    const select = document.getElementById('vocab-day-filter');
    for (let i = 1; i <= 50; i++) {
      const opt = document.createElement('option');
      opt.value = String(i);
      opt.innerText = `Ngày ${i}`;
      select.appendChild(opt);
    }
  }

  // ==========================================
  // DATA LOADING & STATS
  // ==========================================
  async function loadDashboardData() {
    await Promise.all([loadVocabCards(), loadStudents()]);
    updateQuickStats();
  }

  async function loadVocabCards() {
    const tbody = document.getElementById('vocab-table-body');
    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 30px; color: #94a3b8;">Đang tải danh sách từ vựng từ đám mây...</td></tr>';

    try {
      const data = await window.SupabaseService.fetchVocabCards();
      if (data && data.length > 0) {
        allVocabCards = data;
      } else {
        allVocabCards = [];
      }
      renderVocabTable();
    } catch (err) {
      console.error('Lỗi tải từ vựng:', err);
      tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 30px; color: #f87171;">Lỗi: ${err.message}</td></tr>`;
    }
  }

  async function loadStudents() {
    const tbody = document.getElementById('students-table-body');
    tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 30px; color: #94a3b8;">Đang tải danh sách học viên...</td></tr>';

    try {
      allStudents = await window.SupabaseService.adminGetAllStudents();
      renderStudentsTable();
    } catch (err) {
      console.error('Lỗi tải học viên:', err);
      tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 30px; color: #f87171;">Lỗi: ${err.message}</td></tr>`;
    }
  }

  function updateQuickStats() {
    document.getElementById('stat-total-vocab').innerText = allVocabCards.length;
    document.getElementById('stat-total-students').innerText = allStudents.length;

    let mastered = 0;
    allStudents.forEach(s => {
      if (s.stats && s.stats.box5) mastered += s.stats.box5;
    });
    document.getElementById('stat-mastered-cards').innerText = mastered;
  }

  // ==========================================
  // VOCAB TABLE RENDERING & FILTERING
  // ==========================================
  function renderVocabTable() {
    const tbody = document.getElementById('vocab-table-body');
    const term = (document.getElementById('vocab-search-input')?.value || '').toLowerCase().trim();
    const dayFilter = document.getElementById('vocab-day-filter')?.value || 'all';

    const filtered = allVocabCards.filter(c => {
      const matchDay = (dayFilter === 'all') || (String(c.day) === dayFilter);
      const matchTerm = !term || 
        (c.word && c.word.toLowerCase().includes(term)) ||
        (c.meaning && c.meaning.toLowerCase().includes(term)) ||
        (c.phonetics && c.phonetics.toLowerCase().includes(term)) ||
        (c.id && c.id.toLowerCase().includes(term));
      return matchDay && matchTerm;
    });

    if (filtered.length === 0) {
      if (allVocabCards.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="8" style="text-align: center; padding: 50px 20px;">
              <div style="font-size: 2rem; margin-bottom: 8px;">📭</div>
              <h4 style="color: #f8fafc; margin-bottom: 6px;">Cơ sở dữ liệu đám mây chưa có từ vựng nào</h4>
              <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 16px;">Bạn có thể nạp nhanh toàn bộ từ vựng Global Success 12 đã soạn sẵn từ data.js vào đám mây chỉ với 1 click.</p>
              <button class="btn-primary" id="btn-empty-sync">⚡ Đồng bộ từ vựng GS12 ngay</button>
            </td>
          </tr>
        `;
        document.getElementById('btn-empty-sync')?.addEventListener('click', syncAllFromDataJs);
      } else {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 30px; color: #94a3b8;">Không tìm thấy từ vựng nào khớp với bộ lọc.</td></tr>';
      }
      return;
    }

    let html = '';
    filtered.forEach(c => {
      html += `
        <tr>
          <td><code style="color: #a5b4fc;">${c.id}</code></td>
          <td><span class="tag-badge tag-day">Day ${c.day}</span></td>
          <td style="font-weight: 700; color: #fff; font-size: 0.95rem;">${c.word}</td>
          <td style="color: #38bdf8; font-family: monospace;">${c.phonetics || '-'}</td>
          <td><span class="tag-badge tag-pos">${c.pos || '-'}</span></td>
          <td style="color: #e2e8f0;">${c.meaning}</td>
          <td style="color: #94a3b8; font-size: 0.82rem;">${c.collocation || '-'}</td>
          <td>
            <div class="action-btns">
              <button class="btn-icon-sm" title="Sửa từ vựng" onclick="window.adminEditCard('${c.id}')">✏️</button>
              <button class="btn-icon-sm delete" title="Xóa từ vựng" onclick="window.adminDeleteCard('${c.id}')">🗑️</button>
            </div>
          </td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  }

  // ==========================================
  // STUDENTS TABLE RENDERING
  // ==========================================
  function renderStudentsTable() {
    const tbody = document.getElementById('students-table-body');
    if (allStudents.length === 0) {
      tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 30px; color: #94a3b8;">Chưa có học viên nào đăng ký tài khoản.</td></tr>';
      return;
    }

    let html = '';
    allStudents.forEach(s => {
      const isCurAdmin = s.id === currentAdmin.id;
      const isAdminRole = s.role === 'admin';
      const stats = s.stats || { total: 0, box1: 0, box2: 0, box3: 0, box4: 0, box5: 0 };
      const intermediateBoxes = (stats.box2 || 0) + (stats.box3 || 0) + (stats.box4 || 0);

      const dateStr = s.created_at ? new Date(s.created_at).toLocaleDateString('vi-VN') : '-';

      html += `
        <tr>
          <td style="font-weight: 600; color: #fff;">${s.full_name || 'Học viên'}</td>
          <td style="color: #94a3b8;">${s.email}</td>
          <td style="font-size: 0.82rem; color: #64748b;">${dateStr}</td>
          <td>
            <span class="tag-badge ${isAdminRole ? 'tag-role-admin' : 'tag-role-student'}">
              ${isAdminRole ? 'ADMIN' : 'HỌC VIÊN'}
            </span>
          </td>
          <td style="font-weight: 700; color: #38bdf8;">${stats.total || 0} từ</td>
          <td style="color: #f97316; font-weight: 600;">${stats.box1 || 0}</td>
          <td style="color: #c084fc;">${intermediateBoxes}</td>
          <td style="color: #34d399; font-weight: 700;">${stats.box5 || 0}</td>
          <td style="text-align: right; white-space: nowrap;">
            <button class="btn-primary" style="padding: 5px 12px; font-size: 0.78rem; margin-right: 6px;" onclick="window.adminViewStudentDetail('${s.id}')">
              👁️ Xem bài làm
            </button>
            ${isCurAdmin ? '<span style="font-size: 0.78rem; color: #34d399; font-weight: 700;">(Quản Trị Viên)</span>' : `
              <button class="btn-icon-sm delete" title="Xóa học viên này" style="display: inline-flex; vertical-align: middle;" onclick="window.adminDeleteStudent('${s.id}')">
                🗑️
              </button>
            `}
          </td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  }

  // Xóa học viên
  window.adminDeleteStudent = async function (studentId) {
    const student = allStudents.find(s => s.id === studentId);
    const name = student?.full_name || student?.email || 'học viên này';
    if (!confirm(`Bạn có chắc chắn muốn xóa học viên "${name}"?\nToàn bộ tài khoản và tiến độ học tập của học viên sẽ bị xóa.`)) {
      return;
    }

    try {
      await window.SupabaseService.adminDeleteStudent(studentId);
      alert(`Đã xóa thành công học viên: ${name}`);
      await loadStudents();
      updateQuickStats();
    } catch (err) {
      console.error('Lỗi khi xóa học viên:', err);
      alert('Không thể xóa học viên: ' + err.message);
    }
  };

  // ==========================================
  // STUDENT DETAIL REPORT MODAL & BOX MANAGEMENT
  // ==========================================
  function getCardMeta(cardId) {
    const dataList = window.GS12_50_DAYS_DATA || window.IELTS_50_DAYS_DATA;
    if (dataList) {
      for (const d of dataList) {
        if (d.vocab) {
          const v = d.vocab.find(item => item.id === cardId);
          if (v) return { ...v, day: d.day, unit: d.unit };
        }
      }
    }
    const fromAll = allVocabCards.find(c => c.id === cardId);
    if (fromAll) return fromAll;
    return { word: cardId, meaning: '' };
  }

  window.adminChangeCardBox = async function (studentId, cardId, newLevel) {
    try {
      await window.SupabaseService.adminUpdateStudentCardLevel(studentId, cardId, newLevel);
      await window.adminViewStudentDetail(studentId);
      loadStudents();
    } catch (err) {
      console.error('Lỗi đổi hộp:', err);
      alert('Không thể đổi hộp: ' + err.message);
    }
  };

  // CHUẨN HÓA HỘP LEITNER SRS CHO MỘT HỌC VIÊN
  window.adminCalibrateSingleStudent = async function (studentId) {
    const student = allStudents.find(s => s.id === studentId);
    const defaultDate = student?.start_date ? student.start_date.split('T')[0] : (student?.created_at ? student.created_at.split('T')[0] : '2026-09-10');
    
    const inputDate = prompt(`Nhập ngày bắt đầu học của học viên "${student?.full_name || student?.email}" (định dạng YYYY-MM-DD):`, defaultDate);
    if (!inputDate) return;

    if (isNaN(new Date(inputDate).getTime())) {
      alert('Định dạng ngày không hợp lệ! Vui lòng nhập theo định dạng YYYY-MM-DD (VD: 2026-09-10).');
      return;
    }

    try {
      const count = await window.SupabaseService.adminCalibrateStudentCards(studentId, inputDate);
      alert(`Đã chuẩn hóa thành công ${count} thẻ từ vựng đúng chuẩn Hộp SRS (tính cả buổi học hôm nay) theo ngày bắt đầu ${inputDate}!\n- Từ học hôm nay: Đã hoàn thành và chuyển vào Hộp 2\n- Các mốc ôn tập đến hạn hôm nay: Đã hoàn thành và thăng cấp sang Hộp tiếp theo (VD: học 12/09 ➔ đến 15/09 đã lên Hộp 3)`);
      await window.adminViewStudentDetail(studentId);
      loadStudents();
    } catch (err) {
      console.error('Lỗi chuẩn hóa:', err);
      alert('Lỗi chuẩn hóa hộp học viên: ' + err.message);
    }
  };

  window.adminEnrollAllForStudent = async function (studentId) {
    if (!confirm('Bạn có chắc chắn muốn kích hoạt toàn bộ 50 ngày từ vựng Global Success 12 vào Hộp 1 Ngày cho học viên này?')) return;
    try {
      await window.SupabaseService.adminEnrollAllDaysForStudent(studentId);
      alert('Đã kích hoạt toàn bộ 50 ngày học cho học viên thành công!');
      await window.adminViewStudentDetail(studentId);
      loadStudents();
    } catch (err) {
      alert('Lỗi kích hoạt 50 ngày: ' + err.message);
    }
  };

  window.adminResetStudentProgress = async function (studentId) {
    if (!confirm('CẢNH BÁO: Hành động này sẽ xóa toàn bộ lịch sử ôn tập của học viên này để làm lại từ đầu. Bạn có chắc không?')) return;
    try {
      await window.SupabaseService.adminResetStudentProgress(studentId);
      alert('Đã đặt lại tiến độ học tập cho học viên!');
      await window.adminViewStudentDetail(studentId);
      loadStudents();
    } catch (err) {
      alert('Lỗi đặt lại tiến độ: ' + err.message);
    }
  };

  window.adminExportStudentData = async function (studentId) {
    const student = allStudents.find(s => s.id === studentId);
    try {
      const cards = await window.SupabaseService.adminGetStudentCards(studentId);
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
        student: student,
        exportDate: new Date().toISOString(),
        cards: cards
      }, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `gs12_progress_${student?.email || studentId}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    } catch (err) {
      alert('Lỗi xuất dữ liệu: ' + err.message);
    }
  };

  window.adminImportStudentData = function (studentId, file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async function (e) {
      try {
        const json = JSON.parse(e.target.result);
        const cardsToImport = json.cards || (Array.isArray(json) ? json : null);
        if (!cardsToImport || !Array.isArray(cardsToImport)) {
          alert('Tệp JSON không hợp lệ.');
          return;
        }
        await window.SupabaseService.saveBulkCardsProgress(studentId, cardsToImport);
        alert(`Đã khôi phục thành công ${cardsToImport.length} thẻ cho học viên!`);
        await window.adminViewStudentDetail(studentId);
        loadStudents();
      } catch (err) {
        alert('Lỗi đọc tệp sao lưu: ' + err.message);
      }
    };
    reader.readAsText(file);
  };

  window.adminViewStudentDetail = async function (studentId) {
    const student = allStudents.find(s => s.id === studentId);
    if (!student) return;

    const modal = document.getElementById('student-detail-modal');
    document.getElementById('student-modal-name').innerText = `Bài Làm & Tiến Độ: ${student.full_name || 'Học viên'}`;
    const startStr = student.start_date 
      ? new Date(student.start_date).toLocaleDateString('vi-VN') 
      : (student.created_at ? new Date(student.created_at).toLocaleDateString('vi-VN') : '10/09/2026');
    document.getElementById('student-modal-email').innerText = `Email: ${student.email} • Ngày bắt đầu: ${startStr} • Ngày tham gia: ${new Date(student.created_at).toLocaleDateString('vi-VN')}`;

    const body = document.getElementById('student-detail-body');
    body.innerHTML = '<div style="text-align: center; padding: 40px; color: #94a3b8;">⏳ Đang tải toàn bộ bài làm của học viên từ đám mây...</div>';
    modal.classList.add('active');

    try {
      const cards = await window.SupabaseService.adminGetStudentCards(studentId);
      
      const actionBarHtml = `
        <div class="student-action-bar">
          <span style="font-size: 0.8rem; font-weight: 700; color: #cbd5e1; margin-right: 4px;">🛠️ Quản Trị Viên:</span>
          <button class="btn-primary" style="font-size: 0.78rem; padding: 6px 14px; background: linear-gradient(135deg, #0284c7, #0ea5e9); border: none; font-weight: 700;" onclick="window.adminCalibrateSingleStudent('${studentId}')">
            🎯 Chuẩn Hóa Hộp SRS (Hộp 1 ➔ 5)
          </button>
          <button class="btn-secondary" style="font-size: 0.78rem; padding: 6px 12px;" onclick="window.adminEnrollAllForStudent('${studentId}')">
            🚀 Kích hoạt 50 ngày
          </button>
          <button class="btn-secondary" style="font-size: 0.78rem; padding: 6px 12px;" onclick="window.adminExportStudentData('${studentId}')">
            📥 Xuất JSON bài làm
          </button>
          <button class="btn-secondary" style="font-size: 0.78rem; padding: 6px 12px;" onclick="document.getElementById('admin-import-file-${studentId}')?.click()">
            📤 Khôi phục JSON
          </button>
          <input type="file" id="admin-import-file-${studentId}" accept=".json" style="display: none;" onchange="window.adminImportStudentData('${studentId}', this.files[0])">
          <button class="btn-secondary" style="font-size: 0.78rem; padding: 6px 12px; color: #f87171; border-color: rgba(248,113,113,0.3);" onclick="window.adminResetStudentProgress('${studentId}')">
            ⚠️ Đặt lại tiến độ
          </button>
        </div>
      `;

      if (!cards || cards.length === 0) {
        body.innerHTML = actionBarHtml + `
          <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">📭</div>
            <h4 style="color: #f8fafc; margin-bottom: 6px;">Học viên này chưa nạp bài học nào</h4>
            <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 16px;">Bạn có thể kích hoạt nhanh 50 ngày hoặc đợi học viên tự học theo lộ trình.</p>
            <button class="btn-primary" onclick="window.adminEnrollAllForStudent('${studentId}')">🚀 Kích hoạt 50 ngày cho học viên này ngay</button>
          </div>
        `;
        return;
      }

      // Nhóm từ theo Ngày học
      const dayMap = {};
      let totalMastered = 0;
      let totalLearning = 0;
      let totalStruggling = 0;

      cards.forEach(c => {
        const meta = getCardMeta(c.card_id);
        const day = meta.day || 1;
        if (!dayMap[day]) dayMap[day] = [];
        dayMap[day].push({ ...c, meta });

        if (c.level === 5) totalMastered++;
        else if (c.level === 1) totalStruggling++;
        else totalLearning++;
      });

      const learnedDays = Object.keys(dayMap).sort((a, b) => Number(a) - Number(b));

      let html = actionBarHtml + `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-bottom: 24px;">
          <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 14px; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.6rem; font-weight: 800; color: #38bdf8;">${learnedDays.length}/50</div>
            <div style="font-size: 0.78rem; color: #94a3b8;">Số ngày đã học</div>
          </div>
          <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 14px; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.6rem; font-weight: 800; color: #f97316;">${totalStruggling}</div>
            <div style="font-size: 0.78rem; color: #94a3b8;">Từ hay quên (Hộp 1)</div>
          </div>
          <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 14px; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.6rem; font-weight: 800; color: #818cf8;">${totalLearning}</div>
            <div style="font-size: 0.78rem; color: #94a3b8;">Đang củng cố (Hộp 2-4)</div>
          </div>
          <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 14px; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.6rem; font-weight: 800; color: #34d399;">${totalMastered}</div>
            <div style="font-size: 0.78rem; color: #94a3b8;">Đã thuộc làu (Hộp 5)</div>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
          <h4 style="color: #f8fafc; font-size: 0.95rem; margin: 0;">Chi tiết thẻ từ vựng & Điều chỉnh Hộp:</h4>
          <span style="font-size: 0.78rem; color: #a5b4fc;">💡 Bạn có thể đổi trực tiếp Hộp cho bất kỳ từ nào bên dưới</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 14px; max-height: 52vh; overflow-y: auto; padding-right: 6px;">
      `;

      learnedDays.forEach(day => {
        const dayCards = dayMap[day];
        html += `
          <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 8px;">
              <span style="font-weight: 800; color: #a5b4fc; font-size: 0.9rem;">📅 Ngày Học ${day}</span>
              <span style="font-size: 0.78rem; color: #94a3b8;">Đã nạp ${dayCards.length} từ</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px;">
        `;

        dayCards.forEach(c => {
          const boxColors = {
            1: '#f97316',
            2: '#38bdf8',
            3: '#818cf8',
            4: '#c084fc',
            5: '#34d399'
          };
          const lastDate = c.last_reviewed ? new Date(c.last_reviewed).toLocaleDateString('vi-VN') : '-';
          const nextDate = c.next_review_date ? new Date(c.next_review_date).toLocaleDateString('vi-VN') : '-';

          html += `
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 10px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 700; color: #fff; font-size: 0.92rem;">${c.meta.word || c.card_id}</span>
                <select class="admin-box-select" onchange="window.adminChangeCardBox('${studentId}', '${c.card_id}', this.value)" style="border-color: ${boxColors[c.level]}; color: ${boxColors[c.level]};">
                  <option value="1" ${c.level === 1 ? 'selected' : ''}>Hộp 1 (1d)</option>
                  <option value="2" ${c.level === 2 ? 'selected' : ''}>Hộp 2 (3d)</option>
                  <option value="3" ${c.level === 3 ? 'selected' : ''}>Hộp 3 (7d)</option>
                  <option value="4" ${c.level === 4 ? 'selected' : ''}>Hộp 4 (14d)</option>
                  <option value="5" ${c.level === 5 ? 'selected' : ''}>Hộp 5 (Master)</option>
                </select>
              </div>
              <div style="font-size: 0.78rem; color: #94a3b8; margin-bottom: 6px;">${c.meta.meaning || ''}</div>
              <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748b;">
                <span>Ôn lần cuối: ${lastDate}</span>
                <span>Lịch tới: ${nextDate}</span>
              </div>
            </div>
          `;
        });

        html += `
            </div>
          </div>
        `;
      });

      html += `</div>`;
      body.innerHTML = html;

    } catch (err) {
      body.innerHTML = `<div style="text-align: center; padding: 30px; color: #f87171;">Lỗi khi tải chi tiết bài làm: ${err.message}</div>`;
    }
  };

  // CHUẨN HÓA HỘP SRS CHO TOÀN BỘ HỌC VIÊN THEO NGÀY ĐĂNG KÝ LẦN ĐẦU
  async function handleCalibrateAllStudents() {
    const confirmMsg = `⚡ CHUẨN HÓA HỘP SRS CHO TẤT CẢ HỌC VIÊN (TÍNH CẢ HÔM NAY):\n\n` +
      `- Ngày bắt đầu học sẽ ĐƯỢC TÍNH TỰ ĐỘNG THEO NGÀY ĐĂNG KÝ của từng học viên!\n` +
      `- Chuẩn hóa tính luôn cả buổi học của ngày hôm nay đã hoàn thành:\n` +
      `  • Từ mới của hôm nay ➔ Nằm ở Hộp 2 (+3 ngày)\n` +
      `  • Thẻ đến hạn ôn hôm nay (VD: học 12/09, đến 15/09) ➔ Thăng cấp lên Hộp 3 (+7 ngày)\n` +
      `  • Thẻ học ngày 10/09, 11/09 ➔ Đang ở Hộp 3\n` +
      `  • Tự động thăng cấp lên Hộp 4, 5 cho các học viên học từ các tuần trước\n\n` +
      `Bạn có muốn hệ thống tự động chuẩn hóa Hộp cho toàn bộ học viên theo ngày đăng ký của từng bạn không?`;

    if (!confirm(confirmMsg)) return;

    const btn = document.getElementById('btn-calibrate-all-students');
    if (btn) {
      btn.disabled = true;
      btn.innerText = '⏳ Đang chuẩn hóa theo ngày đăng ký...';
    }

    try {
      const res = await window.SupabaseService.adminCalibrateAllStudents();
      let summaryStr = `🎉 ĐÃ CHUẨN HÓA HỘP SRS THÀNH CÔNG!\n- Số học viên: ${res.studentCount}\n- Tổng số thẻ đã cập nhật: ${res.cardCount}\n\nChi tiết ngày bắt đầu:\n`;
      if (res.details && res.details.length > 0) {
        summaryStr += res.details.slice(0, 10).map(d => `• ${d.name} (Đăng ký: ${d.registeredAt}): ${d.cards} thẻ`).join('\n');
        if (res.details.length > 10) summaryStr += `\n... và ${res.details.length - 10} học viên khác.`;
      }
      alert(summaryStr);
      await loadStudents();
      updateQuickStats();
    } catch (err) {
      console.error('Lỗi chuẩn hóa toàn bộ:', err);
      alert('Lỗi chuẩn hóa: ' + err.message);
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerText = '⚡ Chuẩn Hóa Hộp SRS Toàn Bộ Học Viên';
      }
    }
  }

  // ==========================================
  // EVENT LISTENERS & ACTIONS
  // ==========================================
  function bindAdminEvents() {
    // Tab switching
    document.querySelectorAll('.admin-nav .nav-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.admin-nav .nav-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const target = tab.getAttribute('data-tab');
        document.getElementById('pane-vocab').style.display = target === 'vocab' ? 'block' : 'none';
        document.getElementById('pane-students').style.display = target === 'students' ? 'block' : 'none';
      });
    });

    // Search and filter
    document.getElementById('vocab-search-input')?.addEventListener('input', renderVocabTable);
    document.getElementById('vocab-day-filter')?.addEventListener('change', renderVocabTable);

    // Chuẩn hóa toàn bộ học viên theo ngày bắt đầu
    document.getElementById('btn-calibrate-all-students')?.addEventListener('click', handleCalibrateAllStudents);

    // Refresh students
    document.getElementById('btn-refresh-students')?.addEventListener('click', () => {
      loadStudents();
    });

    // Sync from data.js
    document.getElementById('btn-sync-from-datajs')?.addEventListener('click', syncAllFromDataJs);

    // Modal Add Vocab
    document.getElementById('btn-open-add-modal')?.addEventListener('click', openAddVocabModal);
    document.getElementById('btn-close-vocab-modal')?.addEventListener('click', closeVocabModal);
    document.getElementById('btn-cancel-vocab-form')?.addEventListener('click', closeVocabModal);

    // Modal Student Detail
    document.getElementById('btn-close-student-modal')?.addEventListener('click', () => {
      document.getElementById('student-detail-modal')?.classList.remove('active');
    });
    document.getElementById('student-detail-modal')?.addEventListener('click', (e) => {
      if (e.target.id === 'student-detail-modal') {
        document.getElementById('student-detail-modal')?.classList.remove('active');
      }
    });

    // Form submit
    document.getElementById('vocab-form')?.addEventListener('submit', handleVocabFormSubmit);

    // Logout
    document.getElementById('btn-admin-logout')?.addEventListener('click', async () => {
      if (confirm('Bạn có chắc chắn muốn đăng xuất tài khoản Quản trị?')) {
        await window.SupabaseService.signOut();
        location.href = 'index.html';
      }
    });
  }

  // ==========================================
  // VOCAB CRUD MODAL & HANDLERS
  // ==========================================
  function openAddVocabModal() {
    document.getElementById('vocab-modal-title').innerText = 'Thêm Từ Vựng Mới';
    document.getElementById('vocab-form-is-edit').value = '0';
    document.getElementById('form-card-id').readOnly = false;
    document.getElementById('vocab-form').reset();
    const modal = document.getElementById('vocab-modal');
    if (modal) modal.classList.add('active');
  }

  function closeVocabModal() {
    const modal = document.getElementById('vocab-modal');
    if (modal) modal.classList.remove('active');
  }

  window.adminEditCard = function (cardId) {
    const card = allVocabCards.find(c => c.id === cardId);
    if (!card) return;

    document.getElementById('vocab-modal-title').innerText = `Chỉnh Sửa Từ Vựng: ${card.word}`;
    document.getElementById('vocab-form-is-edit').value = '1';

    document.getElementById('form-card-id').value = card.id;
    document.getElementById('form-card-id').readOnly = true; // Không sửa ID khóa chính
    document.getElementById('form-day').value = card.day;
    document.getElementById('form-word').value = card.word;
    document.getElementById('form-phonetics').value = card.phonetics || '';
    document.getElementById('form-pos').value = card.pos || '';
    document.getElementById('form-unit').value = card.unit || '';
    document.getElementById('form-meaning').value = card.meaning || '';
    document.getElementById('form-collocation').value = card.collocation || '';
    document.getElementById('form-example').value = card.example || '';

    const modal = document.getElementById('vocab-modal');
    if (modal) modal.classList.add('active');
  };

  async function handleVocabFormSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById('btn-submit-vocab-form');
    btn.disabled = true;
    btn.innerText = 'Đang lưu...';

    const cardData = {
      id: document.getElementById('form-card-id').value.trim(),
      day: parseInt(document.getElementById('form-day').value, 10),
      word: document.getElementById('form-word').value.trim(),
      phonetics: document.getElementById('form-phonetics').value.trim(),
      pos: document.getElementById('form-pos').value.trim(),
      unit: document.getElementById('form-unit').value.trim(),
      meaning: document.getElementById('form-meaning').value.trim(),
      collocation: document.getElementById('form-collocation').value.trim(),
      example: document.getElementById('form-example').value.trim()
    };

    try {
      await window.SupabaseService.adminSaveVocabCard(cardData);
      closeVocabModal();
      await loadVocabCards();
      updateQuickStats();
      alert('Đã lưu dữ liệu từ vựng thành công lên đám mây!');
    } catch (err) {
      alert('Lỗi lưu từ vựng: ' + err.message);
    } finally {
      btn.disabled = false;
      btn.innerText = 'Lưu Dữ Liệu';
    }
  }

  window.adminDeleteCard = async function (cardId) {
    if (!confirm(`Bạn có chắc chắn muốn xóa từ vựng [${cardId}] khỏi hệ thống?`)) return;
    try {
      await window.SupabaseService.adminDeleteVocabCard(cardId);
      allVocabCards = allVocabCards.filter(c => c.id !== cardId);
      renderVocabTable();
      updateQuickStats();
    } catch (err) {
      alert('Lỗi khi xóa từ vựng: ' + err.message);
    }
  };

  window.adminToggleUserRole = async function (userId, newRole) {
    const roleText = newRole === 'admin' ? 'Quản Trị Viên (Admin)' : 'Học Viên (Student)';
    if (!confirm(`Bạn có chắc chắn muốn chuyển vai trò của người này thành ${roleText}?`)) return;

    try {
      await window.SupabaseService.adminSetUserRole(userId, newRole);
      await loadStudents();
      alert('Đã cập nhật vai trò thành công!');
    } catch (err) {
      alert('Lỗi cập nhật vai trò: ' + err.message);
    }
  };

  async function syncAllFromDataJs() {
    if (!confirm('Bạn có muốn đồng bộ toàn bộ từ vựng Global Success 12 từ file data.js lên Cơ sở dữ liệu Supabase không? Thao tác này sẽ nạp đầy đủ 50 ngày học.')) return;

    const btn = document.getElementById('btn-sync-from-datajs');
    if (btn) {
      btn.disabled = true;
      btn.innerText = '⏳ Đang nạp dữ liệu...';
    }

    try {
      const count = await window.SupabaseService.adminImportAllCardsFromDataJs();
      alert(`Đã nạp thành công ${count} từ vựng lên Cơ sở dữ liệu Supabase!`);
      await loadVocabCards();
      updateQuickStats();
    } catch (err) {
      alert('Lỗi đồng bộ dữ liệu: ' + err.message);
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerText = '⚡ Đồng bộ từ vựng GS12 từ data.js';
      }
    }
  }

  // Khởi động
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAdmin);
  } else {
    initAdmin();
  }
})();
