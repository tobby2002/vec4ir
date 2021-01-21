import sys
import time
import pandas as pd
from gensim.models import Word2Vec
from ir.doc2vec import Doc2VecInference, Matching
from ir.base import Tfidf
from ir.word2vec import WordCentroidDistance, WordMoversDistance
from ir.base import Matching, Tfidf
from ir.core import Retrieval
from ir.utils import build_analyzer
from ir.query_expansion import CentroidExpansion, EmbeddedQueryExpansion

DOCUMENTS = ["This article is about the general concept of art. For the group of creative disciplines, see The arts. For other uses, see Art (disambiguation). Clockwise from upper left: a self-portrait by Vincent van Gogh; a female ancestor figure by a Chokwe artist; detail from The Birth of Venus by Sandro Botticelli; and an Okinawan Shisa lion Art is a diverse range of human activities in creating visual, auditory or performing artifacts (artworks), expressing the author's imaginative, conceptual ideas, or technical skill, intended to be appreciated for their beauty or emotional power.[1][2] In their most general form these activities include the production of works of art, the criticism of art, the study of the history of art, and the aesthetic dissemination of art. The three classical branches of art are painting, sculpture and architecture.[3] Music, theatre, film, dance, and other performing arts, as well as literature and other media such as interactive media, are included in a broader definition of the arts.[1][4] Until the 17th century, art referred to any skill or mastery and was not differentiated from crafts or sciences. In modern usage after the 17th century, where aesthetic considerations are paramount, the fine arts are separated and distinguished from acquired skills in general, such as the decorative or applied arts.Though the definition of what constitutes art is disputed[5][6][7] and has changed over time, general descriptions mention an idea of imaginative or technical skill stemming from human agency[8] and creation.[9] The nature of art and related concepts, such as creativity and interpretation, are explored in a branch of philosophy known as aesthetics.[10]",
                "Science (from the Latin word scientia, meaning knowledge is a systematic enterprise that builds and organizes knowledge in the form of testable explanations and predictions about the universe.[2][3][4] The earliest roots of science can be traced to Ancient Egypt and Mesopotamia in around 3500 to 3000 BCE.[5][6] Their contributions to mathematics, astronomy, and medicine entered and shaped Greek natural philosophy of classical antiquity, whereby formal attempts were made to provide explanations of events in the physical world based on natural causes.[5][6] After the fall of the Western Roman Empire, knowledge of Greek conceptions of the world deteriorated in Western Europe during the early centuries (400 to 1000 CE) of the Middle Ages[7] but was preserved in the Muslim world during the Islamic Golden Age.[8] The recovery and assimilation of Greek works and Islamic inquiries into Western Europe from the 10th to 13th century revived natural philosophy,[7][9] which was later transformed by the Scientific Revolution that began in the 16th century[10] as new ideas and discoveries departed from previous Greek conceptions and traditions.[11][12][13][14] The scientific method soon played a greater role in knowledge creation and it was not until the 19th century that many of the institutional and professional features of science began to take shape;[15][16][17] along with the changing from natural philosophy to the natural sciences.[18] Modern science is typically divided into three major branches that consist of the natural sciences (e.g., biology, chemistry, and physics), which study nature in the broadest sense; the social sciences (e.g., economics, psychology, and sociology), which study individuals and societies; and the formal sciences (e.g., logic, mathematics, and theoretical computer science), which study abstract concepts. There is disagreement,[19][20] however, on whether the formal sciences actually constitute a science as they do not rely on empirical evidence.[21] Disciplines that use existing scientific knowledge for practical purposes, such as engineering and medicine, are described as applied sciences.[22][23][24][25] Science is based on research, which is commonly conducted in academic and research institutions as well as in government agencies and companies. The practical impact of scientific research has led to the emergence of science policies that seek to influence the scientific enterprise by prioritizing the development of commercial products, armaments, health care, and environmental protection.",
                "Deep learning (also known as deep structured learning or hierarchical learning) is part of a broader family of machine learning methods based on artificial neural networks. Learning can be supervised, semi-supervised or unsupervised.[1][2][3] Deep learning architectures such as deep neural networks, deep belief networks, recurrent neural networks and convolutional neural networks have been applied to fields including computer vision, speech recognition, natural language processing, audio recognition, social network filtering, machine translation, bioinformatics, drug design, medical image analysis, material inspection and board game programs, where they have produced results comparable to and in some cases superior to human experts.[4][5][6] Artificial Neural Networks (ANNs) were inspired by information processing and distributed communication nodes in biological systems. ANNs have various differences from biological brains. Specifically, neural networks tend to be static and symbolic, while the biological brain of most living organisms is dynamic (plastic) and analog.[7][8][9]",
                "Cable News Network (CNN) is an American news-based pay television channel owned by AT&T's WarnerMedia.[1] CNN was founded in 1980 by American media proprietor Ted Turner as a 24-hour cable news channel.[2] Upon its launch, CNN was the first television channel to provide 24-hour news coverage,[3] and was the first all-news television channel in the United States.[4] While the news channel has numerous affiliates, CNN primarily broadcasts from 30 Hudson Yards in New York City, and studios in Washington, D.C. and Los Angeles. Its headquarters at the CNN Center in Atlanta is only used for weekend programming. CNN is sometimes referred to as CNN/U.S. (or CNN Domestic)[5] to distinguish the U.S. channel from its international sister network, CNN International. As of August 2010, CNN is available in over 100 million U.S. households.[6] Broadcast coverage of the U.S. channel extends to over 890,000 American hotel rooms,[6] as well as carriage on subscription providers throughout Canada. As of July 2015, CNN is available to about 96,374,000 pay-television households (82.8% of households with at least one television set) in the United States.[7] Globally, CNN programming airs through CNN International, which can be seen by viewers in over 212 countries and territories.[8]The following is a list of notable current and past news anchors, correspondents, hosts, regular contributors and meteorologists from the CNN, CNN International and HLN news networks.[1]",
                "ABC News is the news division of the American Broadcasting Company (ABC), owned by the Disney Media Networks division of The Walt Disney Company. Its flagship program is the daily evening newscast ABC World News Tonight with David Muir; other programs include morning news-talk show Good Morning America, Nightline, Primetime, and 20/20, and Sunday morning political affairs program This Week with George Stephanopoulos.Only after Roone Arledge, the president of ABC Sports at the time, was appointed as president of ABC News in 1977, at a time when the network's prime-time entertainment programs were achieving stronger ratings and drawing in higher advertising revenue and profits to the ABC corporation overall, was ABC able to invest the resources to make it a major source of news content. Arledge, known for experimenting with the broadcast 'model', created many of ABC News' most popular and enduring programs, including 20/20, World News Tonight, This Week, Nightline and Primetime Live.[3] ABC News' longtime slogan, 'More Americans get their news from ABC News than from any other source' (introduced in the late 1980s), was a claim referring to the number of people who watch, listen to and read ABC News content on television, radio and (eventually) the Internet, and not necessarily to the telecasts alone.[4] In June 1998, ABC News (which owned an 80% stake in the service), Nine Network and ITN sold their respective interests in Worldwide Television News to the Associated Press. Additionally, ABC News signed a multi-year content deal with AP for its affiliate video service Associated Press Television News (APTV) while providing material from ABC's news video service ABC News One to APTV.[5]",
             "Computer scientists are lazy art"]

