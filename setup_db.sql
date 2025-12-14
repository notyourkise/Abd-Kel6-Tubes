-- ==============================================================
-- BAGIAN 1: FORCE RESET (Mengatasi Error "Accessed by other users")
-- ==============================================================
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'student_performance_db'
AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS student_performance_db;
CREATE DATABASE student_performance_db;

-- PENTING: Koneksi ulang ke database baru
\c student_performance_db

-- ==============================================================
-- BAGIAN 2: STRUKTUR TABEL BARU (8 TABEL RELATIONAL FIX)
-- ==============================================================

-- 1. Tabel Master Services
CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    service_type VARCHAR(50)
);

-- 2. Tabel Master Activities
CREATE TABLE activities (
    activity_id SERIAL PRIMARY KEY,
    activity_type VARCHAR(100) NOT NULL
);

-- 3. Tabel Utama Student (Hanya Data Diri)
CREATE TABLE student (
    id_student SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    grade_level VARCHAR(20),
    race_ethnicity VARCHAR(50),
    date_of_birth DATE
);

-- 4. Tabel Parent Background
CREATE TABLE parent_background (
    parent_id SERIAL PRIMARY KEY,
    id_student INT NOT NULL,
    parent_type VARCHAR(20), -- Father/Mother/Guardian
    parent_occupation VARCHAR(100),
    parental_level_of_education VARCHAR(100),
    FOREIGN KEY (id_student) REFERENCES student(id_student) ON DELETE CASCADE
);

-- 5. Tabel Exam Scores
CREATE TABLE exam_scores (
    score_id SERIAL PRIMARY KEY,
    id_student INT NOT NULL,
    math_score INT,
    reading_score INT,
    writing_score INT,
    FOREIGN KEY (id_student) REFERENCES student(id_student) ON DELETE CASCADE
);

-- 6. Tabel Study Habits
CREATE TABLE study_habits (
    study_habits_id SERIAL PRIMARY KEY,
    id_student INT NOT NULL,
    study_hours_per_week FLOAT,
    prefers_group_study VARCHAR(5),
    has_private_tutor VARCHAR(5),
    FOREIGN KEY (id_student) REFERENCES student(id_student) ON DELETE CASCADE
);

-- 7. Tabel Student Services (Makan Siang & Kursus)
CREATE TABLE student_services (
    student_service_id SERIAL PRIMARY KEY,
    id_student INT NOT NULL,
    service_id INT NOT NULL,
    service_status VARCHAR(50),
    FOREIGN KEY (id_student) REFERENCES student(id_student) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE
);

-- 8. Tabel Student Activities
CREATE TABLE student_activities (
    sa_id SERIAL PRIMARY KEY,
    id_student INT NOT NULL,
    activity_id INT NOT NULL,
    hours_per_week INT,
    FOREIGN KEY (id_student) REFERENCES student(id_student) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(activity_id) ON DELETE CASCADE
);

-- ==============================================================
-- BAGIAN 3: INPUT DATA (Disesuaikan dengan Struktur Baru)
-- ==============================================================

-- A. Insert Master Data (Services & Activities)
INSERT INTO services (service_name, service_type) VALUES 
('Lunch Program', 'Facility'),          -- ID 1
('Test Preparation Course', 'Academic'); -- ID 2

INSERT INTO activities (activity_type) VALUES 
('Sports'), ('Arts'), ('Music'), ('Debate'), ('Science Club');

-- B. Insert Data Siswa (Saya ambil sampel dari data lama Anda)
INSERT INTO student (name, gender, race_ethnicity, grade_level, date_of_birth) VALUES
('Ahmad Rahman', 'Male', 'Indonesian', '12', '2006-05-15'),
('Budi Santoso', 'Male', 'Indonesian', '11', '2007-08-20'),
('Citra Dewi', 'Female', 'Indonesian', '12', '2006-01-10'),
('Dani Hermawan', 'Male', 'Indonesian', '10', '2008-03-12'),
('Eka Putri', 'Female', 'Indonesian', '11', '2007-11-05'),
('Fajar Wijaya', 'Male', 'Indonesian', '12', '2006-02-14'),
('Gina Sutrisno', 'Female', 'Indonesian', '10', '2008-06-20'),
('Hendra Kusuma', 'Male', 'Indonesian', '11', '2007-09-01'),
('Ira Mahendra', 'Female', 'Indonesian', '12', '2006-12-12'),
('Joko Suryanto', 'Male', 'Indonesian', '10', '2008-01-30');
-- (Anda bisa tambahkan sisa nama lainnya di sini)

-- C. Insert Exam Scores (Generate Random tapi Realistis)
INSERT INTO exam_scores (id_student, math_score, reading_score, writing_score)
SELECT id_student, 
       FLOOR(RANDOM() * 40 + 60), -- Nilai 60-100
       FLOOR(RANDOM() * 40 + 60),
       FLOOR(RANDOM() * 40 + 60)
FROM student;

-- D. Insert Parent Background (Generate Random)
INSERT INTO parent_background (id_student, parent_type, parent_occupation, parental_level_of_education)
SELECT id_student,
       CASE WHEN random() < 0.5 THEN 'Father' ELSE 'Mother' END,
       CASE WHEN random() < 0.3 THEN 'Teacher' WHEN random() < 0.6 THEN 'Private Sector' ELSE 'Government' END,
       CASE WHEN random() < 0.3 THEN 'High School' WHEN random() < 0.7 THEN 'Bachelor' ELSE 'Master' END
FROM student;

-- E. Insert Study Habits (Generate Random)
INSERT INTO study_habits (id_student, study_hours_per_week, prefers_group_study, has_private_tutor)
SELECT id_student,
       FLOOR(RANDOM() * 15 + 2),
       CASE WHEN random() < 0.5 THEN 'Yes' ELSE 'No' END,
       CASE WHEN random() < 0.3 THEN 'Yes' ELSE 'No' END
FROM student;

-- F. Insert Student Services (Logika Lunch & Prep Course)
-- 1. Lunch Program (Semua siswa terdaftar, statusnya beda2)
INSERT INTO student_services (id_student, service_id, service_status)
SELECT id_student, 1, -- ID 1 = Lunch Program
       CASE WHEN random() < 0.4 THEN 'Free/Reduced' ELSE 'Standard' END
FROM student;

-- 2. Test Prep (Hanya sebagian siswa)
INSERT INTO student_services (id_student, service_id, service_status)
SELECT id_student, 2, 'Completed' -- ID 2 = Test Prep
FROM student
WHERE random() < 0.3; 

-- G. Insert Activities (Acak)
INSERT INTO student_activities (id_student, activity_id, hours_per_week)
SELECT s.id_student, a.activity_id, FLOOR(RANDOM() * 10 + 1)
FROM student s
CROSS JOIN activities a
WHERE random() < 0.2; -- Peluang 20% per ekskul

-- ==============================================================
-- CEK HASIL (Jalankan ini untuk memastikan)
-- ==============================================================
SELECT * FROM student LIMIT 5;
SELECT * FROM exam_scores LIMIT 5;