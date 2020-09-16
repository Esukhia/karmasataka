from pathlib import Path
import re
import polib


class Po:
    def __init__(self):
        self.par_marker = '\n\n\n'
        self.trans_pattern = r'(.*?\n\t.*)\n'
        self.trans_delimiter = '\n\t'
        self.file = polib.POFile()
        self.file.metadata = {
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

    def _create_entry(self, msgid, msgstr="", msgctxt=None, comment=None, tcomment=None):
        entry = polib.POEntry(
            msgid=msgid,
            msgstr=msgstr,
            msgctxt=msgctxt,
            comment=comment,
            tcomment=tcomment
        )
        self.file.append(entry)

    def write_to_file(self, filename):
        self.file.save(filename)

    def dump_po_entries(self, dump, origin):
        for num, par in enumerate(dump.strip().split(self.par_marker)):
            pairs = re.split(self.trans_pattern, par)
            pairs = [p for p in pairs if p]
            source = []
            comment = []
            for pair in pairs:
                s, c = pair.split(self.trans_delimiter)
                source.append(s)
                comment.append(c)
            source = ' '.join(source)
            source = self._format_fr(source)
            comment = ' '.join(comment)
            self._create_entry(msgid=source, msgctxt=f'line {num + 1}, {origin}', tcomment=comment)

    @staticmethod
    def _format_fr(text):
        # see http://unicode.org/udhr/n/notes_fra.html
        text = re.sub(r'([ \r\f\v\u202f\u00a0])+', r'\1', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+,', r',', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+\.', r'.', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+?;', '\u202f;', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+?!', '\u202f!', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+?\?', '\u202f?', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+?:', '\u00a0:', text)
        text = re.sub(r'\n-[ \r\f\v\u202f\u00a0]+', '\n—\u0020', text)
        text = re.sub(r'«[ \r\f\v\u202f\u00a0]+?', '«\u00a0', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+?»', '\u00a0»', text)
        text = re.sub(r'\([ \r\f\v\u202f\u00a0]+', r'(', text)
        text = re.sub(r'\[[ \r\f\v\u202f\u00a0]+', r']', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+\)', r')', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+]', r']', text)
        # additions
        text = text.replace('...', '…')
        text = text.replace("'", '’')
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+-[ \r\f\v\u202f\u00a0]+(.+?)[ \r\f\v\u202f\u00a0]+-[ \r\f\v\u202f\u00a0]',
                      r' – \1 – ', text)
        return text

    def txt_to_po(self, filename):
        lines = filename.read_text(encoding='utf-8')
        if self.par_marker not in lines:
            print(' — has no paragraphs. passing...')
            return
        else:
            print('')

        self.dump_po_entries(lines, filename.name)
        self.write_to_file((filename.parent / (filename.stem + ".po")))


if __name__ == '__main__':
    folder = 'fr/sem_pars'
    for file in Path(folder).glob('*.txt'):
        print(file, end='')
        po = Po()
        po.txt_to_po(file)
