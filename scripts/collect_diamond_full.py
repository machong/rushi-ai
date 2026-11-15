"""缓存用户指定老师的官方章节供本机核对；不批准训练或公开分发。"""
import argparse
import hashlib
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://books.masterhsingyun.org'
FOLDER = ROOT / 'data/sources/diamond-full'
CACHE = ROOT / 'data/raw/diamond-full/hsingyun'


class MenuParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.book = None
        self.capture = None
        self.buffer = []
        self.chapters = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'p' and 'title' in attrs.get('class', '').split():
            self.capture = 'title'
            self.buffer = []
        elif tag == 'a':
            self.capture = 'link'
            self.buffer = []
            self.href = attrs.get('href', '')

    def handle_data(self, data):
        if self.capture:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if self.capture == 'title' and tag == 'p':
            title = ''.join(self.buffer).strip()
            if '金剛經講話' in title:
                self.book = title
            elif re.search(r'第[一二三四五六七八九十]+\s', title):
                self.current = {'number': len(self.chapters) + 1, 'book': self.book,
                                'official_chapter_label': title, 'pages': {}}
                self.chapters.append(self.current)
            self.capture = None
        elif self.capture == 'link' and tag == 'a':
            title = ''.join(self.buffer).strip()
            if self.current:
                kind = ('commentary' if '講話' in title else 'translation' if '譯文' in title
                        else 'original_notes' if '原典' in title else None)
                if kind:
                    if kind in self.current['pages']:
                        raise ValueError('同一分出现重复页面类型，需检查目录')
                    self.current['pages'][kind] = {'label': title, 'url': urljoin(BASE, self.href)}
            self.capture = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true', help='联网缓存官方目录列出的96个页面')
    args = parser.parse_args()
    menu = FOLDER / 'hsingyun-menu.html'
    parsed = MenuParser()
    parsed.feed(menu.read_text(encoding='utf-8'))
    if len(parsed.chapters) != 32 or any(len(c['pages']) != 3 for c in parsed.chapters):
        raise ValueError('目录并非完整32分×3类页面，拒绝继续')
    CACHE.mkdir(parents=True, exist_ok=True)
    for chapter in parsed.chapters:
        for kind, page in chapter['pages'].items():
            filename = CACHE / f"{page['url'].rsplit('/', 1)[-1]}.html"
            if not filename.exists():
                if not args.fetch:
                    raise ValueError(f'缺少缓存：{filename}；显式使用 --fetch 才会联网')
                temporary = filename.with_suffix('.part')
                subprocess.run(['curl', '--silent', '--show-error', '--fail', '--location',
                                '--retry', '2', '--max-time', '30', page['url'], '-o', str(temporary)], check=True)
                text = temporary.read_text(encoding='utf-8')
                if 'txtContent' not in text:
                    temporary.unlink()
                    raise ValueError(f"页面不是预期正文：{page['url']}")
                temporary.replace(filename)
                time.sleep(0.2)
            content = filename.read_bytes()
            page.update(cache_file=str(filename.relative_to(ROOT)), sha256=hashlib.sha256(content).hexdigest())
        if chapter['number'] % 4 == 0:
            print(f"已缓存并登记 {chapter['number']}/32 分", flush=True)
    manifest = {'collected_at': datetime.now(timezone.utc).isoformat(), 'teacher': '星云大师',
                'work': '金剛經講話', 'official_catalog': BASE + '/Article/CpChapterMenu?bookno=5',
                'copyright_notice': 'Copyright © 著作權 佛光山 所有 All Rights Reserved.',
                'license_status': 'pending', 'review_status': 'pending',
                'usage': '本机来源核对缓存；未获准训练，不公开整部讲解',
                'chapters': parsed.chapters}
    (FOLDER / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('完成：32分、96个官方页面，训练与人工审核状态均未自动批准。')


if __name__ == '__main__':
    main()
