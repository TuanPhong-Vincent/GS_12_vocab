-- ==============================================================================
-- GLOBAL SUCCESS 12 VOCAB CHALLENGE - DATABASE SCHEMA CHO SUPABASE (PHIÊN BẢN CHUẨN ĐÃ TỐI ƯU)
-- Chạy toàn bộ mã này trong mục SQL Editor trên Dashboard Supabase của bạn.
-- ==============================================================================

-- 1. BẢNG HỒ SƠ NGƯỜI DÙNG (PROFILES)
create table if not exists public.profiles (
  id uuid references auth.users on delete cascade primary key,
  email text,
  full_name text,
  role text default 'student' check (role in ('student', 'admin')),
  start_date timestamp with time zone default timezone('utc'::text, now()),
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Tự động thêm cột start_date nếu bảng profiles đã tồn tại từ trước
alter table public.profiles add column if not exists start_date timestamp with time zone default timezone('utc'::text, now());

-- Hàm tự động tạo profile khi người dùng đăng ký qua auth.users
-- Chỉ cấp quyền ADMIN duy nhất cho thaituanphong12a1@gmail.com, tất cả email khác là student
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email, full_name, role, start_date)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1)),
    case 
      when lower(trim(new.email)) = 'thaituanphong12a1@gmail.com' then 'admin' 
      else 'student' 
    end,
    coalesce((new.raw_user_meta_data->>'start_date')::timestamptz, timezone('utc'::text, now()))
  )
  on conflict (id) do update set
    email = excluded.email,
    full_name = coalesce(excluded.full_name, profiles.full_name),
    start_date = coalesce(profiles.start_date, excluded.start_date),
    role = case 
      when lower(trim(excluded.email)) = 'thaituanphong12a1@gmail.com' then 'admin' 
      else profiles.role 
    end;
  return new;
end;
$$ language plpgsql security definer;

-- Trigger kích hoạt sau khi đăng ký tài khoản mới
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- 2. BẢNG LƯU TRỮ KHO TỪ VỰNG (VOCABULARY CARDS)
create table if not exists public.vocab_cards (
  id text primary key,
  day integer not null,
  module text,
  unit text,
  subtopic text,
  word text not null,
  phonetics text,
  pos text,
  meaning text not null,
  collocation text,
  example text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. BẢNG TIẾN ĐỘ HỌC TẬP CỦA HỌC VIÊN (USER PROGRESS)
create table if not exists public.user_progress (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  card_id text not null,
  level integer default 1 check (level between 1 and 5),
  streak integer default 0,
  next_review_date timestamp with time zone not null,
  last_reviewed timestamp with time zone default timezone('utc'::text, now()),
  unique(user_id, card_id)
);

-- 4. HÀM KIỂM TRA QUYỀN ADMIN (DÙNG SECURITY DEFINER ĐỂ TRÁNH LỖI ĐỆ QUY RLS)
create or replace function public.is_admin()
returns boolean
language sql
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role = 'admin'
  );
$$;

-- 5. BẬT ROW LEVEL SECURITY (RLS) BẢO VỆ DỮ LIỆU
alter table public.profiles enable row level security;
alter table public.vocab_cards enable row level security;
alter table public.user_progress enable row level security;

-- Xóa sạch các policies cũ để cập nhật policies mới không bị lỗi
drop policy if exists "Hồ sơ công khai hoặc xem cá nhân" on public.profiles;
drop policy if exists "Chỉ Admin hoặc chính chủ được sửa hồ sơ" on public.profiles;
drop policy if exists "Cho phép xem hồ sơ" on public.profiles;
drop policy if exists "Cho phép cập nhật hồ sơ" on public.profiles;
drop policy if exists "Ai cũng được xem từ vựng" on public.vocab_cards;
drop policy if exists "Chỉ Admin được sửa từ vựng" on public.vocab_cards;
drop policy if exists "Học viên chỉ xem và sửa tiến độ của chính mình" on public.user_progress;

-- Policies cho bảng PROFILES:
-- Học viên xem được hồ sơ của mình, Admin xem được danh sách tất cả học viên
create policy "Cho phép xem hồ sơ" on public.profiles
  for select using (
    auth.uid() = id or public.is_admin()
  );

create policy "Cho phép cập nhật hồ sơ" on public.profiles
  for update using (
    auth.uid() = id or public.is_admin()
  );

-- Policies cho bảng VOCAB_CARDS:
-- Tất cả mọi người (kể cả khách) đều được đọc từ vựng
create policy "Ai cũng được xem từ vựng" on public.vocab_cards
  for select using (true);

-- Chỉ tài khoản Admin mới được Thêm/Sửa/Xóa từ vựng
create policy "Chỉ Admin được sửa từ vựng" on public.vocab_cards
  for all using (public.is_admin());

-- Policies cho bảng USER_PROGRESS:
-- Mỗi học viên chỉ đọc/ghi tiến độ của riêng họ; Admin có thể xem được tất cả
create policy "Học viên chỉ xem và sửa tiến độ của chính mình" on public.user_progress
  for all using (
    auth.uid() = user_id or public.is_admin()
  );

-- 6. POLICY VÀ HÀM CHO PHÉP ADMIN XÓA HỌC VIÊN
drop policy if exists "Cho phép Admin xóa hồ sơ học viên" on public.profiles;
create policy "Cho phép Admin xóa hồ sơ học viên" on public.profiles
  for delete using (public.is_admin());

