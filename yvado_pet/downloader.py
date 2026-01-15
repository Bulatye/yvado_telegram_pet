import subprocess
import tempfile
import os
import random

# Список User-Agents для обхода блокировок
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
]

DOWNLOAD_DIR="temple_mp3_dowloads/"
def download_audio(url: str) -> str:
    """
    Скачать аудио с YouTube используя yt-dlp как утилиту
    Возвращает путь к скачанному файлу
    """
    # Выбираем случайный User-Agent
    user_agent = random.choice(USER_AGENTS)
    # Формируем команду для yt-dlp
    cmd = f'yt-dlp -x --audio-format mp3 --embed-thumbnail --add-metadata -P "{DOWNLOAD_DIR}" "{url}"'
    # Выполняем команду
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Ошибка: {result.stderr[:100]}")
    
    # Ищем созданный файл
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.mp3'):
            return os.path.join(DOWNLOAD_DIR, file)
    
    raise Exception("Файл не найден")
