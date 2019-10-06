# https://stackoverflow.com/questions/27488446/how-do-i-get-word-frequency-in-a-corpus-using-scikit-learn-countvectorizer
from sklearn.feature_extraction.text import CountVectorizer
corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?',
]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
terms_name = vectorizer.get_feature_names()
print(terms_name)
# ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
toarray = X.toarray()
print(toarray)
# [[0 1 1 1 0 0 1 0 1]
#  [0 2 0 1 0 1 1 0 1]
#  [1 0 0 1 1 0 1 1 1]
#  [0 1 1 1 0 0 1 0 1]]

# todense = X.todense()
# print('todense:', todense)

sumarray = X.toarray().sum(axis=0)


print(sumarray)
#[1 4 2 4 1 1 4 1 4]


list_zip = list(zip(terms_name, toarray, sumarray))

print('list_zip:', list_zip)

list_zip_0 = list_zip[0]
print('list_zip[0]:', list_zip_0)

a = list_zip_0[0]
b = list_zip_0[1]

print(a, b)
mean = b/sumarray

print('mean:', mean)

sum_mean = sum(mean)
sum_len = len(mean)

print('count_mean_value:', sum_mean/sum_len)


