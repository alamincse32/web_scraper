from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.append('i\'ve')
print(stop_words)