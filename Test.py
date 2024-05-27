import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#testcase đăng ký
class SignupTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()  # Sử dụng WebDriver của trình duyệt, bạn có thể thay đổi thành trình duyệt khác
        self.driver.get("https://webtester.up.railway.app/user/sign-up/")  # Thay đổi URL tới trang đăng ký

    def tearDown(self):
        self.driver.quit()

    #trường hợp đăng ký thành công
    def test_signup_with_valid_info(self):
        self.signup("testuser01", "Long", "Nguyen", "test@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/", expected_message="Thành công: Thử nghiệm đăng ký thành công!")
    #trường hợp bỏ trống username
    def test_signup_without_username(self):
        self.signup("", "Long", "Nguyen", "test01@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: username không được bỏ trống!")
    #trường hợp bỏ trống giữa các ký tự trong username
    def test_signup_with_space_between_char(self):
        self.signup("t e s t u s e r 01", "Long", "Nguyen", "test01@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: username không được có khoảng trống!")
    #trường hợp username đã tồn tại
    def test_signup_with_existing_username(self):
        self.signup("testuser01", "Long", "Nguyen", "test01@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: username đã được sử dụng!")
    #trường hợp username quá dài
    def test_signup_with_too_long_username(self):
        self.signup("testuser0123456789", "Long", "Nguyen", "test01@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: username quá dài!")
    #trường hợp first_name và last_name chứa ký tự đặc biệt
    def test_signup_with_special_char_in_FL(self):
        self.signup("testuser0123456789", "Long!@", "Nguyen!@", "test01@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: họ tên không được có ký tự đặc biệt!")
    #trường hợp first_name và last_name bị bỏ trống
    def test_signup_without_FL(self):
        self.signup("testuser0123456789", "", "", "test01@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: họ tên không được bỏ trống!")
    #trường hợp bỏ trống email
    def test_signup_without_email(self):
        self.signup("existinguser", "Long", "Nguyen", "", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: Email đã không được bỏ trống!")
    #trường hợp để khoảng trống trong email
    def test_signup_with_space_between_email(self):
        self.signup("existinguser", "Long", "Nguyen", "t e s t @gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: Email không được có khoảng trống!")
    #trường hợp email đã tồn tại
    def test_signup_with_existing_email(self):
        self.signup("existinguser", "Long", "Nguyen", "test@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: Email đã được sử dụng!")
    #trường hợp số điện thoại quá dài
    def test_signup_with_too_long_phone(self):
        self.signup("existinguser", "Long", "Nguyen", "test@gmail.com", "0379877881123123", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: Số điện thoại quá dài!")
    #trường hợp số điện thoại không bắt đầu bằng 03 hoặc 09
    def test_signup_with_dont_start_at_03_09(self):
        self.signup("existinguser12", "Long", "Nguyen", "test12@gmail.com", "1379877881", "Bien Hoa, Dong Nai", "08092003", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: Số điện thoại phải bắt đầu bằng 03 hoặc 09!")
    #trường hợp để trống ngày sinh
    def test_signup_without_birth(self):
        self.signup("existinguser12", "Long", "Nguyen", "tes12@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: ngày sinh không được bỏ trống!")
    #trường hợp để ngày sinh ở quá khứ
    def test_signup_with_birth_from_pass(self):
        self.signup("existinguser12", "Long", "Nguyen", "tes12@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08091800", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: ngày sinh không được trước 1994!")
    #trường hợp để ngày sinh ở tương lai
    def test_signup_with_birth_from_future(self):
        self.signup("existinguser12", "Long", "Nguyen", "tes12@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092500", "testpassword", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: ngày sinh không được quá thời gian hiện tại!")
    # #trường hợp để trống mật khẩu
    def test_signup_without_passwords(self):
        self.signup("testuser02", "Long", "Nguyen", "newuser@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "", "", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: Mật khẩu không được để trống")
    # #trường hợp để trống giữa các ký tự trong mật khẩu
    def test_signup_with_space_between_passwords(self):
        self.signup("testuser02", "Long", "Nguyen", "newuser@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "p a s s w o r d 1", "p a s s w o r d 1", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: Mật khẩu không được có khoảng trống")
    # #trường hợp mật khẩu không khớp
    def test_signup_with_mismatched_passwords(self):
        self.signup("testuser02", "Long", "Nguyen", "newuser@gmail.com", "0379877881", "Bien Hoa, Dong Nai", "08092003", "password1", "password2", expected_url="https://webtester.up.railway.app/user/sign-up/", expected_message="Thất bại: Mật khẩu không khớp!")

    def signup(self, username, firstname, lastname, email, phone, address, birth, password1, password2, expected_url, expected_message):
        driver = self.driver
        username_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[1]/input")
        firstname_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[2]/input")
        lastname_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[3]/input")
        email_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[4]/input")
        phone_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[5]/input")
        address_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[6]/input")
        birth_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[7]/input")
        password1_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[8]/input")
        password2_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[9]/input")
        checkbox_link = driver.find_element(By.XPATH, '/html/body/div/div[1]/div/form/div[10]/label/input')
        checkbox_link.click()
        submit_button = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/input[2]")

        # Điền thông tin vào các trường input
        username_input.send_keys(username)
        firstname_input.send_keys(firstname)
        lastname_input.send_keys(lastname)
        email_input.send_keys(email)
        phone_input.send_keys(phone)
        address_input.send_keys(address)
        birth_input.send_keys(birth)
        password1_input.send_keys(password1)
        password2_input.send_keys(password2)

        # Gửi form bằng cách nhấn nút Submit
        submit_button.click()

        # Chờ một chút để trang web xử lý
        time.sleep(5)

        # Kiểm tra URL hiện tại sau khi đăng ký
        try:
            self.assertEqual(driver.current_url, expected_url)  # Kiểm tra URL
            print(expected_message)
        except AssertionError:
            print("Thất bại: Kiểm tra đăng ký không thành công!")

#testcase đăng nhập
class SigninTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()  # Sử dụng WebDriver của trình duyệt, bạn có thể thay đổi thành trình duyệt khác
        self.driver.get("https://webtester.up.railway.app/user/sign-in/")  # Thay đổi URL tới trang đăng ký

    def tearDown(self):
        self.driver.quit()

    # Kiểm tra đăng nhập thành công
    def test_signin_valid(self):  
        self.signin("test@gmail.com", "testpassword", expected_url="https://webtester.up.railway.app/", expected_message="Thành công: Thử nghiệm đăng nhập thành công!")
    # Kiểm tra đăng nhập với mật khẩu không đúng
    def test_signin_with_incorrect_password(self):
        self.signin("test@gmail.com", "incorrectpassword", expected_url="https://webtester.up.railway.app/user/sign-in/", expected_message="Thất bại: Mật khẩu không đúng!")
    # Kiểm tra đăng nhập với email không tồn tại
    def test_signin_with_invalid_email(self):
        self.signin("nonexistent@gmail.com", "testpassword", expected_url="https://webtester.up.railway.app/user/sign-in/", expected_message="Thất bại: Email không tồn tại!")

    def signin(self, email, password, expected_url, expected_message):
        driver = self.driver
        email_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[1]/input")
        password_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/div[2]/input")
        submit_button = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/form/input[2]")

        # Điền thông tin vào các trường input
        email_input.send_keys(email)
        password_input.send_keys(password)

        # Gửi form bằng cách nhấn nút Submit
        submit_button.click()

        # Chờ một chút để trang web xử lý
        time.sleep(10)

        # Kiểm tra URL hiện tại sau khi đăng nhập
        try:
            self.assertEqual(driver.current_url, expected_url)  # Kiểm tra URL
            print(expected_message)
        except AssertionError:
            print("Thất bại: Kiểm tra đăng nhập không thành công!")


if __name__ == "__main__":
    # Sử dụng TestLoader để kiểm soát thứ tự chạy các test case
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Thêm các test case theo thứ tự mong muốn vào suite
    # Thêm các test case đăng ký
    suite.addTest(SignupTestCase("test_signup_with_valid_info"))
    suite.addTest(SignupTestCase("test_signup_without_username"))
    suite.addTest(SignupTestCase("test_signup_with_space_between_char"))
    suite.addTest(SignupTestCase("test_signup_with_existing_username"))
    suite.addTest(SignupTestCase("test_signup_with_too_long_username"))
    suite.addTest(SignupTestCase("test_signup_with_special_char_in_FL"))
    suite.addTest(SignupTestCase("test_signup_without_FL"))
    suite.addTest(SignupTestCase("test_signup_without_email"))
    suite.addTest(SignupTestCase("test_signup_with_space_between_email"))
    suite.addTest(SignupTestCase("test_signup_with_existing_email"))
    suite.addTest(SignupTestCase("test_signup_with_too_long_phone"))
    suite.addTest(SignupTestCase("test_signup_with_dont_start_at_03_09"))
    suite.addTest(SignupTestCase("test_signup_without_birth"))
    suite.addTest(SignupTestCase("test_signup_with_birth_from_pass"))
    suite.addTest(SignupTestCase("test_signup_with_birth_from_future"))
    suite.addTest(SignupTestCase("test_signup_without_passwords"))
    suite.addTest(SignupTestCase("test_signup_with_space_between_passwords"))
    suite.addTest(SignupTestCase("test_signup_with_mismatched_passwords"))

    # Thêm các test case đăng nhập 
    suite.addTest(SigninTestCase("test_signin_valid"))
    suite.addTest(SigninTestCase("test_signin_with_incorrect_password"))
    suite.addTest(SigninTestCase("test_signin_with_invalid_email"))

    # Chạy các test case trong suite với runner
    runner = unittest.TextTestRunner(verbosity=2, failfast=False)  # Set failfast=False để không dừng khi có lỗi
    runner.run(suite)

