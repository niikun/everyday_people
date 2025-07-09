#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, canvas
import json
import os
from datetime import datetime, date
import random
import threading
import time

class GargleAppTK:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("うがい習慣アプリ")
        self.root.geometry("800x600")
        self.root.configure(bg='white')
        
        # Load or create progress data
        self.progress_file = "gargle_progress.json"
        self.load_progress()
        
        # App state
        self.game_available = False
        self.selected_game = None
        self.game_score = 0
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.show_main_screen()
        
    def load_progress(self):
        """Load progress from file or create new progress"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                self.progress = json.load(f)
        else:
            self.progress = {
                "total_days": 0,
                "streak": 0,
                "last_gargle_date": None,
                "stamps": [],
                "games_played": 0
            }
    
    def save_progress(self):
        """Save progress to file"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)
    
    def clear_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_main_screen(self):
        """Show main menu screen"""
        self.clear_frame()
        
        # Title
        title_label = tk.Label(self.main_frame, text="うがい習慣アプリ", 
                              font=("Arial", 24, "bold"), bg='white', fg='blue')
        title_label.pack(pady=50)
        
        # Status
        today = date.today().isoformat()
        stamped_today = today in self.progress["stamps"]
        
        if stamped_today:
            status_text = "今日はうがいできました！ ⭐"
            status_color = "green"
        else:
            status_text = "今日のうがいはまだです"
            status_color = "red"
        
        status_label = tk.Label(self.main_frame, text=status_text, 
                               font=("Arial", 16), bg='white', fg=status_color)
        status_label.pack(pady=20)
        
        # Stats
        stats_label = tk.Label(self.main_frame, 
                              text=f"連続日数: {self.progress['streak']}日\\n合計日数: {self.progress['total_days']}日", 
                              font=("Arial", 14), bg='white', fg='black')
        stats_label.pack(pady=20)
        
        # Buttons
        if not stamped_today:
            stamp_button = tk.Button(self.main_frame, text="うがいしました（お母さんに押してもらう）", 
                                   font=("Arial", 14), bg='lightblue', fg='white',
                                   command=self.request_stamp, width=30, height=2)
            stamp_button.pack(pady=10)
        
        if self.game_available:
            game_button = tk.Button(self.main_frame, text="ゲームで遊ぶ", 
                                  font=("Arial", 14), bg='lightgreen', fg='white',
                                  command=self.play_game, width=20, height=2)
            game_button.pack(pady=10)
        
        # Instructions
        instruction_label = tk.Label(self.main_frame, text="Escキーまたは×ボタンで終了", 
                                    font=("Arial", 10), bg='white', fg='gray')
        instruction_label.pack(side=tk.BOTTOM, pady=10)
    
    def request_stamp(self):
        """Request parent to give stamp"""
        today = date.today().isoformat()
        
        if today in self.progress["stamps"]:
            messagebox.showinfo("通知", "今日はもうスタンプをもらっています！")
            return
        
        self.show_stamp_request_screen()
    
    def show_stamp_request_screen(self):
        """Show stamp request screen"""
        self.clear_frame()
        
        # Title
        title_label = tk.Label(self.main_frame, text="お母さんへ", 
                              font=("Arial", 24, "bold"), bg='white', fg='black')
        title_label.pack(pady=50)
        
        # Message
        message_label = tk.Label(self.main_frame, 
                                text="子供がうがいをしました。\\nスタンプを押してください。", 
                                font=("Arial", 16), bg='white', fg='black')
        message_label.pack(pady=30)
        
        # Buttons
        stamp_button = tk.Button(self.main_frame, text="スタンプを押す", 
                               font=("Arial", 14), bg='green', fg='white',
                               command=self.give_stamp, width=20, height=2)
        stamp_button.pack(pady=10)
        
        back_button = tk.Button(self.main_frame, text="戻る", 
                              font=("Arial", 14), bg='red', fg='white',
                              command=self.show_main_screen, width=15, height=2)
        back_button.pack(pady=10)
    
    def give_stamp(self):
        """Give stamp for gargling"""
        today = date.today().isoformat()
        
        if today not in self.progress["stamps"]:
            self.progress["stamps"].append(today)
            self.progress["total_days"] += 1
            
            # Update streak
            if self.progress["last_gargle_date"]:
                last_date = datetime.fromisoformat(self.progress["last_gargle_date"]).date()
                if (date.today() - last_date).days == 1:
                    self.progress["streak"] += 1
                else:
                    self.progress["streak"] = 1
            else:
                self.progress["streak"] = 1
            
            self.progress["last_gargle_date"] = today
            self.game_available = True
            self.save_progress()
            
            self.show_stamp_success_screen()
        else:
            messagebox.showinfo("通知", "今日はもうスタンプをもらっています！")
    
    def show_stamp_success_screen(self):
        """Show stamp success screen"""
        self.clear_frame()
        
        # Title
        title_label = tk.Label(self.main_frame, text="よくできました！", 
                              font=("Arial", 24, "bold"), bg='white', fg='green')
        title_label.pack(pady=50)
        
        # Message
        message_label = tk.Label(self.main_frame, 
                                text="スタンプをもらいました ⭐\\nゲームで遊べます！", 
                                font=("Arial", 16), bg='white', fg='black')
        message_label.pack(pady=30)
        
        # Continue button
        continue_button = tk.Button(self.main_frame, text="続ける", 
                                  font=("Arial", 14), bg='blue', fg='white',
                                  command=self.show_main_screen, width=15, height=2)
        continue_button.pack(pady=20)
    
    def play_game(self):
        """Select and play a random game"""
        if not self.game_available:
            messagebox.showwarning("警告", "ゲームで遊ぶにはスタンプが必要です！")
            return
        
        # Randomly select one of three games
        games = ["catching", "memory", "drawing"]
        self.selected_game = random.choice(games)
        
        self.game_available = False
        self.progress["games_played"] += 1
        self.save_progress()
        
        self.show_game_intro_screen()
    
    def show_game_intro_screen(self):
        """Show game introduction screen"""
        self.clear_frame()
        
        game_names = {
            "catching": "星キャッチゲーム",
            "memory": "メモリーマッチングゲーム", 
            "drawing": "お絵かきゲーム"
        }
        
        game_descriptions = {
            "catching": "落ちてくる星をキャッチしよう！",
            "memory": "同じ色のカードをマッチさせよう！",
            "drawing": "自由にお絵かきしよう！"
        }
        
        # Title
        title_label = tk.Label(self.main_frame, text="今日のゲーム", 
                              font=("Arial", 24, "bold"), bg='white', fg='purple')
        title_label.pack(pady=50)
        
        # Selected game
        if self.selected_game in game_names:
            game_label = tk.Label(self.main_frame, text=game_names[self.selected_game], 
                                 font=("Arial", 18, "bold"), bg='white', fg='blue')
            game_label.pack(pady=20)
            
            desc_label = tk.Label(self.main_frame, text=game_descriptions[self.selected_game], 
                                 font=("Arial", 14), bg='white', fg='black')
            desc_label.pack(pady=10)
        
        # Start button
        start_button = tk.Button(self.main_frame, text="ゲームスタート！", 
                               font=("Arial", 14), bg='green', fg='white',
                               command=self.start_selected_game, width=20, height=2)
        start_button.pack(pady=20)
        
        # Back button
        back_button = tk.Button(self.main_frame, text="戻る", 
                              font=("Arial", 14), bg='red', fg='white',
                              command=self.back_to_main, width=15, height=2)
        back_button.pack(pady=10)
    
    def back_to_main(self):
        """Return to main screen and restore game availability"""
        self.game_available = True
        self.show_main_screen()
    
    def start_selected_game(self):
        """Start the selected game"""
        if self.selected_game == "catching":
            self.play_catching_game()
        elif self.selected_game == "memory":
            self.play_memory_game()
        elif self.selected_game == "drawing":
            self.play_drawing_game()
    
    def play_catching_game(self):
        """Simple catching game simulation"""
        self.clear_frame()
        
        # Title
        title_label = tk.Label(self.main_frame, text="星キャッチゲーム", 
                              font=("Arial", 20, "bold"), bg='white', fg='blue')
        title_label.pack(pady=20)
        
        # Game area
        game_frame = tk.Frame(self.main_frame, bg='black', width=600, height=400)
        game_frame.pack(pady=20)
        game_frame.pack_propagate(False)
        
        # Simple game simulation
        instruction_label = tk.Label(game_frame, text="星をクリックしてキャッチしよう！", 
                                    font=("Arial", 16), bg='black', fg='white')
        instruction_label.pack(pady=50)
        
        # Create stars
        self.stars = []
        for i in range(5):
            star_button = tk.Button(game_frame, text="⭐", font=("Arial", 20),
                                  bg='yellow', command=lambda: self.catch_star())
            star_button.pack(side=tk.LEFT, padx=20, pady=100)
            self.stars.append(star_button)
        
        self.stars_caught = 0
        self.score_label = tk.Label(self.main_frame, text="スコア: 0", 
                                   font=("Arial", 14), bg='white', fg='black')
        self.score_label.pack(pady=10)
        
        # Timer
        self.game_time = 10
        self.timer_label = tk.Label(self.main_frame, text=f"残り時間: {self.game_time}秒", 
                                   font=("Arial", 14), bg='white', fg='red')
        self.timer_label.pack(pady=5)
        
        self.start_game_timer()
    
    def catch_star(self):
        """Catch a star"""
        self.stars_caught += 1
        self.score_label.config(text=f"スコア: {self.stars_caught}")
        
        # Hide caught star
        if self.stars_caught <= len(self.stars):
            self.stars[self.stars_caught - 1].config(state='disabled', bg='gray')
    
    def start_game_timer(self):
        """Start game timer"""
        def countdown():
            time_left = self.game_time
            while time_left > 0:
                self.timer_label.config(text=f"残り時間: {time_left}秒")
                time.sleep(1)
                time_left -= 1
            
            self.game_score = self.stars_caught * 10
            self.show_game_result()
        
        timer_thread = threading.Thread(target=countdown)
        timer_thread.daemon = True
        timer_thread.start()
    
    def play_memory_game(self):
        """Simple memory matching game"""
        self.clear_frame()
        
        # Title
        title_label = tk.Label(self.main_frame, text="メモリーマッチングゲーム", 
                              font=("Arial", 20, "bold"), bg='white', fg='blue')
        title_label.pack(pady=20)
        
        # Instructions
        instruction_label = tk.Label(self.main_frame, text="同じ色のカードを2枚選んでマッチさせよう！", 
                                    font=("Arial", 14), bg='white', fg='black')
        instruction_label.pack(pady=10)
        
        # Game board
        self.game_board = tk.Frame(self.main_frame, bg='white')
        self.game_board.pack(pady=20)
        
        # Create cards
        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange'] * 2
        random.shuffle(colors)
        
        self.cards = []
        self.card_colors = colors
        self.flipped_cards = []
        self.matched_cards = []
        
        for i in range(12):
            row = i // 4
            col = i % 4
            
            card = tk.Button(self.game_board, text="?", font=("Arial", 16),
                           width=4, height=2, bg='lightgray',
                           command=lambda idx=i: self.flip_card(idx))
            card.grid(row=row, column=col, padx=5, pady=5)
            self.cards.append(card)
        
        # Score
        self.matches = 0
        self.match_label = tk.Label(self.main_frame, text="マッチ数: 0", 
                                   font=("Arial", 14), bg='white', fg='black')
        self.match_label.pack(pady=10)
        
        # Back button
        back_button = tk.Button(self.main_frame, text="ゲーム終了", 
                              font=("Arial", 12), bg='red', fg='white',
                              command=self.end_memory_game, width=15)
        back_button.pack(pady=10)
    
    def flip_card(self, index):
        """Flip a card in memory game"""
        if index in self.flipped_cards or index in self.matched_cards:
            return
        
        # Show card color
        self.cards[index].config(bg=self.card_colors[index], text="")
        self.flipped_cards.append(index)
        
        if len(self.flipped_cards) == 2:
            self.root.after(1000, self.check_match)
    
    def check_match(self):
        """Check if flipped cards match"""
        if len(self.flipped_cards) == 2:
            card1, card2 = self.flipped_cards
            
            if self.card_colors[card1] == self.card_colors[card2]:
                # Match found
                self.matched_cards.extend([card1, card2])
                self.matches += 1
                self.match_label.config(text=f"マッチ数: {self.matches}")
                
                if len(self.matched_cards) == 12:
                    self.game_score = self.matches * 10
                    self.show_game_result()
            else:
                # No match - flip cards back
                self.cards[card1].config(bg='lightgray', text="?")
                self.cards[card2].config(bg='lightgray', text="?")
            
            self.flipped_cards = []
    
    def end_memory_game(self):
        """End memory game"""
        self.game_score = self.matches * 10
        self.show_game_result()
    
    def play_drawing_game(self):
        """Simple drawing game"""
        self.clear_frame()
        
        # Title
        title_label = tk.Label(self.main_frame, text="お絵かきゲーム", 
                              font=("Arial", 20, "bold"), bg='white', fg='blue')
        title_label.pack(pady=20)
        
        # Instructions
        instruction_label = tk.Label(self.main_frame, text="マウスでドラッグしてお絵かきしよう！", 
                                    font=("Arial", 14), bg='white', fg='black')
        instruction_label.pack(pady=10)
        
        # Canvas
        self.canvas = tk.Canvas(self.main_frame, width=600, height=400, bg='white', bd=2, relief='sunken')
        self.canvas.pack(pady=20)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        
        self.old_x = None
        self.old_y = None
        
        # Color palette
        color_frame = tk.Frame(self.main_frame, bg='white')
        color_frame.pack(pady=10)
        
        colors = ['black', 'red', 'blue', 'green', 'yellow', 'purple', 'orange']
        self.current_color = 'black'
        
        for color in colors:
            color_button = tk.Button(color_frame, bg=color, width=3, height=1,
                                   command=lambda c=color: self.change_color(c))
            color_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_button = tk.Button(self.main_frame, text="クリア", 
                               font=("Arial", 12), bg='orange', fg='white',
                               command=self.clear_canvas, width=10)
        clear_button.pack(pady=5)
        
        # Finish button
        finish_button = tk.Button(self.main_frame, text="完成！", 
                                font=("Arial", 12), bg='green', fg='white',
                                command=self.finish_drawing, width=10)
        finish_button.pack(pady=5)
    
    def start_draw(self, event):
        """Start drawing"""
        self.old_x = event.x
        self.old_y = event.y
    
    def draw(self, event):
        """Draw on canvas"""
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                  width=3, fill=self.current_color, capstyle=tk.ROUND, smooth=tk.TRUE)
        self.old_x = event.x
        self.old_y = event.y
    
    def change_color(self, color):
        """Change drawing color"""
        self.current_color = color
    
    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.delete("all")
    
    def finish_drawing(self):
        """Finish drawing game"""
        self.game_score = 50  # Base score for participation
        self.show_game_result()
    
    def show_game_result(self):
        """Show game result screen"""
        self.clear_frame()
        
        # Title
        title_label = tk.Label(self.main_frame, text="ゲーム結果", 
                              font=("Arial", 24, "bold"), bg='white', fg='green')
        title_label.pack(pady=50)
        
        # Score
        score_label = tk.Label(self.main_frame, text=f"スコア: {self.game_score}", 
                              font=("Arial", 18), bg='white', fg='black')
        score_label.pack(pady=20)
        
        # Message
        if self.game_score >= 50:
            message = "すごい！上手にできました！"
        elif self.game_score >= 30:
            message = "よくできました！"
        else:
            message = "がんばりました！"
        
        message_label = tk.Label(self.main_frame, text=message, 
                                font=("Arial", 16), bg='white', fg='blue')
        message_label.pack(pady=20)
        
        # Back button
        back_button = tk.Button(self.main_frame, text="メインに戻る", 
                              font=("Arial", 14), bg='blue', fg='white',
                              command=self.show_main_screen, width=20, height=2)
        back_button.pack(pady=30)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GargleAppTK()
    app.run()