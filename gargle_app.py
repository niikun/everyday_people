import pygame
import json
import os
from datetime import datetime, date
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)

class GargleApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("うがい習慣アプリ")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        
        # Load or create progress data
        self.progress_file = "gargle_progress.json"
        self.load_progress()
        
        # App state
        self.current_screen = "main"
        self.game_available = False
        self.waiting_for_stamp = False
        self.selected_game = None
        self.game_score = 0
        
        # Drawing game state
        self.drawing_points = []
        self.drawing_color = RED
        self.drawing_brush_size = 5
        
        # Memory game state
        self.memory_cards = []
        self.memory_flipped = []
        self.memory_matched = []
        self.memory_first_card = None
        self.memory_second_card = None
        self.memory_flip_time = 0
        
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
    
    def request_stamp(self):
        """Request parent to give stamp for gargling"""
        today = date.today().isoformat()
        
        # Check if already got stamp today
        if today in self.progress["stamps"]:
            return False
        
        self.waiting_for_stamp = True
        self.current_screen = "stamp_request"
        return True
    
    def give_stamp(self):
        """Parent gives stamp for gargling"""
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
            self.waiting_for_stamp = False
            self.current_screen = "stamp_success"
            self.save_progress()
            return True
        return False
    
    def play_simple_game(self):
        """Randomly select and play one of three games"""
        if not self.game_available:
            return
        
        # Randomly select one of three games
        games = ["catching", "memory", "drawing"]
        self.selected_game = random.choice(games)
        
        self.current_screen = "game_intro"
        self.game_available = False
        self.progress["games_played"] += 1
        self.save_progress()
    
    def run_catching_game(self):
        """Simple catching game where child catches falling stars"""
        player_x = SCREEN_WIDTH // 2
        player_y = SCREEN_HEIGHT - 100
        player_size = 50
        
        stars = []
        score = 0
        game_time = 30  # 30 seconds
        start_time = pygame.time.get_ticks()
        
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) / 1000
            
            if elapsed_time >= game_time:
                break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return score
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return score
            
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= 5
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
                player_x += 5
            
            # Add new stars
            if random.randint(1, 20) == 1:
                star_x = random.randint(0, SCREEN_WIDTH - 20)
                stars.append([star_x, 0])
            
            # Update stars
            for star in stars[:]:
                star[1] += 3
                if star[1] > SCREEN_HEIGHT:
                    stars.remove(star)
                
                # Check collision
                if (player_x < star[0] + 20 and player_x + player_size > star[0] and
                    player_y < star[1] + 20 and player_y + player_size > star[1]):
                    stars.remove(star)
                    score += 1
            
            # Draw everything
            self.screen.fill(BLACK)
            
            # Draw player
            pygame.draw.rect(self.screen, BLUE, (player_x, player_y, player_size, player_size))
            
            # Draw stars
            for star in stars:
                pygame.draw.circle(self.screen, YELLOW, (star[0] + 10, star[1] + 10), 10)
            
            # Draw UI
            score_text = self.font.render(f"スコア: {score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            time_left = game_time - elapsed_time
            time_text = self.font.render(f"時間: {time_left:.1f}", True, WHITE)
            self.screen.blit(time_text, (10, 50))
            
            instruction_text = self.small_font.render("矢印キーで移動、星をキャッチしよう！", True, WHITE)
            self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 30))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return score
    
    def run_memory_game(self):
        """Simple memory matching game"""
        # Initialize memory game
        colors = [RED, BLUE, GREEN, YELLOW, PINK, (255, 165, 0)]  # Orange
        self.memory_cards = colors * 2  # 6 pairs
        random.shuffle(self.memory_cards)
        self.memory_flipped = [False] * 12
        self.memory_matched = [False] * 12
        self.memory_first_card = None
        self.memory_second_card = None
        self.memory_flip_time = 0
        
        score = 0
        start_time = pygame.time.get_ticks()
        
        while True:
            current_time = pygame.time.get_ticks()
            
            # Check if all cards are matched
            if all(self.memory_matched):
                elapsed_time = (current_time - start_time) / 1000
                score = max(0, 100 - int(elapsed_time))  # Score based on time
                break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return score
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return score
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle card clicks
                    mouse_x, mouse_y = event.pos
                    card_width = 80
                    card_height = 80
                    margin = 10
                    start_x = (SCREEN_WIDTH - (4 * card_width + 3 * margin)) // 2
                    start_y = (SCREEN_HEIGHT - (3 * card_height + 2 * margin)) // 2
                    
                    for i in range(12):
                        row = i // 4
                        col = i % 4
                        card_x = start_x + col * (card_width + margin)
                        card_y = start_y + row * (card_height + margin)
                        
                        if (card_x <= mouse_x <= card_x + card_width and
                            card_y <= mouse_y <= card_y + card_height and
                            not self.memory_flipped[i] and not self.memory_matched[i]):
                            
                            self.memory_flipped[i] = True
                            
                            if self.memory_first_card is None:
                                self.memory_first_card = i
                            elif self.memory_second_card is None:
                                self.memory_second_card = i
                                self.memory_flip_time = current_time
            
            # Check for matches
            if (self.memory_first_card is not None and self.memory_second_card is not None and
                current_time - self.memory_flip_time > 1000):  # Wait 1 second
                
                if self.memory_cards[self.memory_first_card] == self.memory_cards[self.memory_second_card]:
                    self.memory_matched[self.memory_first_card] = True
                    self.memory_matched[self.memory_second_card] = True
                else:
                    self.memory_flipped[self.memory_first_card] = False
                    self.memory_flipped[self.memory_second_card] = False
                
                self.memory_first_card = None
                self.memory_second_card = None
            
            # Draw everything
            self.screen.fill(BLACK)
            
            # Draw cards
            card_width = 80
            card_height = 80
            margin = 10
            start_x = (SCREEN_WIDTH - (4 * card_width + 3 * margin)) // 2
            start_y = (SCREEN_HEIGHT - (3 * card_height + 2 * margin)) // 2
            
            for i in range(12):
                row = i // 4
                col = i % 4
                card_x = start_x + col * (card_width + margin)
                card_y = start_y + row * (card_height + margin)
                
                if self.memory_matched[i]:
                    # Show matched cards
                    pygame.draw.rect(self.screen, self.memory_cards[i], (card_x, card_y, card_width, card_height))
                elif self.memory_flipped[i]:
                    # Show flipped cards
                    pygame.draw.rect(self.screen, self.memory_cards[i], (card_x, card_y, card_width, card_height))
                else:
                    # Show card backs
                    pygame.draw.rect(self.screen, WHITE, (card_x, card_y, card_width, card_height))
                    pygame.draw.rect(self.screen, BLACK, (card_x, card_y, card_width, card_height), 2)
                    pygame.draw.circle(self.screen, BLACK, (card_x + card_width//2, card_y + card_height//2), 10)
            
            # Draw instructions
            instruction_text = self.small_font.render("同じ色のカードをマッチさせよう！", True, WHITE)
            self.screen.blit(instruction_text, (10, 10))
            
            elapsed_time = (current_time - start_time) / 1000
            time_text = self.small_font.render(f"時間: {elapsed_time:.1f}秒", True, WHITE)
            self.screen.blit(time_text, (10, 40))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return score
    
    def run_drawing_game(self):
        """Simple drawing game"""
        self.drawing_points = []
        self.drawing_color = RED
        self.drawing_brush_size = 5
        
        colors = [RED, BLUE, GREEN, YELLOW, PINK, BLACK]
        brush_sizes = [3, 5, 8, 12]
        
        score = 50  # Base score for participation
        start_time = pygame.time.get_ticks()
        game_time = 60  # 60 seconds
        
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) / 1000
            
            if elapsed_time >= game_time:
                break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return score
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return score
                    elif event.key == pygame.K_c:  # Clear canvas
                        self.drawing_points = []
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    
                    # Check color palette clicks
                    color_y = SCREEN_HEIGHT - 60
                    for i, color in enumerate(colors):
                        color_x = 10 + i * 40
                        if (color_x <= mouse_x <= color_x + 30 and
                            color_y <= mouse_y <= color_y + 30):
                            self.drawing_color = color
                            break
                    
                    # Check brush size clicks
                    brush_y = SCREEN_HEIGHT - 110
                    for i, size in enumerate(brush_sizes):
                        brush_x = 10 + i * 40
                        if (brush_x <= mouse_x <= brush_x + 30 and
                            brush_y <= mouse_y <= brush_y + 30):
                            self.drawing_brush_size = size
                            break
                
                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:  # Left mouse button held
                        mouse_x, mouse_y = event.pos
                        if mouse_y < SCREEN_HEIGHT - 120:  # Don't draw on UI area
                            self.drawing_points.append((mouse_x, mouse_y, self.drawing_color, self.drawing_brush_size))
            
            # Draw everything
            self.screen.fill(WHITE)
            
            # Draw all points
            for point in self.drawing_points:
                x, y, color, size = point
                pygame.draw.circle(self.screen, color, (x, y), size)
            
            # Draw color palette
            color_y = SCREEN_HEIGHT - 60
            for i, color in enumerate(colors):
                color_x = 10 + i * 40
                pygame.draw.rect(self.screen, color, (color_x, color_y, 30, 30))
                if color == self.drawing_color:
                    pygame.draw.rect(self.screen, BLACK, (color_x, color_y, 30, 30), 3)
            
            # Draw brush size options
            brush_y = SCREEN_HEIGHT - 110
            for i, size in enumerate(brush_sizes):
                brush_x = 10 + i * 40
                pygame.draw.circle(self.screen, BLACK, (brush_x + 15, brush_y + 15), size)
                if size == self.drawing_brush_size:
                    pygame.draw.rect(self.screen, RED, (brush_x, brush_y, 30, 30), 2)
            
            # Draw UI text
            instruction_text = self.small_font.render("マウスでお絵かきしよう！ Cキーでクリア", True, BLACK)
            self.screen.blit(instruction_text, (10, 10))
            
            time_left = game_time - elapsed_time
            time_text = self.small_font.render(f"残り時間: {time_left:.1f}秒", True, BLACK)
            self.screen.blit(time_text, (10, 40))
            
            color_text = self.small_font.render("色を選ぼう:", True, BLACK)
            self.screen.blit(color_text, (10, SCREEN_HEIGHT - 85))
            
            brush_text = self.small_font.render("筆のサイズ:", True, BLACK)
            self.screen.blit(brush_text, (10, SCREEN_HEIGHT - 135))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # Bonus points for number of strokes
        score += min(len(self.drawing_points) // 10, 50)
        return score
    
    def draw_main_screen(self):
        """Draw main menu screen"""
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.big_font.render("うがい習慣アプリ", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Progress display
        today = date.today().isoformat()
        stamped_today = today in self.progress["stamps"]
        
        if stamped_today:
            status_text = self.font.render("今日はうがいできました！ ⭐", True, GREEN)
        else:
            status_text = self.font.render("今日のうがいはまだです", True, RED)
        
        status_rect = status_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(status_text, status_rect)
        
        # Stats
        stats_text = self.font.render(f"連続日数: {self.progress['streak']}日", True, BLACK)
        stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(stats_text, stats_rect)
        
        total_text = self.font.render(f"合計日数: {self.progress['total_days']}日", True, BLACK)
        total_rect = total_text.get_rect(center=(SCREEN_WIDTH//2, 290))
        self.screen.blit(total_text, total_rect)
        
        # Buttons
        if not stamped_today:
            button_text = self.font.render("うがいしました（お母さんに押してもらう）", True, WHITE)
            button_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 350, 400, 50)
            pygame.draw.rect(self.screen, BLUE, button_rect)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
        
        if self.game_available:
            game_button_text = self.font.render("ゲームで遊ぶ", True, WHITE)
            game_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 420, 200, 50)
            pygame.draw.rect(self.screen, GREEN, game_button_rect)
            game_text_rect = game_button_text.get_rect(center=game_button_rect.center)
            self.screen.blit(game_button_text, game_text_rect)
        
        # Instructions
        instruction_text = self.small_font.render("ESCキーで終了", True, BLACK)
        self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 30))
    
    def draw_stamp_request_screen(self):
        """Draw stamp request screen"""
        self.screen.fill(PINK)
        
        title_text = self.big_font.render("お母さんへ", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)
        
        message_text = self.font.render("子供がうがいをしました。", True, BLACK)
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH//2, 220))
        self.screen.blit(message_text, message_rect)
        
        message2_text = self.font.render("スタンプを押してください。", True, BLACK)
        message2_rect = message2_text.get_rect(center=(SCREEN_WIDTH//2, 260))
        self.screen.blit(message2_text, message2_rect)
        
        # Stamp button
        stamp_button_text = self.font.render("スタンプを押す", True, WHITE)
        stamp_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 320, 200, 50)
        pygame.draw.rect(self.screen, GREEN, stamp_button_rect)
        stamp_text_rect = stamp_button_text.get_rect(center=stamp_button_rect.center)
        self.screen.blit(stamp_button_text, stamp_text_rect)
        
        # Back button
        back_button_text = self.font.render("戻る", True, WHITE)
        back_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, 390, 100, 40)
        pygame.draw.rect(self.screen, RED, back_button_rect)
        back_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_button_text, back_text_rect)
    
    def draw_stamp_success_screen(self):
        """Draw stamp success screen"""
        self.screen.fill(YELLOW)
        
        title_text = self.big_font.render("よくできました！", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title_text, title_rect)
        
        message_text = self.font.render("スタンプをもらいました ⭐", True, BLACK)
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH//2, 280))
        self.screen.blit(message_text, message_rect)
        
        game_text = self.font.render("ゲームで遊べます！", True, BLACK)
        game_rect = game_text.get_rect(center=(SCREEN_WIDTH//2, 320))
        self.screen.blit(game_text, game_rect)
        
        # Continue button
        continue_button_text = self.font.render("続ける", True, WHITE)
        continue_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 75, 380, 150, 50)
        pygame.draw.rect(self.screen, BLUE, continue_button_rect)
        continue_text_rect = continue_button_text.get_rect(center=continue_button_rect.center)
        self.screen.blit(continue_button_text, continue_text_rect)
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        if self.current_screen == "main":
            today = date.today().isoformat()
            stamped_today = today in self.progress["stamps"]
            
            if not stamped_today:
                button_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 350, 400, 50)
                if button_rect.collidepoint(pos):
                    self.request_stamp()
            
            if self.game_available:
                game_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 420, 200, 50)
                if game_button_rect.collidepoint(pos):
                    self.play_simple_game()
        
        elif self.current_screen == "stamp_request":
            stamp_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 320, 200, 50)
            back_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, 390, 100, 40)
            
            if stamp_button_rect.collidepoint(pos):
                self.give_stamp()
            elif back_button_rect.collidepoint(pos):
                self.current_screen = "main"
                self.waiting_for_stamp = False
        
        elif self.current_screen == "stamp_success":
            continue_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 75, 380, 150, 50)
            if continue_button_rect.collidepoint(pos):
                self.current_screen = "main"
        
        elif self.current_screen == "game_intro":
            start_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 320, 200, 50)
            back_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, 390, 100, 40)
            
            if start_button_rect.collidepoint(pos):
                self.current_screen = "game"
            elif back_button_rect.collidepoint(pos):
                self.current_screen = "main"
                self.game_available = True  # Restore game availability
        
        elif self.current_screen == "game":
            if self.selected_game == "catching":
                score = self.run_catching_game()
            elif self.selected_game == "memory":
                score = self.run_memory_game()
            elif self.selected_game == "drawing":
                score = self.run_drawing_game()
            else:
                score = 0
            
            self.current_screen = "game_result"
            self.game_score = score
    
    def draw_game_result_screen(self):
        """Draw game result screen"""
        self.screen.fill(GREEN)
        
        title_text = self.big_font.render("ゲーム結果", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title_text, title_rect)
        
        score_text = self.font.render(f"スコア: {self.game_score}", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 280))
        self.screen.blit(score_text, score_rect)
        
        if self.game_score >= 10:
            message_text = self.font.render("すごい！上手にできました！", True, BLACK)
        elif self.game_score >= 5:
            message_text = self.font.render("よくできました！", True, BLACK)
        else:
            message_text = self.font.render("がんばりました！", True, BLACK)
        
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH//2, 320))
        self.screen.blit(message_text, message_rect)
        
        # Back button
        back_button_text = self.font.render("メインに戻る", True, WHITE)
        back_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 380, 200, 50)
        pygame.draw.rect(self.screen, BLUE, back_button_rect)
        back_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_button_text, back_text_rect)
    
    def draw_game_intro_screen(self):
        """Draw game introduction screen showing which game was selected"""
        self.screen.fill(PINK)
        
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
        title_text = self.big_font.render("今日のゲーム", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Selected game
        if self.selected_game in game_names:
            game_text = self.font.render(game_names[self.selected_game], True, BLACK)
            game_rect = game_text.get_rect(center=(SCREEN_WIDTH//2, 220))
            self.screen.blit(game_text, game_rect)
            
            desc_text = self.font.render(game_descriptions[self.selected_game], True, BLACK)
            desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH//2, 260))
            self.screen.blit(desc_text, desc_rect)
        
        # Start button
        start_button_text = self.font.render("ゲームスタート！", True, WHITE)
        start_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 320, 200, 50)
        pygame.draw.rect(self.screen, GREEN, start_button_rect)
        start_text_rect = start_button_text.get_rect(center=start_button_rect.center)
        self.screen.blit(start_button_text, start_text_rect)
        
        # Back button
        back_button_text = self.font.render("戻る", True, WHITE)
        back_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, 390, 100, 40)
        pygame.draw.rect(self.screen, RED, back_button_rect)
        back_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_button_text, back_text_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_screen == "game_result":
                        back_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 380, 200, 50)
                        if back_button_rect.collidepoint(event.pos):
                            self.current_screen = "main"
                    else:
                        self.handle_click(event.pos)
            
            # Draw current screen
            if self.current_screen == "main":
                self.draw_main_screen()
            elif self.current_screen == "stamp_request":
                self.draw_stamp_request_screen()
            elif self.current_screen == "stamp_success":
                self.draw_stamp_success_screen()
            elif self.current_screen == "game_intro":
                self.draw_game_intro_screen()
            elif self.current_screen == "game":
                if self.selected_game == "catching":
                    score = self.run_catching_game()
                elif self.selected_game == "memory":
                    score = self.run_memory_game()
                elif self.selected_game == "drawing":
                    score = self.run_drawing_game()
                else:
                    score = 0
                
                self.current_screen = "game_result"
                self.game_score = score
            elif self.current_screen == "game_result":
                self.draw_game_result_screen()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    app = GargleApp()
    app.run()