from django import forms


class UserInformation(forms.Form):
    text_information = forms.CharField(label="Enter your text", widget=forms.Textarea)


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
