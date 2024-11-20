#Example Flask App for a hexaganal tile game
#Logic is in this python file


pip install Flask

import random
import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define the Candy Land board
def initialize_board():
    return ["red", "orange", "yellow", "green", "blue", "red", "orange", "yellow", "green", "blue", "red", "orange", "yellow", "green", "blue", "end"]

# Load the saved game state from a file
def load_game_state(filename="events.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return None

# Save the current game state to a file
def save_game_state(players, filename="events.json"):
    with open(filename, 'w') as file:
        json.dump(players, file)

# Game logic function to simulate the turns and moves
def candy_land_sim(players, number_players):
    board = initialize_board()
    total_position = len(board) - 1  # "end" tile position
    
    player_turn = 0  # To keep track of whose turn it is

    # Simulate turns for each player
    while True:
        current_player = list(players.keys())[player_turn]
        roll = random.randint(1, 6)  # Dice roll between 1 and 6
        players[current_player] += roll
        
        # Ensure the player doesn't go past the "end" tile
        if players[current_player] >= total_position:
            players[current_player] = total_position
            winner = current_player
            break

        # Alternate to the next player's turn
        player_turn = (player_turn + 1) % number_players
    
    save_game_state(players)  # Save the game state after the turn
    return winner

# Home route to display the current game state
@app.route('/')
def index():
    game_state = load_game_state()

    if not game_state:
        game_state = {'player1': 0, 'player2': 0}  # Default starting positions if no saved state

    return render_template('index.html', game_state=game_state)

# Route to handle the dice roll and update the game state
@app.route('/roll')
def roll_dice():
    game_state = load_game_state()
    number_players = len(game_state)

    # Run the game simulation and determine the winner
    winner = candy_land_sim(game_state, number_players)

    # Save the updated game state
    save_game_state(game_state)

    return render_template('index.html', game_state=game_state, winner=winner)

if __name__ == "__main__":
    app.run(debug=True)