# student_marks.py

def calculate_average(marks):
    total = 0

    for mark in marks:
        total += mark

    average = total / len(marks)
    return average


def calculate_grade(average):
    if average >= 90:
        return "A"
    elif average >= 75:
        return "B"
    elif average >= 50:
        return "C"
    else:
        return "F"


def display_student_report(student):
    average = calculate_average(student["marks"])
    grade = calculate_grade(average)

    print("\nStudent Report")
    print("----------------------------")
    print("Name:", student["name"])
    print("Subjects:", student["subjects"])
    print("Marks:", student["marks"])
    print("Average:", round(average, 2))
    print("Grade:", grade)


def main():
    students = [
        {
            "name": "Rahul Sharma",
            "subjects": ["Math", "Physics", "Chemistry", "English"],
            "marks": [85, 78, 92, 74]
        },
        {
            "name": "Priya Verma",
            "subjects": ["Math", "Physics", "Chemistry", "English"],
            "marks": [91, 88, 95, 89]
        }
    ]

    for student in students:
        display_student_report(student)


if __name__ == "__main__":
    main()
