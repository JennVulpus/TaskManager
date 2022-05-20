from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

class List(models.Model):
    name = models.CharField(max_length=45)
    owner = models.ForeignKey(Profile, related_name = 'owner', on_delete=models.CASCADE, blank=True, null=True)
    member = models.ManyToManyField(Profile, related_name='members', blank=True)
    group_code = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Location(models.Model):
    name = models.CharField(max_length=45)
    list = models.ForeignKey(List, related_name = 'list_location', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Chore(models.Model):
    name = models.CharField(max_length=45)
    done_date = models.DateField(blank=True, null=True)
    renew_date = models.DateField(blank=True, null=True)
    renew_freq = models.IntegerField()
    list = models.ForeignKey(List, related_name='list_chore', on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, related_name='location', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class History(models.Model):
    chore = models.ForeignKey(Chore, related_name='chore', on_delete=models.CASCADE)
    finished_at = models.DateTimeField()
    list = models.ForeignKey(List, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)