from collections import OrderedDict
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class CustomerGroup(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(_('active'), default=True)

    def get_attendance(self, dt):
        attendance = OrderedDict()
        for customer in self.customers.all().order_by('firstname'):
            attendance['customer_%s' % customer.id] = False
        for instance in self.attendance.filter(attendance_time=dt):
            attendance['customer_%s' % instance.customer.id] = True
        return attendance

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    group = models.ForeignKey(CustomerGroup, related_name='customers')
    is_active = models.BooleanField(_('active'), default=True)


class GroupAttendance(models.Model):
    group = models.ForeignKey(CustomerGroup, related_name='attendance')
    customer = models.ForeignKey(Customer)
    attendance_time = models.DateField()
