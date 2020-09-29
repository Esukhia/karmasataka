import re


def format_fr(text):
    # see http://unicode.org/udhr/n/notes_fra.html
    text = re.sub(r'([ \f\v\u202f\u00a0])+', r'\1', text)
    text = re.sub(r'[ \f\v\u202f\u00a0]+,', r',', text)
    text = re.sub(r'[ \f\v\u202f\u00a0]+\.', r'.', text)
    text = re.sub(r'[ \f\v\u202f\u00a0]+?;', '\u202f;', text)
    text = re.sub(r'[ \f\v\u202f\u00a0]+?!', '\u202f!', text)
    text = re.sub(r'[ \f\v\u202f\u00a0]+?\?', '\u202f?', text)
    text = re.sub(r'[ \f\v\u202f\u00a0]+?:', '\u00a0:', text)
    text = re.sub(r'\n-[ \f\v\u202f\u00a0]+', '\n—\u0020', text)
    text = re.sub(r'«[ \f\v\u202f\u00a0]+?', '«\u00a0', text)
    text = re.sub(r'[ \f\v\u202f\u00a0]+?»', '\u00a0»', text)
    text = re.sub(r'\([ \f\v\u202f\u00a0]+', r'(', text)
    text = re.sub(r'\[[ \f\v\u202f\u00a0]+', r']', text)
    text = re.sub(r'[ \f\v\u202f\u00a0]+\)', r')', text)
    text = re.sub(r'[ \f\v\u202f\u00a0]+]', r']', text)
    # additions
    text = text.replace('...', '…')
    text = re.sub(
        r'[ \f\v\u202f\u00a0]+-[ \f\v\u202f\u00a0]+(.+?)[ \f\v\u202f\u00a0]+-[ \f\v\u202f\u00a0]',
        r' – \1 – ', text)
    text = re.sub(
        r'[ \f\v\u202f\u00a0]+-[ \f\v\u202f\u00a0]+',
        r' – ', text)
    text = re.sub(
        r'[ \f\v\u202f\u00a0]+"(.+?)"([ \f\v\u202f\u00a0]?)',
        r' “\1”\2', text)
    text = re.sub(
        r"[ \f\v\u202f\u00a0]+'(.+?)'([ \f\v\u202f\u00a0]?)",
        r' ‘\1’\2', text)
    text = text.replace("'", '’')
    text = re.sub(r'([^ ])[ \f\v\u202f\u00a0]+\n', r'\1\n', text)
    return text
