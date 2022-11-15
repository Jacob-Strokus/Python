from csv import reader
from sklearn.model_selection import train_test_split
from colorama import Fore, Style
import pandas as pd
import numpy as np
import keras
import time

DEBUG = True
response_file = "Please tell us how often you felt this way over the past week.csv"
response1 = 0
response2 = 0
response3 = 0
response4 = 0
response5 = 0
response6 = 0

user = [response1, response2, response3, response4, response5, response6]
user_list = []

"""
 Helper function to parse each user's survey results, and convert them to numerical data 
 our neural network and understand.
"""
def parse(row, response):
    if str(row) == 'None':
        response = 0
    elif str(row) == '1-2 days':
        response = 1
    elif str(row) == '3-4 days':
        response = 2
    elif str(row) == '5 or more days':
        response = 3

    return response


"""
 Helper function to read the responses everyone gave in the survey, turn them into numerical data, 
 and tie each user's numerical data to a list which will represent that user, and add that user to our
 global list of users.
"""
def read_responses(rsp):
    global response1
    global response2
    global response3
    global response4
    global response5
    global response6
    global user
    global user_list

    with open(rsp, "r") as my_file:
        file_reader = reader(my_file)
        next(file_reader)
        counter = 1
        for i in file_reader:
            if DEBUG:
                print(f"Row {counter}: ", i[1:-1])  # DEBUG to check that the responses are properly recorded.

            response1 = parse(i[1], response1)
            response2 = parse(i[2], response2)
            response3 = parse(i[3], response3)
            response4 = parse(i[4], response4)
            response5 = parse(i[5], response5)
            response6 = parse(i[6], response6)

            user = (response1, response2, response3, response4, response5, response6)
            user_list.append(user)
            counter += 1

        return user_list


"""
 Helper function to get the number of rows and 
 number of columns from the excel file
"""
def get_rows_columns(loc):
    df = pd.read_csv(loc)
    return len(df.index), len(df.columns)


"""
 Helper function to check our neural network accuracy against
"""
def summation(data):
    sum_t = 0
    count = 1

    for i in data:
        # if i == len(data):  # the last question was the control, so skip it
        #     break
        sum_t += i
        count += 1

    return sum_t / count


""" Helper function creates and computes an Artificial Neural Network, which loosely model the neurons in the 
    biological brain. """
def compute_nn(responses):
    count = 0

    rows, columns = get_rows_columns(response_file)

    if DEBUG:
        print(f"# of Rows: {rows}, # of Columns: {columns}")

    train_shape = (rows, columns)  # number of rows, number of columns in our training data
    x_train = np.zeros(train_shape)  # vectorize the data
    y_train = np.zeros(columns)  # vectorize the data
    test_shape = (rows, columns)
    testing_data = np.zeros(test_shape)

    train_shape = (800, 100001)
    x_train = np.zeros(train_shape)
    y_train = np.zeros(800)
    test_shape = (350, 100001)
    testing_data = np.zeros(test_shape)

    for each_response in responses:
        data = each_response[1:]  # skip first column (timestamp)
        if DEBUG:
            print("CONVERTED NUMERICAL DATA: ", data)
        y_train[count] = int(each_response[0])
        for read_elem in data:
            x_train[count][int(read_elem)] = 1
        count += 1

    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.5,
                                                        random_state=0)

    # Build layers Sequentially
    nn_model = keras.Sequential()
    input_layer = keras.layers.Dense(256, input_shape=(100001,))  # this will be the # of columns in our dataset
    nn_model.add(input_layer)

    # internal layer with dropout (randomly sets input to 0 at 0.5 frequency) which helps with overfitting the data
    # if not dropped are scaled up by 1/(1 - rate) such that the sum over all inputs is not changed
    hidden_layer1 = keras.layers.Dropout(0.5)
    nn_model.add(hidden_layer1)

    # internal layer has 200 nodes, and uses a "relu" activation function 
    # rectified linear unit activation function will return zero if weight is negative, otherwise it will return 
    # whichever positive weight is calculated
    hidden_layer2 = keras.layers.Dense(200, activation="relu")
    nn_model.add(hidden_layer2)

    # output layer has one output node, and uses a "hard-sigmoid activation function (talk about what this is)
    # hard-sigmoid activation function just means it will produce an output in the range of [0-1] inclusive
    output_layer = keras.layers.Dense(1, activation="hard_sigmoid")
    nn_model.add(output_layer)

    # Compile the neural network with given attributes: Loss, Optimization, Metrics.

    # LOSS: Binary-cross entropy uses logical regression (cross entropy part) with a binary selection (0 or 1) to
    # calculate the "loss"

    # OPTIMIZATION: momentum-based gradient descent function. Through this momentum is accelerated, and correction is
    # dampened to prevent any major oscillations or overcorrections. This helps maximize accuracy while minimizing loss

    # METRICS: binary-accuracy. The accuracy metric for this neural network should be formed by a binary choice (0 or 1)
    nn_model.compile(loss="binary_crossentropy", optimizer="sgd", metrics=["binary_accuracy"])

    # 'Fitting' the model epochs = number of iterations we want the model to perform. Batch_size = # of samples per
    # gradient fitting refers to how many iterations we should do, at a given batch size.
    nn_model.fit(x_train, y_train, epochs=24, batch_size=32)

    # Evaluating our model, will give an accuracy and a % loss
    loss, acc = nn_model.evaluate(x_test, y_test)
    print("Accuracy:" + Fore.GREEN + " {:.2f}".format(acc) + Style.RESET_ALL + " Loss " + Fore.RED + "{:.6f}".format(loss))
    print(Style.RESET_ALL)


"""
Controls the execution flow of our program.
"""
def main():
    global user_list

    user_list = read_responses(response_file)
    time.sleep(2)
    count = 1
    if DEBUG:
        print("Begin training Neural Network...")
        time.sleep(2)
    compute_nn(user_list)
    time.sleep(2)
    print("Preparing results...")
    time.sleep(2)
    print("\n#########################################################################\n")
    for each in user_list:
        if DEBUG:
            print(f"User: {count} responses: {each}")
        sum_t = summation(each)
        print("####### USER {:d} -- Raw score calculated: {:.2f} #######".format(count, sum_t))
        if sum_t > 1.65:
            print(Fore.RED + f"User {count} has been classified as depressed")
        else:
            print(Fore.GREEN + f"User {count} has been classified as not depressed")
        print(Style.RESET_ALL)
        count += 1

    print("\n#########################################################################\n")


main()
