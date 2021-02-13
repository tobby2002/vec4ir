import sys
import time
import pandas as pd
from gensim.models import Word2Vec, FastText
from ir.doc2vec import Doc2VecInference, Matching
from ir.base import Tfidf
from ir.word2vec import WordCentroidDistance, FastTextCentroidDistance, \
    WordMoversDistance, FastWordCentroidRetrieval, WordCentroidRetrieval, Word2VecRetrieval, StringSentence
from ir.base import Matching, Tfidf
from ir.core import Retrieval
from ir.utils import build_analyzer
from ir.query_expansion import CentroidExpansion, EmbeddedQueryExpansion
from tqdm import tqdm
from ir.utils import build_analyzer
from util import dbmanager, logmanager, dirmanager, utilmanager
from ir.text_preprocessing import TextPreprocessing
from util.utilmanager import build_analyzer, to_jaso, tokenize_by_morpheme_jaso, tokenize_by_morpheme_char

DOCUMENTS = ["This article is about the general concept of art. For the group of creative disciplines, see The arts. For other uses, see Art (disambiguation). Clockwise from upper left: a self-portrait by Vincent van Gogh; a female ancestor figure by a Chokwe artist; detail from The Birth of Venus by Sandro Botticelli; and an Okinawan Shisa lion Art is a diverse range of human activities in creating visual, auditory or performing artifacts (artworks), expressing the author's imaginative, conceptual ideas, or technical skill, intended to be appreciated for their beauty or emotional power.[1][2] In their most general form these activities include the production of works of art, the criticism of art, the study of the history of art, and the aesthetic dissemination of art. The three classical branches of art are painting, sculpture and architecture.[3] Music, theatre, film, dance, and other performing arts, as well as literature and other media such as interactive media, are included in a broader definition of the arts.[1][4] Until the 17th century, art referred to any skill or mastery and was not differentiated from crafts or sciences. In modern usage after the 17th century, where aesthetic considerations are paramount, the fine arts are separated and distinguished from acquired skills in general, such as the decorative or applied arts.Though the definition of what constitutes art is disputed[5][6][7] and has changed over time, general descriptions mention an idea of imaginative or technical skill stemming from human agency[8] and creation.[9] The nature of art and related concepts, such as creativity and interpretation, are explored in a branch of philosophy known as aesthetics.[10]",
                "Science (from the Latin word scientia, meaning knowledge is a systematic enterprise that builds and organizes knowledge in the form of testable explanations and predictions about the universe.[2][3][4] The earliest roots of science can be traced to Ancient Egypt and Mesopotamia in around 3500 to 3000 BCE.[5][6] Their contributions to mathematics, astronomy, and medicine entered and shaped Greek natural philosophy of classical antiquity, whereby formal attempts were made to provide explanations of events in the physical world based on natural causes.[5][6] After the fall of the Western Roman Empire, knowledge of Greek conceptions of the world deteriorated in Western Europe during the early centuries (400 to 1000 CE) of the Middle Ages[7] but was preserved in the Muslim world during the Islamic Golden Age.[8] The recovery and assimilation of Greek works and Islamic inquiries into Western Europe from the 10th to 13th century revived natural philosophy,[7][9] which was later transformed by the Scientific Revolution that began in the 16th century[10] as new ideas and discoveries departed from previous Greek conceptions and traditions.[11][12][13][14] The scientific method soon played a greater role in knowledge creation and it was not until the 19th century that many of the institutional and professional features of science began to take shape;[15][16][17] along with the changing from natural philosophy to the natural sciences.[18] Modern science is typically divided into three major branches that consist of the natural sciences (e.g., biology, chemistry, and physics), which study nature in the broadest sense; the social sciences (e.g., economics, psychology, and sociology), which study individuals and societies; and the formal sciences (e.g., logic, mathematics, and theoretical computer science), which study abstract concepts. There is disagreement,[19][20] however, on whether the formal sciences actually constitute a science as they do not rely on empirical evidence.[21] Disciplines that use existing scientific knowledge for practical purposes, such as engineering and medicine, are described as applied sciences.[22][23][24][25] Science is based on research, which is commonly conducted in academic and research institutions as well as in government agencies and companies. The practical impact of scientific research has led to the emergence of science policies that seek to influence the scientific enterprise by prioritizing the development of commercial products, armaments, health care, and environmental protection.",
                "안녕하세요 여기는 한국에서 가장 좋은 나라 입니다.",
                "안넝 안농 안녕 안너ㄴ 나는 한국 나라 짜파게티",
             "Computer scientists are lazy art"]

