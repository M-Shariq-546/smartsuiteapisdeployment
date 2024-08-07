from django.contrib import admin
from .models import *

class PDFilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file', 'is_active']

admin.site.register(Subjects)
admin.site.register(DocumentSummary)
admin.site.register(DocumentKeypoint)
admin.site.register(DocumentQuiz)
admin.site.register(PDFFiles, PDFilesAdmin)
