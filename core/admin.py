from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Department, Major,
    ClassRoom, Course, TeachDetail,
    TermScore, ScoreDetail
)

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': (
            'first_name', 'last_name', 'email', 'gender',
            'dob', 'village', 'district', 'province',
            'nationality', 'tribe', 'phone', 'degree',
            'position',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


class ScoreDetailAdmin(admin.ModelAdmin):
    model = ScoreDetail

    def get_field_names(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def get_list_display(self, request):
        return self.get_field_names(request) + ['term_score_username',]

    def term_score_username(self, obj):
        return obj.term_score.user.username
    term_score_username.short_description = 'Term Score User'


class TermScoreAdmin(admin.ModelAdmin):
    model = TermScore

    def get_field_names(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def get_list_display(self, request):
        return self.get_field_names(request)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Major)
admin.site.register(ClassRoom)
admin.site.register(Course)
admin.site.register(TeachDetail)
admin.site.register(TermScore, TermScoreAdmin)
admin.site.register(ScoreDetail, ScoreDetailAdmin)
