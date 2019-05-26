FROM python:3.6

RUN apt-get update
RUN apt-get install unzip

# for caching, install pip packages first
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ADD lemmatize.py /app
WORKDIR /app

RUN wget http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/download/tigercorpus-2.2.conll09.tar.gz
RUN tar -xvzf tigercorpus-2.2.conll09.tar.gz && rm tigercorpus-2.2.conll09.tar.gz

RUN wget https://github.com/WZBSocialScienceCenter/germalemma/archive/a44431635dcc541620587605aac64f05e1b5f4f6.zip
RUN unzip a44431635dcc541620587605aac64f05e1b5f4f6.zip && rm a44431635dcc541620587605aac64f05e1b5f4f6.zip && mv germalemma-a44431635dcc541620587605aac64f05e1b5f4f6/* .

RUN wget http://lager.cs.uni-duesseldorf.de/NLP/IWNLP/IWNLP.Lemmatizer_20181001.zip
RUN unzip IWNLP.Lemmatizer_20181001.zip && rm IWNLP.Lemmatizer_20181001.zip

# RUN python -m spacy download de_core_news_sm

# fallback to locally download file because of CDN problems
ADD de_core_news_sm-2.1.0/ /app
RUN python -m spacy link de_core_news_sm de

RUN python germalemma.py tiger_release_aug07.corrected.16012013.conll09 && rm tiger_release_aug07.corrected.16012013.conll09

ENTRYPOINT ["python", "lemmatize.py"]
