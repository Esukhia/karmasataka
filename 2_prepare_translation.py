from pathlib import Path
import polib


class Po:
    def __init__(self, infile):
        self.infile = Path(infile)
        self.outfile = self.infile.parent.parent.parent / out_folder / (self.infile.stem + '.txt')
        self.file = polib.pofile(self.infile)

    def format_entries(self):
        entries = []
        for entry in self.file:
            if entry.tcomment:
                text = entry.tcomment
            else:
                text = entry.msgid
                text = text.replace(' ', '').replace('␣', '').replace(' ', ' ')
            text = text.replace('\n', ' ')
            text = "\t" + text
            entries.append((entry.msgstr, text))
        return '\n'.join(['\n'.join(e) for e in entries])

    def write_txt(self):
        output = self.format_entries()
        self.outfile.write_text(output)


if __name__ == '__main__':
    in_folder = 'fr_sem/po'
    out_folder = 'fr_sem/txt'
    for file in Path(in_folder).glob('*.po'):
        po = Po(file)
        po.write_txt()
