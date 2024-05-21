from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import re
User = get_user_model()

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','phone_number', 'address', 'birth_date', 'password']
    # điều kiện trường email
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Kiểm tra xem email chỉ chứa các ký tự hợp lệ
        if not re.match(r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("Invalid email format. Please use a valid email address.")

        # Kiểm tra xem email có kết thúc bằng @gmail.com hoặc @outlook.com
        if not email.endswith('@gmail.com') and not email.endswith('@outlook.com'):
            raise forms.ValidationError("Invalid email domain. Please use an email ending with @gmail.com or @outlook.com.")

        return email
    # điều kiện trường username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Sử dụng regular expression để kiểm tra username chỉ chứa chữ cái (a-z, A-Z) hoặc số (0-9)
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError("Username should only contain letters (a-z, A-Z) or digits (0-9)")
        return username
    # điều kiện trường phone_number
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Kiểm tra xem phone_number chỉ chứa các chữ số và có độ dài từ 10 đến 11 chữ số
        if not phone_number.isdigit() or len(phone_number) < 10 or len(phone_number) > 11:
            raise forms.ValidationError("Phone number should only contain digits and be between 10 to 11 characters long")
        # Kiểm tra xem phone_number bắt đầu bằng '09' hoặc '03'
        if not phone_number.startswith('09') and not phone_number.startswith('03'):
            raise forms.ValidationError("Phone number should start with '09' or '03'")
        return phone_number
    # điều kiện trường password
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Check for any space in the password
        if ' ' in password:
            raise forms.ValidationError('Password should not contain any spaces.')
        # Check if password contains only allowed characters
        if not re.match(r'^[\w!@#$%^&*()_+=-]+$', password):
            raise forms.ValidationError('Password should contain only letters, digits, and special characters.')
        return password
    # Mã hóa mật khẩu
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Mã hóa mật khẩu
        if commit:
            user.save()
        return user