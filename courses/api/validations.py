from ..models import Course

def duplicate_course_check(name):
    if Course.objects.filter(name=name).exists():
        return True
    return False
