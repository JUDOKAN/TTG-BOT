
import config
import logic
import boxing2d_logic
import driverush2d_logic
import rocketdrift2d_logic
import snakegame2d_logic
import mathdash_logic

MODULE_MAP = {
    'boxing2d':      boxing2d_logic,
    'driverush2d':   driverush2d_logic,
    'rocketdrift2d': rocketdrift2d_logic,
    'snakegame2d':   snakegame2d_logic,
    'mathdash':      mathdash_logic
}

def sync_remote_scores(game_key: str):
    url = config.API_URLS.get(game_key)
    if not url:
        return
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    mod = MODULE_MAP[game_key]
    for entry in data:
        user = entry['user_name']
        score = entry['score']
        mod.add_score(user, score)
        logic.update_general_score(user, game_key, score)

def sync_all():
    for key in MODULE_MAP:
        sync_remote_scores(key)
