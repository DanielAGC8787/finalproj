from django.contrib import admin
from .models import User, Class, ClassMember, Message

admin.site.register(User)
admin.site.register(ClassMember)
admin.site.register(Class)
admin.site.register(Message)

# Register your models here.
