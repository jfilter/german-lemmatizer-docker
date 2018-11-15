import sys
from itertools import zip_longest
from pathlib import Path

from tqdm import tqdm

import spacy
from germalemma import GermaLemma
from spacy_iwnlp import spaCyIWNLP

# setup IWNLP
nlp = spacy.load('de_core_news_sm', disable=['parser', 'ner'])
iwnlp = spaCyIWNLP(
    lemmatizer_path='IWNLP.Lemmatizer_20181001.json')
nlp.add_pipe(iwnlp)

# setup GermaLemma
lemmatizer = GermaLemma()


def replace_with_lemma(token_text, iwnlp_lemmas, pos):
    # iwnlp_lemmas is list, this is single string
    other_canditate = None

    if pos == 'NOUN':
        other_canditate = lemmatizer.find_lemma(token_text, 'N')

    if pos == 'VERB' or pos == 'AUX':
        other_canditate = lemmatizer.find_lemma(token_text, 'V')

    if pos == 'ADJ':
        other_canditate = lemmatizer.find_lemma(token_text, 'ADJ')

    if pos == 'ADV':
        other_canditate = lemmatizer.find_lemma(token_text, 'ADV')

    if iwnlp_lemmas is None:
        if other_canditate is None:
            # default return text
            return token_text
        else:
            # if there are no  iwnlp_lemmas from IWNLP, we take the one from Germ Lemma
            return other_canditate
    else:
        if other_canditate != token_text and other_canditate in iwnlp_lemmas:
            return other_canditate  # both found the same
        else:
            return iwnlp_lemmas[0]  # always first to be reproducible


def process_token(token_text, iwnlp_lemmas, pos):
    # process and make some that some information about the case remains
    prc_tkn = replace_with_lemma(token_text, iwnlp_lemmas, pos)
    res_word = ''
    for x, y in zip_longest(list(prc_tkn), list(token_text), fillvalue=''):
        # keep orginal case if the characters are the same
        if x.lower() == y.lower():
            res_word += y
        else:
            res_word += x

    # remain upper case
    if token_text.isupper() and not res_word.isupper():
        res_word = res_word.upper()

    # remain title case
    if token_text.istitle() and not res_word.istitle():
        res_word = res_word.title()

    return res_word


def lemma(text):
    doc = nlp(text)
    # tried to parallelize it but there was too much overhead
    return [process_token(str(token), token._.iwnlp_lemmas, token.pos_) for token in doc]


def process_file(path):
    text = path.read_text()
    Path('/data/output/' + path.name).write_text(' '.join(lemma(text)))


# # https://stackoverflow.com/questions/46245844/pass-arguments-to-python-argparse-within-docker-container
if __name__ == "__main__":

    if len(sys.argv) > 1:
        results = lemma(sys.argv[1])
        print(' '.join(results))

    else:
        input_path = Path('/data/input')
        if input_path.exists() and input_path.is_dir():
            print('Saving lemmatized text to the output folder...')
            Path('/data/output').mkdir(exist_ok=True)
            files = list(input_path.glob('**/*.txt'))

            for f in tqdm(files):
                process_file(f)

        else:
            print('something went wrong, either give me some input as argument, i.e. `docker run -it lemma "Was ist das für ein Leben?" or mount a directory `/data` that has a sub-directory `/data/input` with .txt files in this directory')
