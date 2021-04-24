from djongo import models
from django import forms


class Mouth(models.Model):
    x = models.IntegerField(null=False)
    y = models.CharField()

    class Meta:
        abstract = True


class Clown(models.Model):
    x = models.IntegerField(null=False)
    y = models.CharField()

    class Meta:
        abstract = True


class Brow(models.Model):
    x = models.IntegerField(null=False)
    y = models.CharField()

    class Meta:
        abstract = True


class Nasolabial_Folds(models.Model):
    x = models.IntegerField(null=False)
    y = models.CharField()

    class Meta:
        abstract = True


class Face(models.Model):
    mouth = models.EmbeddedField(model_container=Mouth)
    clown = models.EmbeddedField(model_container=Clown)
    brow = models.EmbeddedField(model_container=Brow)
    nasolabial_folds = models.EmbeddedField(model_container=Nasolabial_Folds)

    class Meta:
        abstract = True


# 눈 깜박임
class Eye(models.Model):
    x = models.IntegerField(null=False)
    y = models.CharField()

    class Meta:
        abstract = True


class Result(models.Model):
    eye = models.EmbeddedField(model_container=Eye)
    face = models.EmbeddedField(model_container=Face)

    class Meta:
        abstract = True


class face_engine(models.Model):
    result = models.EmbeddedField(model_container=Result)

    objects = models.DjongoManager()