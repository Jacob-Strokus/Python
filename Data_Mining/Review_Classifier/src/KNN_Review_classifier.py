import nltk
import numpy as np
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import ToktokTokenizer
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


nltk.download('stopwords')
nltk.download('wordnet')  # for stemming
tokenizer = ToktokTokenizer()

"""
Function to calculate the K nearest neighbors.
"""
def knn(train_vector, test_vector, score, k):
    classification = []
    similarities = cosine_similarity(test_vector, train_vector)
    for sim in similarities:
        counter = 0
        nearest_neighbors = np.argsort(-sim)[:k + 1]
        for neighbor in nearest_neighbors:
            if int(score[neighbor]) == 1:
                counter += 1

        if counter < 0.5 * k:
            classification.append(-1)
        else:
            classification.append(1)

    return classification


"""
Function to preprocess the data i.e. remove punctuation, remove stop words, stem, and convert words to lower case.
"""
def preprocess_data(data):
    no_punct_data = data.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    token_words = tokenizer.tokenize(no_punct_data)  # Tokenizing our data to get words
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in token_words if word not in stop_words]  # remove all the stop words from our data
    lemmatizer = WordNetLemmatizer()
    stemmed_words = "".join([str(lemmatizer.lemmatize(word)) + ' ' for word in filtered_words])  # stem the data
    return stemmed_words.lower()


"""
Function to convert the train and text data into features.
"""
def get_features(train_data, test_data):
    count_vectorizer = CountVectorizer(preprocessor=preprocess_data, ngram_range=(1, 3), min_df=2, max_df=0.95,
                                       max_features=8000)
    train_vector = count_vectorizer.fit_transform(train_data)
    test_vector = count_vectorizer.transform(test_data)
    return train_vector, test_vector


"""
Function to perform cross-validation through k-fold technique we learned in class.
"""
def kfolds(train_data):

    accuracy_list = []
    k_fold = 5
    k = 134
    training_set = train_data.to_numpy()
    length = len(training_set)

    i = 0
    while i < k_fold:
        split = int((length / k_fold))

        te_subset = training_set[length - (split * (i + 1)): length - (split * (i + 1)) + split]
        test_subset = pd.DataFrame(te_subset)
        test_score_subset = test_subset.iloc[:, 0]
        x_test = test_subset.iloc[:, -1]

        tr_subset = np.concatenate((training_set[:length - (split * (i + 1))], training_set[length -
                                                                                            (split * (i + 1)) + split:]), axis=0)
        train_subset = pd.DataFrame(tr_subset)
        y_train = train_subset.iloc[:, 0]
        x_train = train_subset.iloc[:, -1]

        actual = test_score_subset.tolist()

        train_vec, test_vec = get_features(x_train, x_test)
        expected = knn(train_vec, test_vec, y_train, k)

        print("Fold %d:" % (i + 1), "\nConfusion matrix:")
        print(metrics.confusion_matrix(actual, expected))
        acc = metrics.accuracy_score(actual, expected)
        print("Accuracy: %s" % (acc * 100), "\n")
        accuracy_list.append(acc)

        np.random.shuffle(training_set)  # shuffle the data set after each fold
        i += 1  # increment loop

    print(accuracy_list)
    np.mean(accuracy_list)


"""
Function controls the flow of the program. Driver function.
"""
def main():
    k = 134

    train_data = pd.read_csv('train.csv', header=None)
    train_data.columns = ["y", "x"]
    x_train = train_data["x"]
    y_train = train_data["y"]

    test_data = pd.read_csv('test.csv', header=None)
    test_data.columns = ["x"]
    x_test = test_data["x"]

    train_vec, test_vec = get_features(x_train, x_test)
    classification = knn(train_vec, test_vec, y_train, k)

    with open("results.txt", "w") as f:
        for each in classification:
            f.write(str(each) + "\n")

    kfolds(train_data)


if __name__ == "__main__":
    main()
