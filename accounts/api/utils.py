from django.core.mail import send_mail

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