create or replace function public.admin_delete_student(target_user_id uuid)
returns void
language plpgsql
security definer
as $$
begin
  if not public.is_admin() then
    raise exception 'Chỉ Quản Trị Viên mới có quyền xóa học viên.';
  end if;
  -- Xóa tiến độ học tập của học viên
  delete from public.user_progress where user_id = target_user_id;
  -- Xóa hồ sơ học viên
  delete from public.profiles where id = target_user_id;
  -- Xóa tài khoản auth nếu tồn tại
  delete from auth.users where id = target_user_id;
end;
$$;

-- 7. THIẾT LẬP QUYỀN ADMIN ĐỘC QUYỀN:
-- Đặt toàn bộ tài khoản khác về 'student', CHỈ DUY NHẤT thaituanphong12a1@gmail.com là 'admin'
update public.profiles set role = 'student' where lower(trim(email)) != 'thaituanphong12a1@gmail.com';
update public.profiles set role = 'admin' where lower(trim(email)) = 'thaituanphong12a1@gmail.com';

-- 8. THỦ TỤC CHUẨN HÓA HỘP SRS THEO NGÀY ĐĂNG KÝ LẦN ĐẦU CHO HỌC VIÊN
-- Quy tắc Leitner SRS:
--  - Học viên đăng ký ngày nào -> Đó là Ngày 1.
--  - Các ngày trước hôm nay: Thẻ thuộc Day đó được chuyển vào Hộp 2 (level = 2), ôn lại sau 3 ngày kể từ ngày học.
--    Ví dụ: Học viên A đăng ký ngày 10/09 -> Day 1 (10/09) nằm ở Hộp 2 và ôn lại vào ngày 13/09.
--  - Ngày hôm nay: Từ mới của hôm nay nằm ở Hộp 1 (level = 1) để học.

create or replace function public.admin_calibrate_student_srs(target_user_id uuid)
returns integer
language plpgsql
security definer
as $$
declare
  v_start_date date;
  v_today date := current_date;
  v_diff_days integer;
  v_current_day integer;
  v_day integer;
  v_learned_date date;
  v_next_review date;
  v_last_reviewed date;
  v_level integer;
  v_streak integer;
  v_count integer := 0;
  v_card record;
begin
  if not public.is_admin() then
    raise exception 'Chỉ Quản Trị Viên mới có quyền thực hiện thao tác này.';
  end if;

  -- Lấy ngày bắt đầu học từ start_date hoặc created_at (ngày đăng ký lần đầu)
  select coalesce(start_date::date, created_at::date, current_date)
  into v_start_date
  from public.profiles
  where id = target_user_id;

  if v_start_date is null then
    return 0;
  end if;

  v_diff_days := (v_today - v_start_date);
  v_current_day := greatest(1, least(50, v_diff_days + 1));

  -- Duyệt qua từng ngày từ Ngày 1 đến Ngày hiện tại
  for v_day in 1..v_current_day loop
    v_learned_date := v_start_date + (v_day - 1);

    if v_learned_date > v_today then
      -- Ngày ở tương lai (nếu có)
      v_level := 1;
      v_streak := 0;
      v_last_reviewed := v_learned_date;
      v_next_review := v_learned_date;
    else
      -- Tính luôn cả ngày hôm nay: Học xong từ mới -> Lên Hộp 2 (+3 ngày)
      v_level := 2;
      v_streak := 1;
      v_last_reviewed := v_learned_date;
      v_next_review := v_learned_date + 3;

      -- Mốc Hộp 3 (+7 ngày): nếu mốc ôn Hộp 2 <= today (tính cả hôm nay)
      if v_next_review <= v_today then
        v_last_reviewed := v_next_review;
        v_level := 3;
        v_streak := 2;
        v_next_review := v_last_reviewed + 7;

        -- Mốc Hộp 4 (+14 ngày): nếu mốc ôn Hộp 3 <= today
        if v_next_review <= v_today then
          v_last_reviewed := v_next_review;
          v_level := 4;
          v_streak := 3;
          v_next_review := v_last_reviewed + 14;

          -- Mốc Hộp 5 (+30 ngày): nếu mốc ôn Hộp 4 <= today
          if v_next_review <= v_today then
            v_last_reviewed := v_next_review;
            v_level := 5;
            v_streak := 4;
            v_next_review := v_last_reviewed + 30;

            -- Mốc Master (+60 ngày): nếu mốc ôn Hộp 5 <= today
            if v_next_review <= v_today then
              v_last_reviewed := v_next_review;
              v_streak := 5;
              v_next_review := v_last_reviewed + 60;
            end if;
          end if;
        end if;
      end if;
    end if;

    for v_card in select id from public.vocab_cards where day = v_day loop
      insert into public.user_progress (user_id, card_id, level, streak, last_reviewed, next_review_date)
      values (target_user_id, v_card.id, v_level, v_streak, v_last_reviewed::timestamp with time zone, v_next_review::timestamp with time zone)
      on conflict (user_id, card_id) do update set
        level = excluded.level,
        streak = excluded.streak,
        last_reviewed = excluded.last_reviewed,
        next_review_date = excluded.next_review_date;
      v_count := v_count + 1;
    end loop;
  end loop;

  return v_count;
end;
$$;


