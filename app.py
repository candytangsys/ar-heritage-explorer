from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from database import init_db, DB_PATH

app = Flask(__name__)
app.secret_key = 'tku-ar-heritage-2026-candy'

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
    return redirect(url_for('game'))

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
@app.route('/ar/marker/<int:landmark_id>')
def ar_marker(landmark_id):
    conn = get_db()
    lm = conn.execute("SELECT * FROM landmarks WHERE id = ?", (landmark_id,)).fetchone()
    conn.close()
    if not lm:
        return "找不到此地標", 404
    return render_template('ar_marker.html', lm=lm)

@app.route('/ar/gps')
def ar_gps():
    conn = get_db()
    landmarks = conn.execute("SELECT id, name_zh, lat, lng FROM landmarks").fetchall()
    conn.close()
    return render_template('ar_gps.html', landmarks=[dict(r) for r in landmarks])

# ── 遊戲系統路由 ──────────────────────────────

@app.route('/game')
def game():
    return render_template('game_start.html')

@app.route('/game/map')
def game_map():
    conn = get_db()
    landmarks = conn.execute("SELECT id, name_zh, name_en, lat, lng FROM landmarks").fetchall()
    conn.close()
    return render_template('game_map.html', landmarks=[dict(r) for r in landmarks])

@app.route('/game/profile')
def game_profile():
    return render_template('game_profile.html')

@app.route('/api/game/register', methods=['POST'])
def game_register():
    data = request.get_json()
    nickname = data.get('nickname', '探索者')
    device_id = data.get('device_id')
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("INSERT INTO players (nickname, device_id) VALUES (?, ?)", (nickname, device_id))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return jsonify({'status': 'ok'})

@app.route('/game/unlock')
def game_unlock_page():
    return render_template('game_unlock.html')

@app.route('/api/game/unlock', methods=['POST'])
def game_unlock():
    data = request.get_json()
    device_id = data.get('device_id')
    landmark_id = data.get('landmark_id')
    quiz_correct = data.get('quiz_correct', False)
    points = 10 + (20 if quiz_correct else 5)
    conn = sqlite3.connect(DB_PATH)
    existing = conn.execute(
        "SELECT id FROM player_progress WHERE device_id=? AND landmark_id=?",
        (device_id, landmark_id)
    ).fetchone()
    bonus = 0
    if not existing:
        conn.execute(
            "INSERT INTO player_progress (device_id, landmark_id, quiz_correct, points_earned) VALUES (?,?,?,?)",
            (device_id, landmark_id, quiz_correct, points)
        )
        conn.execute(
            "UPDATE players SET total_points = total_points + ? WHERE device_id = ?",
            (points, device_id)
        )
        conn.commit()
        earned = points
        total_landmarks = conn.execute("SELECT COUNT(*) FROM landmarks").fetchone()[0]
        unlocked_count = conn.execute(
            "SELECT COUNT(*) FROM player_progress WHERE device_id=?", (device_id,)
        ).fetchone()[0]
        if total_landmarks > 0 and unlocked_count >= total_landmarks:
            bonus = 100
            conn.execute(
                "UPDATE players SET total_points = total_points + 100 WHERE device_id = ?",
                (device_id,)
            )
            conn.commit()
    else:
        earned = 0
    conn.close()
    return jsonify({'status': 'ok', 'points_earned': earned, 'bonus': bonus})

@app.route('/api/game/progress')
def game_progress():
    device_id = request.args.get('device_id')
    conn = get_db()
    player = conn.execute("SELECT * FROM players WHERE device_id=?", (device_id,)).fetchone()
    progress = conn.execute(
        "SELECT landmark_id, quiz_correct, points_earned, unlocked_at FROM player_progress WHERE device_id=?",
        (device_id,)
    ).fetchall()
    total_landmarks = conn.execute("SELECT COUNT(*) FROM landmarks").fetchone()[0]
    conn.close()
    if not player:
        return jsonify({'error': 'player not found'}), 404
    unlocked_ids = [p['landmark_id'] for p in progress]
    return jsonify({
        'nickname': player['nickname'],
        'total_points': player['total_points'],
        'unlocked': unlocked_ids,
        'total_landmarks': total_landmarks,
        'progress': [dict(p) for p in progress]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)