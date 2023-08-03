# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bill(models.Model):
    owners_id = models.IntegerField()
    prev = models.CharField(max_length=20)
    pres = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    date = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'bill'


class Owners(models.Model):
    lname = models.CharField(max_length=60)
    fname = models.CharField(max_length=60)
    mi = models.CharField(max_length=2, blank=True, null=True)
    address = models.CharField(max_length=60)
    contact = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'owners'


class TempoBill(models.Model):
    prev = models.CharField(db_column='Prev', max_length=40)  # Field name made lowercase.
    client = models.CharField(db_column='Client', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tempo_bill'


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=60)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'users'
