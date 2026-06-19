from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import math
from database import init_db, DB_PATH

# 解鎖距離門檻（公尺）：GPS 距地標多近才算「抵達現場」
UNLOCK_RADIUS_M = 50

def haversine_m(lat1, lng1, lat2, lng2):
    """兩組經緯度的地表距離（公尺）"""
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

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

# 點數規則：到現場解鎖 +30，答對歷史題額外 +10，全蒐集 +100
UNLOCK_POINTS = 30
QUIZ_BONUS_POINTS = 10

@app.route('/api/game/unlock', methods=['POST'])
def game_unlock():
    """定位解鎖：玩家須在地標 UNLOCK_RADIUS_M 公尺內（GPS 或 AR 鏡頭掃描皆走此判定）"""
    data = request.get_json()
    device_id = data.get('device_id')
    landmark_id = data.get('landmark_id')
    user_lat = data.get('lat')
    user_lng = data.get('lng')

    conn = sqlite3.connect(DB_PATH)
    lm = conn.execute("SELECT lat, lng FROM landmarks WHERE id=?", (landmark_id,)).fetchone()
    if not lm:
        conn.close()
        return jsonify({'status': 'error', 'message': '找不到此地標'}), 404

    # 距離驗證（伺服器端，避免直接呼叫 API 作弊）
    if user_lat is None or user_lng is None:
        conn.close()
        return jsonify({'status': 'no_location', 'message': '需要定位資訊才能解鎖'}), 400
    dist = haversine_m(float(user_lat), float(user_lng), lm[0], lm[1])
    if dist > UNLOCK_RADIUS_M:
        conn.close()
        return jsonify({'status': 'too_far', 'distance': round(dist),
                        'radius': UNLOCK_RADIUS_M, 'message': '尚未抵達地標範圍'})

    existing = conn.execute(
        "SELECT id FROM player_progress WHERE device_id=? AND landmark_id=?",
        (device_id, landmark_id)
    ).fetchone()
    bonus = 0
    if not existing:
        conn.execute(
            "INSERT INTO player_progress (device_id, landmark_id, quiz_correct, points_earned) VALUES (?,?,?,?)",
            (device_id, landmark_id, False, UNLOCK_POINTS)
        )
        conn.execute(
            "UPDATE players SET total_points = total_points + ? WHERE device_id = ?",
            (UNLOCK_POINTS, device_id)
        )
        conn.commit()
        earned = UNLOCK_POINTS
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

@app.route('/api/game/quiz', methods=['POST'])
def game_quiz():
    """歷史小測驗加分：地標須已解鎖；答對 +QUIZ_BONUS_POINTS，每個地標僅計一次"""
    data = request.get_json()
    device_id = data.get('device_id')
    landmark_id = data.get('landmark_id')
    is_correct = bool(data.get('quiz_correct', False))

    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT id, quiz_correct FROM player_progress WHERE device_id=? AND landmark_id=?",
        (device_id, landmark_id)
    ).fetchone()
    if not row:
        conn.close()
        return jsonify({'status': 'locked', 'message': '請先到現場解鎖此地標'}), 403

    already_correct = bool(row[1])
    awarded = 0
    if is_correct and not already_correct:
        awarded = QUIZ_BONUS_POINTS
        conn.execute("UPDATE player_progress SET quiz_correct=1, points_earned=points_earned+? WHERE id=?",
                     (awarded, row[0]))
        conn.execute("UPDATE players SET total_points = total_points + ? WHERE device_id = ?",
                     (awarded, device_id))
        conn.commit()
    conn.close()
    return jsonify({'status': 'ok', 'correct': is_correct,
                    'points_earned': awarded, 'already_correct': already_correct})

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