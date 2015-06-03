from settings import DB_NAME, SQL_FILE
import sqlite3
import requests


def connect():
    connection = sqlite3.connect(DB_NAME)

    with open(SQL_FILE, "r") as f:
        connection.executescript(f.read())
        connection.commit()

    return connection


def get_students(cursor, information):
    get_students = [dict(student) for student in information]
    for student in get_students:
        cursor.execute("""
            INSERT INTO Students(student_name, student_github) VALUES(?, ?)
            """, (student['name'], student['github']))
    return


def get_courses(cursor, information):
    courses_tuple = set()

    get_courses = [course['courses'][0]['name']
                   for course in information if len(course['courses']) > 0]
    for course in get_courses:
        courses_tuple.add(course)

    for course in courses_tuple:
        cursor.execute("""
            INSERT INTO Courses(course_name) VALUES(?)
            """, (course,))
    return


def student_to_course(cursor, information):
    for student_id in information:
        student_id = information.index(student_id)
        get_course = information[student_id]['courses']
        if len(get_course) > 0:
            for course in get_course:
                course_group = course['group']
                course_id = cursor.execute("""
                SELECT course_id FROM courses WHERE course_name = ?
                """, (course['name'],))
                course_id = course_id.fetchone()
                if course_id is not None:
                    cursor.execute("""
            INSERT INTO student_to_course(student_id, course_id, course_group)
            VALUES(?, ?, ?)""", (student_id, course_id[0], course_group))
    return


def main():
    database = connect()
    cursor = database.cursor()

    request = requests.get('https://hackbulgaria.com/api/students/')
    get_students(cursor, request.json())
    get_courses(cursor, request.json())
    student_to_course(cursor, request.json())

    database.commit()


if __name__ == '__main__':
    main()
