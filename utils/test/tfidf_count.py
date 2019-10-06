from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords

train_set = ["The sky is blue.", "The sun is bright."] #Documents
test_set = ["The sun in the sky is bright."] #Query
stopWords = stopwords.words('english')

vectorizer = CountVectorizer(stop_words=stopWords)
transformer = TfidfTransformer()

trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()
testVectorizerArray = vectorizer.transform(test_set).toarray()
print('Fit Vectorizer to train set', trainVectorizerArray)
print('Transform Vectorizer to test set', testVectorizerArray)

transformer.fit(trainVectorizerArray)
print(transformer.transform(trainVectorizerArray).toarray())

transformer.fit(testVectorizerArray)

tfidf = transformer.transform(testVectorizerArray)
print('tfidf dense:', tfidf.todense())
