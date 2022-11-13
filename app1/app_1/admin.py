from django.contrib import admin
from .models import User,Role,Student_Document,Document

class RoleADMIN(admin.ModelAdmin):
    list_display = ("id","role",)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class UserADMIN(admin.ModelAdmin):
    list_display = ("id","username","email","first_name","last_name","is_superuser","role")
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class DocumentADMIN(admin.ModelAdmin):
    list_display = ("id","title","author")
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class Student_DocumentADMIN(admin.ModelAdmin):
    list_display = ("id","student_id","document_id")
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(User,UserADMIN)
admin.site.register(Role,RoleADMIN)
admin.site.register(Student_Document,Student_DocumentADMIN)
admin.site.register(Document,DocumentADMIN)