# DOCUMENTS = ["The quick brown fox jumps over the lazy dog",
#              "Surfing surfers do surf on green waves"]




def test_word2vecretrieval_ir():
    docs = ["the quick", \
                 "brown fox", \
                 "jumps over", \
                 "the lazy dog", \
                 "This is a document about coookies and cream and fox and dog", \
                 "The master thesis on the information retrieval task"]
    sentences = StringSentence(docs)
    from gensim.models import Word2Vec
    print('sentences')
    print(sentences)
    model = FastText(sentences, min_count=1)
    word2vec = Word2VecRetrieval(model,
                                 # match_fn=None,
                                 )
    _ = word2vec.fit(docs)
    # values = word2vec.evaluate([(0, "fox"), (1, "dog")], [[0, 1, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0]])
    docids, score = word2vec.query('quic')
    print(docids, score)

    # values['mean_average_precision']
    # 1.0
    # values['mean_reciprocal_rank']
    # 1.0
    # values['ndcg@k']
    # (1.0, 0.0)
test_word2vecretrieval_ir()

DEFAULT_ANALYZER = utilmanager.build_analyzer('sklearn', stop_words=False, lowercase=True)
def test_fasttext_similar_ir():
    model = FastText([DEFAULT_ANALYZER(doc) for doc in DOCUMENTS], min_count=1)
    model.save('model_ft')
    model.init_sims(replace=True)

    model = Word2Vec.load('model_ft')
    match_op = Matching()
    wcr = Word2VecRetrieval(model.wv, analyzer=DEFAULT_ANALYZER)
    retrieval = Retrieval(wcr, matching=match_op)  #, labels=['1번', '2번', '3번', '4번', '5번', '6번', '7번', '8번'])
    retrieval.fit(DOCUMENTS)

    start = time.time()  # 시작 시간 저장
    result, score = retrieval.query("안냥")
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    print(result)
    print(score)
# test_fasttext_similar_ir()

def test_word2vec_similar_ir():
    model = Word2Vec([DEFAULT_ANALYZER(doc) for doc in DOCUMENTS], iter=3, min_count=1)
    model.save('model_w2v')
    model.init_sims(replace=True)

    model = Word2Vec.load('model_w2v')
    # match_op = Matching()
    wcr = Word2VecRetrieval(model.wv, analyzer=DEFAULT_ANALYZER)
    retrieval = Retrieval(wcr)  #, matching=match_op)  #, labels=['1번', '2번', '3번', '4번', '5번', '6번', '7번', '8번'])
    retrieval.fit(DOCUMENTS)

    start = time.time()  # 시작 시간 저장
    result, score = retrieval.query("안냥", return_scores=True)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    print(result)
    print(score)
# test_word2vec_similar_ir()

def test_word2vec():
    model = Word2Vec([DEFAULT_ANALYZER(doc) for doc in DOCUMENTS], iter=3, min_count=1)
    model.save('model_w2v')
    model.init_sims(replace=True)

    model = Word2Vec.load('model_w2v')
    match_op = Matching()
    wcd = WordCentroidDistance(model.wv)
    retrieval = Retrieval(wcd, matching=match_op)
    retrieval.fit(DOCUMENTS)

    start = time.time()  # 시작 시간 저장
    result, score = retrieval.query("general", return_scores=True)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    print(result)
    print(score)

# test_word2vec()
    # assert result[0] == 0

