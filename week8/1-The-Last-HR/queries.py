import sqlite3

connection = sqlite3.connect("Academy.db")
cursor = connection.cursor()


def list_students_github():
    result = cursor.execute(
        """SELECT student_name, student_github FROM students""")
    return result


def list_courses():
    result = cursor.execute("""SELECT course_name FROM courses""")
    return result


def student_course():
    result = cursor.execute("""
    SELECT student_name,course_name
    FROM students,courses
    JOIN student_to_course
    ON courses.course_id = student_to_course.course_id
    AND students.student_id = student_to_course.student_id
    """)
    return result
