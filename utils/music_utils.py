import yt_dlp
import random
import asyncio
import os
from pathlib import Path

async def get_youtube_audio_info(query):
    """
    유튜브 링크 또는 검색어(query)에서 오디오 스트림 URL과 곡 제목 추출 (비동기)
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,  # 디버깅을 위해 출력 활성화
        'extract_flat': False,
        'noplaylist': True,
        'default_search': 'auto',
        'skip_download': True,
        'no_warnings': False,  # 경고 메시지 표시
        'ignoreerrors': False,
        'nocheckcertificate': True,
        'extractor_retries': 3,
        'source_address': '0.0.0.0',
        'cookiesfrombrowser': ('firefox',),  # Firefox 쿠키 사용 시도
    }
    
    def sync_extract():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if info is None:
                    raise yt_dlp.utils.DownloadError("동영상 정보를 가져올 수 없습니다.")
                    
                if 'entries' in info and info['entries']:
                    info = info['entries'][0]
                elif 'entries' in info and not info['entries']:
                    raise yt_dlp.utils.DownloadError("검색 결과가 없습니다.")
                    
                if not info.get('url'):
                    raise yt_dlp.utils.DownloadError("스트리밍 URL을 찾을 수 없습니다.")
                    
                return {
                    'url': info['url'],
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration', 0)
                }
        except Exception as e:
            print(f"YouTube 다운로드 오류: {str(e)}")
            # 다른 브라우저로 재시도
            if 'firefox' in str(ydl_opts['cookiesfrombrowser']):
                print("Firefox 쿠키로 실패, Chrome 쿠키로 재시도합니다.")
                ydl_opts['cookiesfrombrowser'] = ('chrome',)
                return sync_extract()
            raise yt_dlp.utils.DownloadError(f"동영상을 다운로드할 수 없습니다: {str(e)}")
            
    return await asyncio.to_thread(sync_extract)

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
