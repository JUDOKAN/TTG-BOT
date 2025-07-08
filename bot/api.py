from flask import Flask, jsonify
import sqlite3
import config

app = Flask(__name__)

GAME_DB_MAP = {
    'boxing2d': config.DB_PATH_BOXING2D,
    'driverush2d': config.DB_PATH_DRIVERUSH2D,
    'rocketdrift2d': config.DB_PATH_ROCKETDRIFT2D,
    'snakegame2d': config.DB_PATH_SNAKEGAME2D,
    'mathdash': config.DB_PATH_MATHDASH
}

@app.route('/api/scores/<game_key>', methods=['GET'])
def get_scores(game_key):
    db_path = GAME_DB_MAP.get(game_key)
    if not db_path:
        return jsonify({'error': 'Invalid game key'}), 404
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"SELECT user_name, score FROM {game_key}_scores ORDER BY score DESC")
    data = [{'user_name': row[0], 'score': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(data)

@app.route('/api/scores/general', methods=['GET'])
def get_general_scores():
    conn = sqlite3.connect(config.DB_PATH_GENERAL)
    c = conn.cursor()
    c.execute(
        "SELECT user_name, boxing2d_score, driverush2d_score, rocketdrift2d_score, snakegame2d_score, mathdash_score "
        "FROM general_scores"
    )
    rows = c.fetchall()
    data = []
    for r in rows:
        data.append({
            'user_name': r[0],
            'boxing2d': r[1],
            'driverush2d': r[2],
            'rocketdrift2d': r[3],
            'snakegame2d': r[4],
            'mathdash': r[5]
        })
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
