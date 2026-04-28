CREATE DATABASE IF NOT EXISTS hackforge;
USE hackforge;

-- ─────────────────────────────────────────
-- TABLES
-- ─────────────────────────────────────────

CREATE TABLE hackathons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    theme VARCHAR(255),
    description TEXT,
    venue VARCHAR(255),
    mode ENUM('online', 'offline', 'hybrid') DEFAULT 'offline',
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    max_teams INT DEFAULT 50,
    registration_deadline DATETIME,
    status ENUM('upcoming', 'ongoing', 'completed') DEFAULT 'upcoming',
    prize_pool DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hackathon_id INT NOT NULL,
    team_name VARCHAR(255) NOT NULL,
    college VARCHAR(255),
    project_idea TEXT,
    status ENUM('registered', 'submitted', 'disqualified', 'winner') DEFAULT 'registered',
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hackathon_id) REFERENCES hackathons(id) ON DELETE CASCADE
);

CREATE TABLE participants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    college VARCHAR(255),
    year_of_study INT,
    role ENUM('leader', 'member') DEFAULT 'member',
    github_profile VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
);

CREATE TABLE mentors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    expertise VARCHAR(255),
    organization VARCHAR(255),
    availability ENUM('available', 'busy') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mentor_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mentor_id INT NOT NULL,
    team_id INT NOT NULL,
    hackathon_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mentor_id) REFERENCES mentors(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (hackathon_id) REFERENCES hackathons(id) ON DELETE CASCADE
);

CREATE TABLE judges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    organization VARCHAR(255),
    domain VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE judging_criteria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hackathon_id INT NOT NULL,
    criterion_name VARCHAR(255) NOT NULL,
    description TEXT,
    max_score INT NOT NULL DEFAULT 10,
    weightage DECIMAL(5,2) NOT NULL DEFAULT 1.00,
    FOREIGN KEY (hackathon_id) REFERENCES hackathons(id) ON DELETE CASCADE
);

CREATE TABLE scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    judge_id INT NOT NULL,
    criterion_id INT NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    remarks TEXT,
    scored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (judge_id) REFERENCES judges(id) ON DELETE CASCADE,
    FOREIGN KEY (criterion_id) REFERENCES judging_criteria(id) ON DELETE CASCADE,
    UNIQUE KEY unique_score (team_id, judge_id, criterion_id)
);

CREATE TABLE submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL UNIQUE,
    hackathon_id INT NOT NULL,
    project_title VARCHAR(255) NOT NULL,
    description TEXT,
    github_url VARCHAR(500),
    demo_url VARCHAR(500),
    tech_stack VARCHAR(500),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (hackathon_id) REFERENCES hackathons(id) ON DELETE CASCADE
);

CREATE TABLE announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hackathon_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hackathon_id) REFERENCES hackathons(id) ON DELETE CASCADE
);

-- ─────────────────────────────────────────
-- VIEWS
-- ─────────────────────────────────────────

CREATE VIEW leaderboard AS
SELECT
    t.id AS team_id,
    t.team_name,
    t.college,
    t.hackathon_id,
    h.name AS hackathon_name,
    ROUND(SUM(s.score * jc.weightage), 2) AS weighted_score,
    COUNT(DISTINCT s.judge_id) AS judges_count,
    RANK() OVER (PARTITION BY t.hackathon_id ORDER BY SUM(s.score * jc.weightage) DESC) AS team_rank
FROM teams t
JOIN scores s ON s.team_id = t.id
JOIN judging_criteria jc ON jc.id = s.criterion_id
JOIN hackathons h ON h.id = t.hackathon_id
GROUP BY t.id, t.team_name, t.college, t.hackathon_id, h.name;

CREATE VIEW college_analytics AS
SELECT
    t.college,
    t.hackathon_id,
    h.name AS hackathon_name,
    COUNT(DISTINCT t.id) AS total_teams,
    COUNT(DISTINCT p.id) AS total_participants,
    ROUND(AVG(sub_scores.weighted_score), 2) AS avg_score,
    MAX(sub_scores.weighted_score) AS best_score
