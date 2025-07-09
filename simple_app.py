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
            "games_played": 0
        }

def save_progress(progress):
    """Save progress to file"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    """Simple home page"""
    return '''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>うがい習慣アプリ</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
            .button { padding: 15px 30px; margin: 10px; background: #2196F3; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            .button:hover { background: #1976D2; }
            .success { background: #4CAF50; }
            .success:hover { background: #45a049; }
            .status { padding: 10px; margin: 20px 0; border-radius: 5px; }
            .status.success { background: #e8f5e8; color: #4caf50; }
            .status.pending { background: #ffebee; color: #f44336; }
            .hidden { display: none; }
            
            /* Calendar styles */
            .calendar-container { background: white; border-radius: 10px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .calendar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
            .calendar-nav { background: #2196F3; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; }
            .calendar-nav:hover { background: #1976D2; }
            .calendar-month { font-size: 1.5rem; font-weight: bold; color: #333; }
            .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 1px; background: #ddd; border: 1px solid #ddd; }
            .calendar-day { background: white; padding: 10px; text-align: center; min-height: 50px; position: relative; }
            .calendar-day.other-month { background: #f5f5f5; color: #999; }
            .calendar-day.today { background: #e3f2fd; font-weight: bold; }
            .calendar-day.stamped { background: #e8f5e8; }
            .calendar-day.stamped::after { content: "⭐"; position: absolute; top: 5px; right: 5px; font-size: 18px; }
            .weekday-header { background: #2196F3; color: white; padding: 10px; text-align: center; font-weight: bold; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
            .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
            .stat-number { font-size: 2rem; font-weight: bold; color: #2196F3; }
            .stat-label { color: #666; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>うがい習慣アプリ</h1>
        <div id="status" class="status pending">今日のうがいはまだです</div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="streak">0</div>
                <div class="stat-label">連続日数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total">0</div>
                <div class="stat-label">合計日数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="games-played">0</div>
                <div class="stat-label">ゲーム回数</div>
            </div>
        </div>
        
        <div class="calendar-container">
            <div class="calendar-header">
                <button class="calendar-nav" onclick="changeMonth(-1)">◀</button>
                <div class="calendar-month" id="current-month">2025年7月</div>
                <button class="calendar-nav" onclick="changeMonth(1)">▶</button>
            </div>
            <div class="calendar-grid" id="calendar-grid">
                <!-- Calendar will be populated by JavaScript -->
            </div>
        </div>
        
        <div style="text-align: center;">
            <button id="stamp-btn" class="button" onclick="giveStamp()">うがいしました（お母さんに押してもらう）</button>
            <button id="game-btn" class="button success hidden" onclick="selectGame()">ゲームで遊ぶ</button>
        </div>
        
        <script>
            let progress = null;
            let currentDate = new Date();
            
            window.onload = function() {
                loadProgress();
                renderCalendar();
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
                document.getElementById('games-played').textContent = data.progress.games_played;
                
                if (data.stamped_today) {
                    document.getElementById('status').textContent = '今日はうがいできました！ ⭐';
                    document.getElementById('status').className = 'status success';
                    document.getElementById('stamp-btn').classList.add('hidden');
                    document.getElementById('game-btn').classList.remove('hidden');
                }
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
                    
                    if (progress && progress.stamps && progress.stamps.includes(dayStr)) {
                        dayElement.classList.add('stamped');
                    }
                    
                    calendarGrid.appendChild(dayElement);
                }
            }
            
            function changeMonth(direction) {
                currentDate.setMonth(currentDate.getMonth() + direction);
                renderCalendar();
            }
            
            function giveStamp() {
                fetch('/api/stamp', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        if (data.success) {
                            loadProgress();
                        }
                    });
            }
            
            function selectGame() {
                fetch('/api/game/select', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        alert('今日のゲーム: ' + data.game.name + '\\n' + data.game.description);
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
    """Give stamp for gargling"""
    progress = load_progress()
    today = date.today().isoformat()
    
    if today in progress["stamps"]:
        return jsonify({"success": False, "message": "今日はもうスタンプをもらっています！"})
    
    progress["stamps"].append(today)
    progress["total_days"] += 1
    
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
    
    return jsonify({"success": True, "message": "スタンプをもらいました！"})

@app.route('/api/game/select', methods=['POST'])
def select_game():
    """Randomly select a game"""
    games = [
        {"id": "catching", "name": "星キャッチゲーム", "description": "落ちてくる星をキャッチしよう！"},
        {"id": "memory", "name": "メモリーマッチングゲーム", "description": "同じ色のカードをマッチさせよう！"},
        {"id": "drawing", "name": "お絵かきゲーム", "description": "自由にお絵かきしよう！"}
    ]
    
    selected_game = random.choice(games)
    
    progress = load_progress()
    progress["games_played"] += 1
    save_progress(progress)
    
    return jsonify({"game": selected_game})

if __name__ == '__main__':
    print("Starting Flask app...")
    print("Access the app at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)