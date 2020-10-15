from pathlib import Path
import re
import sys
import shutil
import polib
from antx import transfer
from to_docx import create_total_docx, create_trans_docx
from text_formatting import format_fr
import subprocess


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

        return '\n'.join(['\n'.join(e) for e in entries]), \
               '\n\n'.join([e[0] for e in entries]), \
               all_formatted, \
               all

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
        orig_trans, trans, all, data = self.format_entries()

        bitext = self.infile.parent / (self.infile.stem + '.txt')
        bitext.write_text(orig_trans)

        trans_txt = self.infile.parent / (self.infile.stem + '_translation.txt')
        trans = self._update_translation_pars(trans, trans_txt)
        trans_txt.write_text(trans)

        trans_docx = self.infile.parent / (self.infile.stem + '_translation.docx')
        create_trans_docx(trans, trans_docx)

        total = self.infile.parent / (self.infile.stem + '_total.txt')
        total.write_text(all)

        total_docx = self.infile.parent / (self.infile.stem + '_total.docx')
        create_total_docx(data, total_docx)

    def _update_translation_pars(self, orig_trans, existing):
        if not existing.is_file():
            return orig_trans
        else:
            # update file retaining the paragraph delimitations
            old_trans = existing.read_text(encoding='utf-8')
            if old_trans.replace('\n\n', '') != orig_trans.replace('\n\n', ''):
                updated = self._update_pars(old_trans, orig_trans)
                return updated
            else:
                return orig_trans

    @staticmethod
    def _update_pars(source, target):
        target = target.replace('\n\n', ' ')
        pattern = [["pars", "(\n\n)"]]
        updated = transfer(source, pattern, target, "txt")
        updated = re.sub(r'([!?”:;…,.»"]+?)([^ \f\v\u202f\u00a0\n!?”:;…,.»"])', r'\1 \2', updated)  # reinserting spaces where needed
        updated = re.sub(r'\n\n/ +', '/\n\n', updated)
        updated = re.sub(r'\n\n” ', '”\n\n', updated)
        updated = updated.replace('\n ', '\n')
        updated = updated.replace(' \n', '\n')

        return updated

    def _format_fields(self):
        for entry in self.file:
            entry.msgid = format_fr(entry.msgid)
            entry.msgstr = format_fr(entry.msgstr)


LOEXE = shutil.which('libreoffice')


def gen_pdf(file):
    print('Generating PDF...')
    docxs = list(file.absolute().parent.glob(f'{file.stem}*.docx'))
    for doc in docxs:
        pdf = doc.parent / (doc.stem + '.pdf')
        if pdf.is_file():
            pdf.unlink()
        subprocess.check_call([LOEXE, '--convert-to', 'pdf', '--outdir', str(doc.parent), str(doc)], stdout=subprocess.DEVNULL)


if __name__ == '__main__':
    folder = 'fr/reader'
    if len(sys.argv) > 1:
        stem = sys.argv[1]
        file = Path(folder) / (stem + '.txt')
        print(file.name)
        po = Po(file)
        po.write_txt()
        gen_pdf(file)
    else:
        files = sorted(list(Path(folder).glob('*.po')))
        for file in files:
            print(file.name)
            po = Po(file)
            po.write_txt()
            gen_pdf(file)
