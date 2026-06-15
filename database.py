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

    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            device_id TEXT UNIQUE NOT NULL,
            total_points INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS player_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            landmark_id INTEGER NOT NULL,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            quiz_correct BOOLEAN DEFAULT 0,
            points_earned INTEGER DEFAULT 0
        )
    ''')

    # 建立預設管理員帳號 admin / admin123
    from werkzeug.security import generate_password_hash
    try:
        c.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)",
                  ('admin', generate_password_hash('admin123')))
    except sqlite3.IntegrityError:
        pass

    # 插入淡江大學 8 個校園地標
    c.execute("SELECT COUNT(*) FROM landmarks")
    if c.fetchone()[0] == 0:
        tku_landmarks = [
            (
                '驚聲紀念大樓', 'Ching-Sheng Memorial Building',
                25.17550006512008, 121.45133989343178,
                '251新北市淡水區驚聲路 淡江大學校本部（棟別：T）',
                '驚聲紀念大樓是淡江大學的行政核心建築，以創辦人張驚聲博士命名，內設驚聲國際會議廳與文錙音樂廳，是校內最重要的集會與活動場所。',
                "The Ching-Sheng Memorial Building is named after the university's founder, Dr. Chang Ching-Sheng. It houses the Ching-Sheng International Conference Hall and the Wenci Concert Hall.",
                '張驚聲博士於1950年創辦淡江英語專科學校，後逐步發展為今日的淡江大學。驚聲大樓以其名命名，象徵對創校精神的永久紀念。每逢校慶典禮，師生齊聚於此，傳承淡江精神。',
                'uploads/landmark_1_1.jpg',
                '驚聲紀念大樓以誰的名字命名？', '張錙鋒', '張驚聲', '林添福', '張建邦', 'B'
            ),
            (
                '覺生紀念圖書館', 'Chueh-Sheng Memorial Library',
                25.174775074897696, 121.45107287887555,
                '251新北市淡水區英專路151號 淡江大學校本部（棟別：U）',
                '覺生紀念圖書館是淡江大學的知識中心，外型獨特圓弧造型被學生暱稱為「蛋」，1樓設有自習室與古今中外咖啡廳，2樓為大門入口，3樓提供資訊共享區，5樓設有非書資料室與歐盟資訊中心，10樓則是覺生國際會議廳。',
                "Known affectionately as \"The Egg\" for its distinctive curved architecture, the Chueh-Sheng Memorial Library serves as the university's knowledge hub with study rooms, multimedia resources, and the EU Information Center.",
                '圖書館以淡江大學第二任校長張建邦之父張丁壁（字覺生）命名。非書資料室提供全校師生舒適便利的視聽閱覽環境，天氣炎熱時是學生最愛的避暑勝地。',
                'uploads/landmark_2_1.jpg',
                '覺生紀念圖書館被學生暱稱為什麼？', '蛋', '球', '蛋糕', '太空船', 'A'
            ),
            (
                '海事博物館暨黑天鵝展示廳', 'Maritime Museum & Black Swan Gallery',
                25.176205229576397, 121.45042452960224,
                '251新北市淡水區英專路151號 淡江大學校本部（棟別：M）',
                '海事博物館是全台灣唯一設立在大學校園內的海事博物館，收藏豐富的航海文物與船舶模型。同棟的黑天鵝展示廳定期舉辦藝文展覽，是校內重要的文化場域。衛生保健組也設置於此，提供校醫服務。',
                'The Maritime Museum is the only university-based maritime museum in Taiwan, featuring extensive collections of nautical artifacts and ship models. The adjacent Black Swan Gallery hosts regular art exhibitions.',
                '淡江大學設立海事相關科系已有數十年歷史，海事博物館的成立是對這段航海教育傳統的具體見證。館內最珍貴的展品之一是各式精緻的帆船模型，吸引無數訪客駐足欣賞。',
                'uploads/landmark_3_1.jpg',
                '台灣唯一設立在大學校園內的海事博物館在哪裡？', '台灣大學', '成功大學', '淡江大學', '海洋大學', 'C'
            ),
            (
                '書卷廣場', 'Book Square',
                25.17554046619068, 121.45062699443932,
                '新北市淡水區英專路151號 淡江大學校本部中央廣場',
                '書卷廣場是淡江大學最具代表性的地標之一，因廣場中央的書卷造型雕塑而得名，學生暱稱為「蛋捲廣場」。廣場旁設有海報街，是各社團張貼活動資訊的重要看板區，也是校園生活的核心地帶。',
                "Book Square, nicknamed \"Egg Roll Plaza\" by students, is one of TKU's most iconic landmarks. The adjacent Poster Street serves as the main bulletin area for student clubs and campus activities.",
                '書卷廣場見證了淡江大學數十年來的學生生活，無數的社團博覽會、校慶活動、抗議集會都曾在此舉行。對每一位淡江人來說，這裡承載了最珍貴的青春記憶。目前廣場正為75週年校慶全力施工改造中。',
                'uploads/landmark_4_1.jpg',
                '書卷廣場的學生暱稱是什麼？', '書本廣場', '蛋捲廣場', '圓形廣場', '中央廣場', 'B'
            ),
            (
                '文錙藝術中心', 'Wenci Arts Center',
                25.17507179202431, 121.45219130105401,
                '新北市淡水區英專路151號 淡江大學校本部（棟別：Z）',
                '文錙藝術中心是淡江大學的藝術展覽核心場所，定期舉辦各類藝術展覽與文化活動。大樓右側樓梯可通往美食廣場（學生餐廳），兩間自助餐廳CP值極高，是學生用餐的熱門選擇。',
                "The Wenci Arts Center is TKU's primary venue for art exhibitions and cultural events. The staircase on the right side of the building leads to the campus food court, popular among students for its affordable meals.",
                '文錙藝術中心以淡江大學創辦人張驚聲之子張錙鋒命名，長期致力於推廣藝術教育與文化交流，是連結淡江師生與在地藝術社群的重要橋樑。',
                'uploads/landmark_5_1.jpg',
                '文錙藝術中心右側樓梯通往哪裡？', '圖書館', '體育館', '美食廣場', '停車場', 'C'
            ),
            (
                '學生活動中心', 'Student Activity Center',
                25.17475594848653, 121.45033093473897,
                '新北市淡水區英專路151號 淡江大學校本部（棟別：R）',
                '學生活動中心是校內各學生社團的活動據點，也是學生自治組織的辦公所在地。大樓另一側設有郵局，方便師生寄送包裹與辦理郵務，是校園生活機能不可或缺的一環。',
                'The Student Activity Center serves as the hub for student clubs and the student government. A post office is located on the other side of the building, providing convenient postal services for the campus community.',
                '學生活動中心承載了無數淡江人的社團記憶，從熱血的迎新活動到深夜趕製成果展的日子，這裡是許多學生大學生涯中最難忘的地方之一。',
                'uploads/landmark_6_1.jpg',
                '學生活動中心的另一側有什麼設施？', '便利商店', '郵局', '銀行', '診所', 'B'
            ),
            (
                '五虎崗綜合球場', 'Wuhugong Sports Complex',
                25.175608692268412, 121.45386137472526,
                '新北市淡水區英專路151號 淡江大學五虎崗區（棟別：XC）',
                '五虎崗綜合球場位於淡江大學五虎崗區，提供籃球、排球等多種運動場地。從五虎崗機車停車場沿側邊樓梯繼續前行可抵達金雞母，是校園內重要的體育休閒空間。',
                "Located in TKU's Wuhugong area, the Sports Complex offers facilities for basketball, volleyball and more. The side staircase near the motorcycle parking lot leads to the \"Golden Hen\" area of campus.",
                '五虎崗是淡江大學校園地形的重要特色，因地勢起伏如五隻老虎而得名。球場見證了歷屆淡江運動健將的成長，每年系際盃賽事都在此激烈展開。',
                'uploads/landmark_7_1.jpg',
                '五虎崗機車停車場側邊樓梯可通往哪裡？', '圖書館', '金雞母', '海事博物館', '美食廣場', 'B'
            ),
            (
                '覺生綜合大樓', 'Chueh-Sheng Complex Building',
                25.17443460250129, 121.45083835152828,
                '新北市淡水區英專路151號 淡江大學校本部（棟別：I）',
                '覺生綜合大樓與覺生紀念圖書館相鄰，依地理位置常被簡稱為「圖側」。從水源街入口往校內直走即可抵達。雖然部分通識課程會在此開設，且建築外觀看似與圖書館相連，但兩者實際上是各自獨立、互不相通的大樓喔！',
                'Adjacent to the main library, the Chueh-Sheng Complex houses a variety of facilities, including a café, study rooms, an information sharing zone, and the EU Information Center. Additionally, the Chueh-Sheng International Conference Hall is located on the 10th floor.',
                '覺生綜合大樓與圖書館共同構成淡江大學的學術核心區域，非書資料室提供全校師生舒適便利的視聽閱覽環境，是許多學生在考試季最愛窩著讀書的秘密基地。',
                'uploads/landmark_8_1.jpg',
                '覺生綜合大樓 10 樓是什麼設施？', '咖啡廳', '自習室', '覺生國際會議廳', '歐盟資訊中心', 'C'
            ),
        ]
        c.executemany('''
            INSERT INTO landmarks
            (name_zh, name_en, lat, lng, address, description_zh, description_en, history_story,
             image_path, quiz_question, quiz_a, quiz_b, quiz_c, quiz_d, quiz_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tku_landmarks)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("資料庫建立完成！")