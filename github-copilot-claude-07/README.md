Student Grader

A simple Python utility to calculate student scores and assign grades.

Quick usage

Run the demo:

```bash
python student_grader.py
```

Import and use in code:

```python
from student_grader import grade_student, grade_students

s = {"Math": 90, "English": 85}
print(grade_student(s))
```

Defaults assume each subject is out of 100 marks.
