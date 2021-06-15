from django import forms


class UserInformation(forms.Form):
    text_information = forms.CharField(widget=forms.Textarea)