FROM teams t
JOIN hackathons h ON h.id = t.hackathon_id
LEFT JOIN participants p ON p.team_id = t.id
LEFT JOIN (
    SELECT s.team_id, SUM(s.score * jc.weightage) AS weighted_score
    FROM scores s
    JOIN judging_criteria jc ON jc.id = s.criterion_id
    GROUP BY s.team_id
) sub_scores ON sub_scores.team_id = t.id
GROUP BY t.college, t.hackathon_id, h.name;

CREATE VIEW submission_status AS
SELECT
    t.id AS team_id,
    t.team_name,
    t.hackathon_id,
    t.status AS team_status,
    CASE WHEN sub.id IS NOT NULL THEN 'submitted' ELSE 'pending' END AS submission_status,
    sub.project_title,
    sub.github_url,
    sub.submitted_at
FROM teams t
LEFT JOIN submissions sub ON sub.team_id = t.id;

-- ─────────────────────────────────────────
-- TRIGGERS
-- ─────────────────────────────────────────

DELIMITER $$

CREATE TRIGGER after_submission_insert
AFTER INSERT ON submissions
FOR EACH ROW
BEGIN
    UPDATE teams SET status = 'submitted' WHERE id = NEW.team_id;
END$$

CREATE TRIGGER prevent_score_overflow
BEFORE INSERT ON scores
FOR EACH ROW
BEGIN
    DECLARE max_allowed INT;
    SELECT max_score INTO max_allowed FROM judging_criteria WHERE id = NEW.criterion_id;
    IF NEW.score > max_allowed THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Score exceeds maximum allowed for this criterion';
    END IF;
END$$

CREATE TRIGGER after_hackathon_end
BEFORE UPDATE ON hackathons
FOR EACH ROW
BEGIN
    IF NEW.end_date < NOW() AND OLD.status != 'completed' THEN
        SET NEW.status = 'completed';
    END IF;
END$$

-- ─────────────────────────────────────────
-- STORED PROCEDURES
-- ─────────────────────────────────────────

CREATE PROCEDURE GetLeaderboard(IN hack_id INT)
BEGIN
    SELECT
        team_id,
        team_name,
        college,
        weighted_score,
        judges_count,
        team_rank
    FROM leaderboard
    WHERE hackathon_id = hack_id
    ORDER BY team_rank ASC;
END$$

CREATE PROCEDURE GetTeamFullProfile(IN t_id INT)
BEGIN
    SELECT t.*, h.name AS hackathon_name FROM teams t
    JOIN hackathons h ON h.id = t.hackathon_id
    WHERE t.id = t_id;

    SELECT * FROM participants WHERE team_id = t_id;

    SELECT * FROM submissions WHERE team_id = t_id;

    SELECT s.score, s.remarks, jc.criterion_name, jc.max_score, j.name AS judge_name
    FROM scores s
    JOIN judging_criteria jc ON jc.id = s.criterion_id
    JOIN judges j ON j.id = s.judge_id
    WHERE s.team_id = t_id;
END$$

CREATE PROCEDURE AssignMentor(IN m_id INT, IN t_id INT, IN h_id INT)
BEGIN
    DECLARE already_assigned INT;
    SELECT COUNT(*) INTO already_assigned FROM mentor_assignments
    WHERE mentor_id = m_id AND team_id = t_id AND hackathon_id = h_id;

    IF already_assigned = 0 THEN
        INSERT INTO mentor_assignments (mentor_id, team_id, hackathon_id)
        VALUES (m_id, t_id, h_id);
        UPDATE mentors SET availability = 'busy' WHERE id = m_id;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mentor already assigned to this team';
    END IF;
END$$

DELIMITER ;

-- ─────────────────────────────────────────
-- SAMPLE DATA
-- ─────────────────────────────────────────

