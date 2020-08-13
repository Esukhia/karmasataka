from pathlib import Path
import re

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
            if no_notes == "":
                no_notes, line = line, no_notes
            self._create_entry(msgid=no_notes, msgctxt=f'line {num+1}, {origin}', tcomment=line)

    def txt_to_po(self, filename):
        filename = Path(filename)
        lines = filename.read_text().strip().split('\n')
        self.lines_to_entries(lines, filename.name)

        outfile = Path(out_folder) / (filename.stem + ".po")
        self.write_to_file(outfile)

    @staticmethod
    def remove_peydurma_notes(line):
        truc = re.split(r'(<.*?>)', line)
        if len(truc) > 1:
            return ''.join([a for a in truc if not a.startswith('<')]).replace(':', '')
        else:
            return ""


if __name__ == '__main__':
    in_folder = '0_original_stories/txt'
    out_folder = '0_original_stories/po'
    for file in Path(in_folder).glob('*.txt'):
        po = Po()
        po.txt_to_po(file)
