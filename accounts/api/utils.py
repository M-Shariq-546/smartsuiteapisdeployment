import datetime
from django.core.mail import send_mail
from batch.models import Batch
from departments.models import Department


# This is thread base work to send the email in optimized time
def send_mail_to_new_creation(email, password, role):
    send_mail(
        "Welcome to SmartSuite",
        f'''
Welcome to The SmartSuite! 
    We are warmly welcome you to world of advancements and updates of GCS Wahdat Road Lahore. 

Under the Access of this application, you will experience some of the top notch features and use the most valuable features to enhace your study and have more chances of being get 
goog grades. You can access the application using the following credentials: 

Email : {email}
Password : {password}
Role : {role}

Regards

Team SmartSuite

All Rights are reserverd under the section of copywritting.''',
        "mshariq28022000@gmail.com",
        [f"{email}"],
        fail_silently=False,
        )



# This is thread based working to assign batch to students
def adding_student_to_batch(student, batch_id):
    batch = Batch.objects.get(id=batch_id)
    batch.student.add(student)
    batch.save()



# This is thread based for adding teachers into department

def adding_teacher_to_department(teacher, department_id):
    department = Department.objects.get(id=department_id)
    department.teacher.add(teacher)
    department.save()


def current_year():
    return datetime.date.today().year

def previous_years():
    return [(r,r) for r in range(datetime.date.today().year-5, datetime.date.today().year+1)]
