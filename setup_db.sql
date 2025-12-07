-- Drop existing database if exists
DROP DATABASE IF EXISTS student_performance_db;

-- Create new database
CREATE DATABASE student_performance_db;

-- Connect to the new database
\c student_performance_db

-- Create student table
CREATE TABLE student (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    ethnicity VARCHAR(50),
    parental_level_of_education VARCHAR(100),
    lunch VARCHAR(50),
    test_preparation_course VARCHAR(50),
    math_score INT,
    reading_score INT,
    writing_score INT
);

-- Create study_habits table
CREATE TABLE study_habits (
    habit_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    study_hours_per_week FLOAT,
    hours_internet FLOAT,
    hours_family_study FLOAT,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

-- Create exam_scores table
CREATE TABLE exam_scores (
    exam_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    math_score INT,
    reading_score INT,
    writing_score INT,
    average_score FLOAT,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

-- Create parent_background table
CREATE TABLE parent_background (
    parent_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    parent_education VARCHAR(100),
    parent_occupation VARCHAR(100),
    parent_income_level VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

-- Create services table
CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    service_type VARCHAR(50)
);

-- Create student_services table (many-to-many)
CREATE TABLE student_services (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    service_id INT NOT NULL,
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE
);

-- Create activities table
CREATE TABLE activities (
    activity_id SERIAL PRIMARY KEY,
    activity_name VARCHAR(100) NOT NULL,
    description TEXT,
    activity_type VARCHAR(50)
);

-- Create student_activities table (many-to-many)
CREATE TABLE student_activities (
    participation_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    activity_id INT NOT NULL,
    participation_date DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(activity_id) ON DELETE CASCADE
);

-- Insert dummy data for students
INSERT INTO student (name, gender, ethnicity, parental_level_of_education, lunch, test_preparation_course, math_score, reading_score, writing_score) VALUES
('Ahmad Rahman', 'male', 'Indonesian', 'high school', 'standard', 'none', 72, 78, 75),
('Budi Santoso', 'male', 'Indonesian', 'some college', 'standard', 'completed', 85, 88, 86),
('Citra Dewi', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 92, 95, 94),
('Dani Hermawan', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 88, 91, 89),
('Eka Putri', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 65, 70, 68),
('Fajar Wijaya', 'male', 'Indonesian', 'high school', 'standard', 'completed', 78, 82, 80),
('Gina Sutrisno', 'female', 'Indonesian', 'some college', 'standard', 'completed', 86, 89, 87),
('Hendra Kusuma', 'male', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 91, 93, 92),
('Ira Mahendra', 'female', 'Indonesian', 'master''s degree', 'standard', 'completed', 95, 97, 96),
('Joko Suryanto', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 68, 72, 70),
('Karina Sari', 'female', 'Indonesian', 'high school', 'standard', 'none', 74, 76, 75),
('Luthfi Rahman', 'male', 'Indonesian', 'some college', 'standard', 'completed', 83, 86, 85),
('Maya Wijaya', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 90, 92, 91),
('Nia Pratama', 'female', 'Indonesian', 'master''s degree', 'standard', 'completed', 94, 96, 95),
('Ongki Hartono', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 66, 71, 69),
('Prita Ayu', 'female', 'Indonesian', 'high school', 'standard', 'completed', 79, 81, 80),
('Rizki Pratama', 'male', 'Indonesian', 'some college', 'standard', 'completed', 84, 87, 86),
('Siti Nurhaliza', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 91, 94, 93),
('Teguh Sutrisno', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 93, 95, 94),
('Umy Nurkhairo', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 67, 72, 70),
('Vina Kurniawan', 'female', 'Indonesian', 'high school', 'standard', 'none', 73, 77, 75),
('Wahid Anggara', 'male', 'Indonesian', 'some college', 'standard', 'completed', 82, 85, 84),
('Xenia Setiawan', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 89, 91, 90),
('Yogi Suryanto', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 92, 94, 93),
('Zara Wijaya', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 68, 73, 71),
('Adam Malik', 'male', 'Indonesian', 'high school', 'standard', 'completed', 76, 79, 78),
('Beta Kusuma', 'female', 'Indonesian', 'some college', 'standard', 'completed', 85, 88, 87),
('Candra Wijaya', 'male', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 88, 90, 89),
('Devi Lestari', 'female', 'Indonesian', 'master''s degree', 'standard', 'completed', 93, 95, 94),
('Eka Saputra', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 64, 69, 67),
('Fira Hartono', 'female', 'Indonesian', 'high school', 'standard', 'none', 75, 78, 76),
('Gandi Rahman', 'male', 'Indonesian', 'some college', 'standard', 'completed', 81, 84, 83),
('Hana Wijaya', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 90, 93, 92),
('Ino Suryanto', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 94, 96, 95),
('Jai Kurniawan', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 69, 74, 72),
('Kima Sari', 'female', 'Indonesian', 'high school', 'standard', 'completed', 77, 80, 79),
('Luna Rahman', 'female', 'Indonesian', 'some college', 'standard', 'completed', 84, 87, 86),
('Marno Wijaya', 'male', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 89, 91, 90),
('Nina Kusuma', 'female', 'Indonesian', 'master''s degree', 'standard', 'completed', 95, 97, 96),
('Oto Hartono', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 70, 75, 73),
('Putri Ayu', 'female', 'Indonesian', 'high school', 'standard', 'none', 78, 81, 79),
('Quirino Wijaya', 'male', 'Indonesian', 'some college', 'standard', 'completed', 83, 86, 85),
('Rania Putri', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 91, 93, 92),
('Santo Rahman', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 92, 94, 93),
('Tami Sari', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 66, 71, 69),
('Ustad Kurniawan', 'male', 'Indonesian', 'high school', 'standard', 'completed', 79, 82, 81),
('Vika Wijaya', 'female', 'Indonesian', 'some college', 'standard', 'completed', 85, 88, 87),
('Wati Kusuma', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 90, 92, 91),
('Xander Hartono', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 93, 95, 94),
('Yani Rahman', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 67, 72, 70),
('Zainal Wijaya', 'male', 'Indonesian', 'high school', 'standard', 'none', 74, 77, 76),
('Aira Kusuma', 'female', 'Indonesian', 'some college', 'standard', 'completed', 82, 85, 84),
('Bonny Sari', 'male', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 88, 90, 89),
('Cika Wijaya', 'female', 'Indonesian', 'master''s degree', 'standard', 'completed', 94, 96, 95),
('Danu Hartono', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 65, 70, 68),
('Eka Wijaya', 'female', 'Indonesian', 'high school', 'standard', 'completed', 76, 79, 78),
('Fito Rahman', 'male', 'Indonesian', 'some college', 'standard', 'completed', 84, 87, 86),
('Gina Kusuma', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 89, 91, 90),
('Hendro Wijaya', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 92, 94, 93),
('Ina Hartono', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 68, 73, 71),
('Jaka Sari', 'male', 'Indonesian', 'high school', 'standard', 'none', 75, 78, 76),
('Kiki Wijaya', 'female', 'Indonesian', 'some college', 'standard', 'completed', 83, 86, 85),
('Lina Rahman', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 90, 92, 91),
('Mugi Kusuma', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 93, 95, 94),
('Nani Hartono', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 69, 74, 72),
('Okta Wijaya', 'male', 'Indonesian', 'high school', 'standard', 'completed', 77, 80, 79),
('Prita Sari', 'female', 'Indonesian', 'some college', 'standard', 'completed', 84, 87, 86),
('Qori Rahman', 'male', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 89, 91, 90),
('Rika Kusuma', 'female', 'Indonesian', 'master''s degree', 'standard', 'completed', 94, 96, 95),
('Sandi Wijaya', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 70, 75, 73),
('Tania Hartono', 'female', 'Indonesian', 'high school', 'standard', 'none', 78, 81, 79),
('Ubay Rahman', 'male', 'Indonesian', 'some college', 'standard', 'completed', 82, 85, 84),
('Vina Kusuma', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 91, 93, 92),
('Wawan Wijaya', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 92, 94, 93),
('Xena Sari', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 66, 71, 69),
('Yusuf Hartono', 'male', 'Indonesian', 'high school', 'standard', 'completed', 79, 82, 81),
('Zahra Kusuma', 'female', 'Indonesian', 'some college', 'standard', 'completed', 85, 88, 87),
('Aryo Wijaya', 'male', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 88, 90, 89),
('Bella Rahman', 'female', 'Indonesian', 'master''s degree', 'standard', 'completed', 93, 95, 94),
('Ciko Hartono', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 67, 72, 70),
('Dina Kusuma', 'female', 'Indonesian', 'high school', 'standard', 'none', 75, 78, 76),
('Erwin Wijaya', 'male', 'Indonesian', 'some college', 'standard', 'completed', 81, 84, 83),
('Fiona Rahman', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 90, 93, 92),
('Gilang Hartono', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 94, 96, 95),
('Hilda Kusuma', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 69, 74, 72),
('Ivan Wijaya', 'male', 'Indonesian', 'high school', 'standard', 'completed', 77, 80, 79),
('Jasmine Rahman', 'female', 'Indonesian', 'some college', 'standard', 'completed', 84, 87, 86),
('Kamal Hartono', 'male', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 89, 91, 90),
('Lila Kusuma', 'female', 'Indonesian', 'master''s degree', 'standard', 'completed', 95, 97, 96),
('Malik Wijaya', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 70, 75, 73),
('Nadia Rahman', 'female', 'Indonesian', 'high school', 'standard', 'none', 78, 81, 79),
('Ozer Hartono', 'male', 'Indonesian', 'some college', 'standard', 'completed', 83, 86, 85),
('Paola Kusuma', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 91, 93, 92),
('Qanto Wijaya', 'male', 'Indonesian', 'master''s degree', 'standard', 'completed', 92, 94, 93),
('Rini Rahman', 'female', 'Indonesian', 'some high school', 'free/reduced', 'none', 66, 71, 69),
('Samson Hartono', 'male', 'Indonesian', 'high school', 'standard', 'completed', 79, 82, 81),
('Tisha Kusuma', 'female', 'Indonesian', 'some college', 'standard', 'completed', 85, 88, 87),
('Usman Wijaya', 'male', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 88, 90, 89),
('Vada Rahman', 'female', 'Indonesian', 'master''s degree', 'standard', 'completed', 93, 95, 94),
('Wisnu Hartono', 'male', 'Indonesian', 'some high school', 'free/reduced', 'none', 68, 73, 71),
('Xiomara Kusuma', 'female', 'Indonesian', 'high school', 'standard', 'none', 74, 77, 75),
('Yanuar Wijaya', 'male', 'Indonesian', 'some college', 'standard', 'completed', 82, 85, 84),
('Zara Rahman', 'female', 'Indonesian', 'bachelor''s degree', 'free/reduced', 'completed', 90, 92, 91);

-- Insert study habits
INSERT INTO study_habits (student_id, study_hours_per_week, hours_internet, hours_family_study) 
SELECT student_id, 
       ROUND((RANDOM() * 20 + 5)::numeric, 1),
       ROUND((RANDOM() * 15 + 2)::numeric, 1),
       ROUND((RANDOM() * 10 + 1)::numeric, 1)
FROM student;

-- Insert exam scores
INSERT INTO exam_scores (student_id, math_score, reading_score, writing_score, average_score)
SELECT student_id, math_score, reading_score, writing_score,
       ROUND((math_score + reading_score + writing_score) / 3.0, 2)
FROM student;

-- Insert parent background
INSERT INTO parent_background (student_id, parent_education, parent_occupation, parent_income_level)
SELECT student_id,
       CASE WHEN random() < 0.3 THEN 'High School' WHEN random() < 0.6 THEN 'Bachelor' ELSE 'Master' END,
       CASE WHEN random() < 0.3 THEN 'Professional' WHEN random() < 0.6 THEN 'Business' ELSE 'Government' END,
       CASE WHEN random() < 0.3 THEN 'Low' WHEN random() < 0.6 THEN 'Medium' ELSE 'High' END
FROM student;

-- Insert duplicate parent background for some students
INSERT INTO parent_background (student_id, parent_education, parent_occupation, parent_income_level)
SELECT student_id,
       CASE WHEN random() < 0.3 THEN 'High School' WHEN random() < 0.6 THEN 'Bachelor' ELSE 'Master' END,
       CASE WHEN random() < 0.3 THEN 'Professional' WHEN random() < 0.6 THEN 'Business' ELSE 'Government' END,
       CASE WHEN random() < 0.3 THEN 'Low' WHEN random() < 0.6 THEN 'Medium' ELSE 'High' END
FROM student WHERE student_id <= 105;

-- Insert services
INSERT INTO services (service_name, description, service_type) VALUES
('Math Tutoring', 'One-on-one mathematics tutoring', 'Academic'),
('Reading Program', 'Structured reading enhancement program', 'Academic'),
('Writing Workshop', 'Creative and analytical writing workshops', 'Academic'),
('Science Lab', 'Hands-on science laboratory sessions', 'Academic'),
('Technology Club', 'Computer and technology learning', 'Technology'),
('Sports Program', 'Physical education and sports training', 'Sports'),
('Music Lessons', 'Individual and group music instruction', 'Arts'),
('Art Classes', 'Visual arts and design classes', 'Arts'),
('Debate Team', 'Public speaking and debate preparation', 'Competition'),
('Chess Club', 'Strategic thinking and chess training', 'Competition');

-- Insert student services (many enrolled in multiple services)
INSERT INTO student_services (student_id, service_id, enrollment_date)
SELECT s.student_id, sv.service_id, CURRENT_DATE - INTERVAL '1 day' * (RANDOM() * 365)::INT
FROM student s
CROSS JOIN (SELECT service_id FROM services ORDER BY RANDOM() LIMIT 2 + (RANDOM() * 3)::INT) sv
ORDER BY RANDOM();

-- Insert activities
INSERT INTO activities (activity_name, description, activity_type) VALUES
('Morning Assembly', 'Daily school assembly and announcements', 'General'),
('Science Fair', 'Annual science exhibition and competition', 'Exhibition'),
('Sports Day', 'Inter-class sports competition', 'Sports'),
('Cultural Festival', 'Celebration of diverse cultures', 'Cultural'),
('Debate Competition', 'Inter-school debate championship', 'Competition'),
('Math Olympiad', 'Mathematics problem-solving competition', 'Academic'),
('Science Quiz Bowl', 'Team-based science quiz competition', 'Academic'),
('Art Exhibition', 'Student artwork display and celebration', 'Cultural'),
('Charity Drive', 'Community service and charity program', 'Community'),
('Technology Expo', 'Technology innovation showcase', 'Technology');

-- Insert student activities (many students participate in multiple activities)
INSERT INTO student_activities (student_id, activity_id, participation_date)
SELECT s.student_id, a.activity_id, CURRENT_DATE - INTERVAL '1 day' * (RANDOM() * 365)::INT
FROM student s
CROSS JOIN (SELECT activity_id FROM activities ORDER BY RANDOM() LIMIT 1 + (RANDOM() * 2)::INT) a
ORDER BY RANDOM();

-- Verify data insertion
SELECT 'student' as table_name, COUNT(*) as record_count FROM student
UNION ALL
SELECT 'study_habits', COUNT(*) FROM study_habits
UNION ALL
SELECT 'exam_scores', COUNT(*) FROM exam_scores
UNION ALL
SELECT 'parent_background', COUNT(*) FROM parent_background
UNION ALL
SELECT 'services', COUNT(*) FROM services
UNION ALL
SELECT 'student_services', COUNT(*) FROM student_services
UNION ALL
SELECT 'activities', COUNT(*) FROM activities
UNION ALL
SELECT 'student_activities', COUNT(*) FROM student_activities;
