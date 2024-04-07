from django.contrib import admin

from userauths.models import ContactUs, User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']


admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
