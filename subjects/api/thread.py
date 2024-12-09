from notifications.models import *

def NotificationCreationAndSending(request_user, subject_name, title, description):
    print('================== Thread for file added/updated started')
    new_notification = Notification.objects.create(
                title = title,
                description = description,
                type="file",
                sent_by=request_user,
                is_sent=True  # Assuming you mark it as sent immediately
    )
    students = subject_name.subject.semester.batch.student.all()
    new_notification.users.add(*students)
    
    for student in students:
        NotificationStatus.objects.create(
            user=student,
            notification = new_notification,
        )
    print('================== Thread for file added/updated started')
    return {'message':'success'}


def NotificationCreationAndSendingForMessage(title, description, request_user, group_chat):
    new_notification = Notification.objects.create(
                title = title,
                description = description,
                type="chat",
                sent_by=request_user,
                is_sent=True  # Assuming you mark it as sent immediately
    )
    students = group_chat.students.all()
    new_notification.users.add(*students)
    
    for student in students:
        NotificationStatus.objects.create(
            user=student,
            notification = new_notification,
        )
    return {'message': 'success'}

def TeacherAssignedToSubject(title, description, request_user, subject):
    new_notification = Notification.objects.create(
        title=title,
        description=description,
        type="teacher",
        sent_by=request_user,
        is_sent=True  # Assuming you mark it as sent immediately
    )
    students = subject.semester.batch.student.all()
    new_notification.users.add(*students)

    for student in students:
        NotificationStatus.objects.create(
            user=student,
            notification=new_notification,
        )
    return {'message': 'success'}

def SummaryCreatedNotification(title, description , request_user, subject):
    new_notification = Notification.objects.create(
        title=title,
        description=description,
        type="summary",
        sent_by=request_user,
        is_sent=True  # Assuming you mark it as sent immediately
    )
    students = subject.semester.batch.student.all()
    new_notification.users.add(*students)

    for student in students:
        NotificationStatus.objects.create(
            user=student,
            notification=new_notification,
        )
    return {'message': 'success'}

def KeypointsCreatedNotification(title, description , request_user, subject):
    new_notification = Notification.objects.create(
        title=title,
        description=description,
        type="keypoint",
        sent_by=request_user,
        is_sent=True  # Assuming you mark it as sent immediately
    )
    students = subject.semester.batch.student.all()
    new_notification.users.add(*students)

    for student in students:
        NotificationStatus.objects.create(
            user=student,
            notification=new_notification,
        )
    return {'message': 'success'}

def QuizCreatedNotification(title, description , request_user, subject):
    new_notification = Notification.objects.create(
        title=title,
        description=description,
        type="quiz",
        sent_by=request_user,
        is_sent=True  # Assuming you mark it as sent immediately
    )
    students = subject.semester.batch.student.all()
    new_notification.users.add(*students)

    for student in students:
        NotificationStatus.objects.create(
            user=student,
            notification=new_notification,
        )
    return {'message': 'success'}

def QuizCompletion(title, description , request_user, subject):
    new_notification = Notification.objects.create(
        title=title,
        description=description,
        type="quiz",
        sent_by=request_user,
        is_sent=True  # Assuming you mark it as sent immediately
    )
    teacher = subject.teacher
    new_notification.users.add(*teacher)

    NotificationStatus.objects.create(
        user=teacher,
        notification=new_notification,
    )
    return {'message': 'success'}