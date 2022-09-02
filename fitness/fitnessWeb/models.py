from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
import os

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('images', filename)

class User(AbstractUser):
    pic = models.ImageField(upload_to=get_image_path, blank=True, null=True, default="images/user.png")
    class Role(models.TextChoices):
        instructor = "instructor"
        member = "member"
    role = models.CharField(choices=Role.choices, max_length=100)


class Class(models.Model):
    class Category(models.TextChoices):
        jake = "Jake"
        bob = "Bob"
        harold = "Harold"
        jenny = "Jenny"
        chris = "Chris"
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1000)
    instructor = models.CharField(choices=Category.choices, max_length=100)
    room = models.IntegerField()
    time = models.TimeField()
    class Weekday(models.TextChoices):
        sunday = "Sunday"
        monday = "Monday"
        tuesday = "Tuesday"
        wednesday = "Wednesday"
        thursday = "Thursday"
        friday = "Friday"
        saturday = "Saturday"
    weekday = models.CharField(choices=Weekday.choices, max_length=100)

    def __str__(self):
        return f"{self.title}"

class ClassMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classes")
    gym_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="members")

    def __str__(self):
        return f"{self.user} to {self.gym_class}"

class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey("User", on_delete=models.CASCADE, related_name="mesages_sent")
    read = models.BooleanField(default=False)
    value = models.TextField(blank=True)

    def serialize(self):
        return{
            "id": self.id,
            "sender": self.sender.username,
            "user": self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "value": self.value
        }