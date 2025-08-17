import re
from models.user_model import User

class AuthService:
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PHONE_PATTERN = r'^(032|033|034|035|036|037|038|039|096|097|098|086|083|084|085|081|082|088|091|094|070|079|077|076|078|090|093|089|056|058|092|059|099)[0-9]{7}$'

    def __init__(self, user_repo):
        self.user_repo = user_repo


    def login(self, email, password):
        user_data = self.user_repo.get_user_by_email(email)
        if not user_data:
            return False, "Email hoặc mật khẩu không chính xác"

        user = User.from_dict(user_data)
        if user.password != password:
            return False, "Email hoặc mật khẩu không chính xác"

        return True, "Đăng nhập thành công"



    def register(self, name, phone, email , password , confirm_password ):
        # 1. Kiểm tra nhập đầy đủ
        if not all([name, phone, email, password, confirm_password]):
            return False, "Vui lòng nhập đầy đủ thông tin"

        # 2. Kiểm tra mật khẩu khớp
        if password != confirm_password:
            return False, "Mật khẩu không trùng khớp"

        # 3. Kiểm tra định dạng email
        if not re.match(self.EMAIL_PATTERN, email):
            return False, "Email không hợp lệ"

        # 4. Kiểm tra định dạng số điện thoại
        if not re.match(self.PHONE_PATTERN, phone):
            return False, "Số điện thoại không hợp lệ"

        # 6. Kiểm tra email đã tồn tại
        if self.user_repo.get_user_by_email(email):
            return False, "Email đã được sử dụng. Vui lòng nhập Email khác"

        # 7. Lưu thông tin người dùng
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=password
        )
        self.user_repo.add_user(new_user)  # Thêm user bằng model

        return True, "Đăng ký thành công"
