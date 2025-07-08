import os

# Bot token
TOKEN = 'your_bot_token_here'

# Veritabanı dizini (klasörü logic.py içindeki init ile oluşturulur)
DB_FOLDER = os.path.join(os.getcwd(), 'db')

# Her oyuna ait SQLite dosyaları
DB_PATH_BOXING2D      = os.path.join(DB_FOLDER, 'boxing2d.db')
DB_PATH_DRIVERUSH2D   = os.path.join(DB_FOLDER, 'driverush2d.db')
DB_PATH_ROCKETDRIFT2D = os.path.join(DB_FOLDER, 'rocketdrift2d.db')
DB_PATH_SNAKEGAME2D   = os.path.join(DB_FOLDER, 'snakegame2d.db')
DB_PATH_MATHDASH      = os.path.join(DB_FOLDER, 'mathdash.db')

# Tüm oyunların skorlarının bulunduğu genel veritabanı
DB_PATH_GENERAL       = os.path.join(DB_FOLDER, 'general.db')

# Web site bağlantısı (help komutunda gösterilecek)
WEBSITE_URL = 'http://127.0.0.1:5000'

# Oyunların oynanacağı sayfa URL’leri
GAME_URLS = {
    'boxing2d':      'http://127.0.0.1:5000/Boxer2D',
    'driverush2d':   'http://127.0.0.1:5000/DriveRush2D',
    'rocketdrift2d': 'http://127.0.0.1:5000/RocketDrift2D',
    'snakegame2d':    'http://127.0.0.1:5000/SnakeGame2D',
    'mathdash':      'http://127.0.0.1:5000/MathDash'
}

# Skor verilerini JSON olarak dönen REST API uç noktaları
API_URLS = {
    'boxing2d':      'https://example.com/api/scores/boxing2d',
    'driverush2d':   'https://example.com/api/scores/drive-rush-2d',
    'rocketdrift2d': 'https://example.com/api/scores/rocket-drift-2d',
    'snakegame2d':   'https://example.com/api/scores/snake-game-2d',
    'mathdash':      'https://example.com/api/scores/math-dash'
}
