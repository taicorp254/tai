from django import forms
from .models import Page_users, Subscribers, InCart, CheckedOut

class PageUsers(forms.ModelForm):
    class Meta:
        model = Page_users
        fields = ('username', 'email', 'phone', 'password')
        widgets = {'password':forms.PasswordInput()}

class PageUserLogin(forms.ModelForm):
    class Meta:
        model = Page_users
        fields = ('username', 'password')
        widgets = {'password':forms.PasswordInput()}

class UserSubscriber(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ('email', 'name')

class AddToCart(forms.ModelForm):
    class Meta:
        model = InCart
        fields = ('amount',)

class UpdateProfileImage(forms.ModelForm):
    class Meta:
        model = Page_users
        fields = ('profile_picture',)
class UpdateUsername(forms.ModelForm):
    class Meta:
        model = Page_users
        fields = ('username',)
class UpdatePhoneNumber(forms.ModelForm):
    class Meta:
        model = Page_users
        fields = ('phone',)
class UpdateEmail(forms.ModelForm):
    class Meta:
        model = Page_users
        fields = ('email',)
class UpdatePassword(forms.ModelForm):
    class Meta:
        model = Page_users
        fields = ('password',)