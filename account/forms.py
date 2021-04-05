from account.models import CustomUser
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150,widget=forms.TextInput({
        'type':'text',
        'placeholder':'username',
        'name':'username'
    }),error_messages={'required':'Username must be set'})
    password = forms.CharField(max_length=12,widget=forms.PasswordInput({
        'type':'password',
        'placeholder':'password',
        'name':'password'
    }),error_messages={'required':'Password must be set'})
    confirm_password = forms.CharField(max_length=12,widget=forms.PasswordInput({
        'type':'password',
        'placeholder':'password',
        'name':'confirm_password'
    }),error_messages={'required':'Confirm password must be set'})

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if CustomUser.objects.filter(username=username).exists():
            self.add_error('username',"This username already taken")
        if password != confirm_password:
            self.add_error('confirm_password','Passwords dont match')
        elif len(password) < 6:
            self.add_error('password',"Password it too weak")
        elif not password.isalnum():
            self.add_error('password',"Password must contain letters and digits")


    
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if CustomUser.objects.filter(username=username).exists():
    #         self.add_error('username','This username already taken')

