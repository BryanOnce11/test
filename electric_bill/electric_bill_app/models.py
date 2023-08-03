from django.db import models

# Create your models here.

class Bill(models.Model):
    owners_id = models.IntegerField()
    prev = models.CharField(max_length=20)
    pres = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    date = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'bill'



class Owners(models.Model):
    lname = models.CharField(max_length=60)
    fname = models.CharField(max_length=60)
    mi = models.CharField(max_length=2, blank=True, null=True)
    address = models.CharField(max_length=60)
    contact = models.CharField(max_length=15)

    class Meta:
        managed = True
        db_table = 'owners'


class TempoBill(models.Model):
    prev = models.CharField(max_length=40)
    client = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'tempo_bill'


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'user'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'