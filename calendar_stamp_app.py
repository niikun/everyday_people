from flask import Flask, render_template, jsonify, request
import json
import random
from datetime import datetime, timedelta
import calendar
import os

app = Flask(__name__)

# グローバル変数でカレンダースタンプを管理
calendar_stamps = {}  # {date: [stamps]}
stories = [
    "今日は素晴らしい一日でした！太陽が輝いて、鳥たちが歌っていました。",
    "今日は新しい発見がありました。小さな花が咲いているのを見つけました。",
    "今日は友達と楽しい時間を過ごしました。笑顔がたくさん生まれました。",
    "今日は頑張った自分にご褒美をあげましょう。お疲れ様でした！",
    "今日は静かな時間を過ごしました。心が落ち着いて穏やかな気持ちです。",
    "今日は冒険の日でした！新しい道を歩いて、素敵な景色を見ました。",
    "今日は感謝の気持ちでいっぱいです。周りの人々に感謝しています。",
    "今日は学びの日でした。新しい知識を身につけることができました。",
    "今日は創造的な一日でした。何か新しいものを作り出すことができました。",
    "今日は愛に満ちた一日でした。大切な人たちを思い出しました。",
    "今日は希望の日です。明日への期待で心が踊っています。",
    "今日は勇気を出した日でした。難しいことにも挑戦できました。",
    "今日は自然を感じた日でした。風や空の美しさに心が癒されました。",
    "今日は成長を実感した日でした。昨日より少し強くなれました。",
    "今日は平和な一日でした。心静かに過ごすことができました。"
]

@app.route('/')
def index():
    return render_template('calendar.html')

@app.route('/api/get_calendar/<int:year>/<int:month>')
def get_calendar(year, month):
    """指定された年月のカレンダーデータを取得"""
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # その月のスタンプデータを取得
    month_stamps = {}
    for date_str, stamps in calendar_stamps.items():
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            if date_obj.year == year and date_obj.month == month:
                month_stamps[date_str] = stamps
        except ValueError:
            continue
    
    return jsonify({
        'calendar': cal,
        'year': year,
        'month': month,
        'month_name': month_name,
        'stamps': month_stamps
    })

@app.route('/api/place_stamp', methods=['POST'])
def place_stamp():
    """指定された日付にスタンプを配置"""
    data = request.get_json()
    date_str = data.get('date')  # YYYY-MM-DD format
    x = data.get('x', 50)
    y = data.get('y', 50)
    
    if not date_str:
        return jsonify({'error': '日付が指定されていません'})
    
    stamp_types = ["⭐", "🌸", "💖", "🎈", "🌈", "🎀", "🦋", "🌺", "✨", "🎁", "🌟", "🌻", "🍀", "🎊", "🎉"]
    colors = ["red", "blue", "green", "purple", "orange", "pink", "gold", "cyan", "magenta", "lime"]
    
    stamp_emoji = random.choice(stamp_types)
    stamp_color = random.choice(colors)
    
    stamp_info = {
        'id': f"{date_str}_{len(calendar_stamps.get(date_str, []))}_",
        'x': x,
        'y': y,
        'emoji': stamp_emoji,
        'color': stamp_color,
        'timestamp': datetime.now().isoformat()
    }
    
    if date_str not in calendar_stamps:
        calendar_stamps[date_str] = []
    
    calendar_stamps[date_str].append(stamp_info)
    
    return jsonify({
        'success': True,
        'stamp': stamp_info,
        'date': date_str,
        'total_count': len(calendar_stamps[date_str])
    })

@app.route('/api/get_day_stamps/<date>')
def get_day_stamps(date):
    """指定された日のスタンプを取得"""
    stamps = calendar_stamps.get(date, [])
    return jsonify({
        'date': date,
        'stamps': stamps,
        'count': len(stamps)
    })

@app.route('/api/clear_day_stamps/<date>', methods=['POST'])
def clear_day_stamps(date):
    """指定された日のスタンプをクリア"""
    if date in calendar_stamps:
        calendar_stamps[date] = []
    return jsonify({'success': True, 'date': date})

@app.route('/api/get_story/<date>')
def get_story(date):
    """指定された日のストーリーを取得"""
    stamps = calendar_stamps.get(date, [])
    
    if len(stamps) == 0:
        return jsonify({'error': 'まずはスタンプを置いてください！'})
    
    # 日付に基づいてストーリーを選択
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        story_index = (date_obj.day + len(stamps)) % len(stories)
        story = stories[story_index]
        
        if len(stamps) >= 5:
            bonus_message = f"\n\n🎉 {date}は{len(stamps)}個のスタンプを集めました！素晴らしい一日でしたね！"
            story += bonus_message
        
        return jsonify({
            'story': story,
            'date': date,
            'stamp_count': len(stamps)
        })
    except ValueError:
        return jsonify({'error': '無効な日付です'})

@app.route('/api/get_monthly_stats/<int:year>/<int:month>')
def get_monthly_stats(year, month):
    """月間統計を取得"""
    total_stamps = 0
    stamped_days = 0
    
    for date_str, stamps in calendar_stamps.items():
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            if date_obj.year == year and date_obj.month == month:
                if len(stamps) > 0:
                    stamped_days += 1
                    total_stamps += len(stamps)
        except ValueError:
            continue
    
    return jsonify({
        'year': year,
        'month': month,
        'total_stamps': total_stamps,
        'stamped_days': stamped_days,
        'month_name': calendar.month_name[month]
    })

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    """進捗を保存"""
    try:
        data = {
            'calendar_stamps': calendar_stamps,
            'last_saved': datetime.now().isoformat()
        }
        with open('calendar_stamp_progress.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True, 'message': 'カレンダーを保存しました！'})
    except Exception as e:
        return jsonify({'error': f'保存に失敗しました: {str(e)}'})

@app.route('/api/load_progress', methods=['POST'])
def load_progress():
    """進捗を読み込み"""
    global calendar_stamps
    try:
        with open('calendar_stamp_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            calendar_stamps = data.get('calendar_stamps', {})
            return jsonify({
                'success': True,
                'message': 'カレンダーを読み込みました！',
                'stamps': calendar_stamps
            })
    except FileNotFoundError:
        return jsonify({'error': 'セーブファイルが見つかりません'})
    except Exception as e:
        return jsonify({'error': f'データの読み込みに失敗しました: {str(e)}'})

if __name__ == '__main__':
    # テンプレートフォルダを作成
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(host='0.0.0.0', port=5000, debug=True)