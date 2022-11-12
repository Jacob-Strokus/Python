from sklearn.model_selection import train_test_split
import numpy as np
import keras

active_counter = 0
inactive_counter = 0
active_dict = {}
inactive_dict = {}

# function to calculate products in the set
def calculate_product(likelihood_set, activity, e):
    product = 0
    for item in likelihood_set:
        product = pow((item / activity), e)
    return product


def naive_bayes_training():

    global active_counter
    global inactive_counter
    global active_dict
    global inactive_dict

    train_file = open("train.dat", "r")

    while True:
        line = train_file.readline()
        if line == "":
            break

        data = line[2:].split(" ")[:-1]  # skip training score
        active = int(line[0])
        for x in data:
            if active == 0:
                inactive_counter += 1
                if x in inactive_dict:
                    inactive_dict[x] += 1
                else:
                    inactive_dict[x] = 1
            elif active == 1:
                active_counter += 1
                if x in active_dict:
                    active_dict[x] += 1
                else:
                    active_dict[x] = 1

    remove = []
    for key, val in active_dict.items():
        if key not in inactive_dict:
            remove.append(key)
    for key in remove:
        active_dict.pop(key)
    to_remove = []
    for key, val in inactive_dict.items():
        if key not in active_dict:
            to_remove.append(key)
    for key in to_remove:
        inactive_dict.pop(key)

    train_file.close()


def naive_bayes_testing():

    test_file = open("test.dat", "r")
    out_file = open("naive_bayes.txt", "w")
    output_string = ""

    total = active_counter + inactive_counter
    prior0 = inactive_counter / total
    prior1 = active_counter / total

    while True:
        line = test_file.readline()
        if line == "":
            break

        data = line.split(" ")[:-1]

        prob0_set = []
        prob1_set = []
        for item in data:
            if item in inactive_dict:
                if inactive_dict[item] / len(inactive_dict) > 0.00001:
                    prob0_set.append(inactive_dict[item])

            if item in active_dict:
                if active_dict[item] / len(active_dict) > 0.00001:
                    prob1_set.append(active_dict[item])

        # calculate nb
        prob0_raw = calculate_product(prob0_set, inactive_counter, 0.02)
        prob1_raw = calculate_product(prob1_set, active_counter, 0.02)

        total = prob0_raw + prob1_raw

        # normalize the likelihood of each class probability
        likelihood0 = prob0_raw / total
        likelihood1 = prob1_raw / total

        p0 = prior0 * likelihood0
        p1 = prior1 * likelihood1

        if p0 > p1:
            output = "0\n"
        elif p0 < p1:
            output = "1\n"
        else:  # there was a tie
            output = "0\n"

        output_string += output

    out_file.write(output_string)
    test_file.close()
    out_file.close()


def neural_network():

    train_file = open("train.dat", "r")
    test_file = open("test.dat", "r")
    out_file = open("neural_network.txt", "w")
    output_string = ""
    train_shape = (800, 100001)  # 100001
    x_train = np.zeros(train_shape)
    y_train = np.zeros(800)
    test_shape = (350, 100001)  # 100001
    testing_data = np.zeros(test_shape)
    count = 0

    while True:
        line = train_file.readline()
        if line == "":
            break

        data = line[2:].split(" ")[:-1]  # skip train score
        y_train[count] = int(line[0])
        for read_elem in data:
            x_train[count][int(read_elem)] = 1
        count += 1

    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, stratify=y_train, test_size=0.5,
                                                        random_state=0)
    nn_model = keras.Sequential()
    input_layer = keras.layers.Dense(256, input_shape=(100001,))
    nn_model.add(input_layer)
    hidden_layer1 = keras.layers.Dropout(0.5)
    nn_model.add(hidden_layer1)
    hidden_layer2 = keras.layers.Dense(200, activation="relu")
    nn_model.add(hidden_layer2)
    hidden_layer3 = keras.layers.Dense(200, activation="relu")
    nn_model.add(hidden_layer3)
    output_layer = keras.layers.Dense(1, activation="hard_sigmoid")
    nn_model.add(output_layer)
    nn_model.compile(loss="binary_crossentropy", optimizer="sgd", metrics=["binary_accuracy"])
    nn_model.fit(x_train, y_train, epochs=24, batch_size=32)
    loss, acc = nn_model.evaluate(x_test, y_test)

    count = 0

    while True:
        line = test_file.readline()
        if line == "":
            break

        data = line.split(" ")[:-1]
        for read_elem in data:
            testing_data[count][int(read_elem)] = 1
        count += 1

    output = nn_model.predict(testing_data)

    for each_class in output:
        probability = each_class[0] + loss
        if probability > 0.54:
            output = "1\n"
        else:
            output = "0\n"

        output_string += output

    out_file.write(output_string)
    test_file.close()
    out_file.close()


# naive_bayes_training()
# naive_bayes_testing()
neural_network()
