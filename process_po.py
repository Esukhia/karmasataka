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

    def _create_entry(self, msgid, msgstr="", msgstr_plural=None, msgctxt=None, comment=None, tcomment=None):
        """

        :param msgid: string, the entry msgid.
        :param msgstr: string, the entry msgstr.
        :param msgstr_plural: list, the entry msgstr_plural lines.
        :param msgctxt: string, the entry context.
        :param comment: string, the entry comment.
        :param tcomment: string, the entry translator comment.
        """
        entry = polib.POEntry(
            msgid=msgid,
            msgstr=msgstr,
            msgstr_plural=msgstr_plural,
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
            no_notes = re.sub('\[.+?\]', '', no_notes)
            # segment
            t = Text(no_notes)
            no_notes = t.tokenize_words_raw_text
            # format tokens
            no_notes = re.sub('([^།་_]) ([^_།་])', '\g<1>␣\g<2>', no_notes)   # affixed particles
            no_notes = re.sub('_', ' ', no_notes)   # spaces
            if no_notes == "":
                no_notes, line = line, no_notes
            self._create_entry(msgid=no_notes, msgctxt=f'line {num+1}, {origin}', tcomment=line)

    def txt_to_po(self, filename):
        filename = Path(filename)
        lines = filename.read_text(encoding='utf-8').strip().split('\n')
        self.lines_to_entries(lines, filename.name)

        outfile = Path(out_folder) / (filename.stem + ".po")
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
    in_folder = 'bo/txt'
    out_folder = 'bo/po'
    for file in Path(in_folder).glob('*.txt'):
        po = Po()
        po.txt_to_po(file)
