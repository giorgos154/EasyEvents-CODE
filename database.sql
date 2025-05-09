USE easyevents;

DROP TABLE IF EXISTS invitations;
DROP TABLE IF EXISTS points;
DROP TABLE IF EXISTS friendships;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS discussions;
DROP TABLE IF EXISTS event_participations;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS rewards;
DROP TABLE IF EXISTS user_info;
DROP TABLE IF EXISTS users;

/* =============================
   Users
   ============================= */
CREATE TABLE users (
  user_id   INT AUTO_INCREMENT PRIMARY KEY,
  username  VARCHAR(50)  NOT NULL UNIQUE,
  email     VARCHAR(255) NOT NULL UNIQUE,
  password  VARCHAR(255) NOT NULL,
  role      ENUM('organizer','attendee') NOT NULL
);

/* =============================
   User Info
   ============================= */
CREATE TABLE user_info (
  user_id             INT PRIMARY KEY,
  first_name          VARCHAR(50) NOT NULL,
  last_name           VARCHAR(50) NOT NULL,
  date_of_birth       DATE,
  phone_number        VARCHAR(20),
  address_street      VARCHAR(255),
  address_city        VARCHAR(100),
  address_postal_code VARCHAR(20),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

/* =============================
   Events
   ============================= */
CREATE TABLE events (
  event_id          INT AUTO_INCREMENT PRIMARY KEY,
  organizer_id      INT NOT NULL,
  title             VARCHAR(255) NOT NULL,
  description       TEXT,
  category          VARCHAR(100),
  event_date        DATETIME NOT NULL,
  venue             VARCHAR(255),
  is_public         BOOLEAN DEFAULT TRUE,
  max_participants  INT,
  is_paid           BOOLEAN DEFAULT FALSE,
  cost              DECIMAL(10,2) DEFAULT 0.00,
  payment_method    ENUM('credit_card','bank_transfer','cryptocurrency'),
  status            ENUM('scheduled','cancelled','completed') DEFAULT 'scheduled',
  FOREIGN KEY (organizer_id) REFERENCES users(user_id)
);

/* =============================
   Event Participations
   ============================= */
CREATE TABLE event_participations (
  participation_id   INT AUTO_INCREMENT PRIMARY KEY,
  user_id            INT NOT NULL,
  event_id           INT NOT NULL,
  registration_date  DATETIME DEFAULT CURRENT_TIMESTAMP,
  status             ENUM('registered','checkedIn','withdrawn') DEFAULT 'registered',
  FOREIGN KEY (user_id)  REFERENCES users(user_id),
  FOREIGN KEY (event_id) REFERENCES events(event_id)
);

/* =============================
   Discussions
   ============================= */
CREATE TABLE discussions (
  message_id   INT AUTO_INCREMENT PRIMARY KEY,
  event_id     INT NOT NULL,
  user_id      INT NOT NULL,
  message_text TEXT,
  timestamp    DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (event_id) REFERENCES events(event_id),
  FOREIGN KEY (user_id)  REFERENCES users(user_id)
);

/* =============================
   Ratings
   ============================= */
CREATE TABLE ratings (
  rating_id        INT AUTO_INCREMENT PRIMARY KEY,
  event_id         INT NOT NULL,
  user_id          INT NOT NULL,
  organizer_rating TINYINT UNSIGNED,
  event_rating     TINYINT UNSIGNED,
  comment          TEXT,
  FOREIGN KEY (event_id) REFERENCES events(event_id),
  FOREIGN KEY (user_id)  REFERENCES users(user_id)
);

/* =============================
   Friendships
   ============================= */
CREATE TABLE friendships (
  friendship_id INT AUTO_INCREMENT PRIMARY KEY,
  user1_id      INT NOT NULL,
  user2_id      INT NOT NULL,
  FOREIGN KEY (user1_id) REFERENCES users(user_id),
  FOREIGN KEY (user2_id) REFERENCES users(user_id)
);

/* =============================
   Points
   ============================= */
CREATE TABLE points (
  transaction_id   INT AUTO_INCREMENT PRIMARY KEY,
  user_id          INT NOT NULL,
  event_id         INT NULL,
  reason           VARCHAR(100),
  points_change    INT NOT NULL,
  transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id)  REFERENCES users(user_id),
  FOREIGN KEY (event_id) REFERENCES events(event_id)
);

/* =============================
   Rewards
   ============================= */
CREATE TABLE rewards (
  reward_id       INT AUTO_INCREMENT PRIMARY KEY,
  name            VARCHAR(100) NOT NULL,
  description     TEXT,
  points_required INT NOT NULL
);

/* =============================
   Invitations
   ============================= */
