from notifications.models import *

def NotificationCreationAndSending(request_user, subject_name, title, description):
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