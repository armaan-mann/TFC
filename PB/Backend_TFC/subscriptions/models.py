from django.db import models
from accounts.models import User as user
from django.db.models import CASCADE, SET_NULL



# Create your models here.
class Plans(models.Model):
    MEMBERSHIP_OPTIONS = [["150", "Annual Plan"], ["15", "Monthly Plan"], ["200", "Premium Annual Plan"]]
    membership_type = models.CharField(choices=MEMBERSHIP_OPTIONS, max_length=50, default=None)
    duration = models.PositiveIntegerField(default=30)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.membership_type == "150" or self.membership_type == "200":
            return "Annually"
        elif self.membership_type == "15":
            return "Monthly"

    def update_duration(self):
        if self.membership_type == "Annually":
            self.duration = 365
        elif self.membership_type == "Monthly":
            self.duration = 30


class UserMemberships(models.Model):
    user = models.OneToOneField(user, related_name="userMembership", on_delete=SET_NULL, null=True, blank=True)
    membership = models.ForeignKey(Plans, related_name="userMembership", on_delete=SET_NULL, null=True, blank=True)
    card_info = models.CharField(max_length=120)
    isActiveMembership = models.BooleanField(default=True)
    next_payment = models.DateField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class UserPayHistory(models.Model):
    User = models.ForeignKey(UserMemberships, on_delete=CASCADE)
    username = models.CharField(max_length=120, default="None")
    Membership = models.CharField(max_length=120, null=True, blank=True)
    Card_info = models.CharField(max_length=120)
    IsActiveMembership = models.BooleanField(default=True)
    amount = models.IntegerField(null=True, blank=True)
    Next_payment = models.DateField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.User.user.username
