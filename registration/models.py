from django.db import models
from django.core.validators import *
from django.core.urlresolvers import reverse

# validators for email and phone using regular expressions.
# Added as custom validators while saving to Visitor object to db
phoneValidator = RegexValidator(r'^\d+$', 'Only numbers are allowed.')
emailValidator = RegexValidator(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', 'invalid email format')

# Visitor is the only table we have in our db


class Visitor(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    phone = models.CharField(max_length=10, validators=[phoneValidator, MaxLengthValidator])
    email = models.EmailField("email", validators=[emailValidator])
    visitingPerson = models.CharField(max_length=30)
    # automatically save the created_at timestamp while saving the Visitor object to db
    created_at = models.DateTimeField(auto_now_add=True)

    # upon saving visitor object to db, we redirect the url from register page to visitor details page
    def get_absolute_url(self):
        return reverse('registration:detail', kwargs={'pk': self.pk})

    # overriding the __str__ functionality to show useful representation of the object
    def __str__(self):
        return str(self.id) + ',' + self.firstName + ',' + self.lastName + ',' + self.phone + ',' \
               + self.email + ',' + self.visitingPerson
