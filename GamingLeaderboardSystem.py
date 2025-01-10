import os
import oracledb
from flask import Flask, jsonify, request

app = Flask(__name__)

# Database configuration
dsn = os.getenv('DB_DSN', oracledb.makedsn("192.168.61.225", 1521, service_name="XE"))
db_user = os.getenv('DB_USER', 'system')
db_password = os.getenv('DB_PASSWORD', 'root')

def create_connection():
    try:
        connection = oracledb.connect(user=db_user, password=db_password, dsn=dsn)
        return connection
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        print(f"Error connecting to Oracle DB: {error_obj.message}")
        return None

# Fetch all players
@app.route('/api/players', methods=['GET'])
def get_players():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        cursor.execute("SELECT player_id, player_name, created_at FROM players")
        
        players = [{'player_id': row[0], 'player_name': row[1], 'created_at': row[2]} for row in cursor.fetchall()]
        cursor.close()
        connection.close()

        return jsonify({"players": players})
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500

# Insert a new player
@app.route('/api/players', methods=['POST'])
def insert_player():
    data = request.get_json()
    player_id = data.get('player_id')
    player_name = data.get('player_name')
    created_at = data.get('created_at')

    if not player_id or not player_name or not created_at:
        return jsonify({"error": "All fields are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        cursor.callproc("add_player", [player_id, player_name, created_at])
        connection.commit()

        return jsonify({"message": f"Player {player_name} inserted successfully"}), 201
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Fetch all games
@app.route('/api/games', methods=['GET'])
def get_games():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT game_id, game_name FROM games")

        games = [{'game_id': row[0], 'game_name': row[1]} for row in cursor.fetchall()]
        cursor.close()
        connection.close()

        return jsonify({"games": games})
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500

# Insert a new score
@app.route('/api/scores', methods=['POST'])
def insert_score():
    data = request.get_json()
    match_id = data.get('match_id')
    player_id = data.get('player_id')
    score = data.get('score')
    game_name = data.get('game_name')
    achieved_at = data.get('achieved_at')

    if not match_id or not player_id or not score or not game_name or not achieved_at:
        return jsonify({"error": "All fields are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        cursor.callproc("insert_scores", [match_id, player_id, score, game_name, achieved_at])
        connection.commit()

        return jsonify({"message": f"Score for player {player_id} added successfully"}), 201
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Fetch rankings for a game
@app.route('/api/rankings/<int:game_id>', methods=['GET'])
def get_rankings(game_id):
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        cursor.execute("""
            SELECT player_id, game_id, total_score, rank, last_updated 
            FROM rankings WHERE game_id = :game_id ORDER BY rank
        """, [game_id])

        rankings = [{'player_id': row[0], 'game_id': row[1], 'total_score': row[2], 'rank': row[3], 'last_updated': row[4]} 
                    for row in cursor.fetchall()]
        cursor.close()
        connection.close()

        return jsonify({"rankings": rankings})
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500


# Delete a player
@app.route('/api/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        cursor.execute("DELETE FROM players WHERE player_id = :player_id", [player_id])
        connection.commit()

        return jsonify({"message": f"Player {player_id} deleted successfully"}), 200
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
