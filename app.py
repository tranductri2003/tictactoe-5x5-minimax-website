import time
from tictactoe_5x5_computer_first import TicTacToe
import streamlit as st

# Player: X
# Computer: O

# Custom CSS styles for the Tic-Tac-Toe board and move history
CUSTOM_CSS = """
<style>
div.stButton > button {
    font-size: 2em;
    height: 100px;
    width: 100px;
    margin: 5px;
    border: 2px solid #9C27B0;
    border-radius: 10px;
}
div.streamlit-expanderHeader {
    font-size: 1.2em;
}
.sidebar .markdown-text-container {
    font-size: 1.2em;
}
div#header-container {
    text-align: center;
}
</style>
"""

st.set_page_config(page_title="5x5 TicTacToe")

# Define the layout of the page
st.markdown('<div id="header-container"></div>', unsafe_allow_html=True)
st.title('5x5 Tic-Tac-Toe Game')


def draw_tic_tac_toe_board():
    # Iterate over the rows in the board
    for i in range(5):
        # Streamlit columns for each cell
        cols = st.columns(5)
        for j in range(5):
            with cols[j]:
                # Define a unique key for each button using its row and column
                key = f'cell-{i}-{j}'  # Sử dụng index của hàng và cột để tạo key
                # Display a button with the cell value
                if st.button(get_symbol(st.session_state.board[i][j]) or " ", key=key) and st.session_state.current_player == 'X':
                    # Update the last clicked position
                    if st.session_state.board[i][j] == ' ':
                        st.session_state.board[i][j] = 'X' 
                        end_time_player = time.time()
                        st.session_state.move_history.append(f'Turn {len(st.session_state.move_history)+1}: Player move: ({i}, {j}) Thinking time: {end_time_player - st.session_state.start_time_player} seconds')
                        st.session_state.current_player = 'O'
                        st.experimental_rerun()


def get_symbol(value):   #https://emojidb.org/large-blue-circle-emojis
    if value == 'X':
        return '❌'  # Unicode symbol for X
    elif value == 'O':
        return '🔵'  # Unicode symbol for O
    else:
        return ' '  # Space for empty cell

def reset_game():
    game = TicTacToe()
    st.session_state.board = game.board
    st.session_state.current_player = 'O'
    st.session_state.move_history = []

    
# Initialize the board and last clicked position in the session state if they don't exist
if 'board' not in st.session_state:
    reset_game()
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'O'
if 'move_history' not in st.session_state:
    st.session_state.move_history = []
    

# Use Streamlit's markdown to add raw HTML/CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if st.session_state.current_player == 'O':
    game = TicTacToe()
    game.board = st.session_state.board
    
    if game.checkWin('X'):
        st.success("You win!")
        
        st.markdown(
            """
            <style>
            .element-container:has(style){
                display: none;
            }
            #button-after {
                display: none;
            }
            .element-container:has(#button-after) {
                display: none;
            }
            .element-container:has(#button-after) + div button {
                background-color: orange;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
        
        if st.button("Play Again"):
            reset_game()
            st.experimental_rerun()
    else:
        start_time_computer = time.time()
        move = game.computerMove()
        end_time_computer = time.time()
        st.session_state.move_history.append(f'Turn {len(st.session_state.move_history)+1}: Computer move: {move} Thinking time: {end_time_computer - start_time_computer} seconds')

        if game.checkDraw():
            st.success("Draw!")
            
            st.markdown(
                """
                <style>
                .element-container:has(style){
                    display: none;
                }
                #button-after {
                    display: none;
                }
                .element-container:has(#button-after) {
                    display: none;
                }
                .element-container:has(#button-after) + div button {
                    background-color: orange;
                    }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
            
            if st.button("Play Again"):
                reset_game()
                st.experimental_rerun()
        elif game.checkWin('O'):
            st.success("Computer win!")
            
            st.markdown(
                """
                <style>
                .element-container:has(style){
                    display: none;
                }
                #button-after {
                    display: none;
                }
                .element-container:has(#button-after) {
                    display: none;
                }
                .element-container:has(#button-after) + div button {
                    background-color: orange;
                    }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
            
            if st.button("Play Again"):
                reset_game()
                st.experimental_rerun()
        else:
            st.session_state.board = game.board
            st.session_state.current_player = 'X'
        st.session_state.start_time_player = time.time()
    

# Draw the board
draw_tic_tac_toe_board()


# Display move history in the sidebar
st.sidebar.header('Move History')
for move in st.session_state.move_history:
    st.sidebar.write(move)


# Footer content
footer_text = """
---

### About Me
- **Github:** [tranductri2003](https://github.com/tranductri2003)
- **Facebook:** [Trần Đức Trí](https://www.facebook.com/tranductri2003/)
- **Linkedln:** [Duc Tri Tran](https://www.linkedin.com/in/duc-tri-tran-464343218/)

### Source Code
- **Repository:** [tranductri2003](https://github.com/tranductri2003/tictactoe-5x5-minimax-website)

### Another Game
- **8 Puzzles:** [8 Puzzles Game](http://lqdlover.ddns.net:8500/)
- **5x5 TicTacToe:** [5x5 TicTacToe](http://lqdlover.ddns.net:8501/)
"""

# Add footer to the app
st.markdown(footer_text, unsafe_allow_html=True)