from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Company


class MyCompanyCreationForm(UserCreationForm):
    class Meta:
        model = Company
        fields = ['username', 'company_name',
                  'password1', 'password2', 'avatar']


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'description', 'avatar']
