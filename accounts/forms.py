from django import forms
from django.contrib.auth.models import User
from django import forms

class SignUpForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')   
        required = ('username','first_name','last_name','email','password')
       
class ActivationForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length=150,required=False)
    email = forms.CharField(label = 'Email',max_length=150,required=False)
