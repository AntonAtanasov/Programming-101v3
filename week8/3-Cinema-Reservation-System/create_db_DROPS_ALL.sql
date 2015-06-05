DROP TABLE IF EXISTS Movies;

CREATE TABLE IF NOT EXISTS Movies(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    rating REAL
    );


DROP TABLE IF EXISTS Projections;

CREATE TABLE IF NOT EXISTS Projections(
    id INTEGER PRIMARY KEY,
    movie_id INTEGER,
    type TEXT,
    projection_date DATE,
    projection_time TIME,
    FOREIGN KEY(movie_id) REFERENCES Movies(id)
    );

DROP TABLE IF EXISTS Reservations;

CREATE TABLE IF NOT EXISTS Reservations(
    id INTEGER PRIMARY KEY,
    username TEXT,
    projection_id INTEGER,
    row INTEGER,
    col INTEGER,
   FOREIGN KEY(projection_id) REFERENCES Projections(id)
    );

PRAGMA foreign_keys = ON;

INSERT INTO Movies(name, rating)
VALUES ("The Hunger Games: Catching Fire", 7.9),
       ("Wreck-It Ralph", 7.8),
       ("Her", 8.3);

INSERT INTO Projections(movie_id, type, projection_date, projection_time)
VALUES(1, "3D", date("2014-07-01"), strftime('%H:%M',"19:10")),
      (1, "2D", date("2014-03-02"), strftime('%H:%M',"19:30")),
      (2, "3D", date("2014-06-03"), strftime('%H:%M',"22:00")),
      (2, "2D", date("2014-07-04"), strftime('%H:%M',"22:30")),
      (3, "3D", date("2014-08-13"), strftime('%H:%M',"14:00"));

INSERT INTO Reservations(username, projection_id, row, col)
VALUES('RadoRado', 1, 2, 1),
      ('RadoRado', 1, 3, 5),
      ('RadoRado', 1, 7, 8),
      ('Ivo', 3, 10, 1),
      ('Ivo', 3, 1, 10),
      ('Mysterious', 5, 2, 3),
      ('Mysterious', 5, 2, 4);

