# 🏥 HỆ THỐNG QUẢN LÝ TIÊM CHỦNG

## 📌 Giới thiệu

Hệ thống quản lý tiêm chủng được xây dựng nhằm hỗ trợ các cơ sở y tế trong việc:

* Quản lý bệnh nhân
* Quản lý kho vaccine
* Theo dõi lịch sử tiêm chủng
* Nhắc lịch hẹn tiêm mũi tiếp theo

Ứng dụng được phát triển bằng **Python (Flask)** và sử dụng **SQL Server** làm hệ quản trị cơ sở dữ liệu.

---

## 🚀 Công nghệ sử dụng

* **Backend:** Flask (Python)
* **Database:** SQL Server (SQL Express)
* **ORM:** SQLAlchemy
* **Frontend:** HTML, CSS (Jinja2 Template)
* **Thư viện bảo mật:** Werkzeug (hash password)

---

## 🧩 Chức năng chính

### 👤 Quản lý người dùng

* Đăng nhập / đăng xuất
* Phân quyền (Admin, Bác sĩ, Y tá, Tiếp đón)

### 🧑‍⚕️ Quản lý bệnh nhân

* Thêm / xem danh sách bệnh nhân
* Tìm kiếm bệnh nhân theo tên hoặc số điện thoại

### 💉 Quản lý vaccine

* Nhập kho vaccine
* Theo dõi số lượng tồn

### 📋 Tiêm chủng

* Lập phiếu tiêm
* Ghi nhận phản ứng sau tiêm
* Tự động trừ số lượng vaccine

### 📅 Lịch hẹn

* Lưu lịch hẹn mũi tiếp theo
* Hiển thị danh sách hẹn trong 7 ngày tới

---

## 🗄️ Cấu trúc cơ sở dữ liệu

Hệ thống gồm các bảng chính:

* `roles` – Vai trò người dùng
* `users` – Tài khoản đăng nhập
* `patients` – Thông tin bệnh nhân
* `vaccines` – Kho vaccine
* `immunization_records` – Lịch sử tiêm
* `appointments` – Lịch hẹn

---

## ⚙️ Cài đặt và chạy dự án

### 🔹 Bước 1: Clone project

```bash
git clone <link-repo>
cd quan_ly_tiem_chung
```

---

### 🔹 Bước 2: Tạo môi trường ảo

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 🔹 Bước 3: Cài thư viện

```bash
pip install flask flask_sqlalchemy pyodbc werkzeug
```

---

### 🔹 Bước 4: Cấu hình database

Trong file `app.py`, sử dụng:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@LAPTOP-6N9MDA60\\SQLEXPRESS/QuanLyTiemChung?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
```

📌 Lưu ý:

* Cần cài **ODBC Driver 17 for SQL Server**
* Đã tạo sẵn database `QuanLyTiemChung` trong SQL Server

---

### 🔹 Bước 5: Chạy chương trình

```bash
python app.py
```

Truy cập:

```
http://127.0.0.1:5000
```

---

## 🔑 Tài khoản mặc định

Hệ thống sẽ tự tạo:

* **Username:** admin
* **Password:** 123456

---

## 📸 Giao diện (gợi ý thêm)

Bạn có thể chèn hình:

* Trang đăng nhập
* Quản lý bệnh nhân
* Lập phiếu tiêm
* Lịch hẹn

---

## 💡 Hướng phát triển

* Thêm báo cáo thống kê (biểu đồ)
* Xuất file PDF
* Tích hợp AI dự đoán nhu cầu vaccine
* Xây dựng API RESTful

---

## 👨‍💻 Tác giả

* Tác giả: Nguyễn Hoàng Huy
* Năm: 2026

---

## 📄 Giấy phép

Dự án phục vụ mục đích học tập và nghiên cứu.
