-- ============================================================
-- Movie Tracker Database Setup
-- Run this script once to create tables and seed sample data
-- ============================================================

-- Drop tables if starting fresh (comment out in production)
-- DROP TABLE IF EXISTS Users CASCADE;
-- DROP TABLE IF EXISTS Info CASCADE;
-- DROP TABLE IF EXISTS Movie CASCADE;

-- Movie table
CREATE TABLE IF NOT EXISTS Movie (
    Movie_ID SERIAL PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    IMDB VARCHAR(20) NOT NULL,
    Letterboxd VARCHAR(20) NOT NULL,
    Rotten_Tomatoes VARCHAR(20) NOT NULL,
    Date_Released TIMESTAMP NOT NULL,
    Genre VARCHAR(100) NOT NULL
);

-- Info table (one-to-one with Movie)
CREATE TABLE IF NOT EXISTS Info (
    Info_ID SERIAL PRIMARY KEY,
    Movie_ID INTEGER NOT NULL REFERENCES Movie(Movie_ID) ON DELETE CASCADE,
    Director VARCHAR(100) NOT NULL,
    Actor1 VARCHAR(100) NOT NULL,
    Actor2 VARCHAR(100) NOT NULL,
    Actor3 VARCHAR(100) NOT NULL,
    Description VARCHAR(500) NOT NULL
);

-- Users/Reviews table (many-to-one with Movie)
CREATE TABLE IF NOT EXISTS Users (
    User_ID SERIAL PRIMARY KEY,
    Movie_ID INTEGER NOT NULL REFERENCES Movie(Movie_ID) ON DELETE CASCADE,
    Name VARCHAR(100) NOT NULL,
    Review VARCHAR(100) NOT NULL,
    Date_Watched TIMESTAMP DEFAULT NOW(),
    Rating VARCHAR(20) NOT NULL
);

-- ============================================================
-- Sample Data — Top 10 Movies
-- ============================================================

INSERT INTO Movie (Title, IMDB, Letterboxd, Rotten_Tomatoes, Date_Released, Genre) VALUES
('The Shawshank Redemption', '9.3', '4.7', '91%', '1994-09-23', 'Drama'),
('The Godfather',            '9.2', '4.6', '97%', '1972-03-24', 'Crime / Drama'),
('The Dark Knight',          '9.0', '4.5', '94%', '2008-07-18', 'Action / Crime'),
('Schindler''s List',         '9.0', '4.5', '98%', '1993-12-15', 'Biography / Drama'),
('12 Angry Men',             '9.0', '4.4', '100%','1957-04-10', 'Drama'),
('The Lord of the Rings: The Return of the King', '9.0', '4.4', '93%', '2003-12-17', 'Adventure / Fantasy'),
('Pulp Fiction',             '8.9', '4.4', '92%', '1994-10-14', 'Crime / Drama'),
('The Good, the Bad and the Ugly', '8.8', '4.4', '97%', '1966-12-23', 'Western'),
('Fight Club',               '8.8', '4.3', '79%', '1999-10-15', 'Drama / Thriller'),
('Forrest Gump',             '8.8', '4.1', '71%', '1994-07-06', 'Drama / Romance')
ON CONFLICT DO NOTHING;

INSERT INTO Info (Movie_ID, Director, Actor1, Actor2, Actor3, Description) VALUES
(1, 'Frank Darabont',        'Tim Robbins',       'Morgan Freeman',    'Bob Gunton',       'Two imprisoned men bond over years, finding solace and redemption through acts of common decency.'),
(2, 'Francis Ford Coppola',  'Marlon Brando',     'Al Pacino',         'James Caan',       'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.'),
(3, 'Christopher Nolan',     'Christian Bale',    'Heath Ledger',      'Aaron Eckhart',    'Batman faces the Joker, a criminal mastermind who plunges Gotham City into anarchy.'),
(4, 'Steven Spielberg',      'Liam Neeson',       'Ralph Fiennes',     'Ben Kingsley',     'A businessman saves over a thousand Jewish lives during the Holocaust.'),
(5, 'Sidney Lumet',          'Henry Fonda',       'Lee J. Cobb',       'Martin Balsam',    'A jury holdout attempts to prevent a miscarriage of justice by examining a murder case.'),
(6, 'Peter Jackson',         'Elijah Wood',       'Viggo Mortensen',   'Ian McKellen',     'Gandalf and Aragorn lead the world of Men against Sauron''s army.'),
(7, 'Quentin Tarantino',     'John Travolta',     'Uma Thurman',       'Samuel L. Jackson','The lives of two mob hitmen, a boxer, and a pair of diner bandits intertwine.'),
(8, 'Sergio Leone',          'Clint Eastwood',    'Eli Wallach',       'Lee Van Cleef',    'A bounty hunter and a bandit search for a buried cache of Confederate gold.'),
(9, 'David Fincher',         'Brad Pitt',         'Edward Norton',     'Helena Bonham Carter','An insomniac and a soap salesman form an underground fight club.'),
(10,'Robert Zemeckis',       'Tom Hanks',         'Robin Wright',      'Gary Sinise',      'The presidencies of Kennedy and Johnson through the eyes of Forrest Gump.')
ON CONFLICT DO NOTHING;
