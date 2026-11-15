"""只处理文字与定位，不生成经义解释。"""
import difflib
import re
import unicodedata
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts = []
        self.containers = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div':
            if self.depth:
                self.depth += 1
            elif 'txtContent' in attrs.get('class', '').split():
                self.depth = 1
                self.containers += 1
        if self.depth and tag in ('br', 'p', 'h1', 'h2', 'h3', 'li', 'tr'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if self.depth and tag in ('p', 'h1', 'h2', 'h3', 'li', 'tr'):
            self.parts.append('\n')
        if tag == 'div' and self.depth:
            self.depth -= 1

    def handle_data(self, text):
        if self.depth:
            self.parts.append(text)

    def lines(self):
        if self.containers != 1:
            raise ValueError('正文容器数量异常，需人工检查页面')
        return [line.strip() for line in ''.join(self.parts).splitlines() if line.strip()]


def article_lines(html):
    parser = ArticleParser()
    parser.feed(html)
    return parser.lines()


def original_section(lines):
    if '原典' not in lines or '註釋' not in lines:
        raise ValueError('未找到明确的原典/注释边界')
    start, end = lines.index('原典'), lines.index('註釋')
    if end <= start + 2:
        raise ValueError('原典片段为空或缺少章题')
    title = lines[start + 1]
    # 删除页面的注释序号，不改变经文字词。
    text = re.sub(r'\*\d+', '', ''.join(lines[start + 2:end]))
    return re.sub(r'\*\d+', '', title), text


def cbeta_main(path):
    root = ET.parse(path).getroot()
    body = root.find('.//{http://www.tei-c.org/ns/1.0}body')
    chars, locators = [], []
    current = None

    def add(text, active):
        if text and active:
            for char in text:
                if not char.isspace():
                    chars.append(char)
                    locators.append(current)

    def walk(element, active=False):
        nonlocal current
        tag = element.tag.rsplit('}', 1)[-1]
        if tag == 'lb' and element.get('ed') == 'T':
            current = element.get('n')
        elif tag == 'lb' and element.get('ed') is None:
            current = element.get('n')
        if tag == 'div' and element.get('type') == 'jing':
            active = True
        add(element.text, active)
        for child in element:
            walk(child, active)
            add(child.tail, active)

    walk(body)
    text = ''.join(chars)
    if not text.startswith('如是我聞') or not text.endswith('信受奉行。'):
        raise ValueError('CBETA 正文边界异常（需与标题及附文真言分开）')
    if any(line is None for line in locators):
        raise ValueError('经文存在未定位字符')
    return text, locators


def normalized(text):
    chars, indices = [], []
    for i, char in enumerate(text):
        if unicodedata.category(char)[0] in ('L', 'N'):
            chars.append(char)
            indices.append(i)
    return ''.join(chars), indices


def align_chapters(cbeta_text, originals):
    a, a_indices = normalized(cbeta_text)
    b_parts = [normalized(part)[0] for part in originals]
    b = ''.join(b_parts)
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    opcodes = matcher.get_opcodes()
    boundaries = [0]
    offset = 0
    for part in b_parts[:-1]:
        offset += len(part)
        options = []
        for tag, i1, i2, j1, j2 in opcodes:
            if j1 <= offset <= j2 and tag == 'equal':
                options.append(i1 + offset - j1)
        if not options or len(set(options)) != 1:
            raise ValueError(f'第 {len(boundaries)} 分末尾不在唯一文本匹配中，须人工核对')
        boundaries.append(options[0])
    boundaries.append(len(a))
    raw_boundaries = [0]
    for boundary in boundaries[1:-1]:
        position = a_indices[boundary]
        # 开引号归后文，避免把下一分的开引号及页行归入上一分。
        while position > raw_boundaries[-1] and cbeta_text[position - 1] in '「『“‘（(':
            position -= 1
        raw_boundaries.append(position)
    raw_boundaries.append(len(cbeta_text))
    if any(x >= y for x, y in zip(raw_boundaries, raw_boundaries[1:])):
        raise ValueError('章节边界不连续或为空')
    chapters = []
    for n, (start, end) in enumerate(zip(raw_boundaries, raw_boundaries[1:])):
        segment = cbeta_text[start:end]
        norm, _ = normalized(segment)
        local = difflib.SequenceMatcher(a=norm, b=b_parts[n], autojunk=False)
        differences = [{'kind': tag, 'cbeta': norm[i1:i2], 'commentary_edition': b_parts[n][j1:j2]}
                       for tag, i1, i2, j1, j2 in local.get_opcodes() if tag != 'equal']
        chapters.append({'number': n + 1, 'cbeta_start': start, 'cbeta_end': end,
                         'cbeta_text': segment, 'normalized_similarity': local.ratio(),
                         'differences_ignoring_punctuation': differences,
                         'alignment_status': 'machine_matched_pending_human_review'})
    if ''.join(c['cbeta_text'] for c in chapters) != cbeta_text:
        raise ValueError('章节拼接未覆盖完整正文')
    return chapters, matcher.ratio()