INSERT INTO hackathons (name, theme, description, venue, mode, start_date, end_date, max_teams, registration_deadline, prize_pool) VALUES
('HackForge 2025', 'AI for Social Good', 'Build AI-powered solutions for real-world problems', 'MIT Pune', 'offline', '2025-03-01 09:00:00', '2025-03-02 18:00:00', 30, '2025-02-25 23:59:59', 50000.00),
('CodeStorm 2025', 'Sustainable Tech', 'Green technology innovation hackathon', 'Online', 'online', '2025-04-10 10:00:00', '2025-04-11 22:00:00', 50, '2025-04-05 23:59:59', 30000.00);

INSERT INTO judges (name, email, organization, domain) VALUES
('Dr. Anita Sharma', 'anita@techcorp.com', 'TechCorp India', 'AI/ML'),
('Mr. Rohan Mehta', 'rohan@startup.io', 'Startup.io', 'Product'),
('Ms. Priya Nair', 'priya@google.com', 'Google', 'Engineering');

INSERT INTO judging_criteria (hackathon_id, criterion_name, description, max_score, weightage) VALUES
(1, 'Innovation', 'How unique and creative is the idea', 10, 1.5),
(1, 'Technical Complexity', 'Depth of technical implementation', 10, 2.0),
(1, 'Impact', 'Real world impact potential', 10, 1.5),
(1, 'Presentation', 'Quality of demo and pitch', 10, 1.0);

INSERT INTO mentors (name, email, expertise, organization) VALUES
('Vikram Singh', 'vikram@mentor.com', 'Machine Learning', 'IIT Bombay'),
('Sneha Kulkarni', 'sneha@mentor.com', 'Web Development', 'Infosys'),
('Arjun Patel', 'arjun@mentor.com', 'DevOps & Cloud', 'AWS');

INSERT INTO teams (hackathon_id, team_name, college, project_idea) VALUES
(1, 'NeuralNinjas', 'MIT Pune', 'AI-powered crop disease detection'),
(1, 'ByteBusters', 'COEP', 'Smart waste management system'),
(1, 'CodeCrafters', 'VIT Pune', 'Accessible education platform for blind students');

INSERT INTO participants (team_id, name, email, phone, college, year_of_study, role) VALUES
(1, 'Aarav Shah', 'aarav@email.com', '9876543210', 'MIT Pune', 3, 'leader'),
(1, 'Riya Desai', 'riya@email.com', '9876543211', 'MIT Pune', 2, 'member'),
(2, 'Karan Joshi', 'karan@email.com', '9876543212', 'COEP', 4, 'leader'),
(2, 'Meera Iyer', 'meera@email.com', '9876543213', 'COEP', 3, 'member'),
(3, 'Dev Malhotra', 'dev@email.com', '9876543214', 'VIT Pune', 2, 'leader');

INSERT INTO submissions (team_id, hackathon_id, project_title, description, github_url, tech_stack) VALUES
(1, 1, 'CropGuard AI', 'CNN-based plant disease detection mobile app', 'https://github.com/neuralninja/cropguard', 'Python, TensorFlow, Flutter'),
(2, 1, 'WasteWise', 'IoT + ML smart bin routing system', 'https://github.com/bytebusters/wastewise', 'Node.js, Python, Arduino'),
(3, 1, 'EduSense', 'Screen reader + AI tutor for visually impaired', 'https://github.com/codecrafters/edusense', 'React, FastAPI, OpenAI');

INSERT INTO scores (team_id, judge_id, criterion_id, score) VALUES
(1, 1, 1, 9), (1, 1, 2, 8), (1, 1, 3, 9), (1, 1, 4, 8),
(2, 2, 1, 7), (2, 2, 2, 9), (2, 2, 3, 8), (2, 2, 4, 7),
(3, 3, 1, 8), (3, 3, 2, 7), (3, 3, 3, 9), (3, 3, 4, 9);