def test_fasttext():
    import config

    print("time :start")  # 현재시각 - 시작시간 = 실행 시간
    # model = FastText([doc.split() for doc in DOCUMENTS], size=100, workers=16, sg=1, iter=3, word_ngrams=5)
    # model = FastText([tokenize_by_eojeol_jaso(doc) for doc in DOCUMENTS], size=100, workers=16, sg=1, iter=3, word_ngrams=5)
    # model = FastText([to_jaso(doc) for doc in DOCUMENTS], size=50, workers=12, sg=1, iter=3, word_ngrams=1)


    # model = FastText([tokenize_by_eojeol_jaso(doc) for doc in DOCUMENTS], size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
    # model = FastText([tokenize_by_eojeol_jaso(doc) for doc in DOCUMENTS], size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)


    model = FastText([ tokenize_by_morpheme_char(doc) for doc in DOCUMENTS], size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
    # model.train(DOCUMENTS, total_examples=len(DOCUMENTS), epochs=config.MODEL_EPOCHS)
    model.save('model_ft')
    print("save model_ft")
    # model.init_sims(replace=True)
    model = FastText.load('model_ft')
    match_op = Matching()
    wcd = FastTextCentroidDistance(model.wv)

    ### simple mode
    # retrieval = Retrieval(wcd, matching=match_op)

    ### expansion mode
    n_expansions = 2
    expansion_op = EmbeddedQueryExpansion(model.wv, m=n_expansions)
    retrieval = Retrieval(wcd,  # The retrieval model
                          matching=match_op,
                          query_expansion=expansion_op)


    retrieval.fit(DOCUMENTS)

    start = time.time()  # 시작 시간 저장
    q = '한국에서 가장 좋은 나라'
    # qparse = to_jaso(q)
    print(q)
    result, score = retrieval.query(q, return_scores=True)
    # result = retrieval.query(q)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    print(result, score)

# test_fasttext()

def test_centroid_expansion():
    model = Word2Vec([doc.split() for doc in DOCUMENTS], iter=1, min_count=1)

    model = Word2Vec.load('model_w2v')
    m = 2
    expansion = CentroidExpansion(model.wv, m=m)
    expansion.fit(DOCUMENTS)
    query = "surf"
    expanded_query = expansion.transform(query)
    # surf => surf surf Surfing
    print(query, expanded_query, sep='=>')
    assert len(expanded_query.split()) == len(query.split()) + m



def test_embedded_query_expansion():
    model = Word2Vec([doc.split() for doc in DOCUMENTS], iter=1, min_count=1)
    m = 2
    expansion = EmbeddedQueryExpansion(model.wv, m=m)
    expansion.fit(DOCUMENTS)
    query = "evaluate and test word "
    expanded_query = expansion.transform(query)
    # surf => surf surf Surfing
    print(query, expanded_query, sep='=>')
    assert len(expanded_query.split()) == len(query.split()) + m

def test_expansion_inside_retrieval():
    # Integration test within full retrieval pipeline
    model = Word2Vec([doc.split() for doc in DOCUMENTS], iter=1, min_count=1)
    # model.save('model_w2v_e')
    # model.init_sims(replace=True)
    # model = Word2Vec.load('model_w2v_e')
    n_expansions = 2
    tfidf = Tfidf()
    match_op = Matching()
    expansion_op = EmbeddedQueryExpansion(model.wv, m=n_expansions)

    retrieval = Retrieval(tfidf,  # The retrieval model
                          matching=match_op,
                          query_expansion=expansion_op)
    # ids = ['fox_ex', 'surf_ex']
    # retrieval.fit(DOCUMENTS, ids)
    retrieval.fit(DOCUMENTS)
    start = time.time()  # 시작 시간 저장
    result = retrieval.query("An 81-year-old woman named Eileen")
    print(result)

    result, score = retrieval.query("한국에서 가장 좋은 나라", return_scores=True)

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    print('result:%s' % result)
    print('score:%s' % score)
    # assert result[0] == 'surf_ex'
# test_expansion_inside_retrieval()

def test_tfidf():
    # Test tfidf retrieval with auto-generated ids
    tfidf = Tfidf()
    tfidf.fit(DOCUMENTS)
    result, score = tfidf.query('안녕 scientists', return_scores=True)
    print(result, score)
# test_tfidf()