CREATE TABLE invitations (
  invitation_id     INT AUTO_INCREMENT PRIMARY KEY,
  sender_userid     INT NOT NULL,
  receipient_userid INT NOT NULL,
  event_id          INT NOT NULL,
  sender_message    TEXT,
  status            ENUM('pending','accepted','rejected') DEFAULT 'pending',
  FOREIGN KEY (sender_userid)     REFERENCES users(user_id),
  FOREIGN KEY (receipient_userid) REFERENCES users(user_id),
  FOREIGN KEY (event_id)          REFERENCES events(event_id)
);

/****************************************************
    Data Inserts
****************************************************/

/* Users */
INSERT INTO users (username, email, password, role) VALUES
  ('galaxiasEV', 'Events@galaxyevents.com', 'Galaxy', 'organizer'),
  ('maria_k',  'mariak02@gmail.com',  'maria', 'attendee'),
  ('nikos_d',  'nikosdim90@gmail.com',  'nikolaos2015!@', 'attendee'),
  ('elena_m',  'elena.events@planningpro.gr',  'elena2025!', 'organizer'),
  ('george_k', 'georgek.tech@gmail.com', 'georgetech23', 'attendee'),
  ('sofia_p',  'sofiapap.art@gmail.com',  'sofia_art!', 'attendee'),
  ('andreas_l','andreas.leo91@gmail.com', 'andreas_sports24', 'attendee'),
  ('christina_t', 'christina.theo94@gmail.com', 'christina_music!', 'attendee');

/* User Info */
INSERT INTO user_info (user_id, first_name, last_name, date_of_birth, phone_number, address_street, address_city, address_postal_code) VALUES
  (1, 'Galaxias', 'Events', '1985-03-12', '2101234567', '56 Athinon Ave.', 'Athens', '10435'),
  (2, 'Maria',  'Kapsali', '1992-07-22', '2310123456', '12 Egnatias St.', 'Thessaloniki', '54625'),
  (3, 'Nikos',  'Dimitriou', '1990-11-05', '2610123456', '100 Agiou Andreou St.', 'Patras', '26222'),
  (4, 'Elena',  'Markopoulou', '1988-05-15', '2101112233', '45 Ermou St.', 'Athens', '10563'),
  (5, 'George', 'Konstantinou', '1995-09-28', '2310445566', '78 Tsimiski St.', 'Thessaloniki', '54622'),
  (6, 'Sofia',  'Papandreou', '1993-12-03', '2102223344', '22 Solonos St.', 'Athens', '10671'),
  (7, 'Andreas','Leonidou', '1991-08-17', '2310778899', '15 Mitropoleos St.', 'Thessaloniki', '54624'),
  (8, 'Christina', 'Theodorou', '1994-04-25', '2101234567', '89 Patision St.', 'Athens', '11144');

/* Events */
INSERT INTO events (organizer_id, title, description, category, event_date, venue, is_public, max_participants, is_paid, cost, payment_method, status) VALUES
  (1, 'Tech Meetup', 'Tech demos, lightning talks, and workshops.', 'Technology', '2025-06-15 18:00:00', 'Athens Concert Hall', TRUE, 150, FALSE, 0.00, 'cryptocurrency', 'completed'),
  (1, 'Summer Coding Camp', '5-day coding bootcamp: HTML/CSS, JS, React, full-stack.', 'Workshop', '2025-07-10 09:00:00', 'Thessaloniki City Hall', TRUE, 50, TRUE, 200.00, 'credit_card', 'completed'),
  (1, 'Startup Pitch Night', 'Pitch to investors and tech leaders.', 'Business', '2025-08-05 19:30:00', 'Patras Innovation Hub', TRUE, 100, TRUE, 50.00, 'bank_transfer', 'scheduled'),
  (1, 'AI & Ethics Symposium', 'Explore the ethical side of AI.', 'Technology', '2025-09-20 10:00:00', 'Athens Digital Forum', TRUE, 200, TRUE, 75.00, 'credit_card', 'scheduled'),
  (4, 'Art in Motion', 'Where art meets technology.', 'Art', '2025-06-25 17:00:00', 'Thessaloniki Cultural Center', TRUE, NULL, FALSE, 0.00, NULL, 'scheduled'),
  (4, 'Greek Music Night', 'An evening of Greek music from past to present.', 'Music', '2025-07-15 20:00:00', 'Chania Rooftop Garden', TRUE, 120, TRUE, 35.00, 'credit_card', 'scheduled'),
  (1, 'Blockchain Workshop', 'Smart contracts and DApp development.', 'Technology', '2025-08-25 09:00:00', 'Patras Tech Hub', TRUE, 40, TRUE, 250.00, 'cryptocurrency', 'scheduled'),
  (4, 'Photography Masterclass', 'Photography theory and practice, various locations.', 'Art', '2025-07-30 11:00:00', 'Kalamata Photography Studio', TRUE, 30, TRUE, 180.00, 'credit_card', 'scheduled'),
  (1, 'Past Tech Conference', 'Major completed tech event.', 'Technology', '2024-12-15 10:00:00', 'Athens Digital Hub', TRUE, 200, TRUE, 100.00, 'credit_card', 'completed'),
  (1, 'Winter Code Sprint', 'Web dev focused winter camp.', 'Workshop', '2025-01-20 09:00:00', 'Thessaloniki Tech Center', TRUE, 50, TRUE, 150.00, 'bank_transfer', 'completed'),
  (1, 'Digital Marketing Summit', 'Trends and strategies in digital marketing.', 'Business', '2025-02-28 14:00:00', 'Heraklion Business Center', TRUE, 150, TRUE, 75.00, 'credit_card', 'completed');

