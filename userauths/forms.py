from django.utils import timezone
import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import re
User = get_user_model()

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}),max_length=20)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First Name"}), max_length=30)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last Name"}), max_length=30)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone Number"}), max_length=20, required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Address"}), max_length=255, required=False)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"placeholder": "Select Birth Date", "type": "date"}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))
    
    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        # Kiểm tra độ dài username
        if len(username) > 12:
            raise forms.ValidationError('Username should be at most 12 characters long.')

        # Kiểm tra xem username chỉ chứa chữ cái và số (không chứa ký tự đặc biệt)
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('Username should contain only letters and digits.')

        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        # Kiểm tra xem email có chứa ký tự '@' không
        if '@' not in email:
            raise forms.ValidationError('Invalid email format: missing "@" character.')

        # Kiểm tra xem email có kết thúc bằng '@gmail.com' hoặc '@outlook.com'
        if not email.endswith('@gmail.com') and not email.endswith('@outlook.com'):
            raise forms.ValidationError('Email must end with @gmail.com or @outlook.com.')

        # Lấy phần tên email trước '@'
        username_part = email.split('@')[0]

        # Kiểm tra độ dài phần tên email trước '@'
        if len(username_part) > 30:
            raise forms.ValidationError('Email username part must be 30 characters or less.')

        # Kiểm tra xem email có chứa ký tự đặc biệt không
        if any(char in email for char in r"""!#$%&'*+/=?^_`{|}~"""):
            raise forms.ValidationError('Email should not contain special characters.')

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')

        # Kiểm tra xem mật khẩu có chứa khoảng trắng không
        if ' ' in password1:
            raise forms.ValidationError('Password should not contain spaces.')

        # Kiểm tra xem mật khẩu có bắt đầu bằng khoảng trắng không
        if password1 and password1[0] == ' ':
            raise forms.ValidationError('Password should not start with a space.')

        # Kiểm tra xem mật khẩu có chứa ký tự '>' hoặc '<' không
        if '>' in password1 or '<' in password1:
            raise forms.ValidationError('Password should not contain ">" or "<" characters.')

        # Kiểm tra xem mật khẩu có chứa icon hoặc ký tự emoji không
        if re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]', password1):
            raise forms.ValidationError('Password should not contain emoji or icon characters.')

        return password1
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if not birth_date:
            raise forms.ValidationError('Please select a birth date.')

        if isinstance(birth_date, str):
            try:
                # Chuyển đổi birth_date từ chuỗi sang đối tượng datetime.date
                birth_date = datetime.date.fromisoformat(birth_date)
            except ValueError:
                raise forms.ValidationError('Invalid date format.')
        elif not isinstance(birth_date, datetime.date):
            raise forms.ValidationError('Invalid date format.')

        # Kiểm tra nếu ngày sinh không phải là tương lai
        if birth_date > timezone.now().date():
            raise forms.ValidationError('The birth date cannot be in the future.')

        # Kiểm tra nếu ngày sinh không trước năm 1924
        earliest_date = datetime.date(1924, 1, 1)
        if birth_date < earliest_date:
            raise forms.ValidationError('The birth date cannot be before 1924.')

        return birth_date

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').strip()
        if not re.match(r'^[a-zA-Z]+$', first_name):
            raise forms.ValidationError("First name should only contain letters and no spaces.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').strip()
        if not re.match(r'^[a-zA-Z]+$', last_name):
            raise forms.ValidationError("Last name should only contain letters and no spaces.")
        return last_name
    
    def clean_address(self):
        address = self.cleaned_data.get('address').strip()
        if not address:
            raise forms.ValidationError("Address cannot be empty.")
        return address
    
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

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'address', 'birth_date', 
            'password1', 'password2'
        ]

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        user.birth_date = self.cleaned_data['birth_date']
        
        if commit:
            user.save()
        return user

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','phone_number', 'address', 'birth_date', 'password']
    # điều kiện trường email
    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        # Kiểm tra xem email có chứa ký tự '@' không
        if '@' not in email:
            raise forms.ValidationError('Invalid email format: missing "@" character.')

        # Kiểm tra xem email có kết thúc bằng '@gmail.com' hoặc '@outlook.com'
        if not email.endswith('@gmail.com') and not email.endswith('@outlook.com'):
            raise forms.ValidationError('Email must end with @gmail.com or @outlook.com.')

        # Lấy phần tên email trước '@'
        username_part = email.split('@')[0]

        # Kiểm tra độ dài phần tên email trước '@'
        if len(username_part) > 30:
            raise forms.ValidationError('Email username part must be 30 characters or less.')

        # Kiểm tra xem email có chứa ký tự đặc biệt không
        if any(char in email for char in r"""!#$%&'*+/=?^_`{|}~"""):
            raise forms.ValidationError('Email should not contain special characters.')

        return email
    # điều kiện trường username
    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        # Kiểm tra độ dài username
        if len(username) > 12:
            raise forms.ValidationError('Username should be at most 12 characters long.')

        # Kiểm tra xem username chỉ chứa chữ cái và số (không chứa ký tự đặc biệt)
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('Username should contain only letters and digits.')

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
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'birth_date']

    def clean_password(self):
        # Không thay đổi mật khẩu trong form này
        return self.cleaned_data.get('password')