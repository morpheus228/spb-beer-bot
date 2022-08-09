from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str

DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")

DB_PASSWORD = env.str("DB_PASSWORD")