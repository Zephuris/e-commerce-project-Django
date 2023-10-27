from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UsernameField

class NewUserForm(UserCreationForm):
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(
                                attrs={"id":"signup-email",
                                       "class":"form-control"}))
    password1 = forms.CharField(label="password",widget=forms.PasswordInput(
                                    attrs={"class":"form-contorl",
                                           "id":"signup-password",
                                            "placeholder":"Secret word"}))
    
    class Meta:
        model = User
        fields = ('email',"username",'password1','password2')
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update()
    def save(self, commit: bool = ...) -> Any:
        user = super(NewUserForm,self).save(commit = False)
        user.email = self.cleaned_data['email']
        if commit :
            user.save()
        return user
    
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'signin-password',
        }
))
    
class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name','last_name','email')
class CommentForm(forms.Form):
    name = forms.CharField(max_length=35,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))