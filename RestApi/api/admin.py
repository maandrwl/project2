from django.contrib import admin
from .models import Subject, Assignment, Account, Score


class SubjectAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Subject._meta.fields]

class AssignmentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Assignment._meta.fields]

class AccountAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Account._meta.fields]

class ScoreAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Score._meta.fields]

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Score, ScoreAdmin)