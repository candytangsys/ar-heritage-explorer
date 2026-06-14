#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
淡江大學校園地標批量新增腳本
自動將 8 個地標資料一次性插入資料庫
"""

import sqlite3
from database import DB_PATH

# 地標資料
landmarks_data = [
    {
        'name_zh': '驚聲紀念大樓',
        'name_en': 'Ching-Sheng Memorial Building',
        'lat': 25.17720,
        'lng': 121.44860,
        'address': '新北市淡水區英專路151號 淡江大學校本部（棟別：T）',
        'description_zh': '驚聲紀念大樓是淡江大學的行政核心建築，以創辦人張驚聲博士命名，內設驚聲國際會議廳與文錙音樂廳，是校內最重要的集會與活動場所。',
        'description_en': 'The Ching-Sheng Memorial Building is named after the university\'s founder, Dr. Chang Ching-Sheng. It houses the Ching-Sheng International Conference Hall and the Wenci Concert Hall.',
        'history_story': '張驚聲博士於1950年創辦淡江英語專科學校，後逐步發展為今日的淡江大學。驚聲大樓以其名命名，象徵對創校精神的永久紀念。每逢校慶典禮，師生齊聚於此，傳承淡江精神。',
        'quiz_question': '驚聲紀念大樓以誰的名字命名？',
        'quiz_a': '張錙鋒',
        'quiz_b': '張驚聲',
        'quiz_c': '林添福',
        'quiz_d': '張建邦',
        'quiz_answer': 'B'
    },
    {
        'name_zh': '覺生紀念圖書館',
        'name_en': 'Chueh-Sheng Memorial Library',
        'lat': 25.17658,
        'lng': 121.44750,
        'address': '新北市淡水區英專路151號 淡江大學校本部（棟別：U）',
        'description_zh': '覺生紀念圖書館是淡江大學的知識中心，外型獨特圓弧造型被學生暱稱為「蛋」，館內設有自習室、資訊共享區、歐盟資訊中心及非書資料室，提供舒適的視聽閱覽環境。',
        'description_en': 'Known affectionately as "The Egg" for its distinctive curved architecture, the Chueh-Sheng Memorial Library serves as the university\'s knowledge hub with study rooms, multimedia resources, and the EU Information Center.',
        'history_story': '圖書館以淡江大學第二任校長張建邦之父張丁壁（字覺生）命名。非書資料室提供全校師生舒適便利的視聽閱覽環境，天氣炎熱時是學生最愛的避暑勝地。',
        'quiz_question': '覺生紀念圖書館被學生暱稱為什麼？',
        'quiz_a': '蛋',
        'quiz_b': '球',
        'quiz_c': '蛋糕',
        'quiz_d': '太空船',
        'quiz_answer': 'A'
    },
    {
        'name_zh': '海事博物館暨黑天鵝展示廳',
        'name_en': 'Maritime Museum & Black Swan Gallery',
        'lat': 25.17800,
        'lng': 121.44920,
        'address': '新北市淡水區英專路151號 淡江大學校本部（棟別：M）',
        'description_zh': '海事博物館是全台灣唯一設立在大學校園內的海事博物館，收藏豐富的航海文物與船舶模型。同棟的黑天鵝展示廳定期舉辦藝文展覽，是校內重要的文化場域。衛生保健組也設置於此，提供校醫服務。',
        'description_en': 'The Maritime Museum is the only university-based maritime museum in Taiwan, featuring extensive collections of nautical artifacts and ship models. The adjacent Black Swan Gallery hosts regular art exhibitions.',
        'history_story': '淡江大學設立海事相關科系已有數十年歷史，海事博物館的成立是對這段航海教育傳統的具體見證。館內最珍貴的展品之一是各式精緻的帆船模型，吸引無數訪客駐足欣賞。',
        'quiz_question': '台灣唯一設立在大學校園內的海事博物館在哪裡？',
        'quiz_a': '台灣大學',
        'quiz_b': '成功大學',
        'quiz_c': '淡江大學',
        'quiz_d': '海洋大學',
        'quiz_answer': 'C'
    },
    {
        'name_zh': '書卷廣場（蛋捲廣場）',
        'name_en': 'Book Square (Egg Roll Plaza)',
        'lat': 25.17680,
        'lng': 121.44810,
        'address': '新北市淡水區英專路151號 淡江大學校本部中央廣場',
        'description_zh': '書卷廣場是淡江大學最具代表性的地標之一，因廣場中央的書卷造型雕塑而得名，學生暱稱為「蛋捲廣場」。廣場旁設有海報街，是各社團張貼活動資訊的重要看板區，也是校園生活的核心地帶。',
        'description_en': 'Book Square, nicknamed "Egg Roll Plaza" by students, is one of TKU\'s most iconic landmarks. The adjacent Poster Street serves as the main bulletin area for student clubs and campus activities.',
        'history_story': '書卷廣場見證了淡江大學數十年來的學生生活，無數的社團博覽會、校慶活動、抗議集會都曾在此舉行。對每一位淡江人來說，這裡承載了最珍貴的青春記憶。目前廣場正為75週年校慶全力施工改造中。',
        'quiz_question': '書卷廣場的學生暱稱是什麼？',
        'quiz_a': '書本廣場',
        'quiz_b': '蛋捲廣場',
        'quiz_c': '圓形廣場',
        'quiz_d': '中央廣場',
        'quiz_answer': 'B'
    },
    {
        'name_zh': '文錙藝術中心',
        'name_en': 'Wenci Arts Center',
        'lat': 25.17640,
        'lng': 121.44870,
        'address': '新北市淡水區英專路151號 淡江大學校本部（棟別：Z）',
        'description_zh': '文錙藝術中心是淡江大學的藝術展覽核心場所，定期舉辦各類藝術展覽與文化活動。大樓右側樓梯可通往美食廣場（學生餐廳），兩間自助餐廳CP值極高，是學生用餐的熱門選擇。',
        'description_en': 'The Wenci Arts Center is TKU\'s primary venue for art exhibitions and cultural events. The staircase on the right side of the building leads to the campus food court, popular among students for its affordable meals.',
        'history_story': '文錙藝術中心以淡江大學創辦人張驚聲之子張錙鋒命名，長期致力於推廣藝術教育與文化交流，是連結淡江師生與在地藝術社群的重要橋樑。',
        'quiz_question': '文錙藝術中心右側樓梯通往哪裡？',
        'quiz_a': '圖書館',
        'quiz_b': '體育館',
        'quiz_c': '美食廣場',
        'quiz_d': '停車場',
        'quiz_answer': 'C'
    },
    {
        'name_zh': '學生活動中心',
        'name_en': 'Student Activity Center',
        'lat': 25.17730,
        'lng': 121.44780,
        'address': '新北市淡水區英專路151號 淡江大學校本部（棟別：R）',
        'description_zh': '學生活動中心是校內各學生社團的活動據點，也是學生自治組織的辦公所在地。大樓另一側設有郵局，方便師生寄送包裹與辦理郵務，是校園生活機能不可或缺的一環。',
        'description_en': 'The Student Activity Center serves as the hub for student clubs and the student government. A post office is located on the other side of the building, providing convenient postal services for the campus community.',
        'history_story': '學生活動中心承載了無數淡江人的社團記憶，從熱血的迎新活動到深夜趕製成果展的日子，這裡是許多學生大學生涯中最難忘的地方之一。',
        'quiz_question': '學生活動中心的另一側有什麼設施？',
        'quiz_a': '便利商店',
        'quiz_b': '郵局',
        'quiz_c': '銀行',
        'quiz_d': '診所',
        'quiz_answer': 'B'
    },
    {
        'name_zh': '五虎崗綜合球場',
        'name_en': 'Wuhugong Sports Complex',
        'lat': 25.17550,
        'lng': 121.44650,
        'address': '新北市淡水區英專路151號 淡江大學五虎崗區（棟別：XC）',
        'description_zh': '五虎崗綜合球場位於淡江大學五虎崗區，提供籃球、排球等多種運動場地。從五虎崗機車停車場沿側邊樓梯繼續前行可抵達金雞母，是校園內重要的體育休閒空間。',
        'description_en': 'Located in TKU\'s Wuhugong area, the Sports Complex offers facilities for basketball, volleyball and more. The side staircase near the motorcycle parking lot leads to the "Golden Hen" area of campus.',
        'history_story': '五虎崗是淡江大學校園地形的重要特色，因地勢起伏如五隻老虎而得名。球場見證了歷屆淡江運動健將的成長，每年系際盃賽事都在此激烈展開。',
        'quiz_question': '五虎崗機車停車場側邊樓梯可通往哪裡？',
        'quiz_a': '圖書館',
        'quiz_b': '金雞母',
        'quiz_c': '海事博物館',
        'quiz_d': '美食廣場',
        'quiz_answer': 'B'
    },
    {
        'name_zh': '覺生綜合大樓',
        'name_en': 'Chueh-Sheng Complex Building',
        'lat': 25.17665,
        'lng': 121.44760,
        'address': '新北市淡水區英專路151號 淡江大學校本部（棟別：I）',
        'description_zh': '覺生綜合大樓與覺生紀念圖書館相鄰，1樓設有自習室與古今中外咖啡廳，2樓為大門入口，3樓提供資訊共享區，5樓設有非書資料室與歐盟資訊中心，10樓則是覺生國際會議廳。',
        'description_en': 'Adjacent to the library, the Chueh-Sheng Complex houses a café, study rooms, an information sharing zone, the EU Information Center, and the Chueh-Sheng International Conference Hall on the 10th floor.',
        'history_story': '覺生綜合大樓與圖書館共同構成淡江大學的學術核心區域，非書資料室提供全校師生舒適便利的視聽閱覽環境，是許多學生在考試季最愛窩著讀書的秘密基地。',
        'quiz_question': '覺生綜合大樓 10 樓是什麼設施？',
        'quiz_a': '咖啡廳',
        'quiz_b': '自習室',
        'quiz_c': '覺生國際會議廳',
        'quiz_d': '歐盟資訊中心',
        'quiz_answer': 'C'
    }
]

def add_landmarks():
    """批量新增地標"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        for i, landmark in enumerate(landmarks_data, 1):
            cursor.execute('''
                INSERT INTO landmarks 
                (name_zh, name_en, lat, lng, address, description_zh, description_en,
                 history_story, quiz_question, quiz_a, quiz_b, quiz_c, quiz_d, quiz_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                landmark['name_zh'],
                landmark['name_en'],
                landmark['lat'],
                landmark['lng'],
                landmark['address'],
                landmark['description_zh'],
                landmark['description_en'],
                landmark['history_story'],
                landmark['quiz_question'],
                landmark['quiz_a'],
                landmark['quiz_b'],
                landmark['quiz_c'],
                landmark['quiz_d'],
                landmark['quiz_answer']
            ))
            print(f"✅ 已新增地標 {i}: {landmark['name_zh']}")
        
        conn.commit()
        print(f"\n🎉 成功新增全部 {len(landmarks_data)} 個地標！")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 錯誤: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 50)
    print("淡江大學校園地標批量新增工具")
    print("=" * 50)
    add_landmarks()
