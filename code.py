import streamlit as st
import random

# Initialize game state
if 'board' not in st.session_state:
    st.session_state.board = [' ' for _ in range(9)]  # Empty 3x3 board
    st.session_state.current_player = 'X'  # Player 'X' starts
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.turns = 0

# Function to check if the game has a winner
def check_winner():
    # Check rows, columns, and diagonals
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in winning_combinations:
        if st.session_state.board[combo[0]] == st.session_state.board[combo[1]] == st.session_state.board[combo[2]] != ' ':
            return st.session_state.board[combo[0]]  # Return the winner ('X' or 'O')
    return None

# Minimax algorithm to make the best move for the AI
def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif ' ' not in board:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Function for the AI to make its move
def ai_move():
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if st.session_state.board[i] == ' ':
            st.session_state.board[i] = 'O'
            score = minimax(st.session_state.board, 0, False)
            st.session_state.board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    st.session_state.board[best_move] = 'O'

# Function to handle a player's move
def make_move(index):
    if st.session_state.board[index] == ' ' and not st.session_state.game_over:
        # Player makes the move
        st.session_state.board[index] = st.session_state.current_player
        st.session_state.turns += 1

        # Check for winner after player's move
        winner = check_winner()
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
        elif st.session_state.turns == 9:
            st.session_state.game_over = True  # Game ends in a tie if all spots are filled
            st.session_state.winner = 'Tie'
        else:
            # Switch to AI's turn
            st.session_state.current_player = 'O'
            ai_move()
            # Check for winner after AI's move
            winner = check_winner()
            if winner:
                st.session_state.game_over = True
                st.session_state.winner = winner
            elif st.session_state.turns == 9:
                st.session_state.game_over = True
                st.session_state.winner = 'Tie'
            else:
                # Switch back to player
                st.session_state.current_player = 'X'

# Display the current board
st.title("Tic-Tac-Toe Game")

# Display game status
if st.session_state.game_over:
    if st.session_state.winner == 'Tie':
        st.write("It's a tie!")
    else:
        st.write(f"Player {st.session_state.winner} wins!")
else:
    st.write(f"Player {st.session_state.current_player}'s turn")

# Create buttons for the Tic-Tac-Toe board in a 3x3 grid
col1, col2, col3 = st.columns(3)

# Create buttons in the grid
for i in range(9):
    button_label = st.session_state.board[i]
    
    if i < 3:
        with col1:
            button_label = st.button(button_label if button_label != ' ' else '', key=f"btn_{i}", on_click=make_move, args=(i,))
    elif 3 <= i < 6:
        with col2:
            button_label = st.button(button_label if button_label != ' ' else '', key=f"btn_{i}", on_click=make_move, args=(i,))
    else:
        with col3:
            button_label = st.button(button_label if button_label != ' ' else '', key=f"btn_{i}", on_click=make_move, args=(i,))

# Restart game button
if st.session_state.game_over:
    if st.button("Restart Game"):
        st.session_state.board = [' ' for _ in range(9)]
        st.session_state.current_player = 'X'
        st.session_state.game_over = False
        st.session_state.winner = None
        st.session_state.turns = 0
