from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class CustomerGroup(models.Model):
    name = models.CharField(max_length=255)

    def get_attendance(self, dt):
        attendance = {'customer_%s' % customer.id: False for customer in self.customers.all()}
        for instance in self.attendance.filter(attendance_time=dt):
            attendance['customer_%s' % instance.customer.id] = True
        return attendance

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    group = models.ForeignKey(CustomerGroup, related_name='customers')


class GroupAttendance(models.Model):
    group = models.ForeignKey(CustomerGroup, related_name='attendance')
    customer = models.ForeignKey(Customer)
    attendance_time = models.DateField()
