from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime, date
import random

app = Flask(__name__)
CORS(app)

# Data file path
PROGRESS_FILE = "gargle_progress.json"

def load_progress():
    """Load progress from file or create new progress"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "total_days": 0,
            "streak": 0,
            "last_gargle_date": None,
            "stamps": [],
            "selected_stamps": {},  # 日付 -> スタンプリストのマッピング
            "daily_stamp_count": {},  # 日付 -> スタンプ数のマッピング
            "stories_heard": 0
        }

def save_progress(progress):
    """Save progress to file"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def get_ai_story():
    """Get a random AI story"""
    stories = [
        {
            "title": "おひさまとお花のお話",
            "content": "昔々、小さなお花が咲いていました。🌸 お花は毎日おひさまに「おはよう！」と元気に挨拶をしていました。☀️ おひさまも嬉しくて、お花をあたたかく照らしてくれました。そして、お花はどんどん大きくなって、とても美しく咲きました。✨ 毎日の挨拶が、素敵な友情を育んだのです。"
        },
        {
            "title": "森の動物たちのお話",
            "content": "森に住む動物たちは、みんなで仲良く暮らしていました。🐰🦌🐿️ うさぎさんは人参を分けてくれて、りすさんはドングリをくれました。🥕🌰 みんなで助け合って、とても幸せな毎日を送っていました。そして、困った時はいつも助け合うことを約束しました。💕"
        },
        {
            "title": "雲の上のお話",
            "content": "空の上に住む雲さんは、毎日いろんな形に変身していました。☁️ 今日は犬さんの形、明日は猫さんの形になって、下にいる子供たちを喜ばせていました。🐕🐱 雲さんは「みんなが笑顔になってくれると嬉しいな」と思いながら、今日も空を飛んでいます。✈️"
        },
        {
            "title": "魔法のお星さまのお話",
            "content": "夜空に光る小さなお星さまは、実は魔法の力を持っていました。⭐ お星さまは、頑張っている子供たちに特別な夢を送ってくれます。✨ 今夜もお星さまが輝いて、あなたの夢を見守ってくれています。眠る前に空を見上げて、お星さまに「ありがとう」と言ってみてくださいね。🌙"
        },
        {
            "title": "虹色の蝶々のお話",
            "content": "ある日、虹色に光る美しい蝶々が花畑に現れました。🦋🌈 蝶々は「みんなで仲良くしよう」というメッセージを運んでいました。お花たちも、蜂さんも、みんなが蝶々を見て笑顔になりました。🐝🌺 蝶々は「優しい心があれば、どこでも虹色の幸せを作れるよ」と教えてくれました。"
        }
    ]
    
    return random.choice(stories)

