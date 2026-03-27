from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

User = get_user_model()

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ('password1', 'password2'):
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = '비밀번호를 입력하세요'

        if field == 'password1':
            self.fields[field].label = '비밀번호'
        else:
            self.fields[field].label = '비밀번호 확인'

    class Meta:
        model = User
        fields = ('email', 'name', )
        labels = {
            'email': '이메일',
            'name': '이름',
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'example@example.com',
                    'class': 'form-control'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'placeholder': '이름을 입력해주세요',
                    'class': 'form-control',
                }
            )
        }


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = '이메일'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'example@example.com'
        self.fields['password'].label = '비밀번호'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = '비밀번호를 입력해주세요'