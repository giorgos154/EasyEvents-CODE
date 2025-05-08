use easyevents;
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
  payment_method   ENUM('credit_card','bank_transfer','cryptocurrency'),
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
  (1, 'Galaxias', 'Events', '1985-03-12', '2101234567', 'Leof. Athinon 56',      'Athina',        '10435'),
  (2, 'Maria',  'Kapsali',      '1992-07-22', '2310123456', 'Egnatias 12',          'Thessaloniki',  '54625'),
  (3, 'Nikos',  'Dimitriou',    '1990-11-05', '2610123456', 'Odos Agiou Andreou 100','Patra',        '26222'),
  (4, '-Elenas Planning-',  'Elena Markopoulou',  '1988-05-15', '2101112233', 'Ermou 45', 'Athina',  '10563'),
  (5, 'George', 'Konstantinou', '1995-09-28', '2310445566', 'Tsimiski 78',          'Thessaloniki',  '54622'),
  (6, 'Sofia',  'Papandreou',   '1993-12-03', '2102223344', 'Solonos 22',           'Athina',        '10671'),
  (7, 'Andreas','Leonidou',     '1991-08-17', '2310778899', 'Mitropoleos 15',       'Thessaloniki',  '54624'),
  (8, 'Christina', 'Theodorou', '1994-04-25', '2101234567', 'Patision 89',          'Athina',        '11144');

/* Events */
INSERT INTO events (organizer_id, title, description, category, event_date, venue, is_public, max_participants, is_paid, cost, payment_method, status) VALUES
  (1, 'Tech Meetup', 'Join the premier tech networking event of the month! Features live tech demos, lightning talks from industry experts, and hands-on workshops.', 'Technology', '2025-06-15 18:00:00', 'Athens Concert Hall', TRUE, 150, FALSE, 0.00, 'cryptocurrency', 'scheduled'),
  (1, 'Summer Coding Camp', 'Transform from beginner to confident coder in this intensive 5-day workshop. Curriculum covers: HTML5/CSS3, JavaScript fundamentals, React basics, and building full-stack applications.', 'Workshop', '2025-07-10 09:00:00', 'Thessaloniki City Hall', TRUE, 50, TRUE, 200.00, 'credit_card', 'scheduled'),
  (1, 'Startup Pitch Night', 'Your gateway to startup success! Present your innovative ideas to a panel of distinguished investors and industry leaders.', 'Business', '2025-08-05 19:30:00', 'Patras Innovation Hub', TRUE, 100, TRUE, 50.00, 'bank_transfer', 'scheduled'),
  (1, 'AI & Ethics Symposium', 'Join us for a thought-provoking symposium exploring the ethical implications of artificial intelligence in today''s world.', 'Technology', '2025-09-20 10:00:00', 'Athens Digital Forum', TRUE, 200, TRUE, 75.00, 'credit_card', 'scheduled'),
  (4, 'Art in Motion', 'Experience art like never before in this unique exhibition where traditional artwork meets modern technology.', 'Art', '2025-06-25 17:00:00', 'Thessaloniki Cultural Center', TRUE, NULL, FALSE, 0.00, NULL, 'scheduled'),
  (4, 'Greek Music Night', 'An unforgettable evening celebrating the rich tapestry of Greek music, from traditional rebetiko to modern compositions.', 'Music', '2025-07-15 20:00:00', 'Chania Rooftop Garden', TRUE, 120, TRUE, 35.00, 'credit_card', 'scheduled'),
  (1, 'Blockchain Workshop', 'Comprehensive hands-on workshop covering blockchain fundamentals, smart contract development, and decentralized applications.', 'Technology', '2025-08-25 09:00:00', 'Patras Tech Hub', TRUE, 40, TRUE, 250.00, 'cryptocurrency', 'scheduled'),
  (4, 'Photography Masterclass', 'Master the art of photography in this intensive workshop. Learn about composition, lighting, camera settings, and post-processing techniques. Includes practical sessions in various locations around the city. Suitable for beginners and intermediate photographers.', 'Art', '2025-07-30 11:00:00', 'Kalamata Photography Studio', TRUE, 30, TRUE, 180.00, 'credit_card', 'scheduled');

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

/* Points transactions */
INSERT INTO points (user_id, event_id, reason, points_change, transaction_date) VALUES
  (2, 1, 'attendance',          50,  '2025-06-15 20:00:00'),
  (3, 1, 'attendance',          50,  '2025-06-15 20:00:00'),
  (5, 1, 'attendance',          50,  '2025-06-15 20:00:00'),
  (6, 5, 'early_registration',  20,  '2025-05-05 15:45:00'),
  (7, 6, 'early_registration',  20,  '2025-05-06 09:30:00'),
  (8, 6, 'early_registration',  20,  '2025-05-06 10:15:00');

/* Rewards */
INSERT INTO rewards (name, description, points_required) VALUES
  ('Coffee Voucher', 'Free coffee at the event venue', 100),
  ('VIP Season Pass', 'Exclusive 3-month priority access to all events, VIP seating, and special meet-and-greet opportunities with speakers and performers', 1000),
  ('Backstage Experience', 'Go behind the scenes! Meet speakers, performers, and organizers before events. Includes photo opportunities and exclusive insider access', 800),
  ('Tech Workshop Bundle', 'Get lifetime access to HD recordings of any workshop, plus supplementary materials and coding examples', 600),
  ('Premium Event Kit', 'Deluxe laptop backpack, 20000mAh power bank, premium notebook, and branded accessories', 400),
  ('Networking Dinner Pass', 'Join exclusive post-event dinner sessions with speakers, performers, and VIP guests', 500),
  ('Professional Headshot', 'Professional photography session at any event venue with digital retouching and multiple poses', 300),
  ('Private Mentoring', 'One-hour private session with an event speaker or industry expert of your choice', 700),
  ('Event Series Pass', 'Full access to any event series (workshops, seminars, or performances) including all materials and perks', 900);

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
  (1, 2, 3, 'Join us for the pitch night!', 'pending');

/* Discussions */
INSERT INTO discussions (event_id, user_id, message_text, timestamp) VALUES
  (1, 2, 'Looking forward to the meetup!', '2025-05-04 08:30:00'),
  (5, 6, 'The concept sounds amazing! Can''t wait to see the interactive installations.', '2025-05-05 16:00:00'),
  (6, 7, 'Will there be traditional dance lessons too?', '2025-05-06 10:00:00'),
  (6, 8, 'Looking forward to experiencing Greek music culture!', '2025-05-06 11:30:00'),
  (7, 5, 'Excited to learn about blockchain development!', '2025-05-07 15:00:00');

/* Ratings */
INSERT INTO ratings (event_id, user_id, organizer_rating, event_rating, comment) VALUES
  (1, 2, 5, 4, 'Great event!'),
  (5, 6, 5, 5, 'Absolutely amazing! The interactive art installations were mind-blowing.'),
  (6, 7, 4, 5, 'Beautiful venue and amazing music selection!'),
  (6, 8, 5, 4, 'Loved the traditional instruments showcase.');
