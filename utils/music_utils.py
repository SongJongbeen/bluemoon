import yt_dlp
import random

def get_youtube_audio_info(query):
    """
    유튜브 링크 또는 검색어(query)에서 오디오 스트림 URL과 곡 제목 추출
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': False,
        'noplaylist': True,
        'default_search': 'auto',
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info and info['entries']:
            info = info['entries'][0]
        return {
            'url': info['url'],
            'title': info.get('title', 'Unknown Title'),
            'duration': info.get('duration', 0)
        }

class MusicQueue:
    def __init__(self):
        self.queue = []
        self.repeat_mode = 'off'  # 'off', 'one', 'all'

    def add(self, item):
        self.queue.append(item)

    def pop(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def clear(self):
        self.queue.clear()

    def shuffle(self):
        random.shuffle(self.queue)

    def __len__(self):
        return len(self.queue)

    def __getitem__(self, idx):
        return self.queue[idx]

    def is_empty(self):
        return len(self.queue) == 0

    def set_repeat(self, mode):
        assert mode in ('off', 'one', 'all')
        self.repeat_mode = mode

    def get_repeat(self):
        return self.repeat_mode
