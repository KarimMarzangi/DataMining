from django.db import models

class UsersDetails(models.Model):
    name=models.CharField(max_length=100)
    namefamily=models.CharField(max_length=100)
    email=models.EmailField(max_length=100, primary_key="email")
    mobile=models.CharField(max_length=11)
    bank=models.CharField(max_length=20)
    account=models.CharField(max_length=30)
    class meta:
        db_table="users"