# train_data = "../data/movies.tsv"
# df = pd.read_csv(docu_data, sep='\t', names=['no', 'title', 'content'], header=None)

docu_data = "../../data/movie_text/text_summarizer_data.csv"
df = pd.read_csv(docu_data, sep=',', names=['no', 'title', 'content'], header=None)
docu_title = df['content'].values.tolist()
print(docu_title)

# DOCUMENTS = ["The quick brown fox jumps over the lazy dog",
#              "Surfing surfers do surf on green waves"]
def test_word2vec():
    # model = Word2Vec([doc.split() for doc in DOCUMENTS], iter=5, min_count=1)
    # model.save('model_w2v')
    # model.init_sims(replace=True)

    model = Word2Vec.load('model_w2v')
    match_op = Matching()
    wcd = WordCentroidDistance(model.wv)
    retrieval = Retrieval(wcd, matching=match_op)
    retrieval.fit(DOCUMENTS)

    start = time.time()  # 시작 시간 저장
    result = retrieval.query("An 81-year-old woman named Eileen")
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    print(result)

# test_word2vec()
    # assert result[0] == 0

def test_centroid_expansion():
    # model = Word2Vec([doc.split() for doc in DOCUMENTS], iter=1, min_count=1)

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
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    print(result)
    # assert result[0] == 'surf_ex'
test_expansion_inside_retrieval()

