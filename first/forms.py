from cProfile import label
from django.forms import ModelForm
from django import forms
from first.models import Restaurant, Review
from django.utils.translation import gettext_lazy as _


REVIEW_POINT_CHOICES = (
    ('1',1),
    ('2',2),
    ('3',3),
    ('4',4),
    ('5',5)
)

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['point', 'comment', 'restaurant']
        labels = {
            'point' : _('평점'),
            'comment' : _('코멘트'),
        }
        helt_texts = {
            'point' : _('평점을 입력해주세요.'),
            'comment' : _('코멘트를 입력해주세요.'),
        }
        widgets = {
            'restaurant' : forms.HiddenInput(),
            'point' : forms.Select(choices=REVIEW_POINT_CHOICES),
        }


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'photo', 'password']
        labels = {
            'name' : _('name'),
            'address' : _('address'),
            'photo' : _('photo url'),
            'password' : _('password'),
        }
        helt_texts = {
            'name' : _('Please enter your name.'),
            'address' : _('Please enter your address.'),
            'photo' : _('Please enter your photo url.'),
            'password' : _('Please enter your password.'),
        }
        widgets = {
            'password' : forms.PasswordInput()
        }
        error_message = {
            'name' : {
                'max_length' : _('Name is too long. Please enter no more than 30 characters.'),
            },
            'photo' : {
                'max_length' : _('ImageUrl is too long. Please enter no more than 30 characters.'),
            },
            'password' : {
                'max_length' : _('Password is too long. Please enter no more than 30 characters.'),
            },
        }


class UpdateRestaurantForm(RestaurantForm):
    class Meta:
        model = Restaurant
        exclude = ['password']