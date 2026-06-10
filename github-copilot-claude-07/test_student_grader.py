import unittest

from student_grader import (
    calculate_total,
    percentage,
    grade_from_percentage,
    grade_student,
    grade_students,
)


class TestStudentGrader(unittest.TestCase):
    def test_calculate_total(self):
        self.assertEqual(calculate_total({"a": 10, "b": 20}), 30.0)
        self.assertEqual(calculate_total({"x": 0}), 0.0)

    def test_percentage(self):
        self.assertAlmostEqual(percentage(50, 100), 50.0)
        with self.assertRaises(ValueError):
            percentage(10, 0)

    def test_grade_from_percentage(self):
        self.assertEqual(grade_from_percentage(95)[0], "A+")
        self.assertEqual(grade_from_percentage(89.9)[0], "A")
        self.assertEqual(grade_from_percentage(79.9)[0], "B")
        self.assertEqual(grade_from_percentage(69.9)[0], "C")
        self.assertEqual(grade_from_percentage(59.9)[0], "D")
        self.assertEqual(grade_from_percentage(49.9)[0], "F")

    def test_grade_student(self):
        marks = {"Math": 90, "Eng": 80}
        res = grade_student(marks)
        self.assertIn("total", res)
        self.assertIn("percentage", res)
        self.assertIn("grade", res)

    def test_grade_students(self):
        students = [
            {"name": "S", "marks": {"a": 50, "b": 50}},
            {"name": "Bad", "marks": {}},
        ]
        res = grade_students(students)
        self.assertEqual(res[0]["name"], "S")
        self.assertIn("percentage", res[0])
        self.assertIn("error", res[1])


if __name__ == "__main__":
    unittest.main()
