# from flask import Flask, render_template, request, redirect
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "tram_y_te_bi_mat_2026"

# Cấu hình SQL Server (User: sa, Pass: 123456, DB: QuanLyTiemChung)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@LAPTOP-6N9MDA60\\SQLEXPRESS/QuanLyTiemChung?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Cấu hình đường dẫn file database (sẽ tự tạo file database.db)
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# --- KHAI BÁO CÁC MODEL (BẢNG) ---

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='staff_members')

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)

class Vaccine(db.Model):
    __tablename__ = 'vaccines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    batch_number = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=0)
    expiry_date = db.Column(db.Date)

# 5. Bảng Lịch sử tiêm chủng
class ImmunizationRecord(db.Model):
    __tablename__ = 'immunization_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccines.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Quan trọng
    injection_date = db.Column(db.Date)
    dose_number = db.Column(db.Integer)
    reaction = db.Column(db.Text)
    next_appointment = db.Column(db.Date, nullable=True)  # Ngày hẹn tiêm mũi tiếp theo

    # Thêm các dòng này để Template không bị lỗi khi gọi r.patient.fullname
    patient = db.relationship('Patient', backref='records')
    vaccine = db.relationship('Vaccine', backref='records')
    staff = db.relationship('User', backref='records')

# 6. Bảng Lịch hẹn & Theo dõi
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    
    scheduled_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Chờ tiêm') # Chờ tiêm, Đã tiêm, Bỏ lỡ
    notes = db.Column(db.Text)

    patient = db.relationship('Patient', backref='my_appointments')

