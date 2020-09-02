from pathlib import Path
import polib


class Po:
    def __init__(self, infile):
        self.infile = Path(infile)
        self.file = polib.pofile(self.infile)

    def format_entries(self):
        entries = []
        for entry in self.file:
            text = "\t" + entry.msgid
            entries.append((entry.msgstr, text))
        return '\n'.join(['\n'.join(e) for e in entries]), '\n'.join([e[0] for e in entries])

    def write_txt(self):
        orig_trans, trans = self.format_entries()

        bitext = self.infile.parent / (self.infile.stem + '.txt')
        bitext.write_text(orig_trans)

        translation = self.infile.parent / (self.infile.stem + '_translation.txt')
        translation.write_text(trans)


if __name__ == '__main__':
    folder = 'fr/reader'
    for file in Path(folder).glob('*.po'):
        po = Po(file)
        po.write_txt()
