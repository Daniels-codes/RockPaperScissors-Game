# 🎮 Rock Paper Scissors Game 🪨📜✂️

A modern, fun, and visually appealing Rock Paper Scissors game built with **Python** and **Tkinter**!  
Challenge the computer in Easy or Hard mode, enjoy animated buttons, toggle background music, track your stats,  
and customize the look with multiple themes. Perfect for a quick game or flexing your Python skills! 😎

---

## ✨ Features

- **Game Modes**: Choose Easy (random computer moves) or Hard (strategic computer moves).
- **Input Options**: Play with **R/S/P** keys or click rock, paper, scissors images.
- **Themes**: Switch between 5 cool themes — *Default, Forest, Ocean, Sunset, Neon* (featuring a slick `#CCCC00` Theme button in Default! 🌟).
- **Power-Up Mode**: Win **3 times in a row** to double your points! ⚡
- **Leaderboard & Stats**: Track your top streaks and favorite choice (e.g., paper! 📜).
- **Sounds & Animations**: Enjoy click sounds, win/lose/draw effects, and button shake animations.
- **BGM Toggle**: Play or mute background music with a stylish purple button. 🎶
- **Reset Game**: Start over with a single click.

---

## 📦 Setup

**1. Clone the Repository**
```bash
git clone https://github.com/your-username/RockPaperScissors-Game.git
cd RockPaperScissors-Game
```
**2. Install Dependencies**
Ensure Python 3.12+ is installed, then run:
```bash
pip install -r requirements.txt
```
**3. Download Assets folder**    
**4. Run the Game**
```bash
DansRockPaperScissors.py
```

---

## 🎲 How to Play

1. Launch the game and select Easy or Hard mode from the main menu.

1. Choose your move with R (Rock), S (Scissors), or P (Paper) keys, or click the images.

1. Watch the animated VS screen to see if you win, lose, or draw!

1. Check the Leaderboard for your top streaks or Stats for your win rate and favorite choice.

1. Toggle BGM or switch themes with the Change Theme button (rocking that #CCCC00 in Default!).

1. Use Reset Game to clear memory and start over or Quit to exit.

---
## 📂 Project Structure
<pre>
RockPaperScissors-Game/
├── assets/
│   ├── rock.png
│   ├── paper.png
│   ├── scissors.png
│   ├── click.mp3
│   ├── win.wav
│   ├── lose.wav
│   ├── tie.aiff
│   ├── bgm.mp3
├── DansRockPaperScissors.py
├── requirements.txt
├── .gitignore
├── LICENSE
├── README.md
    </pre>
---

## 🛠️ Dependencies  

Python: 3.12 or higher

Pygame: 2.6.0 (for game logic and sound handling)

Pillow: 10.4.0 (for image processing)  

**Install manually with:**
```bash
pip install pygame==2.6.0
Pillow==10.4.0
```
---

## 📝 Notes  

The game generates game_log.csv (for stats/leaderboard) and config.json (for theme persistence) on first run.
These are excluded from the repo via .gitignore.

Tested on Windows; should work on macOS/Linux with proper asset paths.

If you encounter a ModuleNotFoundError for pygame or Pillow, ensure dependencies are installed.

💡 Want to contribute? Fork the repo and submit a pull request with new themes, sounds, or features! 🚀

---

## 📜 License
This project is licensed under the MIT License — see the LICENSE file for details

---

## 🙌 Acknowledgments
Built with ❤️ for a fun, engaging game experience.
Special thanks to:

1. Tkinter for the sleek UI.

2. Pygame for awesome sound effects and music.

3. You, for playing and enjoying this game! 😄
