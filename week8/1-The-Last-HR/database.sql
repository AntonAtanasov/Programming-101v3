DROP TABLE IF EXISTS Students;

CREATE TABLE Students(
  student_id INTEGER PRIMARY KEY,
  student_name TEXT,
  student_github TEXT
);

DROP TABLE IF EXISTS Courses;

CREATE TABLE Courses(
  course_id INTEGER PRIMARY KEY,
  course_name TEXT
);

DROP TABLE IF EXISTS Student_To_Course;

CREATE TABLE Student_To_Course(
  student_id INTEGER,
  course_id INTEGER,
  course_group INTEGER,
  FOREIGN KEY(student_id) REFERENCES Students(student_id),
  FOREIGN KEY(course_id) REFERENCES Courses(course_id)
);