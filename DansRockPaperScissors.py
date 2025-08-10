import tkinter as tk
from PIL import Image, ImageTk
import pygame
import random
import csv
import os
import json
from datetime import datetime

# Initialize pygame mixer
try:
    pygame.mixer.init()
    print("Pygame mixer initialized.")
except Exception as e:
    print(f"Failed to initialize mixer: {e}")

# Tkinter setup
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("600x500")

# Asset paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")
print(f"Asset path: {ASSETS}")

# Theme definitions
themes = {
    "Default": {
        "bg": "#1e1e2f",
        "fg": "white",
        "buttons": {
            "easy": "#4CAF50",
            "hard": "#f44336",
            "leaderboard": "#2196F3",
            "stats": "#FFC107",
            "reset": "#FF5722",
            "bgm": "#9C27B0",
            "theme": "#FF4081",
            "quit": "#555",
            "back": "#555"
        },
        "highlight": "#FFD700",
        "power_up": "#FF4500"
    },
    "Forest": {
        "bg": "#2e3b2b",
        "fg": "white",
        "buttons": {
            "easy": "#4CAF50",
            "hard": "#689F38",
            "leaderboard": "#8BC34A",
            "stats": "#AED581",
            "reset": "#7CB342",
            "bgm": "#558B2F",
            "theme": "#66BB6A",
            "quit": "#424242",
            "back": "#424242"
        },
        "highlight": "#DCE775",
        "power_up": "#FF7043"
    },
    "Ocean": {
        "bg": "#1e3a5f",
        "fg": "white",
        "buttons": {
            "easy": "#4FC3F7",
            "hard": "#0288D1",
            "leaderboard": "#0277BD",
            "stats": "#4DD0E1",
            "reset": "#039BE5",
            "bgm": "#26A69A",
            "theme": "#4DB6AC",
            "quit": "#455A64",
            "back": "#455A64"
        },
        "highlight": "#B3E5FC",
        "power_up": "#FF8A80"
    },
    "Sunset": {
        "bg": "#3c2f2f",
        "fg": "white",
        "buttons": {
            "easy": "#FF7043",
            "hard": "#D81B60",
            "leaderboard": "#F06292",
            "stats": "#FFCA28",
            "reset": "#F57C00",
            "bgm": "#EC407A",
            "theme": "#FF8A65",
            "quit": "#5D4037",
            "back": "#5D4037"
        },
        "highlight": "#FFCCBC",
        "power_up": "#FF1744"
    },
    "Neon": {
        "bg": "#121212",
        "fg": "white",
        "buttons": {
            "easy": "#00E676",
            "hard": "#FF1744",
            "leaderboard": "#00B0FF",
            "stats": "#CCCC00",
            "reset": "#FF9100",
            "bgm": "#F50057",
            "theme": "#00E676",
            "quit": "#424242",
            "back": "#424242"
        },
        "highlight": "#76FF03",
        "power_up": "#FF4081"
    }
}

# Load and save theme
def load_theme():
    config_path = os.path.join(BASE_DIR, "config.json")
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("theme", "Default")
    except FileNotFoundError:
        return "Default"

def save_theme(theme_name):
    config_path = os.path.join(BASE_DIR, "config.json")
    try:
        with open(config_path, "w") as f:
            json.dump({"theme": theme_name}, f)
    except Exception as e:
        print(f"Error saving theme: {e}")

# Initialize theme
current_theme = load_theme()
root.configure(bg=themes[current_theme]["bg"])

# Image and sound references
image_refs = {}

def load_image(name, size=None):
    try:
        path = os.path.join(ASSETS, name)
        print(f"Loading image from: {path}")
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        image_refs[name] = photo
        print(f"Loaded image: {name}")
        return photo
    except Exception as e:
        print(f"Image load error: {name} → {e}")
        return None

def load_sound(name):
    try:
        path = os.path.join(ASSETS, name)
        print(f"Loading sound from: {path}")
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"Sound load error: {name} → {e}")
        return None

# Load images
small_image_size = (80, 80)
large_image_size = (120, 120)
rock_img_small = load_image("rock.png", small_image_size)
paper_img_small = load_image("paper.png", small_image_size)
scissors_img_small = load_image("scissors.png", small_image_size)
rock_img_large = load_image("rock.png", large_image_size)
paper_img_large = load_image("paper.png", large_image_size)
scissors_img_large = load_image("scissors.png", large_image_size)
rock_img_anim = load_image("rock.png", (90, 90) if small_image_size == (80, 80) else (130, 130))
paper_img_anim = load_image("paper.png", (90, 90) if small_image_size == (80, 80) else (130, 130))
scissors_img_anim = load_image("scissors.png", (90, 90) if small_image_size == (80, 80) else (130, 130))

