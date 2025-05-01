import streamlit as st
import numpy as np

# --- Page Config (MUST be first Streamlit command) ---
st.set_page_config(page_title="Tic-Tac-Toe", layout="wide")

# --- Minimax Algorithm ---
def minimax(board, depth, is_maximizing):
    # Check for terminal states (win, loss, or draw)
    winner = check_winner(board)
    if winner == 1:
        return 1  # Maximizing (AI) win
    if winner == -1:
        return -1  # Minimizing (Player) win
    if all(cell != 0 for row in board for cell in row):  # Draw condition
        return 0

    # Maximizing Player (AI)
    if is_maximizing:
        best = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:  # If the cell is empty, make a move
                    board[i][j] = 1  # AI move
                    best = max(best, minimax(board, depth + 1, False))  # Recursively call minimax
                    board[i][j] = 0  # Undo the move
        return best
    # Minimizing Player (Human)
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = -1  # Human move
                    best = min(best, minimax(board, depth + 1, True))  # Recursively call minimax
                    board[i][j] = 0  # Undo the move
        return best

def best_move(board):
    best_val = -float('inf')
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:  # If the cell is empty, try the move
                board[i][j] = 1  # AI move
                move_val = minimax(board, 0, False)  # Minimax for AI
                board[i][j] = 0  # Undo the move
                if move_val > best_val:  # Maximize AI's score
                    best_val = move_val
                    move = (i, j)  # Best move for AI
    return move

def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for row in board:
        if row[0] == row[1] == row[2] != 0:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return 0

# --- UI for Game ---
def draw_board(board):
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            cell_key = f'{i}-{j}'  # Use a unique key for each button
            if board[i][j] == 1:
                cols[j].button('X', key=f'{cell_key}-X', disabled=True, use_container_width=True)
            elif board[i][j] == -1:
                cols[j].button('O', key=f'{cell_key}-O', disabled=True, use_container_width=True)
            else:
                if cols[j].button(' ', key=cell_key, use_container_width=True):
                    board[i][j] = 1  # Player move
                    if check_winner(board) == 0:
                        ai_move(board)  # AI moves if game is not over
                    break  # Exit the loop once a valid move is made

def ai_move(board):
    move = best_move(board)  # Get the best move from minimax
    board[move[0], move[1]] = -1  # Update the board with 'O' (AI's move)

# --- Session State for Board Management ---
if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)

board = st.session_state.board

# --- Game Title ---
st.title("🎮 Tic-Tac-Toe with Minimax AI")

# --- Draw the Board ---
draw_board(board)

# --- Check Game Status ---
winner = check_winner(board)
if winner == 1:
    st.success("🎉 You win!")
elif winner == -1:
    st.success("😱 AI wins!")
elif all(board[i][j] != 0 for i in range(3) for j in range(3)):
    st.warning("It's a draw!")
