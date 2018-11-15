<div align="center">
  <img src="matt-artz-353291-unsplash.jpg" alt="Scissors">
</div>

# German Lemmatizer

Combining the Power of Several Tools for [Lemmatization](https://en.wikipedia.org/wiki/Lemmatisation) of German Text.

Built upon:

-   [WITD]() uses the crowd-generated token tables on [de.wikitionary]().
-   [GermaLemma](https://github.com/WZBSocialScienceCenter/germalemma): Looks up lemmas in the [TIGER Corpus](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/) and uses [Pattern]() as a fallback for some rule-based lemmatizations.

It works as follows. First POSing the text with [spaCy](). Then looks up lemmas on WITD and GermanLemma. If they disagree, choose the one from WITD. If only found by one, take it. Try to keep the casing of the original token.

## Installation

1. Install [Docker](https://docs.docker.com/).

## Usage

1. Read and accept the [license terms of the TIGER Corpus](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/license/htmlicense.html) (free to use for non-commercial purposes).
2. Start Docker.
3. To execute, you have two options:

    1. To lemmatize a string from the termial, run:

    ```
    docker run -it xx "Was ist das für ein Leben?"
    ```

    2. To lemmatize a collection of text, do as follows. Create a folder with a subfolder `input` and place your text as `.txt` files in that subfolder. Then give the absolute path to that folder (not the `input` folder) run:

    ```
    docker run -it -v /an/absolute/path/:/data xx
    ```

## The Case for Reproduciblilty

Everything – all the code and all the data – is packaged in the Docker image. This means that every lemmatization is reproduceable. For the future, I may update the data and code but I will tag each image with a specific version.

## Dev Remarks

-   Tried to base in on an [Docker Apline Imaage](https://hub.docker.com/_/alpine/) but there were too many installation hassels.
-   Tried to parallelise with [joblib](https://github.com/joblib/joblib) but it created too much overhead
-   To build an image run `docker build -t lemma .` in this folder
-   For debugging purposes, you may want enter the container and override the entry point: `docker run -it --entrypoint /bin/bash lemma`

## License

MIT.
