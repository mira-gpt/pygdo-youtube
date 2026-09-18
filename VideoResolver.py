"""Small, dependency-free YouTube metadata resolver."""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class YouTubeMetadata:
    video_id: str
    url: str
    title: str
    description: str
    channel: str
    thumbnail: str


class _MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.metadata: dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'meta':
            return
        attrs = {key.lower(): value or '' for key, value in attrs}
        key = (attrs.get('name') or attrs.get('property') or '').lower()
        content = attrs.get('content')
        if key and content:
            self.metadata.setdefault(key, content)


class VideoResolver:
    """Canonicalise URLs and fetch metadata without a YouTube API key."""

    VIDEO_ID = re.compile(r'^[A-Za-z0-9_-]{11}$')
    URL = re.compile(
        r'https?://(?:www\.)?(?:youtube\.com/(?:watch\?[^\s]*?v=|shorts/|live/|embed/)|youtu\.be/)'
        r'([A-Za-z0-9_-]{11})(?:[^A-Za-z0-9_-]|$)', re.IGNORECASE)

    @classmethod
    def video_id(cls, text: str) -> str | None:
        match = cls.URL.search(text)
        return match.group(1) if match else None

    @classmethod
    def canonical_url(cls, video_id: str) -> str:
        if not cls.VIDEO_ID.fullmatch(video_id):
            raise ValueError('Invalid YouTube video ID')
        return f'https://www.youtube.com/watch?v={video_id}'

    @classmethod
    async def resolve(cls, video_id: str) -> YouTubeMetadata:
        return await asyncio.to_thread(cls.resolve_sync, video_id)

    @classmethod
    def resolve_sync(cls, video_id: str) -> YouTubeMetadata:
        url = cls.canonical_url(video_id)
        document = cls._get(url)
        parser = _MetadataParser()
        parser.feed(document)
        metadata = parser.metadata
        title = metadata.get('og:title') or metadata.get('title') or ''
        description = metadata.get('og:description') or metadata.get('description') or ''
        channel = metadata.get('author') or metadata.get('og:site_name') or 'YouTube'
        thumbnail = metadata.get('og:image') or f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'
        if not title:
            title, channel = cls._oembed(url)
        return YouTubeMetadata(video_id, url, title or video_id, description, channel, thumbnail)

    @staticmethod
    def _get(url: str) -> str:
        request = Request(url, headers={
            'User-Agent': 'PyGDO-YouTube/1.0 (+https://github.com/mira-gpt/pygdo-youtube)',
            'Accept-Language': 'en',
        })
        with urlopen(request, timeout=10) as response:
            return response.read().decode('utf-8', errors='replace')

    @classmethod
    def _oembed(cls, url: str) -> tuple[str, str]:
        endpoint = 'https://www.youtube.com/oembed?' + urlencode({'url': url, 'format': 'json'})
        try:
            data = json.loads(cls._get(endpoint))
            return str(data.get('title') or ''), str(data.get('author_name') or '')
        except Exception:
            return '', ''
