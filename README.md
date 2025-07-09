# ♟️ Freestyle Chess

A full-featured Chess960 (Fischer Random) game built in Python using Pygame.  
Freestyle Chess supports randomized starting positions, check/checkmate/stalemate detection, resign buttons, and an intuitive 2D GUI.

---

## 🔥 Features

- ♞ **Chess960 / Fischer Random Logic**  
  Automatically generates valid randomized starting positions with bishops on opposite-colored squares and king between rooks.

- ✅ **Legal Move Validation**  
  All piece movement rules implemented from scratch, including:

  - Pawn movement, capturing, initial double-step
  - Knight, Bishop, Rook, Queen, King movements
  - En Passant (basic logic included)

- ⛔ **Check, Checkmate & Stalemate Detection**  
  Real-time detection of game-ending conditions using simulation of all possible legal moves.

- 🎮 **Graphical Interface**  
  Built with `Pygame`, includes:

  - Interactive square selection
  - Colored overlays for selection and available moves
  - Turn indicator (White / Black)
  - Buttons to resign or restart game

- 🚩 **Resign Mechanism**  
  Each player can resign with a dedicated on-screen button.

---

## 🖥️ Demo

## ![screenshot](res/screenshot.png)

## 🧱 Project Structure

```
Freestyle-Chess/
├── main.py              # Entry point
├── game.py              # Game loop and UI logic
├── chess.py             # Chess960 engine & rules
├── piece.py             # Piece rendering
├── utils.py             # Input helpers
├── res/
│   ├── board.png        # Chess board image
│   ├── pieces.png       # Spritesheet for pieces
│   └── chess_icon.png   # Window icon
```

---

## 🚀 Getting Started

### 1. Install Requirements

```bash
pip install pygame
```

### 2. Run the Game

```bash
python main.py
```

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Pygame** – For rendering, input, and game loop
- **Object-Oriented Design** – Modular class structure for scalability

---

## 📌 To Do / Possible Additions

- [ ] Castling logic for Chess960
- [ ] Highlight checks visually
- [ ] AI Opponent (Minimax / Alpha-Beta)
- [ ] Move history and PGN export

---
