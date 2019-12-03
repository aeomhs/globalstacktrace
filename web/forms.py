from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    
    email.widget.attrs.update({'class': 'validate'})
    password.widget.attrs.update({'class': 'validate'})

