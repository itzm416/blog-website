import email
from django import forms
from django.contrib.auth.models import User
from blogapp.models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm

class UserPasswordReset(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='New Password Confirmation')

class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x1','placeholder':'Password'}), label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='New Password Confirmation')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control x1','placeholder':'Username'}))  
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='Password')

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control x1','placeholder':'Username'}),min_length=4, max_length=10)  
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control x1','placeholder':'Email'}))  
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='Password Confirmation')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control x4','placeholder':'first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control x5','placeholder':'last name'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)           
    
        return self.cleaned_data

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','category','image']
        labels = {'title':'Title','content':'Content','category':'Category','image':'Image'}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title','maxlength':'200'}),
            'content':forms.Textarea(attrs={'class':'form-control','placeholder':'Content'}),
            'category':forms.Select(attrs={'class':'form-select'}),
            'image':forms.FileInput(attrs={'class':'form-control'})
        }