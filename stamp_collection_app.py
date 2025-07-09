import tkinter as tk
from tkinter import messagebox
import random
import json
from datetime import datetime

class StampCollectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("スタンプコレクション")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f8ff')
        
        self.stamps = []
        self.stories = [
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
        
        self.setup_ui()
        self.load_progress()
        
    def setup_ui(self):
        # タイトル
        title_label = tk.Label(
            self.root, 
            text="スタンプコレクション", 
            font=("Arial", 20, "bold"),
            bg='#f0f8ff',
            fg='#4169e1'
        )
        title_label.pack(pady=10)
        
        # スタンプカウンター
        self.counter_label = tk.Label(
            self.root,
            text="スタンプ数: 0",
            font=("Arial", 14),
            bg='#f0f8ff',
            fg='#333'
        )
        self.counter_label.pack(pady=5)
        
        # キャンバス（スタンプを置く場所）
        self.canvas = tk.Canvas(
            self.root,
            width=700,
            height=400,
            bg='white',
            relief='solid',
            borderwidth=2
        )
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.place_stamp)
        
        # ボタンフレーム
        button_frame = tk.Frame(self.root, bg='#f0f8ff')
        button_frame.pack(pady=10)
        
        # クリアボタン
        clear_btn = tk.Button(
            button_frame,
            text="クリア",
            command=self.clear_stamps,
            font=("Arial", 12),
            bg='#ff6b6b',
            fg='white',
            padx=20
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # ストーリーボタン
        story_btn = tk.Button(
            button_frame,
            text="お話しを聞く",
            command=self.tell_story,
            font=("Arial", 12),
            bg='#4ecdc4',
            fg='white',
            padx=20
        )
        story_btn.pack(side=tk.LEFT, padx=5)
        
        # 保存ボタン
        save_btn = tk.Button(
            button_frame,
            text="保存",
            command=self.save_progress,
            font=("Arial", 12),
            bg='#45b7d1',
            fg='white',
            padx=20
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # 説明ラベル
        instruction_label = tk.Label(
            self.root,
            text="白い画面をクリックしてスタンプを置いてください！",
            font=("Arial", 12),
            bg='#f0f8ff',
            fg='#666'
        )
        instruction_label.pack(pady=5)
        
    def place_stamp(self, event):
        x, y = event.x, event.y
        
        # ランダムなスタンプの種類を選択
        stamp_types = ["⭐", "🌸", "💖", "🎈", "🌈", "🎀", "🦋", "🌺", "✨", "🎁"]
        colors = ["red", "blue", "green", "purple", "orange", "pink", "gold", "cyan"]
        
        stamp_emoji = random.choice(stamp_types)
        stamp_color = random.choice(colors)
        
        # スタンプを描画
        stamp_id = self.canvas.create_text(
            x, y,
            text=stamp_emoji,
            font=("Arial", 20),
            fill=stamp_color,
            tags="stamp"
        )
        
        # スタンプ情報を保存
        stamp_info = {
            'id': stamp_id,
            'x': x,
            'y': y,
            'emoji': stamp_emoji,
            'color': stamp_color,
            'timestamp': datetime.now().isoformat()
        }
        self.stamps.append(stamp_info)
        
        # カウンターを更新
        self.update_counter()
        
        # アニメーション効果
        self.animate_stamp(stamp_id)
        
    def animate_stamp(self, stamp_id):
        # 簡単なアニメーション（少し大きくしてから元に戻す）
        self.canvas.create_oval(
            self.canvas.coords(stamp_id)[0] - 15,
            self.canvas.coords(stamp_id)[1] - 15,
            self.canvas.coords(stamp_id)[0] + 15,
            self.canvas.coords(stamp_id)[1] + 15,
            outline="gold",
            width=3,
            tags="effect"
        )
        # 効果を0.5秒後に消す
        self.root.after(500, lambda: self.canvas.delete("effect"))
        
    def update_counter(self):
        count = len(self.stamps)
        self.counter_label.config(text=f"スタンプ数: {count}")
        
    def clear_stamps(self):
        self.canvas.delete("stamp")
        self.stamps.clear()
        self.update_counter()
        
    def tell_story(self):
        if len(self.stamps) == 0:
            messagebox.showinfo("お話し", "まずはスタンプを置いてください！")
            return
            
        # スタンプの数に応じてストーリーを選択
        story_index = len(self.stamps) % len(self.stories)
        story = self.stories[story_index]
        
        # 特別なメッセージを追加
        if len(self.stamps) >= 10:
            bonus_message = f"\n\n🎉 すごい！{len(self.stamps)}個のスタンプを集めました！"
            story += bonus_message
            
        messagebox.showinfo("ご褒美のお話し", story)
        
    def save_progress(self):
        try:
            data = {
                'stamps': self.stamps,
                'total_count': len(self.stamps),
                'last_saved': datetime.now().isoformat()
            }
            with open('stamp_progress.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("保存完了", "スタンプコレクションを保存しました！")
        except Exception as e:
            messagebox.showerror("エラー", f"保存に失敗しました: {str(e)}")
            
    def load_progress(self):
        try:
            with open('stamp_progress.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.stamps = data.get('stamps', [])
                
                # 保存されたスタンプを復元
                for stamp in self.stamps:
                    stamp_id = self.canvas.create_text(
                        stamp['x'], stamp['y'],
                        text=stamp['emoji'],
                        font=("Arial", 20),
                        fill=stamp['color'],
                        tags="stamp"
                    )
                    stamp['id'] = stamp_id
                    
                self.update_counter()
                
        except FileNotFoundError:
            pass  # ファイルが存在しない場合は何もしない
        except Exception as e:
            messagebox.showerror("エラー", f"データの読み込みに失敗しました: {str(e)}")

def main():
    root = tk.Tk()
    app = StampCollectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()