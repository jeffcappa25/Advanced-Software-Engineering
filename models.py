from django.db import models
from django.contrib.auth.models import User

##code for choosing parent account or student account##
TIPE_CHOICE = (
    ('Parent', u'Parent'),
    ('Student', u'Student'),
)

#This code for Billing model#
class Bill(models.Model):
    creator = models.ForeignKey(User, related_name='+')
    created = models.DateTimeField(auto_now_add=True)
    bill_sum = models.IntegerField()
    description = models.CharField(max_length=30)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'

##code for creating login##
class Login(models.Model):
    user = models.ForeignKey(User, related_name='+')
    tipe = models.CharField(max_length=30, choices=TIPE_CHOICE)
    relation = models.CharField(max_length=40, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Custom user'
        verbose_name_plural = 'Custom users'


