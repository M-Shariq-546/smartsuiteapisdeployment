from ..models import Course

def duplicate_course_check(name):
    if Course.objects.filter(name=name, is_active=True).exists():
        return True
    return False
