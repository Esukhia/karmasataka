from pathlib import Path
import polib


class Po:
    def __init__(self, infile):
        self.infile = Path(infile)
        self.outfile = self.infile.parent.parent.parent.parent / out_folder / (self.infile.stem + '.txt')
        self.translation = self.infile.parent.parent.parent.parent / out_folder / (self.infile.stem + '_translation.txt')
        self.file = polib.pofile(self.infile)

    def format_entries(self):
        entries = []
        for entry in self.file:
            text = "\t" + entry.msgid
            entries.append((entry.msgstr, text))
        return '\n'.join(['\n'.join(e) for e in entries]), '\n'.join([e[0] for e in entries])

    def write_txt(self):
        output, trans = self.format_entries()
        self.outfile.write_text(output)
        self.translation.write_text(trans)


if __name__ == '__main__':
    in_folder = 'fr_com/target/po'
    out_folder = 'fr_com/target/txt'
    for file in Path(in_folder).glob('*.po'):
        po = Po(file)
        po.write_txt()
