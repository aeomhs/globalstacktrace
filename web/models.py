from django.db import models


class Card(models.Model):
    # cid = models.AutoField(primary_key=True)
    homepage = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Project(models.Model):
    # pid = models.AutoField(primary_key=True)
    summary = models.TextField()
    link = models.TextField()


class User(models.Model):
    # uid = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Certification(models.Model):
    # cfid = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    certification_name = models.CharField(max_length=100)
    certification_type = models.IntegerField()
    organization = models.CharField(max_length=100)



class Card_Project(models.Model):
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)


class Card_Certification(models.Model):
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    certification_id = models.ForeignKey(Certification, on_delete=models.CASCADE)


class Certification_type(models.Model):
    certification_type = models.IntegerField()
    certification_name = models.CharField(max_length=100)


class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)


