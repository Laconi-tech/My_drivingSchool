from django.contrib import admin
from .models import Users, Planning, My_Planning

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')

@admin.register(Planning)
class PlannigAdmin(admin.ModelAdmin):
    list_display = ('rdv_stutent', 'rdv_instructor', 'rdv_date')

# @admin.register(My_Planning)
# class My_PlannigAdmin(admin.ModelAdmin):
#     list_display = ('rdv_member', 'title', 'rdv_date')

class My_PlanningAdmin(admin.ModelAdmin):
    list_display = ('title', 'rdv_date', 'get_rdv_members')

    def get_rdv_members(self, obj):
        return ", ".join([user.username for user in obj.rdv_member.all()])
    get_rdv_members.short_description = 'RDV Members'

admin.site.register(My_Planning, My_PlanningAdmin)


# admin.site.register(Users, UsersAdmin)
# admin.site.register(Planning, PlannigAdmin)