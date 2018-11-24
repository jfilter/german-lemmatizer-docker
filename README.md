<div align="center">
  <img src="matt-artz-353291-unsplash.jpg" alt="Scissors">
</div>

# `German Lemmatizer`

Combining the Power of Several Tools for [Lemmatization](https://en.wikipedia.org/wiki/Lemmatisation) of German Text.

Built upon:

-   [IWNLP](https://github.com/Liebeck/spacy-iwnlp) uses the crowd-generated token tables on [de.wikitionary](https://de.wiktionary.org/).
-   [GermaLemma](https://github.com/WZBSocialScienceCenter/germalemma): Looks up lemmas in the [TIGER Corpus](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/) and uses [Pattern](https://www.clips.uantwerpen.be/pattern) as a fallback for some rule-based lemmatizations.

`German Lemmatizer` works as follows. First [spaCy](https://spacy.io/) tags the token with POS. Then `German Lemmatizer` looks up lemmas on IWNLP and GermanLemma. If they disagree, choose the one from IWNLP. If they agree or only one tool finds it, take it. Try to preserve the casing of the original token.

## Installation

1. Install [Docker](https://docs.docker.com/).

## Usage

1. Read and accept the [license terms of the TIGER Corpus](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/license/htmlicense.html) (free to use for non-commercial purposes).
2. Start Docker.
3. To execute, you have two options:

    1. To lemmatize a string from the termial, run:

    ```bash
    docker run -it filter/german-lemmatizer:0.3.0 "Was ist das für ein Leben?"
    ```

    2. To lemmatize a collection of text, add two local folders to the docker container (NB: you have to give absolute paths):

    ```bash
    docker run -it -v $(pwd)/some_input_folder:/input -v $(pwd)/some_output_folder:/output filter/german-lemmatizer:0.3.0 [--line]
    ```

    With `--line` each lines is treated as a single document instead of the whole file.

## The Case for Reproduciblilty

Everything – all the code and all the data – is packaged in the Docker image. This means that every lemmatization is reproduceable. For the future, I may update the code and/or data but each images is tagged with a specific version.

## Dev Remarks

-   Tried to base in on an [Docker Apline Image](https://hub.docker.com/_/alpine/) but there were too many installation hassels.
-   Tried to parallelise with [joblib](https://github.com/joblib/joblib) but it created too much overhead
-   To build an image run `docker build -t lemma .` in this folder
-   For debugging purposes, you may want enter the container and override the entry point: `docker run -it --entrypoint /bin/bash lemma`

## License

MIT.
