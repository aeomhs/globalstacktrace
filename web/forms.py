from django import forms
from .models import MyUser, Card, Project, Certification


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    email.widget.attrs.update({'class': 'validate'})
    password.widget.attrs.update({'class': 'validate'})


class SignupForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    date_of_birth = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'))
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    email.widget.attrs.update({'class': 'validate'})
    name.widget.attrs.update({'class': 'validate'})
    date_of_birth.widget.attrs.update({'class': 'datepicker'})
    password.widget.attrs.update({'class': 'validate'})
    confirm_password.widget.attrs.update({'class': 'validate'})

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class CardForm(forms.ModelForm):
    # SKILL CHOICES
    pl_c = 'C'
    pl_java = 'JAVA'
    pl_python = 'PYTHON'
    PL_TYPE_CHOICES = (
        (pl_c, 'C'),
        (pl_java, 'JAVA'),
        (pl_python, 'PYTHON'),
    )

    skill = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple,
        choices=PL_TYPE_CHOICES,
    )

    class Meta:
        model = Card
        fields = ['summary', 'homepage', 'skill']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'link']


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'date', 'certificate_type', 'organization']
