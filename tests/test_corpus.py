import tempfile
import unittest
from pathlib import Path

from rushi.corpus.diamond import article_lines, original_section, cbeta_main, align_chapters


class CorpusTests(unittest.TestCase):
    def test_exclude_navigation_and_notes_from_original(self):
        html = '<nav>导航</nav><div class="txtContent borStyleA"><p><b>原典</b><br/>章题*1<br/>甲*2乙。<br/><b>註釋</b><br/>不应混入的注释</p></div><footer>页脚</footer>'
        lines = article_lines(html)
        self.assertNotIn('导航', ''.join(lines))
        self.assertNotIn('页脚', ''.join(lines))
        self.assertEqual(original_section(lines), ('章题', '甲乙。'))

    def test_reject_unexpected_article_structure(self):
        with self.assertRaises(ValueError):
            article_lines('<div>无正文容器</div>')
        with self.assertRaises(ValueError):
            original_section(['原典', '无注释边界'])

    def test_cbeta_main_excludes_appendix_and_back(self):
        xml = '''<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:cb="http://www.cbeta.org/ns/1.0"><text><body>
        <lb n="0001a01" ed="T"/><byline>译者题记</byline>
        <cb:div type="jing"><p>如是我聞，<lb n="0001a02" ed="T"/>測試信受奉行。</p></cb:div>
        <cb:div type="w"><p>附文不进入正文</p></cb:div></body><back><p>校勘不进入正文</p></back></text></TEI>'''
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.xml'
            path.write_text(xml, encoding='utf-8')
            text, lines = cbeta_main(path)
        self.assertEqual(text, '如是我聞，測試信受奉行。')
        self.assertEqual(lines[0], '0001a01')
        self.assertEqual(lines[-1], '0001a02')

    def test_alignment_preserves_text_and_opening_quotes(self):
        text = '甲乙丙。 「丁戊己。」庚辛壬。'.replace(' ', '')
        chapters, _ = align_chapters(text, ['甲乙丙。', '丁戊己。', '庚辛壬。'])
        self.assertEqual(''.join(c['cbeta_text'] for c in chapters), text)
        self.assertEqual(chapters[0]['cbeta_text'], '甲乙丙。')
        self.assertEqual(chapters[1]['cbeta_text'], '「丁戊己。」')


if __name__ == '__main__':
    unittest.main()
