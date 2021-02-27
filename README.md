# Vec4IR+Tensorflow LTR
(venv) neoui-iMac:bin neo1$ alias python=python3


References
----------
$ python manage.py makemigrations <app-name>
$ python manage.py migrate <app-name>
$ python manage.py showmigrations <app-name>
 python manage.py sqlmigrate <app-name> <migration-name>


Word embeddings for information retrieval.
[![DOI](https://zenodo.org/badge/85768267.svg)](https://zenodo.org/badge/latestdoi/85768267)
[![Build Status](https://travis-ci.org/lgalke/vec4ir.svg?branch=master)](https://travis-ci.org/lgalke/vec4ir)


## Quick start

Visit the [test file](tests/ir/test_vec4ir.py) for a rough but quick introduction to the framework.
For a comparison between the methods available in vec4ir, we refer to our  paper [Word Embeddings for Practical Information Retrieval](https://dl.gi.de/handle/20.500.12116/3987) ([Author Copy](http://lpag.de/publications/word_embeddings_for_IR.pdf)).

## For word2vec
https://github.com/kavgan/nlp-in-practice/blob/master/word2vec/Word2Vec.ipynb
https://www.freecodecamp.org/news/how-to-get-started-with-word2vec-and-then-how-to-make-it-work-d0a2fca9dad3/

## Tensorflow Saver 
http://jaynewho.com/post/8

User’s guide
============

<img src="figures/vec4ir-associations.png" alt="Detailed information retrieval pipeline as considered in the vec4ir framework. With the query node as starting point, each out-going edge is a configurable option of the native evaluation script. Rectangles resemble algorithms, and folder-like shapes resemble data stored on disk. One example configuration is highlighted by bold edges." id="basics-ir" style="width:100.0%" />

Philosophy
----------

The information retrieval framework `vec4ir` has the goal is *simulate* a practical information retrieval setting. In order to encourage research in this field, the focus lies on extensibility. Adding a new retrieval model for evaluation should be as easy as possible. The target audience are researchers evaluating their own retrieval models and curious data scientists, who want to evaluate which retrieval model fits their data best.

Terminology
-----------

In the following, We recapture the most important definitions that are relevant to the framework.

### Information Retrieval (IR)

The information retrieval task can be defined as follows:

Given a corpus of documents *D* and a query *q*, return {*d* ∈ *D* ∣ *d* relevant to *q*} in rank order.

A practical information retrieval system typically consists of at least the two
components: [matching](#def:matching), [similarity scoring](#def:scoring).
Several other components can also be considered, such as query expansion,
pseudo-relevance feedback, query parsing and the analysis process itself.

### Matching

The matching operation refers to the initial filtering process of documents.
For instance, the output of the matching operation contains all the document
which contain *at least one* of the query terms. Other variants of the matching
operation may also allow fuzzy matching (up to a certain threshold in
Levenshtein distance) or enforce exact match of a phrase.

### Similarity scoring

The scoring step refers to the process of assigning scores. The scores resemble
the relevance of a specific document to the query. They are used to create a
ranked ordering of the matched documents. This sorting happens either
ascending, when considering distance scores, or descending in case of
similarity scores.

### Word embeddings and Word2Vec

A word embedding is a distributed (dense) vector representation for each word
of a vocabulary. It is capable of capturing semantic and syntactic properties
of the input texts . Interestingly, even arithmetic operations on the word
vectors are meaningful: e.g. *King* - *Queen* = *Man* - *Woman*. The two most
popular approaches to learn a word embedding from raw text are:

-   Skip-Gram Negative Sampling by Mikolov et al. (2013) (Word2Vec)
-   Global Word Vectors by Pennington, Socher, and Manning (2014) (GloVe)

Skip-gram negative sampling (or Word2Vec) is an algorithm based on a shallow
neural network which aims to learn a word embedding. It is highly efficient, as
it avoids dense matrix multiplication and does not require the full term
co-occurrence matrix. Given some target word *w*<sub>*t*</sub>, the
intermediate goal is to train the neural network to predict the words in the
*c*-neighbourhood of *w*<sub>*t*</sub>:
*w*<sub>*t* − *c*</sub>, …, *w*<sub>*t* − 1</sub>, *w*<sub>*t* + 1</sub>, …, *w*<sub>*t* + *c*</sub>.
First, the word is directly associated to its respective vector, which as used
as input for a (multinomial) logistic regression to predict the words in the
*c*-neighbourhood. Then, the weights for the logistic regression are adjusted,
as well as the vector itself (by back-propagation). The Word2Vec algorithm
employs negative sampling: additional *k* noise words which do not appear in
the *c*-neighbourhood are introduced as possible outputs, for which the desired
output is known to be `false`. Thus, the model does not reduce the weights to
all other vocabulary words but only to those sampled *k* noise words. When
these noise words appear in a similar context as *w*<sub>*t*</sub>, the model
gets more and more fine-grained over the training epochs. In contrast to
Word2Vec, the GloVe (Pennington, Socher, and Manning 2014) algorithm computes
the whole term co-occurrence matrix for a given corpus. To obtain word vectors,
the term co-occurrence matrix is factorised. The training objective is that the
euclidean dot product of each two word vectors match the log-probability of
their words’ co-occurrence.

### Word centroid similarity (WCS)

An intuitive approach to use word embeddings in information retrieval is the
word centroid similarity (WCS). The representation for each document is the
centroid of its respective word vectors. Since word vectors carry semantic
information of the words, one could assume that the centroid of the word
vectors within a document encodes its meaning to some extent.
At query time, the centroid of the query’s word vectors is computed.
The cosine similarity to the centroids of the (matching) documents is used
as a measure of relevance. When the initial word frequencies of the queries and
documents are first re-weighted according to inverse-document frequency
(i.e. frequent words in the corpus are discounted), the technique is labeled
IDF re-weighted word centroid similarity (IWCS).

Features
--------

The key features of this information retrieval framework are:

-   Simulation of a practical IR setting
-   Native word embedding support in conjunction with `gensim` (Řehuřek and Sojka 2010))
-   Built-in evaluation
-   API design inspired by `sklearn` (Buitinck et al. 2013) .
-   Extendable by new retrieval models

Dependencies
------------

Besides `python3` itself, the package `vec4ir` depends on the following python packages.

-   [numpy](http://www.numpy.org/)
-   [scipy](http://www.scipy.org/)
-   [gensim](http://radimrehurek.com/gensim/)
-   [pandas](http://pandas.pydata.org/)
-   [networkx](https://networkx.github.io/)
-   [rdflib](https://rdflib.readthedocs.io/en/stable/)
-   [nltk](http://www.nltk.org/)
-   [sklearn](http://scikit-learn.org/stable/index.html)
-   [pyyaml](http://pyyaml.org/wiki/PyYAMLDocumentation)

Installation
------------

As `vec4ir` is packaged as a python package, it can be installed by via `pip`:

``` sh
cd python-vec4ir; pip install -e .
```

In case anything went wrong with the installation of dependencies, try to install them manually: We also recommend to install `numpy` and `scipy` in beforehand (either manually, or as binary system packages).

``` sh
pip3 install -r requirements.txt
```

In addition, we provide a helper script to setup a new virtual environment. It
can be invoked `requirements.sh` to setup a new virtual environment `venv` in
the current working directory. The newly created virtual environment has to be
activated via `source <venv-name>/bin/activate` before performing the actual installation
steps as described above.


## WordMoversDistance and wmd

To compute the Word Mover's distance, the `pyemd` package is required.
It can be installed via `pip install pyemd`. However, the python3 developer
system package (such as `python3-devel` on Solus) may be required for the
installation of `pyemd` to succeed.

The evaluation script
---------------------

The package includes a native command line script `vec4ir-evaluate` for
evaluation of an information retrieval pipeline. The pipeline of query
expansion, matching and scoring is applied to a set of queries and the metrics
mean average precision (MAP), mean reciprocal rank (MRR), normalised discounted
cumulative gain (NDCG), precision and recall are computed. Hence, the script
may be used *as-is* for evaluation of your datasets or as a reference
implementation for the usage of the framework. The behaviour of the evaluation
script and the resulting information retrieval pipeline can be controlled by
the following command-line arguments:

#### Meta options

As a meta option (affecting other options), we allow the specification of a configuration file.

-   `-c, --config` Path to a configuration file, in which the file paths for the datasets and embedding models are specified. The default value is `config.yml`.

#### General options

-   `-d, --dataset` The data set to operate on. (mandatory)
-   `-e, --embedding` The word embedding model to use. (mandatory)
-   `-r, --retrieval-model` The retrieval model for similarity scoring. One of `tfidf` (default), `wcd`, `wmd`, `d2v`.
-   `-q, --query-expansion` The expansion technique to apply on the queries. One of `wcd`, `eqe1`, `eqe2`.

The arguments `--dataset` and `--embedding` expect the provided keys to be present in the configuration file specified by `--config`. While the key for the embedding should be below `embeddings` in the configuration file, the key for the dataset should be below `data`. An minimal example structure would be:

``` yaml
embeddings:
    word2vec: # possible value for --embedding
        path: "/path/to/GoogleNews-vectors-negative300.bin.gz"
data:
    short-ntcir2: # possible value for --dataset
        type: "ntcir"
        root_path: "path/to/data/NTCIR2/"
        field: "title"
        topic: "title"
        rels: 2
```

The options below the respective keys specify the responsible constructor
(`type`) and its arguments (`root_path`, `field`, …). More details on the
natively supported dataset formats can be found in the [developer’s
guide](devguide.md). The alternatives for the retrieval model
(`--retrieval-model`) are described in more detail
[below](#employing-word-embeddings).

#### Embedding options

-   `-n, --normalize` Normalise the embedding model’s word vectors.
-   `-a, --all-but-the-top` All-but-the-top embedding post-processing as proposed by Mu, Bhat, and Viswanath (2017) .
-   `-t, --train` Number of epochs used for up-training out-of-vocabulary words.

In the special case of `--train 0` the behaviour of the script is *not* equivalent to omitting this parameter. After building a vocabulary from the input documents, the word vectors are *intersected* with the word vectors of the embedding. More specific, missing vocabulary words are initialised with close-to-zero random vectors. Instead, out-of-vocabulary words are ignored, when the `--train` parameter is omitted.

#### Retrieval options

-   `-I, --no-idf` Do *not* use IDF re-weighted word frequencies for aggregation of word vectors.
-   `-w, --wmd` Fraction of *additional* documents to take into account for `wmd` retrieval model.

By default, `vec4ir-evaluate` uses IDF re-weighted word centroid similarity if `-r wcd` is provided. If IDF re-weighting is not desired, it is necessary to provide the `--no-idf` argument. The `--wmd` argument refers to the fraction of additional documents to consider, when the Word Mover’s distance (`-r wmd`) was chosen as retrieval model. For example, consider `--wmd 0.1` and 120 matching documents for a specific query. When 20 documents should be retrieved, the word centroid similarity is consulted to retrieve the top 20 + 0.1 ⋅ (120 − 20)=30 documents. These 30 most relevant (with respect to word centroid similarity) documents are then be re-ranked according to the Word Mover’s distance. A `--wmd` value of zero corresponds to re-ranking the top *k* documents by Word Mover’s distance, while the highest possible value of `1.0` corresponds to computing the full Word Mover’s distance without taking the WCS into account.

#### Output options

The output options control the online and persistent output of the evaluation script. The special option `--stats` can be provided to compute the ratio of out-of-vocabulary tokens, print the top 50 most frequent out-of-vocabulary tokens and exit.

-   `-o, --output` File path for writing the output.
-   `-v, --verbose` Verbosity level.
-   `-s, --stats` Compute out-of-vocabulary statistics and exit.

#### Evaluation options

The following arguments affect the evaluation process:

-   `-k` Number of documents to retrieve (defaults to 20).
-   `-Q, --filter-queries` Drop queries, which contain out-of-vocabulary words.
-   `-R, --replacement` Treatment for missing relevance information in the gold standard. Chose `drop` to disregard them (default) or `zero` to treat them as non-relevant.

In most cases, the defaults of *not* filtering the queries and replacing missing values by zeroes (indicating non-relevance) are appropriate.

#### Analysis options

The analysis process of splitting a string into tokens can be customised by the following arguments:

-   `-M, --no-matching` Do *not* conduct a matching operation.
-   `-T, --tokenizer` The tokeniser for the matching operation. One of `sklearn`, `sword`, `nltk`.
-   `-S, --dont-stop` Do *not* remove English stop-words.
-   `-C, --cased` Conduct a case *sensitive* analysis.

Please note that the analysis process, also directly affects the matching operation. The defaults are to conduct a matching operation, tokenise according to `sklearn` tokeniser (F. Pedregosa et al. 2011) (a token consists of at least two subsequent word-characters), remove English stop-words and transform all characters to lower case. The `sword` tokeniser additionally considers single-character words as token. The `nltk` tokeniser retains all punctuation punctuation as tokens (Bird 2006).

Basic framework usage
---------------------

We provide a minimal example including the matching operation and the [TF-IDF retrieval model](http://kak.tx0.org/IR/TFxIDF). As an example, assume we have two documents `fox valley` and `dog nest` and two queries `fox` and `dog`. First, we create an instance of the `Matching` class, whose optional arguments are passed directly to `sklearn`’s `CountVectorizer`.

``` python
>>> match_op = Matching()
```

In its default form, the matching is a non-fuzzy boolean `OR` matching. The `Matching` instance can be used after fitting a set of documents via `match_op.fit(documents)` using its `match_op.predict(query_string)` method to return the indices of the matching documents. However, the preferred way to apply the matching operation is inside of a `Retrieval` instance. The `Retrieval` instance expects a retrieval model as mandatory argument, besides an optional `Matching` instance (and an optional query expansion instance). For now, we create an instance of the `Tfidf` class and pass it to the `Retrieval` constructor.

``` python
>>> tfidf = Tfidf()
>>> retrieval = Retrieval(retrieval_model=tfidf, matching=match_op)
>>> retrieval.fit(titles)
>>> retrieval.query("fox")
[0]
>>> retrieval.query("dog")
[1]
```

At index time, the `Retrieval` instance invokes the `fit` method on the provided delegates of query expansion, matching and the retrieval model. At query time, the `Retrieval` instance consults the `predict` method of the `matching` argument for a set of matching indices. The matching indices are passed as `indices` keyword argument to the `query` method of the retrieval model. The result of the retrieval model is then transformed back into respective the document identifiers.

Employing word embeddings
-------------------------

Several supplied retrieval models make use of a word embedding. However those retrieval models do not learn a word embedding themselves, but take a `gensim` `Word2Vec` object as argument.

``` python
from gensim.models import Word2Vec
model = Word2Vec(documents['full-text'], min_count=1)
wcd = WordCentroidDistance(model)
RM = Retrieval(wcd, matching=match_op).fit(documents['full-text'])
```

Several embedding-based retrieval models are provided natively:

-   Word centroid similarity  
    The cosine similarity between centroid of the document’s word vectors and the centroid of the query’s word vectors (`WordCentroidDistance(idf=False)`).

-   IDF re-weighted word centroid similarity  
    The cosine similarity between the document centroid and the query centroid after re-weighting the terms by inverse document frequency (`WordCentroidDistance(idf=True)`).

-   Word Mover’s distance  
    The cost of moving from the words of the query to the words of the documents is minimised. The optional `complete` parameter (between zero and one) allows to control the amount of considered documents. Setting `complete=0` results in re-ranking the documents returned by word centroid similarity with respect to Word Mover’s Distance, while setting `complete=1.0` computes the Word Movers distance for all matched documents.

-   Doc2Vec inference  
    The `Doc2VecInference` class expects a `gensim` `Doc2Vec` instance as base model instead of a `Word2Vec` object. The model is employed to infer document vectors for the documents and the queries. The matching documents are ranked according to the cosine similarity between inferred vectors of the query and the documents. The parameters `alpha`, `min_alpha` and `epochs` control the inference step of the `Doc2Vec` instance.

All these provided embedding-based retrieval models are designed for usage inside the `Retrieval` wrapper.

Evaluating the model
--------------------

To evaluate your retrieval model `RM` just invoke its `evaluate(X, Y)` method with `X` being a list of (`query_id`, `query_string`) pairs. The gold standard `Y` is a two-level data structure. The first level corresponds to the `query_id` and the second level to the `document_id`. Thus `Y[query_id][document_id]` should return the relevance number for the specific query-document pair. The exact type of `Y` is flexible, it can be a list of dictionaries, a 2-dimensional `numpy` array, or a `pandas.DataFrame` with a (hierarchical) multi-index.

``` python
scores = RM.evaluate(X, Y)
```

The `evaluate(X, Y, k=None)` method returns a dictionary of various computed metrics per query. The scores can be manually reduced to their mean afterwards with a dictionary comprehension:

``` python
import numpy as np
mean_scores = {k : np.mean(v) for k,v in scores.items()}
```

The metrics and therefore keys of the resulting scores dictionary consist of:

-   `MAP`  
    Mean Average Precision (`@k`)

-   `precision`  
    Precision (`@k`)

-   `recall`  
    Recall (`@k`)

-   `f1_score`  
    Harmonic mean of precision and recall

-   `ndcg`  
    Normalised discounted cumulative gain (produces sensible scores with respect to the gold standard, even if *k* is given)

-   `MRR`  
    Mean reciprocal rank (`@k`)

Where *k* is the number of documents to retrieve.

Extending by new models
-----------------------

In order to create a new retrieval model, one has to implement a class with at least two methods: `fit(X)` and `query(query, k=None, indices=None)`. In the following, we will demonstrate the implementation of a dummy retrieval model: the `GoldenRetriever` model which returns a random sample of *k* matched documents.

``` python

import random as RNG

class GoldenRetriever(RetriEvalMixin):
    def __init__(self, seed='bone'):
        # Configuration
        RNG.seed(seed)
      
    def fit(self, documents):
        # Keep track of the documents
        self._fit_X = np.asarray(documents)

    def query(self, query, k=None, indices=None):
        # Pre-selected matching documents
        if indices is not None:
            docs = self._fit_X[indices]
        else:
            docs = self._fit_X

        # Now we could do more magic with docs, or…
        ret = RNG.sample(range(docs.shape[0]), k)

        # Note that our result is assumed to be
        # relative to the matched indices
        # and NOT a subset of them
        return ret
```

The newly developed class contains the following three mandatory methods:

-   The constructor  
    All configuration is performed in the constructor, such that the model is ready to fit documents. No expensive computation is performed in the constructor.

-   `fit(self, documents)`  
    The `fit` method is called at index time, the retrieval model becomes aware of the documents and saves its internal representation of the documents.

-   `query(self, query, k=None, indices=None)`  
    The `query` method is called at query time. Beside the query string itself, it is expected to allow two keyword arguments: `k` resembling the number of desired documents, and `indices` which provides the indices of documents, that matched the query.

The reduction of the models own view on the documents (`docs = self._fit_X[indices]`) is important, since the returned indices are expected to be relative to this reduction (more details in the next section). These relative indices provide one key benefit. Oftentimes, the documents identifiers are not plain indices but string values. Using relative (to the matching) indices allows our retrieval model to disregard the fact that the document identifiers could be a string value or some other index, which does not match the position in our array of documents `X`. The presumably surrounding `Retrieval` class will keep track of the document identifiers for you and transpose the query’s result `ret` to the identifier space.

The inheritance from `RetriEvalMixin` provides the `evaluation` method described above, which internally invokes the `query` method of the new retrieval model.

Matching, scoring, and query expansion
--------------------------------------

We provide a `Retrieval` class that implements the desired retrieval process of Figure . The `Retrieval` class consists of up to three components. It combines the retrieval model (mentioned above) as mandatory object and two optional objects: a matching operation and a query expansion object. Upon invocation of `fit(X)` the `Retrieval` class delegates the documents `X` to all prevalent components, i.e. it calls `fit(X)` on the matching object, the query expansion object, and the retrieval model object. A query expansion class is expected to provide two methods.

-   `fit(X)`  
    This method is invoked with the set of raw documents `X`

-   `transform(q)`  
    This method is invoked with the query string `q` and should return the expanded query string.

We provide more details on the implementation of a full information retrieval pipeline in the [Developer’s Guide](devguide.md).

Combining multiple fields and models
------------------------------------

**Highly experimental, some techniques do not support it yet**

The `vec4ir` package also provides an experimental operator overloading API for combining multiple retrieval models.

``` python
RM_title = WordCentroidDistance().fit(documents['title'])
RM_content = Tfidf().fit(documents['full-text'])
RM = RM_title ** 2 + RM_content  # Sum up scores, weight title field twice
R = Retrieval(retrieval_model=RM, labels=documents['id'])
```

On invocation of the `query` method on the combined retrieval model `RM`, both
the model for the title and the model for the content get consulted and their
respective scores are merged according to the operator. Operator overloading is
provided for addition, multiplication, as well as the power operator `**`, which
effectivly weights all returned scores of the retrieval model.

For these `Combined` retrieval models, the consulted operand retrieval models are
expected to return (`doc_id`, `score`) pairs in their result set. However, in
this case the result set does not have to be sorted. Thus, the query method of
the operand retrieval models is invoked with `sort=False`. Still, the
retrieval instance `R` will invoke the outer-most, combined retrieval model with `sort=True`,
such that the final results can be sorted.

References
----------
$ python manage.py makemigrations <app-name>
$ python manage.py migrate <app-name>
$ python manage.py showmigrations <app-name>
 python manage.py sqlmigrate <app-name> <migration-name>


Scheduler for IR/LTR 
check below in api/views.py
# from . import scheduler
# sc = scheduler.Scheduler()
# ir_model_dic = sc.irmodel_dic

Example for GET api 
----------
# e.g. 
http://127.0.0.1:8000/api/indexing/solr/test_analytics?fl=id,sales_i,expenses_i,savings_i,share_value_i,created_dt&rows=1000&fq__created_dt=[2020-12-28T00:00:00Z%20TO%202021-01-3T00:00:00Z]&facet_date_field_start=2020-12-28T00:00:00Z&facet_date_field_end=2021-01-3T00:00:00Z

pip freeze > requirements.txt

# mecab # 설치법 
# MeCab MacOS + python 설치 삽질 후기 (리뉴얼)
https://calyfactory.github.io/mecab%EC%9D%98-custom-dictionary%EC%99%80-konlpy-%EC%97%B0%EB%8F%99%ED%95%98%EA%B8%B0/
https://joyae.github.io/2020-10-02-Mecab/  --> good
                      https://lovablebaby1015.wordpress.com/2018/09/24/mecab-macos-%EC%84%A4%EC%B9%98-%EC%82%BD%EC%A7%88-%ED%9B%84%EA%B8%B0-%EC%9E%91%EC%84%B1%EC%A4%91/

##########################################
mecab install
##########################################
mecab-ko 설치
mecab-dic 설치
mecab-python 설치


## 소개
[MeCab](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html)에서 제공하는 [python 바인딩 소스](https://code.google.com/p/mecab/downloads/detail?name=mecab-python-0.996.tar.gz&can=2&q=)가 Python 3.x에서 문제를 일으키므로 SWIG를 최신  버전(SWIG 3.0.0)을 사용하여 다시 생성한 소스입니다.

1) mecab-ko 설치

https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz
tar -xvf mecab-0.996-ko-0.9.2.tar.gz
cd mecab-0.996-ko-0.9.2
./configure
make
sudo make install

2) mecab-dic 설치
https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz
tar -xvf mecab-ko-dic-2.1.1-20180720.tar.gz
cd mecab-ko-dic-2.1.1-20180720
./configure
make
sudo make install

다음과 같은 과정을 거치면 기본으로 /usr/local/lib/mecab/dic/mecab-ko-dic에 설치가 된다.

sudo chmod -R 777 /usr/local/lib/mecab/dic/mecab-ko-dic
sudo chown -R wi:wi /usr/local/lib/mecab/dic/mecab-ko-dic

3) mecab-python 설치
mecab-python-0.996 Installation
## 설치
    :::text
    % git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git
    % cd mecab-python-0.996
    % python setup.py build
    % su
    # python setup.py install
You can change the install directory with the --prefix option. For example:

    :::text
    % python setup.py install --prefix=/usr/local/lib/mecab/dic/mecab-ko-dic
## 사용법
샘플 프로그램인 test.py를 참조하세요.
##########################################
mecab 설치순서 end
##########################################


#jamo process
https://joyhong.tistory.com/137
# word2vec
https://ichi.pro/ko/gensim-eul-sayongayeo-word2vec-hunlyeon-22278944385252

# [장애 메세지]ModuleNotFoundError: No module named '_sqlite3'[해결 방안]
1. Install the sqlite-devel package:
yum install sqlite-devel -y
2. Recompile python from the source:
./configure
make
make altinstall
출처: https://kogun82.tistory.com/192 [Ctrl+C&V 로 하는 프로그래밍]

sqlite-devel-3.7.17-8.el7_7.1.x86_64.rpm


####
AttributeError: module '_jpype' has no attribute 'setResource'

sudo pip uninstall konlpy
sudo pip uninstall JPype1
sudo pip uninstall JPype1-py3
sudo pip uninstall lxml
sudo pip uninstall numpy

삭제하고 재 설치
sudo pip install konlpy
sudo pip install lxml
sudo pip install numpy

select sa.* from pg_catelog.pg_stat_activity sa



