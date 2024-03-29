from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    phone_number = forms.CharField()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class AccountForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    phone_number = forms.CharField()


class UploadForm(forms.Form):
    job_id = forms.CharField()
