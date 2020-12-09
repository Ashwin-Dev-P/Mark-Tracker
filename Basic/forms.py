from django import forms
from Basic.models import User,markDetails,additionalInfo

class UserForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class MarkForms(forms.ModelForm):
    class Meta:
        model = markDetails
        fields = "__all__"
class infoForms(forms.ModelForm):
    class Meta:
        model = additionalInfo
        fields = "__all__"


