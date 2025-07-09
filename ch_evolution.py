from flask import Flask, render_template, jsonify, request
import json
import random
from datetime import datetime, timedelta
import calendar
import os

app = Flask(__name__)

# グローバル変数でカレンダースタンプを管理
calendar_stamps = {}  # {date: [stamps]}

# キャラクターの成長段階
CHARACTER_STAGES = [
    {"name": "卵", "emoji": "🥚", "min_stamps": 0, "description": "まだ眠っている卵です"},
    {"name": "ひよこ", "emoji": "🐣", "min_stamps": 10, "description": "可愛いひよこが生まれました！"},
    {"name": "にわとり", "emoji": "🐔", "min_stamps": 30, "description": "立派なにわとりに成長しました"},
    {"name": "鷹", "emoji": "🦅", "min_stamps": 70, "description": "空を舞う鷹に進化しました！"},
    {"name": "フェニックス", "emoji": "🔥", "min_stamps": 150, "description": "伝説のフェニックスに覚醒しました！"},
    {"name": "ドラゴン", "emoji": "🐉", "min_stamps": 300, "description": "最強のドラゴンに進化しました！"}
]

# 成長段階別のストーリー
STAGE_STORIES = {
    "卵": [
        "静かな森の奥で、小さな卵が温かい光に包まれています。",
        "卵の中で、新しい命がゆっくりと育っています。",
        "風が優しく卵を撫でて、愛情を込めて見守っています。"
    ],
    "ひよこ": [
        "ピヨピヨと鳴く可愛いひよこが、初めて世界を見回しています。",
        "ひよこは小さな足で一歩一歩、勇敢に歩き回っています。",
        "温かい陽だまりで、ひよこが気持ちよさそうに羽を広げています。"
    ],
    "にわとり": [
        "立派に成長したにわとりが、朝日と共に元気よく鳴いています。",
        "にわとりは仲間たちと一緒に、広い庭を歩き回っています。",
        "美しい羽根を持つにわとりが、誇らしげに胸を張っています。"
    ],
    "鷹": [
        "空高く舞い上がる鷹が、雲の上を自由に飛び回っています。",
        "鋭い目をした鷹が、遠くの山々を見渡しています。",
        "風に乗って滑空する鷹の姿は、とても勇敢で美しいです。"
    ],
    "フェニックス": [
        "炎に包まれた美しいフェニックスが、夜空を照らしています。",
        "不死鳥フェニックスは、希望の光を世界に届けています。",
        "黄金の羽根を持つフェニックスが、新しい命を与えています。"
    ],
    "ドラゴン": [
        "威厳あふれるドラゴンが、天空を支配しています。",
        "古代の知恵を持つドラゴンが、世界を見守っています。",
        "最強のドラゴンは、すべての生命を慈しんでいます。"
    ]
}

def get_character_stage(total_stamps):
    """スタンプ数に基づいてキャラクターの段階を取得"""
    for stage in reversed(CHARACTER_STAGES):
        if total_stamps >= stage["min_stamps"]:
            return stage
    return CHARACTER_STAGES[0]

def get_total_stamps():
    """全スタンプ数を計算"""
    total = 0
    for stamps in calendar_stamps.values():
        total += len(stamps)
    return total

def get_next_stage_info(current_total):
    """次の段階までの情報を取得"""
    current_stage = get_character_stage(current_total)
    current_index = CHARACTER_STAGES.index(current_stage)
    
    if current_index < len(CHARACTER_STAGES) - 1:
        next_stage = CHARACTER_STAGES[current_index + 1]
        remaining = next_stage["min_stamps"] - current_total
        return {
            "next_stage": next_stage,
            "remaining": remaining,
            "is_max": False
        }
    else:
        return {
            "next_stage": None,
            "remaining": 0,
            "is_max": True
        }

@app.route('/')
def index():
    return render_template('character_evolution.html')

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
    
    # キャラクター情報を取得
    total_stamps = get_total_stamps()
    current_stage = get_character_stage(total_stamps)
    next_info = get_next_stage_info(total_stamps)
    
    return jsonify({
        'calendar': cal,
        'year': year,
        'month': month,
        'month_name': month_name,
        'stamps': month_stamps,
        'character': {
            'stage': current_stage,
            'total_stamps': total_stamps,
            'next_stage_info': next_info
        }
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
    
    # 進化チェック
    total_stamps = get_total_stamps()
    old_stage = get_character_stage(total_stamps - 1)
    new_stage = get_character_stage(total_stamps)
    evolved = old_stage != new_stage
    
    return jsonify({
        'success': True,
        'stamp': stamp_info,
        'date': date_str,
        'day_count': len(calendar_stamps[date_str]),
        'total_stamps': total_stamps,
        'character': {
            'stage': new_stage,
            'evolved': evolved,
            'next_stage_info': get_next_stage_info(total_stamps)
        }
    })

@app.route('/api/get_character_info')
def get_character_info():
    """現在のキャラクター情報を取得"""
    total_stamps = get_total_stamps()
    current_stage = get_character_stage(total_stamps)
    next_info = get_next_stage_info(total_stamps)
    
    return jsonify({
        'stage': current_stage,
        'total_stamps': total_stamps,
        'next_stage_info': next_info,
        'all_stages': CHARACTER_STAGES
    })

@app.route('/api/get_story')
def get_story():
    """現在のキャラクターに応じたストーリーを取得"""
    total_stamps = get_total_stamps()
    
    if total_stamps == 0:
        return jsonify({'error': 'まずはスタンプを置いてキャラクターを育ててください！'})
    
    current_stage = get_character_stage(total_stamps)
    stage_name = current_stage["name"]
    
    stories = STAGE_STORIES.get(stage_name, ["素晴らしい冒険が待っています！"])
    story = random.choice(stories)
    
    # 特別なメッセージを追加
    if total_stamps >= 100:
        story += f"\n\n🎉 {total_stamps}個のスタンプを集めました！{current_stage['name']}はとても幸せそうです！"
    
    return jsonify({
        'story': story,
        'character': current_stage,
        'total_stamps': total_stamps
    })

@app.route('/api/clear_day_stamps/<date>', methods=['POST'])
def clear_day_stamps(date):
    """指定された日のスタンプをクリア"""
    if date in calendar_stamps:
        calendar_stamps[date] = []
    return jsonify({'success': True, 'date': date})

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
            'total_stamps': get_total_stamps(),
            'character_stage': get_character_stage(get_total_stamps()),
            'last_saved': datetime.now().isoformat()
        }
        with open('character_evolution_progress.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True, 'message': 'キャラクターの進捗を保存しました！'})
    except Exception as e:
        return jsonify({'error': f'保存に失敗しました: {str(e)}'})

@app.route('/api/load_progress', methods=['POST'])
def load_progress():
    """進捗を読み込み"""
    global calendar_stamps
    try:
        with open('character_evolution_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            calendar_stamps = data.get('calendar_stamps', {})
            return jsonify({
                'success': True,
                'message': 'キャラクターの進捗を読み込みました！',
                'stamps': calendar_stamps,
                'character': get_character_stage(get_total_stamps())
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