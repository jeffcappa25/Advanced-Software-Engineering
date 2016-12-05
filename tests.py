 # -*- coding: utf-8 -*-
from django.test import TestCase
from .models import Login, Bill
from django.contrib.auth.models import User

#registration test
class Test(TestCase):
    def setUp(self):
        student = User.objects.create(username='Jack')
        Login.objects.create(user=student, tipe="Student")
        Bill.objects.create(creator=student, bill_sum=100, description="unit test student pay")
        parent = User.objects.create(username='Bil')
        Login.objects.create(user=parent, tipe="Parent", relation=student.username)
        Bill.objects.create(creator=parent, bill_sum=200, description="unit test parent pay")
#student login test
    def test_student(self):
        user = User.objects.get(username='Jack')
        user_custom = Login.objects.get(user=user)
        new_bill = Bill.objects.get(creator=user)
        self.assertEqual(user.username, 'Jack')
        self.assertEqual(user_custom.tipe, 'Student')
        self.assertEqual(new_bill.description, 'unit test student pay')
#parent login test
    def test_parent(self):
        user = User.objects.get(username='Bil')
        user_custom = Login.objects.get(user=user)
        new_bill = Bill.objects.get(creator=user)
        self.assertEqual(user.username, 'Bil')
        self.assertEqual(user_custom.tipe, 'Parent')
        self.assertEqual(new_bill.description, 'unit test parent pay')

#transaction test 
    def test_tipe_locally(self):
        try:
            raises_error('a', b='c')
        except ValueError:
            pass
        else:
            self.fail('Did not see ValueError')
#revisit
    def test_assert_raises(self):
        self.assertRaises(ValueError, raises_error, 'a', b='c')
