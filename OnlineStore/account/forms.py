from django.forms import TextInput, EmailInput, CharField, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control col-lg-12',
            }),
            'email': EmailInput(attrs={
                'class': 'form-control col-lg-12',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control col-lg-12'
        self.fields['password2'].widget.attrs['class'] = 'form-control col-lg-12'


class Authenticate(AuthenticationForm):
    fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(Authenticate, self).__init__(*args, **kwargs)

    username = UsernameField(widget=TextInput(
        attrs={'class': 'form-control col-lg-12',
               }))
    password = CharField(widget=PasswordInput(
        attrs={
            'class': 'form-control col-lg-12',
        }))