images_small = {"rock": rock_img_small, "paper": paper_img_small, "scissors": scissors_img_small}
images_large = {"rock": rock_img_large, "paper": paper_img_large, "scissors": scissors_img_large}
images_anim = {"rock": rock_img_anim, "paper": paper_img_anim, "scissors": scissors_img_anim}

# Load sounds
click_sound = load_sound("click.mp3")
win_sound = load_sound("win.wav")
lose_sound = load_sound("lose.wav")
draw_sound = load_sound("tie.aiff")
bgm = load_sound("bgm.mp3")

# Background music control
bgm_playing = False
if bgm:
    bgm.set_volume(0.5)
    bgm.play(loops=-1)
    bgm_playing = True

# Game variables
choices = ["rock", "paper", "scissors"]
scores = {"player": 0, "computer": 0}
win_streak = 0
best_streak = 0
mode = None
is_fullscreen = False
power_up_active = False
game_count = 0
first_game = True

# Game logic
def get_computer_choice(player_choice):
    if mode == "Easy":
        return random.choice(choices)
    else:
        counter = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
        lose = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        return counter[player_choice] if random.random() < 0.66 else lose[player_choice]

def get_result(p, c):
    global win_streak, best_streak, power_up_active, game_count
    game_count += 1
    if p == c:
        win_streak = 0
        if draw_sound: draw_sound.play()
        return "Draw"
    elif (p == "rock" and c == "scissors") or (p == "paper" and c == "rock") or (p == "scissors" and c == "paper"):
        scores["player"] += (2 if power_up_active else 1)
        win_streak += 1
        best_streak = max(best_streak, win_streak)
        power_up_active = win_streak >= 3
        if win_sound: win_sound.play()
        return "You Win"
    else:
        scores["computer"] += 1
        win_streak = 0
        power_up_active = False
        if lose_sound: lose_sound.play()
        return "You Lose"

