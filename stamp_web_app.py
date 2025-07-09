from flask import Flask, render_template, jsonify, request
import json
import random
from datetime import datetime
import os

app = Flask(__name__)

# グローバル変数でスタンプを管理
stamps = []
stories = [
    "昔々、小さな村に心優しい少女が住んでいました。彼女は毎日森で動物たちと遊んでいました。",
    "ある日、魔法使いのおじいさんが村にやってきて、不思議な種を少女にくれました。",
    "その種を植えると、一晩で美しい花が咲き、花からは甘い香りがしました。",
    "花の香りにつられて、森の動物たちが集まってきて、みんなで楽しいお茶会をしました。",
    "お茶会の最後に、動物たちは少女に特別な贈り物をくれました。それは友情の証でした。",
    "遠い星から来た小さな宇宙人が、地球の美しさに感動して涙を流しました。",
    "海の底に住む人魚が、陸の世界を見たくて魔法の薬を飲みました。",
    "雲の上に住む天使が、人間の優しさを学ぶために地上に降りてきました。",
    "古い図書館で、本の中の登場人物たちが夜中に動き回っていました。",
    "時計屋のおじいさんが作った特別な時計は、幸せな時間だけを刻んでいました。"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/place_stamp', methods=['POST'])
def place_stamp():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    
    stamp_types = ["⭐", "🌸", "💖", "🎈", "🌈", "🎀", "🦋", "🌺", "✨", "🎁"]
    colors = ["red", "blue", "green", "purple", "orange", "pink", "gold", "cyan"]
    
    stamp_emoji = random.choice(stamp_types)
    stamp_color = random.choice(colors)
    
    stamp_info = {
        'id': len(stamps) + 1,
        'x': x,
        'y': y,
        'emoji': stamp_emoji,
        'color': stamp_color,
        'timestamp': datetime.now().isoformat()
    }
    
    stamps.append(stamp_info)
    
    return jsonify({
        'success': True,
        'stamp': stamp_info,
        'total_count': len(stamps)
    })

@app.route('/api/get_stamps')
def get_stamps():
    return jsonify({
        'stamps': stamps,
        'total_count': len(stamps)
    })

@app.route('/api/clear_stamps', methods=['POST'])
def clear_stamps():
    global stamps
    stamps = []
    return jsonify({'success': True, 'total_count': 0})

@app.route('/api/get_story')
def get_story():
    if len(stamps) == 0:
        return jsonify({'error': 'まずはスタンプを置いてください！'})
    
    story_index = len(stamps) % len(stories)
    story = stories[story_index]
    
    if len(stamps) >= 10:
        bonus_message = f"\n\n🎉 すごい！{len(stamps)}個のスタンプを集めました！"
        story += bonus_message
    
    return jsonify({
        'story': story,
        'stamp_count': len(stamps)
    })

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    try:
        data = {
            'stamps': stamps,
            'total_count': len(stamps),
            'last_saved': datetime.now().isoformat()
        }
        with open('stamp_progress.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True, 'message': 'スタンプコレクションを保存しました！'})
    except Exception as e:
        return jsonify({'error': f'保存に失敗しました: {str(e)}'})

@app.route('/api/load_progress', methods=['POST'])
def load_progress():
    global stamps
    try:
        with open('stamp_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            stamps = data.get('stamps', [])
            return jsonify({
                'success': True,
                'stamps': stamps,
                'total_count': len(stamps),
                'message': 'データを読み込みました！'
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