from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from database import init_db, DB_PATH

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

class Admin(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username FROM admins WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return Admin(row[0], row[1])
    return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ── 使用者頁面 ──────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/landmark/<int:landmark_id>')
def landmark(landmark_id):
    conn = get_db()
    lm = conn.execute("SELECT * FROM landmarks WHERE id = ?", (landmark_id,)).fetchone()
    conn.close()
    if not lm:
        return "找不到此地標", 404
    return render_template('landmark.html', lm=lm)

@app.route('/api/landmarks')
def api_landmarks():
    conn = get_db()
    rows = conn.execute("SELECT id, name_zh, name_en, lat, lng, image_path FROM landmarks").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ── 管理員頁面 ──────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        row = conn.execute("SELECT * FROM admins WHERE username = ?", (username,)).fetchone()
        conn.close()
        if row and check_password_hash(row['password_hash'], password):
            login_user(Admin(row['id'], row['username']))
            return redirect(url_for('admin_dashboard'))
        flash('帳號或密碼錯誤')
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    conn = get_db()
    landmarks = conn.execute("SELECT * FROM landmarks ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template('admin_dashboard.html', landmarks=landmarks)

@app.route('/admin/landmark/new', methods=['GET', 'POST'])
@login_required
def admin_new():
    if request.method == 'POST':
        return save_landmark(None)
    return render_template('admin_form.html', lm=None)

@app.route('/admin/landmark/<int:lm_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit(lm_id):
    conn = get_db()
    lm = conn.execute("SELECT * FROM landmarks WHERE id = ?", (lm_id,)).fetchone()
    conn.close()
    if request.method == 'POST':
        return save_landmark(lm_id)
    return render_template('admin_form.html', lm=lm)

@app.route('/admin/landmark/<int:lm_id>/delete', methods=['POST'])
@login_required
def admin_delete(lm_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM landmarks WHERE id = ?", (lm_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

def save_landmark(lm_id):
    f = request.form
    image_path = None

    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f'uploads/{filename}'

    conn = sqlite3.connect(DB_PATH)
    if lm_id is None:
        conn.execute('''
            INSERT INTO landmarks (name_zh, name_en, lat, lng, address,
            description_zh, description_en, history_story, image_path,
            quiz_question, quiz_a, quiz_b, quiz_c, quiz_d, quiz_answer)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (f['name_zh'], f['name_en'], f['lat'], f['lng'], f['address'],
              f['description_zh'], f['description_en'], f['history_story'],
              image_path, f['quiz_question'], f['quiz_a'], f['quiz_b'],
              f['quiz_c'], f['quiz_d'], f['quiz_answer']))
    else:
        if image_path:
            conn.execute('''
                UPDATE landmarks SET name_zh=?, name_en=?, lat=?, lng=?, address=?,
                description_zh=?, description_en=?, history_story=?, image_path=?,
                quiz_question=?, quiz_a=?, quiz_b=?, quiz_c=?, quiz_d=?, quiz_answer=?
                WHERE id=?
            ''', (f['name_zh'], f['name_en'], f['lat'], f['lng'], f['address'],
                  f['description_zh'], f['description_en'], f['history_story'],
                  image_path, f['quiz_question'], f['quiz_a'], f['quiz_b'],
                  f['quiz_c'], f['quiz_d'], f['quiz_answer'], lm_id))
        else:
            conn.execute('''
                UPDATE landmarks SET name_zh=?, name_en=?, lat=?, lng=?, address=?,
                description_zh=?, description_en=?, history_story=?,
                quiz_question=?, quiz_a=?, quiz_b=?, quiz_c=?, quiz_d=?, quiz_answer=?
                WHERE id=?
            ''', (f['name_zh'], f['name_en'], f['lat'], f['lng'], f['address'],
                  f['description_zh'], f['description_en'], f['history_story'],
                  f['quiz_question'], f['quiz_a'], f['quiz_b'],
                  f['quiz_c'], f['quiz_d'], f['quiz_answer'], lm_id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)