def log_game(p, c, result):
    log_path = os.path.join(BASE_DIR, "game_log.csv")
    with open(log_path, "a", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Timestamp", "Player", "Computer", "Result", "Mode", "Player Score", "Computer Score", "Streak"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), p, c, result, mode, scores["player"], scores["computer"], win_streak])

def read_game_log():
    log_path = os.path.join(BASE_DIR, "game_log.csv")
    games = []
    try:
        with open(log_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                games.append(row)
    except FileNotFoundError:
        return []
    return games

def reset_game():
    global scores, win_streak, best_streak, game_count, power_up_active, first_game
    scores = {"player": 0, "computer": 0}
    win_streak = 0
    best_streak = 0
    game_count = 0
    power_up_active = False
    first_game = True
    log_path = os.path.join(BASE_DIR, "game_log.csv")
    try:
        with open(log_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Player", "Computer", "Result", "Mode", "Player Score", "Computer Score", "Streak"])
        print("Game log reset.")
    except Exception as e:
        print(f"Error resetting game log: {e}")
    if mode:
        show_game_screen()
    else:
        show_main_menu()

# UI functions
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def show_input_popup():
    global first_game
    if not first_game:
        return
    first_game = False
    popup = tk.Toplevel(root)
    popup.title("Input Options")
    popup.geometry("300x150")
    popup.configure(bg=themes[current_theme]["bg"])
    popup.transient(root)
    popup.grab_set()
    tk.Label(popup, text="🎮 Input Options 🎮", font=("Helvetica", 14, "bold"), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).pack(pady=10)
    tk.Label(popup, text="Use R (Rock), S (Scissors), P (Paper)\nor click the images to choose!", font=("Helvetica", 12), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).pack(pady=5)
    tk.Button(popup, text="OK", font=("Helvetica", 12), bg=themes[current_theme]["buttons"]["back"], fg=themes[current_theme]["fg"], command=popup.destroy).pack(pady=10)
    popup.update()
    x = root.winfo_x() + (root.winfo_width() - popup.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - popup.winfo_height()) // 2
    popup.geometry(f"+{x}+{y}")

def show_theme_selector():
    popup = tk.Toplevel(root)
    popup.title("Select Theme")
    popup.geometry("400x300")
    popup.configure(bg=themes[current_theme]["bg"])
    popup.transient(root)
    popup.grab_set()
    tk.Label(popup, text="🎨 Choose Theme 🎨", font=("Helvetica", 14, "bold"), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).pack(pady=10)

    frame = tk.Frame(popup, bg=themes[current_theme]["bg"])
    frame.pack(pady=10)

    def apply_theme(theme_name):
        global current_theme
        current_theme = theme_name
        save_theme(theme_name)
        popup.destroy()
        if mode:
            show_game_screen()
        else:
            show_main_menu()

    for i, (theme_name, theme) in enumerate(themes.items()):
        tk.Button(frame, text=theme_name, font=("Helvetica", 12), bg=theme["bg"], fg=theme["fg"],
                  command=lambda t=theme_name: apply_theme(t)).grid(row=i, column=0, padx=10, pady=5, sticky="ew")

    tk.Button(popup, text="Cancel", font=("Helvetica", 12), bg=themes[current_theme]["buttons"]["back"], fg=themes[current_theme]["fg"], command=popup.destroy).pack(pady=10)
    popup.update()
    x = root.winfo_x() + (root.winfo_width() - popup.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - popup.winfo_height()) // 2
    popup.geometry(f"+{x}+{y}")

def show_main_menu():
    clear_screen()
    root.unbind("<KeyPress>")
    root.configure(bg=themes[current_theme]["bg"])
    font_size = 24 if is_fullscreen else 20
    pady_val = 40 if is_fullscreen else 30
    tk.Label(root, text="🎮 Rock Paper Scissors 🎮", font=("Helvetica", font_size, "bold"), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).pack(pady=pady_val)

    frame = tk.Frame(root, bg=themes[current_theme]["bg"])
    frame.pack(pady=20)

    btn_width = 20 if is_fullscreen else 15
    btn_font = ("Helvetica", 16 if is_fullscreen else 14)
    padx_val = 15 if is_fullscreen else 10
    pady_val = 15 if is_fullscreen else 10

    tk.Button(frame, text="😊 Easy Mode", font=btn_font, width=btn_width, bg=themes[current_theme]["buttons"]["easy"], fg=themes[current_theme]["fg"],
              command=lambda: start_game("Easy")).grid(row=0, column=0, padx=padx_val, pady=pady_val)
    tk.Button(frame, text="😈 Hard Mode", font=btn_font, width=btn_width, bg=themes[current_theme]["buttons"]["hard"], fg=themes[current_theme]["fg"],
              command=lambda: start_game("Hard")).grid(row=0, column=1, padx=padx_val, pady=pady_val)

    tk.Button(frame, text="🏆 Leaderboard", font=btn_font, width=btn_width, bg=themes[current_theme]["buttons"]["leaderboard"], fg=themes[current_theme]["fg"],
              command=show_leaderboard).grid(row=1, column=0, padx=padx_val, pady=pady_val)
    tk.Button(frame, text="📊 Stats", font=btn_font, width=btn_width, bg=themes[current_theme]["buttons"]["stats"], fg=themes[current_theme]["fg"],
              command=show_stats).grid(row=1, column=1, padx=padx_val, pady=pady_val)

    tk.Button(frame, text="🔄 Reset Game", font=btn_font, width=btn_width, bg=themes[current_theme]["buttons"]["reset"], fg=themes[current_theme]["fg"],
              command=reset_game).grid(row=2, column=0, padx=padx_val, pady=pady_val)
    tk.Button(frame, text="🔊 Play BGM" if not bgm_playing else "🔇 Mute BGM", font=btn_font, width=btn_width, bg=themes[current_theme]["buttons"]["bgm"], fg=themes[current_theme]["fg"],
              command=toggle_bgm).grid(row=2, column=1, padx=padx_val, pady=pady_val)

    theme_frame = tk.Frame(root, bg=themes[current_theme]["bg"])
    theme_frame.pack(pady=10)
    tk.Button(theme_frame, text="🎨 Change Theme", font=btn_font, width=btn_width, bg=themes[current_theme]["buttons"]["theme"], fg=themes[current_theme]["fg"],
              command=show_theme_selector).pack()

    tk.Button(root, text="❌ Quit", font=("Helvetica", 14 if is_fullscreen else 12), width=10, bg=themes[current_theme]["buttons"]["quit"], fg=themes[current_theme]["fg"],
              command=root.quit).pack(pady=10)

def toggle_bgm():
    global bgm_playing
    if bgm:
        if bgm_playing:
            bgm.stop()
            bgm_playing = False
        else:
            bgm.play(loops=-1)
            bgm_playing = True
    show_main_menu()

def show_leaderboard():
    clear_screen()
    root.unbind("<KeyPress>")
    root.configure(bg=themes[current_theme]["bg"])
    font_size = 24 if is_fullscreen else 20
    pady_val = 20 if is_fullscreen else 10
    tk.Label(root, text="🏆 Leaderboard 🏆", font=("Helvetica", font_size, "bold"), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).pack(pady=pady_val)

    games = read_game_log()
    games.sort(key=lambda x: int(x["Streak"]), reverse=True)
    top_games = games[:5]

    frame = tk.Frame(root, bg=themes[current_theme]["bg"])
    frame.pack(pady=10)
    tk.Label(frame, text="Date | Player | Comp. | Result | Mode | Score | Streak", font=("Helvetica", 12 if is_fullscreen else 10),
             fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).grid(row=0, column=0, pady=5)
    for i, game in enumerate(top_games, 1):
        text = f"{game['Timestamp']} | {game['Player']} | {game['Computer']} | {game['Result']} | {game['Mode']} | {game['Player Score']}-{game['Computer Score']} | {game['Streak']}"
        tk.Label(frame, text=text, font=("Helvetica", 10 if is_fullscreen else 8), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).grid(row=i, column=0, pady=2)

    tk.Button(root, text="🔙 Back to Menu", font=("Helvetica", 14 if is_fullscreen else 12), bg=themes[current_theme]["buttons"]["back"], fg=themes[current_theme]["fg"],
              command=show_main_menu).pack(pady=20)

def show_stats():
    clear_screen()
    root.unbind("<KeyPress>")
    root.configure(bg=themes[current_theme]["bg"])
    font_size = 24 if is_fullscreen else 20
    pady_val = 20 if is_fullscreen else 10
    tk.Label(root, text="📊 Game Stats 📊", font=("Helvetica", font_size, "bold"), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).pack(pady=pady_val)

    games = read_game_log()
    total_games = len(games)
    wins = sum(1 for g in games if g["Result"] == "You Win")
    losses = sum(1 for g in games if g["Result"] == "You Lose")
    draws = sum(1 for g in games if g["Result"] == "Draw")
    choices_made = [g["Player"] for g in games]
    favorite_choice = max(set(choices_made), key=choices_made.count, default="None") if choices_made else "None"
    win_rate = (wins / total_games * 100) if total_games > 0 else 0

    frame = tk.Frame(root, bg=themes[current_theme]["bg"])
    frame.pack(pady=10)
    stats = [
        f"Total Games: {total_games}",
        f"Wins: {wins} ({win_rate:.1f}%)",
        f"Losses: {losses}",
        f"Draws: {draws}",
        f"Favorite Choice: {favorite_choice.capitalize()}"
    ]
    for i, stat in enumerate(stats):
        tk.Label(frame, text=stat, font=("Helvetica", 12 if is_fullscreen else 10), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).grid(row=i, column=0, pady=2)

    tk.Button(root, text="🔙 Back to Menu", font=("Helvetica", 14 if is_fullscreen else 12), bg=themes[current_theme]["buttons"]["back"], fg=themes[current_theme]["fg"],
              command=show_main_menu).pack(pady=20)

def show_game_screen():
    clear_screen()
    root.configure(bg=themes[current_theme]["bg"])
    images = images_large if is_fullscreen else images_small
    images_anim_choice = images_anim
    font_size_large = 18 if is_fullscreen else 16
    font_size_small = 16 if is_fullscreen else 14
    pady_val = 15 if is_fullscreen else 10
    padx_val = 10

    show_input_popup()

    main_frame = tk.Frame(root, bg=themes[current_theme]["bg"])
    main_frame.pack(expand=True, fill="both", pady=pady_val)

    tk.Label(main_frame, text=f"Mode: {mode}", font=("Helvetica", font_size_large), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"]).pack(pady=pady_val)
    score_label = tk.Label(main_frame, text=f"Player: {scores['player']}  Computer: {scores['computer']}",
                           font=("Helvetica", font_size_large), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"])
    score_label.pack()

    streak_label = tk.Label(main_frame, text=f"Streak: {win_streak}  Best: {best_streak}", font=("Helvetica", font_size_small),
                            fg=themes[current_theme]["highlight"], bg=themes[current_theme]["bg"])
    streak_label.pack()

    power_up_label = tk.Label(main_frame, text="⚡ Power-Up Active!" if power_up_active else "", font=("Helvetica", font_size_small),
                              fg=themes[current_theme]["power_up"], bg=themes[current_theme]["bg"])
    power_up_label.pack()

    result_images_frame = tk.Frame(main_frame, bg=themes[current_theme]["bg"])
    result_images_frame.pack(pady=pady_val, fill="x")

    player_img_label = tk.Label(result_images_frame, bg=themes[current_theme]["bg"])
    player_img_label.pack(side="left", padx=padx_val, expand=True)

    vs_label = tk.Label(result_images_frame, text="VS", font=("Helvetica", 24 if is_fullscreen else 20, "bold"),
                        fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"])
    vs_label.pack(side="left", expand=True)

    computer_img_label = tk.Label(result_images_frame, bg=themes[current_theme]["bg"])
    computer_img_label.pack(side="left", padx=padx_val, expand=True)

    result_label = tk.Label(main_frame, text="", font=("Helvetica", 20 if is_fullscreen else 18), fg=themes[current_theme]["fg"], bg=themes[current_theme]["bg"])
    result_label.pack(pady=pady_val)

    choice_frame = tk.Frame(main_frame, bg=themes[current_theme]["bg"])
    choice_frame.pack(pady=pady_val, fill="x")

    def animate_button(btn, choice, callback):
        btn.config(image=images_anim_choice[choice])
        root.after(200, lambda: btn.config(image=images[choice]))
        callback()

    def animate_choice_labels():
        def shake(label, count=3):
            if count == 0:
                label.configure(padx=padx_val, pady=pady_val)
                return
            label.configure(padx=padx_val + (5 if count % 2 else -5), pady=pady_val)
            root.after(50, lambda: shake(label, count - 1))
        shake(player_img_label)
        shake(computer_img_label)

    def make_choice(player_choice):
        if click_sound:
            click_sound.play()
        computer_choice = get_computer_choice(player_choice)
        result = get_result(player_choice, computer_choice)

        if images[player_choice]:
            player_img_label.config(image=images[player_choice])
            player_img_label.image = images[player_choice]
        else:
            player_img_label.config(image="", text=player_choice.capitalize(), fg=themes[current_theme]["fg"], font=("Helvetica", font_size_small))

        if images[computer_choice]:
            computer_img_label.config(image=images[computer_choice])
            computer_img_label.image = images[computer_choice]
        else:
            computer_img_label.config(image="", text=computer_choice.capitalize(), fg=themes[current_theme]["fg"], font=("Helvetica", font_size_small))

        animate_choice_labels()
        result_label.config(text=result)
        score_label.config(text=f"Player: {scores['player']}  Computer: {scores['computer']}")
        streak_label.config(text=f"Streak: {win_streak}  Best: {best_streak}")
        power_up_label.config(text="⚡ Power-Up Active!" if power_up_active else "")
        log_game(player_choice, computer_choice, result)

    choice_buttons = {}
    for choice in choices:
        if images[choice] is not None:
            btn = tk.Button(choice_frame, image=images[choice], bg=themes[current_theme]["bg"], bd=0)
            btn.image = images[choice]
            btn.config(command=lambda c=choice, b=btn: animate_button(b, c, lambda: make_choice(c)))
            btn.pack(side="left", padx=padx_val, expand=True)
            choice_buttons[choice] = btn
        else:
            print(f"Image for '{choice}' is not loaded.")

    def handle_key(event):
        key = event.keysym.lower()
        key_to_choice = {"r": "rock", "s": "scissors", "p": "paper"}
        if key in key_to_choice and key_to_choice[key] in choice_buttons:
            choice = key_to_choice[key]
            animate_button(choice_buttons[choice], choice, lambda: make_choice(choice))

    root.bind("<KeyPress>", handle_key)

    tk.Button(main_frame, text="🔙 Back to Menu", font=("Helvetica", 14 if is_fullscreen else 12), bg=themes[current_theme]["buttons"]["back"], fg=themes[current_theme]["fg"],
              command=show_main_menu).pack(pady=20)

def start_game(selected_mode):
    global mode
    mode = selected_mode
    show_game_screen()

def update_layout(event=None):
    global is_fullscreen
    new_is_fullscreen = root.winfo_width() >= 800
    if new_is_fullscreen != is_fullscreen:
        is_fullscreen = new_is_fullscreen
        if mode:
            show_game_screen()
        else:
            show_main_menu()

root.bind("<Configure>", update_layout)

# Start the game
show_main_menu()
root.mainloop()
