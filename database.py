import sqlite3
import os

DB_PATH = 'heritage.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS landmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_zh TEXT NOT NULL,
            name_en TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            address TEXT,
            description_zh TEXT,
            description_en TEXT,
            history_story TEXT,
            image_path TEXT,
            quiz_question TEXT,
            quiz_a TEXT,
            quiz_b TEXT,
            quiz_c TEXT,
            quiz_d TEXT,
            quiz_answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # 建立預設管理員帳號 admin / admin123
    from werkzeug.security import generate_password_hash
    try:
        c.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)",
                  ('admin', generate_password_hash('admin123')))
    except sqlite3.IntegrityError:
        pass

    # 插入一筆範例地標（淡水紅毛城）
    c.execute("SELECT COUNT(*) FROM landmarks")
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO landmarks 
            (name_zh, name_en, lat, lng, address, description_zh, description_en, history_story,
             quiz_question, quiz_a, quiz_b, quiz_c, quiz_d, quiz_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            '淡水紅毛城', 'Fort San Domingo',
            25.1763, 121.4330,
            '新北市淡水區中正路28巷1號',
            '紅毛城是台灣現存最古老的建築之一，建於1629年，歷經西班牙、荷蘭、英國等多國統治。',
            'Fort San Domingo is one of the oldest surviving buildings in Taiwan, built in 1629.',
            '相傳鄭成功曾在此地與荷蘭人談判，要求荷蘭人交出台灣。這段歷史成為台灣最戲劇性的一頁。',
            '紅毛城最初是由哪個國家建造的？',
            '荷蘭', '西班牙', '英國', '葡萄牙', 'B'
        ))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("資料庫建立完成！")