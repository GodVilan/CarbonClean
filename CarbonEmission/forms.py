from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserActivity

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Enter your email")

class PasswordResetConfirmForm(forms.Form):
    token = forms.CharField(label="Confirmation Code")
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if new_password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

class UserActivityForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('Transport', 'Transportation'),
        ('Buildings', 'Buildings'),
        ('Industry', 'Industry'),
    ]

    SUBCATEGORY_CHOICES = {
        'Transport': [('Car', 'Car'), ('Bus', 'Bus'), ('Train', 'Train')],
        'Buildings': [('Electricity', 'Electricity'), ('Heating', 'Heating')],
        'Industry': [('Manufacturing', 'Manufacturing'), ('Construction', 'Construction')],
    }

    UNIT_CHOICES = {
        'Car': 'KM',
        'Bus': 'KM',
        'Train': 'KM',
        'Electricity': 'KWH',
        'Heating': 'KWH',
        'Manufacturing': 'Units',
        'Construction': 'Hours',
    }

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="Category")
    sub_category = forms.ChoiceField(choices=[], label="Subcategory")
    quantity = forms.FloatField(label="Quantity")
    unit = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label="Unit"
    )

    class Meta:
        model = UserActivity
        fields = ['category', 'sub_category', 'quantity', 'unit']

    def __init__(self, *args, **kwargs):
        super(UserActivityForm, self).__init__(*args, **kwargs)

        initial_category = self.initial.get('category') or self.data.get('category') or 'Transport'
        self.fields['sub_category'].choices = self.SUBCATEGORY_CHOICES.get(initial_category, [])

        initial_subcategory = self.initial.get('sub_category') or self.data.get('sub_category')
        if initial_subcategory:
            self.fields['unit'].initial = self.UNIT_CHOICES.get(initial_subcategory, '')

    class Media:
        js = ('js/update_subcategory.js',)