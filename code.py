import streamlit as st
import random

# --- Minimax Algorithm ---
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == "X":
        return -10 + depth  # X is the human player
    if winner == "O":
        return 10 - depth  # O is the AI player
    if is_board_full(board):
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = ""
        return best
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = ""
        return best

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    return None

def is_board_full(board):
    return all(board[i][j] != "" for i in range(3) for j in range(3))

def best_move(board):
    best_val = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                move_val = minimax(board, 0, False)
                board[i][j] = ""
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move

# --- Streamlit UI ---
st.title("Tic-Tac-Toe with Minimax AI")
st.write("Play Tic-Tac-Toe against the computer. You play as 'X', and the AI plays as 'O'.")

if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "X"  # Player starts as 'X'
    st.session_state.winner = None

# Draw the Tic-Tac-Toe grid
board = st.session_state.board
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        if cols[j].button(board[i][j] if board[i][j] != "" else "", key=f"{i}-{j}"):
            if board[i][j] == "" and st.session_state.winner is None:
                # Player move
                board[i][j] = "X"
                st.session_state.turn = "O"
                st.session_state.winner = check_winner(board)
                if not st.session_state.winner and not is_board_full(board):
                    # AI move
                    ai_move = best_move(board)
                    board[ai_move[0]][ai_move[1]] = "O"
                    st.session_state.turn = "X"
                    st.session_state.winner = check_winner(board)

# Display winner message
if st.session_state.winner:
    if st.session_state.winner == "X":
        st.success("🎉 You win!")
    elif st.session_state.winner == "O":
        st.success("🤖 AI wins!")
    else:
        st.success("It's a draw!")
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]  # Reset the board
    st.session_state.winner = None
    st.session_state.turn = "X"  # Reset turn to player
