from ..models import Batch
from semesters.models import Semester
def batch_name(year, course_name, end_year):
    return course_name+" "+year+"-"+end_year


def validate_batch(batch_name):
    if Batch.objects.filter(name=batch_name, is_active=True).exists():
        return True
    return False

def students_validations(students):
    for student in students:
        if Batch.objects.filter(student=student).exists():
            return True, student
    return False, None

def adding_students_in_batch(instance, students):
    for student in students:
        instance.student.add(student)
        instance.save()


def getStudentsList(instance):
    return [student.id for student in instance.student.all()]

def semester_name_setup(number, batch_name):
    return f"Semester # {number} of {batch_name.name}"


def create_semesters(self, batch_id, course_id, added_by_id):
    from ..models import Batch
    from courses.models import Course
    from accounts.models import CustomUser # Import inside the task to avoid circular imports
    batch = Batch.objects.get(id=batch_id)
    course = Course.objects.get(id=course_id)
    added_by = CustomUser.objects.get(id=added_by_id)

    for i in range(1, 9):
        semester_name = semester_name_setup(i, batch)
        Semester.objects.create(
            name=semester_name,
            course=course,
            batch=batch,
            added_by=added_by
        )