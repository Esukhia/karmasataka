from pathlib import Path
import re
from botok import Text
import polib


class Po:
    def __init__(self):
        self.file = polib.POFile()
        self.file.metadata = {
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

    def _create_entry(self, msgid, msgstr="", msgctxt=None, comment=None, tcomment=None):
        """

        :param msgid: string, the entry msgid.
        :param msgstr: string, the entry msgstr.
        :param msgctxt: string, the entry context.
        :param comment: string, the entry comment.
        :param tcomment: string, the entry translator comment.
        """
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

    def lines_to_entries(self, lines, origin):
        for num, line in enumerate(lines):
            no_notes = self.remove_peydurma_notes(line)
            if no_notes == "":
                no_notes, line = line, no_notes
            no_notes = re.sub('\[.+?\]', '', no_notes)
            # segment
            t = Text(no_notes)
            no_notes = t.tokenize_words_raw_text
            # format tokens
            no_notes = re.sub('([^།་_]) ([^_།་])', '\g<1>␣\g<2>', no_notes)   # affixed particles
            no_notes = re.sub('_', ' ', no_notes)   # spaces
            self._create_entry(msgid=no_notes, msgctxt=f'line {num+1}, {origin}', tcomment=line)

    def txt_to_po(self, filename):
        lines = filename.read_text(encoding='utf-8').strip().split('\n')
        self.lines_to_entries(lines, filename.name)

        outfile = filename.parent / (filename.stem + ".po")
        self.write_to_file(outfile)

    @staticmethod
    def remove_pagination(line):
        note = re.split(r'(\[.*?\])', line)
        if len(note) > 1:
            return ''.join([a for a in note if not a.startswith('\[')])
        else:
            return ""

    @staticmethod
    def remove_peydurma_notes(line):
        note = re.split(r'(<.*?>)', line)
        if len(note) > 1:
            return ''.join([a for a in note if not a.startswith('<')]).replace(':', '')
        else:
            return ""


if __name__ == '__main__':
    folder = 'sem/bo/'
    idx = 0
    files = sorted(list(Path(folder).glob('*.txt')))
    to_loop = files[idx-1:idx] if idx > 0 else files
    for file in to_loop:
        print(file)
        po = Po()
        po.txt_to_po(file)