@app.route('/')
def home():
    """Cute home page with stamp selection and AI stories"""
    return '''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>✨ うがい習慣アプリ ✨</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;600;700&display=swap');
            
            body { 
                font-family: 'Noto Sans JP', sans-serif; 
                max-width: 900px; 
                margin: 0 auto; 
                padding: 20px; 
                background: linear-gradient(135deg, #FFE5F3 0%, #E5F3FF 100%);
                min-height: 100vh;
            }
            
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: white;
                border-radius: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            
            .header h1 {
                font-size: 2.5rem;
                color: #FF6B9D;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            
            .mascot {
                font-size: 4rem;
                margin: 10px 0;
                animation: bounce 2s infinite;
            }
            
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-20px); }
                60% { transform: translateY(-10px); }
            }
            
            .button { 
                padding: 15px 30px; 
                margin: 10px; 
                background: linear-gradient(45deg, #FF6B9D, #FF8FB3);
                color: white; 
                border: none; 
                border-radius: 25px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
                transition: all 0.3s ease;
            }
            
            .button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
            }
            
            .success { 
                background: linear-gradient(45deg, #4CAF50, #8BC34A);
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
            }
            
            .success:hover { 
                box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
            }
            
            .status { 
                padding: 15px; 
                margin: 20px 0; 
                border-radius: 15px; 
                text-align: center;
                font-size: 1.2rem;
                font-weight: 600;
            }
            
            .status.success { 
                background: linear-gradient(45deg, #E8F5E8, #C8E6C9); 
                color: #2E7D32;
                border: 2px solid #4CAF50;
            }
            
            .status.pending { 
                background: linear-gradient(45deg, #FFF3E0, #FFE0B2); 
                color: #E65100;
                border: 2px solid #FF9800;
            }
            
            .hidden { display: none; }
            
            /* Calendar styles */
            .calendar-container { 
                background: white; 
                border-radius: 20px; 
                padding: 25px; 
                margin: 20px 0; 
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            }
            
            .calendar-header { 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                margin-bottom: 25px; 
            }
            
            .calendar-nav { 
                background: linear-gradient(45deg, #FF6B9D, #FF8FB3);
                color: white; 
                border: none; 
                padding: 12px 20px; 
                border-radius: 50px; 
                cursor: pointer;
                font-size: 18px;
                transition: all 0.3s ease;
            }
            
            .calendar-nav:hover { 
                transform: scale(1.1);
            }
            
            .calendar-month { 
                font-size: 1.8rem; 
                font-weight: 700; 
                color: #FF6B9D;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }
            
            .calendar-grid { 
                display: grid; 
                grid-template-columns: repeat(7, 1fr); 
                gap: 3px; 
                background: #F5F5F5; 
                border-radius: 10px;
                padding: 10px;
            }
            
            .calendar-day { 
                background: white; 
                padding: 15px; 
                text-align: center; 
                min-height: 50px; 
                position: relative;
                border-radius: 10px;
                transition: all 0.3s ease;
            }
            
            .calendar-day:hover { 
                background: #F8F9FA;
                transform: scale(1.05);
            }
            
            .calendar-day.other-month { 
                background: #F8F9FA; 
                color: #999; 
            }
            
            .calendar-day.today { 
                background: linear-gradient(45deg, #FFE5F3, #E5F3FF);
                font-weight: bold;
                border: 2px solid #FF6B9D;
            }
            
            .calendar-day.stamped { 
                background: linear-gradient(45deg, #E8F5E8, #C8E6C9);
                border: 2px solid #4CAF50;
            }
            
            .weekday-header { 
                background: linear-gradient(45deg, #FF6B9D, #FF8FB3);
                color: white; 
                padding: 12px; 
                text-align: center; 
                font-weight: 600;
                border-radius: 8px;
            }
            
            .stats-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin: 20px 0; 
            }
            
            .stat-card { 
                background: white; 
                padding: 25px; 
                border-radius: 20px; 
                box-shadow: 0 8px 25px rgba(0,0,0,0.1); 
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 30px rgba(0,0,0,0.15);
            }
            
            .stat-number { 
                font-size: 2.5rem; 
                font-weight: 700; 
                color: #FF6B9D;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }
            
            .stat-label { 
                color: #666; 
                margin-top: 10px;
                font-weight: 600;
            }
            
            /* Stamp selection styles */
            .stamp-selection {
                background: white;
                border-radius: 20px;
                padding: 25px;
                margin: 20px 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                text-align: center;
            }
            
            .stamp-options {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            
            .stamp-option {
                padding: 15px;
                background: #F8F9FA;
                border: 3px solid transparent;
                border-radius: 15px;
                cursor: pointer;
                font-size: 2rem;
                transition: all 0.3s ease;
            }
            
            .stamp-option:hover {
                background: #E3F2FD;
                transform: scale(1.1);
            }
            
            .stamp-option.selected {
                border-color: #FF6B9D;
                background: #FFE5F3;
            }
            
            /* Story styles */
            .story-container {
                background: white;
                border-radius: 20px;
                padding: 25px;
                margin: 20px 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            }
            
            .story-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: #FF6B9D;
                margin-bottom: 15px;
                text-align: center;
            }
            
            .story-content {
                font-size: 1.1rem;
                line-height: 1.6;
                color: #333;
                text-align: justify;
            }
            
            .story-button {
                background: linear-gradient(45deg, #9C27B0, #BA68C8);
                box-shadow: 0 4px 15px rgba(156, 39, 176, 0.3);
            }
            
            .story-button:hover {
                box-shadow: 0 6px 20px rgba(156, 39, 176, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>✨ うがい習慣アプリ ✨</h1>
            <div class="mascot">🦄</div>
        </div>
        
        <div id="status" class="status pending">今日のうがいはまだです 😊</div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="streak">0</div>
                <div class="stat-label">🔥 連続日数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total">0</div>
                <div class="stat-label">⭐ 合計日数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="stories-heard">0</div>
                <div class="stat-label">📚 お話を聞いた回数</div>
            </div>
        </div>
        
        <div class="calendar-container">
            <div class="calendar-header">
                <button class="calendar-nav" onclick="changeMonth(-1)">◀️</button>
                <div class="calendar-month" id="current-month">2025年7月</div>
                <button class="calendar-nav" onclick="changeMonth(1)">▶️</button>
            </div>
            <div class="calendar-grid" id="calendar-grid">
                <!-- Calendar will be populated by JavaScript -->
            </div>
        </div>
        
        <div class="stamp-selection" id="stamp-selection">
            <h3>🎨 今日のスタンプを選んでね！</h3>
            <div class="stamp-options" id="stamp-options">
                <div class="stamp-option" data-stamp="⭐" onclick="selectStamp('⭐')">⭐</div>
                <div class="stamp-option" data-stamp="🌟" onclick="selectStamp('🌟')">🌟</div>
                <div class="stamp-option" data-stamp="💫" onclick="selectStamp('💫')">💫</div>
                <div class="stamp-option" data-stamp="🎉" onclick="selectStamp('🎉')">🎉</div>
                <div class="stamp-option" data-stamp="🎊" onclick="selectStamp('🎊')">🎊</div>
                <div class="stamp-option" data-stamp="🏆" onclick="selectStamp('🏆')">🏆</div>
                <div class="stamp-option" data-stamp="🥇" onclick="selectStamp('🥇')">🥇</div>
                <div class="stamp-option" data-stamp="🎖️" onclick="selectStamp('🎖️')">🎖️</div>
                <div class="stamp-option" data-stamp="🌈" onclick="selectStamp('🌈')">🌈</div>
                <div class="stamp-option" data-stamp="🦄" onclick="selectStamp('🦄')">🦄</div>
                <div class="stamp-option" data-stamp="✨" onclick="selectStamp('✨')">✨</div>
                <div class="stamp-option" data-stamp="💖" onclick="selectStamp('💖')">💖</div>
            </div>
            <div style="margin-top: 20px;">
                <p>選択したスタンプ: <span id="selected-stamps-display">⭐</span></p>
                <p>今日のスタンプ数: <span id="today-stamp-count">0</span> / 5</p>
            </div>
        </div>
        
        <div style="text-align: center;">
            <button id="stamp-btn" class="button" onclick="giveStamp()">🦷 スタンプを追加！ 🦷</button>
            <button id="story-btn" class="button story-button hidden" onclick="getStory()">📖 お話を聞く</button>
            <button id="finish-btn" class="button success hidden" onclick="finishDay()">✅ 今日は完了！</button>
        </div>
        
        <div class="story-container hidden" id="story-container">
            <div class="story-title" id="story-title"></div>
            <div class="story-content" id="story-content"></div>
        </div>
        
        <script>
            let progress = null;
            let currentDate = new Date();
            let selectedStamp = '⭐';
            let todayStamps = [];
            let maxStampsPerDay = 5;
            
            window.onload = function() {
                loadProgress();
                renderCalendar();
                selectStamp('⭐');
            };
            
            function loadProgress() {
                fetch('/api/progress')
                    .then(response => response.json())
                    .then(data => {
                        progress = data.progress;
                        updateUI(data);
                        renderCalendar();
                    });
            }
            
            function updateUI(data) {
                document.getElementById('streak').textContent = data.progress.streak;
                document.getElementById('total').textContent = data.progress.total_days;
                document.getElementById('stories-heard').textContent = data.progress.stories_heard || 0;
                
                const today = new Date().toISOString().split('T')[0];
                todayStamps = data.progress.selected_stamps && data.progress.selected_stamps[today] ? data.progress.selected_stamps[today] : [];
                
                // Update today's stamp count
                document.getElementById('today-stamp-count').textContent = todayStamps.length;
                document.getElementById('selected-stamps-display').textContent = todayStamps.join(' ') || '（まだありません）';
                
                if (todayStamps.length >= maxStampsPerDay) {
                    document.getElementById('status').textContent = '今日はたくさんスタンプを押しました！ 🎉';
                    document.getElementById('status').className = 'status success';
                    document.getElementById('stamp-btn').classList.add('hidden');
                    document.getElementById('story-btn').classList.remove('hidden');
                    document.getElementById('finish-btn').classList.remove('hidden');
                } else if (todayStamps.length > 0) {
                    document.getElementById('status').textContent = `今日は ${todayStamps.length} 個のスタンプを押しました！ 😊`;
                    document.getElementById('status').className = 'status success';
                    document.getElementById('story-btn').classList.remove('hidden');
                } else {
                    document.getElementById('status').textContent = '今日のうがいはまだです 😊';
                    document.getElementById('status').className = 'status pending';
                }
            }
            
            function selectStamp(stamp) {
                selectedStamp = stamp;
                document.querySelectorAll('.stamp-option').forEach(option => {
                    option.classList.remove('selected');
                });
                document.querySelector(`[data-stamp="${stamp}"]`).classList.add('selected');
            }
            
            function renderCalendar() {
                const year = currentDate.getFullYear();
                const month = currentDate.getMonth();
                
                document.getElementById('current-month').textContent = `${year}年${month + 1}月`;
                
                const calendarGrid = document.getElementById('calendar-grid');
                calendarGrid.innerHTML = '';
                
                const weekdays = ['日', '月', '火', '水', '木', '金', '土'];
                weekdays.forEach(day => {
                    const dayHeader = document.createElement('div');
                    dayHeader.className = 'weekday-header';
                    dayHeader.textContent = day;
                    calendarGrid.appendChild(dayHeader);
                });
                
                const firstDay = new Date(year, month, 1);
                const lastDay = new Date(year, month + 1, 0);
                const firstDayOfWeek = firstDay.getDay();
                const daysInMonth = lastDay.getDate();
                
                for (let i = 0; i < firstDayOfWeek; i++) {
                    const emptyDay = document.createElement('div');
                    emptyDay.className = 'calendar-day other-month';
                    calendarGrid.appendChild(emptyDay);
                }
                
                const today = new Date();
                const todayStr = today.toISOString().split('T')[0];
                
                for (let day = 1; day <= daysInMonth; day++) {
                    const dayElement = document.createElement('div');
                    dayElement.className = 'calendar-day';
                    dayElement.textContent = day;
                    
                    const dayDate = new Date(year, month, day);
                    const dayStr = dayDate.toISOString().split('T')[0];
                    
                    if (dayStr === todayStr) {
                        dayElement.classList.add('today');
                    }
                    
                    if (progress && progress.selected_stamps && progress.selected_stamps[dayStr]) {
                        dayElement.classList.add('stamped');
                        
                        // Add multiple stamps
                        const stamps = progress.selected_stamps[dayStr];
                        if (Array.isArray(stamps) && stamps.length > 0) {
                            const stampContainer = document.createElement('div');
                            stampContainer.style.position = 'absolute';
                            stampContainer.style.top = '2px';
                            stampContainer.style.right = '2px';
                            stampContainer.style.fontSize = '12px';
                            stampContainer.style.display = 'flex';
                            stampContainer.style.flexWrap = 'wrap';
                            stampContainer.style.maxWidth = '30px';
                            
                            stamps.forEach(stamp => {
                                const stampElement = document.createElement('span');
                                stampElement.textContent = stamp;
                                stampElement.style.marginRight = '1px';
                                stampContainer.appendChild(stampElement);
                            });
                            
                            dayElement.appendChild(stampContainer);
                        } else if (typeof stamps === 'string') {
                            // Backward compatibility for single stamp
                            const stampElement = document.createElement('div');
                            stampElement.style.position = 'absolute';
                            stampElement.style.top = '5px';
                            stampElement.style.right = '5px';
                            stampElement.style.fontSize = '18px';
                            stampElement.textContent = stamps;
                            dayElement.appendChild(stampElement);
                        }
                    }
                    
                    calendarGrid.appendChild(dayElement);
                }
            }
            
            function changeMonth(direction) {
                currentDate.setMonth(currentDate.getMonth() + direction);
                renderCalendar();
            }
            
            function giveStamp() {
                if (todayStamps.length >= maxStampsPerDay) {
                    alert('今日はもうたくさんスタンプを押しました！ 🎉');
                    return;
                }
                
                fetch('/api/stamp', { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ stamp: selectedStamp })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Success animation
                        document.getElementById('status').innerHTML = '🎉 やったね！スタンプ追加！ 🎉';
                        document.getElementById('status').className = 'status success';
                        setTimeout(() => {
                            loadProgress();
                        }, 1000);
                    } else {
                        alert(data.message);
                    }
                });
            }
            
            function finishDay() {
                fetch('/api/finish-day', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('今日のうがいお疲れ様でした！ 🎉');
                        loadProgress();
                    }
                });
            }
            
            function getStory() {
                fetch('/api/story', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('story-title').textContent = data.story.title;
                        document.getElementById('story-content').textContent = data.story.content;
                        document.getElementById('story-container').classList.remove('hidden');
                        
                        // Scroll to story
                        document.getElementById('story-container').scrollIntoView({ behavior: 'smooth' });
                        
                        // Update stories heard count
                        loadProgress();
                    });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get current progress"""
    progress = load_progress()
    today = date.today().isoformat()
    
    return jsonify({
        "progress": progress,
        "stamped_today": today in progress["stamps"],
        "today": today
    })

@app.route('/api/stamp', methods=['POST'])
def give_stamp():
    """Add stamp for gargling with selected stamp"""
    data = request.json
    selected_stamp = data.get('stamp', '⭐')
    
    progress = load_progress()
    today = date.today().isoformat()
    
    # Initialize structures if needed
    if "selected_stamps" not in progress:
        progress["selected_stamps"] = {}
    if "daily_stamp_count" not in progress:
        progress["daily_stamp_count"] = {}
    
    # Get today's stamps
    today_stamps = progress["selected_stamps"].get(today, [])
    if not isinstance(today_stamps, list):
        # Convert old format to new format
        today_stamps = [today_stamps] if today_stamps else []
    
    # Check if max stamps reached
    if len(today_stamps) >= 5:
        return jsonify({"success": False, "message": "今日はもうたくさんスタンプを押しました！"})
    
    # Add stamp
    today_stamps.append(selected_stamp)
    progress["selected_stamps"][today] = today_stamps
    progress["daily_stamp_count"][today] = len(today_stamps)
    
    # Update stamps list if first stamp of the day
    if today not in progress["stamps"]:
        progress["stamps"].append(today)
        progress["total_days"] += 1
        
        # Update streak
        if progress["last_gargle_date"]:
            last_date = datetime.fromisoformat(progress["last_gargle_date"]).date()
            if (date.today() - last_date).days == 1:
                progress["streak"] += 1
            else:
                progress["streak"] = 1
        else:
            progress["streak"] = 1
        
        progress["last_gargle_date"] = today
    
    save_progress(progress)
    
    return jsonify({
        "success": True, 
        "message": f"スタンプを追加しました！ ({len(today_stamps)}/5)",
        "stamp_count": len(today_stamps)
    })

@app.route('/api/finish-day', methods=['POST'])
def finish_day():
    """Mark day as finished"""
    progress = load_progress()
    today = date.today().isoformat()
    
    # Make sure today is in stamps if has any stamps
    if progress["selected_stamps"].get(today, []):
        if today not in progress["stamps"]:
            progress["stamps"].append(today)
            progress["total_days"] += 1
    
    save_progress(progress)
    
    return jsonify({"success": True, "message": "今日のうがいが完了しました！"})

@app.route('/api/story', methods=['POST'])
def get_story():
    """Get AI story"""
    progress = load_progress()
    
    if "stories_heard" not in progress:
        progress["stories_heard"] = 0
    
    progress["stories_heard"] += 1
    save_progress(progress)
    
    story = get_ai_story()
    
    return jsonify({"story": story})

if __name__ == '__main__':
    print("🌟 Starting Cute Gargle App! 🌟")
    print("Access at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)