# --- CÁC ROUTE ĐIỀU HƯỚNG ---

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user_role=session.get('role'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        user = User.query.filter_by(username=u).first()
        
        if user and check_password_hash(user.password_hash, p):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role.role_name
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))
        flash('Sai tài khoản hoặc mật khẩu!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if session.get('role') != 'Admin':
        flash('Bạn không có quyền truy cập!', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role_id = request.form['role_id']
        
        new_user = User(username=username, password_hash=password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit()
        flash('Đã thêm nhân viên mới thành công!', 'success')
        
    users = User.query.all()
    roles = Role.query.all()
    return render_template('manage_users.html', users=users, roles=roles)

# Tạo tài khoản Admin đầu tiên nếu chưa có
with app.app_context():
    db.create_all()
    # Tự động tạo các vai trò nếu chưa có
    for r_name in ['Admin', 'Bác sĩ', 'Y tá', 'Tiếp đón']:
        if not Role.query.filter_by(role_name=r_name).first():
            db.session.add(Role(role_name=r_name))
    db.session.commit()
    if not User.query.filter_by(username='admin').first():
        admin_role = Role.query.filter_by(role_name='Admin').first()
        if admin_role:
            hashed_pw = generate_password_hash('123456')
            first_admin = User(username='admin', password_hash=hashed_pw, role_id=admin_role.id)
            db.session.add(first_admin)
            db.session.commit()

# --- QUẢN LÝ BỆNH NHÂN ---
@app.route('/patients', methods=['GET', 'POST'])
def manage_patients():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_p = Patient(
            fullname=request.form['fullname'],
            dob=request.form['dob'],
            gender=request.form['gender'],
            phone=request.form['phone'],
            address=request.form['address']
        )
        db.session.add(new_p)
        db.session.commit()
        flash('Thêm bệnh nhân thành công!', 'success')
    
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

# --- QUẢN LÝ KHO VACCINE ---
@app.route('/vaccines', methods=['GET', 'POST'])
def manage_vaccines():
    if session.get('role') not in ['Admin', 'Y tá']:
        flash('Bạn không có quyền vào kho!', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_v = Vaccine(
            name=request.form['name'],
            batch_number=request.form['batch'],
            quantity=request.form['quantity'],
            expiry_date=request.form['expiry']
        )
        db.session.add(new_v)
        db.session.commit()
        flash('Nhập kho thành công!', 'success')

    vaccines = Vaccine.query.all()
    return render_template('vaccine.html', vaccines=vaccines) # Tên biến phải khớp với vòng lặp {% for v in vaccines %}

# --- LẬP PHIẾU TIÊM CHỦNG (QUAN TRỌNG NHẤT) ---
@app.route('/inject', methods=['GET', 'POST'])
def inject():
    if 'user_id' not in session: 
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            v_id = request.form.get('vaccine_id')
            vax = Vaccine.query.get(v_id)

            if not vax or vax.quantity <= 0:
                flash('Vaccine này đã hết trong kho hoặc không tồn tại!', 'danger')
            else:
                # 1. Xử lý ngày tiêm hiện tại
                date_str = request.form.get('date')
                if date_str:
                    inj_date = datetime.strptime(date_str, '%Y-%m-%d')
                else:
                    inj_date = datetime.now()

                # 2. LẤY NGÀY HẸN TIẾP THEO TỪ FORM (PHẦN THÊM MỚI)
                next_app_str = request.form.get('next_appointment')
                next_appointment = None
                if next_app_str:
                    next_appointment = datetime.strptime(next_app_str, '%Y-%m-%d').date()

                # 3. TẠO BẢN GHI (CẬP NHẬT TRƯỜNG next_appointment)
                record = ImmunizationRecord(
                    patient_id=request.form.get('patient_id'),
                    vaccine_id=v_id,
                    staff_id=session['user_id'],
                    injection_date=inj_date,
                    dose_number=request.form.get('dose', 1),
                    reaction=request.form.get('reaction', ''),
                    next_appointment=next_appointment  # <--- GÁN GIÁ TRỊ VÀO ĐÂY
                )
                
                vax.quantity -= 1
                db.session.add(record)
                db.session.commit()
                flash('Ghi nhận tiêm chủng và lịch hẹn thành công!', 'success')
                return redirect(url_for('inject'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi hệ thống: {str(e)}', 'danger')

    patients = Patient.query.all()
    vaccines = Vaccine.query.all() 
    records = ImmunizationRecord.query.order_by(ImmunizationRecord.id.desc()).all()
    return render_template('inject.html', patients=patients, vaccines=vaccines, records=records)

# lịch sử tiêm chủng
@app.route('/patient/history/<int:patient_id>')
def patient_history(patient_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Lấy thông tin bệnh nhân
    patient = Patient.query.get_or_404(patient_id)
    
    # Lấy danh sách các mũi tiêm, sắp xếp mũi mới nhất lên đầu
    history = ImmunizationRecord.query.filter_by(patient_id=patient_id).order_by(ImmunizationRecord.injection_date.desc()).all()
    
    # Lấy danh sách các lịch hẹn sắp tới (nếu có)
    appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.scheduled_date.asc()).all()
    
    return render_template('patient_history.html', 
                           patient=patient, 
                           history=history, 
                           appointments=appointments)

# cập nhật phản ứng sau khi tiêm 
@app.route('/update_reaction/<int:record_id>', methods=['POST'])
def update_reaction(record_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Lấy bản ghi tiêm chủng từ database
    record = ImmunizationRecord.query.get_or_404(record_id)
    
    # Cập nhật phản ứng từ form textarea
    record.reaction = request.form.get('reaction')
    
    try:
        db.session.commit()
        flash('Đã cập nhật tình trạng phản ứng sau tiêm!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Lỗi khi lưu dữ liệu!', 'danger')
        
    return redirect(url_for('inject'))

# nhắc hẹn tiêm mũi tiếp theo 
@app.route('/appointments')
def manage_appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    today = datetime.now().date()
    # Lấy các hẹn trong vòng 7 ngày tới
    upcoming_date = today + timedelta(days=7)
    
    appointments = ImmunizationRecord.query.filter(
        ImmunizationRecord.next_appointment >= today,
        ImmunizationRecord.next_appointment <= upcoming_date
    ).all()
    
    return render_template('appointments.html', appointments=appointments, today=today)

@app.route('/search')
def search():
    q = request.args.get('query')
    results = Patient.query.filter(Patient.fullname.contains(q) | Patient.phone.contains(q)).all()
    return render_template('search_results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)