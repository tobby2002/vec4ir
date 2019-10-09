from sklearn.feature_extraction.text import TfidfVectorizer
words = ['the cat sat on the mat cat', 'the fat rat sat on a mat', 'the bat and a rat sat on a mat']
tfidf_vectorizer = TfidfVectorizer(min_df=1, use_idf=True)
tfidf_matrix = tfidf_vectorizer.fit_transform(words)
terms_name = tfidf_vectorizer.get_feature_names()
toarry=tfidf_matrix.todense()
for i in tfidf_matrix.toarray():
    print(zip(terms_name, i))
    print('i:', i)

# [(u'and', 0.0), (u'bat', 0.0), (u'cat', 0.78800079617844954), (u'fat', 0.0), (u'mat', 0.23270298212286766), (u'on', 0.23270298212286766), (u'rat', 0.0), (u'sat', 0.23270298212286766), (u'the', 0.46540596424573533)]
# [(u'and', 0.0), (u'bat', 0.0), (u'cat', 0.0), (u'fat', 0.57989687146162439), (u'mat', 0.34249643393071422), (u'on', 0.34249643393071422), (u'rat', 0.44102651785124652), (u'sat', 0.34249643393071422), (u'the', 0.34249643393071422)]
# [(u'and', 0.50165133177159349), (u'bat', 0.50165133177159349), (u'cat', 0.0), (u'fat', 0.0), (u'mat', 0.29628335772067432), (u'on', 0.29628335772067432), (u'rat', 0.38151876810273028), (u'sat', 0.29628335772067432), (u'the', 0.29628335772067432)]