/* Participations */
INSERT INTO event_participations (user_id, event_id, registration_date, status) VALUES
  (2, 1, '2025-05-01 10:00:00', 'registered'),
  (3, 1, '2025-05-02 14:30:00', 'registered'),
  (5, 1, '2025-05-04 11:20:00', 'registered'),
  (6, 5, '2025-05-05 15:45:00', 'registered'),
  (7, 6, '2025-05-06 09:30:00', 'registered'),
  (8, 6, '2025-05-06 10:15:00', 'registered'),
  (5, 7, '2025-05-07 14:00:00', 'registered'),
  (6, 8, '2025-05-08 16:20:00', 'registered');

/* Points Transactions */
INSERT INTO points (user_id, event_id, reason, points_change, transaction_date) VALUES
  (2, 1, 'attendance', 50, '2025-06-15 20:00:00'),
  (3, 1, 'attendance', 50, '2025-06-15 20:00:00'),
  (5, 1, 'attendance', 50, '2025-06-15 20:00:00'),
  (6, 5, 'early_registration', 20, '2025-05-05 15:45:00'),
  (7, 6, 'early_registration', 20, '2025-05-06 09:30:00'),
  (8, 6, 'early_registration', 20, '2025-05-06 10:15:00');

/* Rewards */
INSERT INTO rewards (name, description, points_required) VALUES
  ('Coffee Voucher', 'Free coffee at the event venue', 100),
  ('VIP Season Pass', '3-month priority access with VIP perks', 1000),
  ('Backstage Experience', 'Meet speakers and go behind the scenes', 800),
  ('Tech Workshop Bundle', 'Lifetime access to workshop recordings & materials', 600),
  ('Premium Event Kit', 'Backpack, power bank, notebook, and swag', 400),
  ('Networking Dinner Pass', 'Join post-event dinner with VIPs', 500),
  ('Professional Headshot', 'Pro photo session at venue with editing', 300),
  ('Private Mentoring', '1-hour session with an expert of your choice', 700),
  ('Event Series Pass', 'Access to any full event series with perks', 900);

/* Friendships */
INSERT INTO friendships (user1_id, user2_id) VALUES
  (2, 3),
  (2, 5),
  (3, 6),
  (5, 7),
  (2, 8),
  (7, 8);

/* Invitations */
INSERT INTO invitations (sender_userid, receipient_userid, event_id, sender_message, status) VALUES
  (1, 2, 3, 'Join us for the pitch night!', 'pending'),
  (4, 2, 5, 'Come to the art exhibition! A unique experience awaits.', 'pending'),
  (4, 2, 6, 'Greek Music Night will transport you!', 'accepted'),
  (1, 2, 7, 'Don’t miss the blockchain workshop—it’ll be hands-on.', 'pending'),
  (4, 2, 8, 'Into photography? Come with me to the masterclass!', 'rejected');

/* Discussions */
INSERT INTO discussions (event_id, user_id, message_text, timestamp) VALUES
  (1, 2, 'Looking forward to the meetup!', '2025-05-04 08:30:00'),
  (5, 6, 'The concept sounds amazing! Can’t wait to see the interactive installations.', '2025-05-05 16:00:00'),
  (6, 7, 'Will there be traditional dance lessons too?', '2025-05-06 10:00:00'),
  (6, 8, 'Looking forward to experiencing Greek music culture!', '2025-05-06 11:30:00'),
  (7, 5, 'Excited to learn about blockchain development!', '2025-05-07 15:00:00');

/* Ratings */
INSERT INTO ratings (event_id, user_id, organizer_rating, event_rating, comment) VALUES
  (1, 2, 5, 4, 'Great event!'),
  (5, 6, 5, 5, 'Absolutely amazing! The interactive art installations were mind-blowing.'),
  (6, 7, 4, 5, 'Beautiful venue and amazing music selection!'),
  (6, 8, 5, 4, 'Loved the traditional instruments showcase.');
