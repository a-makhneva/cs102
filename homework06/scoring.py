import typing as tp

import naive_bayes.bayes as bayes
import naive_bayes.stemmer as stemmer
from naive_bayes.db import News, session

s = session()
rows = s.query(News).all()
extracts_train: tp.List[str] = []
labels_train: tp.List[str] = []
extracts_test: tp.List[str] = []
labels_test: tp.List[str] = []
# Train dataset is every 7 rows of 10, others are test
for i in range(len(rows)):
    row = s.query(News).filter(News.id == (i + 1)).first()  # id is unique and enumerated from id
    if str(i)[len(str(i)) - 1] in ("0", "1", "2", "3", "4", "5", "6"):
        extracts_train.append(row.title)
        labels_train.append(row.label)
    else:
        extracts_test.append(row.title)
        labels_test.append(row.label)
extracts_test = [stemmer.clear(x).lower() for x in extracts_test]
extracts_train = [stemmer.clear(x).lower() for x in extracts_train]

unique_words_train = []
for sentence in extracts_train:
    words = sentence.split(" ")
    for word in words:
        if not word in unique_words_train:
            unique_words_train.append(word)
print(len(unique_words_train))

unique_words_test = []
for sentence in extracts_test:
    words = sentence.split(" ")
    for word in words:
        if not word in unique_words_test:
            unique_words_test.append(word)
print(len(unique_words_test))

common_words = []
for i in unique_words_test:
    for j in unique_words_train:
        if i == j:
            common_words.append(i)
            break

print(len(common_words))

# The dataset is too small, will try augmetation
X_train, X_test = extracts_train, extracts_test
y_train, y_test = labels_train, labels_test
# X_train, X_test = extracts[:stop_sign], extracts[stop_sign:]
# y_train, y_test = labels[:stop_sign], labels[stop_sign:]
model = bayes.NaiveBayesClassifier(alpha=0.99)
model.fit(X_train, y_train)
print("Classifier accuracy: ", end="")
print(model.score(X_test, y_test))
