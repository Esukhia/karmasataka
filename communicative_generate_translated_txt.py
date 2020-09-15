from pathlib import Path
import re
import polib


class Po:
    def __init__(self, infile):
        self.infile = Path(infile)
        self.file = polib.pofile(self.infile)
        self._format_fields()
        self.par_marker = '\n\n\n'
        self.trans_pattern = r'(.*?\n\t.*)\n'
        self.trans_delimiter = '\n\t'

    def format_entries(self):
        entries = []
        for entry in self.file:
            text = "\t" + entry.msgid
            entries.append((entry.msgstr, text))

        all = []
        pair_dump = Path('fr/sem_pars/') / (self.infile.stem + '.txt')
        source_sem_pairs = self.parse_txt_dump(pair_dump.read_text(encoding='utf-8'))
        if len(entries) != len(source_sem_pairs):
            exit('source/semantic paragraphs and communicative paragraph have different lengths.\nExiting...')
        for i in range(len(entries)):
            all.append([entries[i][0], source_sem_pairs[i]])

        all_formatted = ''
        for com, pairs in all:
            pairs = '\n'.join(['\n'.join(['\t' + a, '\t' + b]) for a, b in pairs])
            all_formatted += com + '\n' + pairs + '\n\n'

        return '\n'.join(['\n'.join(e) for e in entries]), '\n\n'.join([e[0] for e in entries]), all_formatted

    def parse_txt_dump(self, dump):
        parsed = []
        for par in dump.strip().split(self.par_marker):
            pairs = re.split(self.trans_pattern, par)
            pairs = [p for p in pairs if p]
            parsed_pairs = []
            for pair in pairs:
                c, s = pair.split(self.trans_delimiter)
                parsed_pairs.append((s, c))
            parsed.append(parsed_pairs)
        return parsed

    def write_txt(self):
        orig_trans, trans, all = self.format_entries()

        bitext = self.infile.parent / (self.infile.stem + '.txt')
        bitext.write_text(orig_trans)

        translation = self.infile.parent / (self.infile.stem + '_translation.txt')
        translation.write_text(trans)

        total = self.infile.parent / (self.infile.stem + '_total.txt')
        total.write_text(all)

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
        text = re.sub(r'-[ \r\f\v\u202f\u00a0]+', '–\u0020', text)
        text = re.sub(r'«[ \r\f\v\u202f\u00a0]+?', '«\u00a0', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+?»', '\u00a0»', text)
        text = re.sub(r'\([ \r\f\v\u202f\u00a0]+', r'(', text)
        text = re.sub(r'\[[ \r\f\v\u202f\u00a0]+', r']', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+\)', r')', text)
        text = re.sub(r'[ \r\f\v\u202f\u00a0]+]', r']', text)
        # additions
        text = text.replace('...', '…')
        return text

    def _format_fields(self):
        for entry in self.file:
            entry.msgid = self._format_fr(entry.msgid)
            entry.msgstr = self._format_fr(entry.msgstr)


if __name__ == '__main__':
    folder = 'fr/reader'
    for file in Path(folder).glob('*.po'):
        po = Po(file)
        po.write_txt()
