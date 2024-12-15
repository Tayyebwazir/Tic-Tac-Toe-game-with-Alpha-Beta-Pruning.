

import tkinter as tk
from tkinter import messagebox

# Constants
PLAYER = 'X'
AI = 'O'
EMPTY = ''

# Initialize the board
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

# Function to check if a player has won
def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Function to check if the board is full
def is_full(board):
    return all(all(cell != EMPTY for cell in row) for row in board)

# Minimax with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, AI):
        return 10 - depth
    if check_winner(board, PLAYER):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Function to find the best move for AI
def best_move():
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                score = minimax(board, 0, False, -float('inf'), float('inf'))
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Function to display the game over message
def show_game_over_message(message, color):
    # Create a popup window
    popup = tk.Toplevel(root)
    popup.title("Game Over")
    popup.geometry("300x300")  # Set window size
    popup.configure(bg=color)
    popup.transient(root)  # Set the popup as a child of the main window
    popup.grab_set()  # Prevent interaction with the main window

    # Add an emoji/icon at the top
    emoji_label = tk.Label(popup, text="🎉", font=("Arial", 50), bg=color, fg="white")
    emoji_label.pack(pady=20)

    # Add the game result message
    message_label = tk.Label(
        popup, text=message, font=("Arial", 24, "bold"), bg=color, fg="white"
    )
    message_label.pack(pady=10)

    # Add a "New Game" button
    new_game_button = tk.Button(
        popup, text="New Game", font=("Arial", 16), bg="navy", fg="white", command=lambda: [popup.destroy(), reset_board()]
    )
    new_game_button.pack(pady=20)

    # Center the popup on the screen
    popup.geometry(f"+{root.winfo_screenwidth()//2-150}+{root.winfo_screenheight()//2-150}")

# GUI Setup
def update_button(i, j):
    global board
    if board[i][j] == EMPTY:
        board[i][j] = PLAYER
        buttons[i][j].config(text=PLAYER, bg="red", fg="white", state=tk.DISABLED)
        if check_winner(board, PLAYER):
            show_game_over_message("You Win!", "green")
            return
        if is_full(board):
            show_game_over_message("It's a Draw!", "gray")
            return

        # AI's turn
        move = best_move()
        if move:
            x, y = move
            board[x][y] = AI
            buttons[x][y].config(text=AI, bg="pink", fg="black", state=tk.DISABLED)
            if check_winner(board, AI):
                show_game_over_message("'AI' Wins", "purple")
                return
        if is_full(board):
            show_game_over_message("It's a Draw!", "gray")
            return

def reset_board():
    global board
    board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", bg="yellow", state=tk.NORMAL)

# Tkinter GUI
root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.config(bg="#F5F5F5", padx=10, pady=10, borderwidth=5, relief="solid")

# Center the window on the screen
root.geometry("+{}+{}".format(root.winfo_screenwidth() // 3, root.winfo_screenheight() // 4))

# Bring the window to the front
root.attributes('-topmost', True)

# Title and header
title_frame = tk.Frame(root, bg="#333", padx=5, pady=5, relief="solid", borderwidth=2)
title_frame.grid(row=0, column=0, columnspan=3, pady=10)

title_label = tk.Label(title_frame, text="Tic-Tac-Toe AI", font=("Arial", 24, "bold"), bg="#333", fg="#FFF")
title_label.pack()

# Add a decorative shape (circles) near the title
shape_frame = tk.Frame(root, bg="#F5F5F5")
shape_frame.grid(row=1, column=0, columnspan=3)
for i in range(3):
    for j in range(3):
        canvas = tk.Canvas(shape_frame, width=20, height=20, bg="#F5F5F5", highlightthickness=0)
        canvas.grid(row=i, column=j, padx=5, pady=5)
        canvas.create_oval(5, 5, 15, 15, fill="yellow", outline="black")

# Subtitle
subtitle_label = tk.Label(root, text="Challenge the unbeatable AI!", font=("Arial", 14), bg="#F5F5F5", fg="#777")
subtitle_label.grid(row=2, column=0, columnspan=3, pady=5)

# Buttons grid with spacing
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", font=("Arial", 20), width=5, height=2,
                                  bg="yellow", command=lambda i=i, j=j: update_button(i, j))
        buttons[i][j].grid(row=i+3, column=j, padx=10, pady=10)  # Added more space with padx and pady

# Reset button
reset_button = tk.Button(root, text="New Game", font=("Arial", 15), command=reset_board, bg="#32CD32", fg="white")
reset_button.grid(row=6, column=0, columnspan=3, pady=10)

# Start the Tkinter main loop
root.mainloop()
