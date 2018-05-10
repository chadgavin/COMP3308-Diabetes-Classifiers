import sys
import math
import statistics

# Getting arguments
training_file_name = sys.argv[1]
testing_file_name = sys.argv[2]
algorithm = sys.argv[3]

# A set of entries for which each entry is made up of another list with corresponding attributes.
training_entries = []
testing_entries = []

# Number of attributes for this classification.
# NOTE: This value does not include a class attribute.
number_of_attributes = 0


def read_single_file():
    global training_entries
    global testing_entries
    global number_of_attributes

    # Open files
    training_file = open(training_file_name, "r")
    testing_file = open(testing_file_name, "r")

    # Reading entries.
    for line in training_file:
        attributes = line.rstrip('\n').split(",")
        number_of_attributes = len(attributes) - 1

        for index in range(0, number_of_attributes):
            attributes[index] = float(attributes[index])

        training_entries.append(attributes)

    for line in testing_file:
        attributes = line.rstrip('\n').split(",")

        for index in range(0, number_of_attributes):
            attributes[index] = float(attributes[index])

        testing_entries.append(attributes)

    # Closing file for data integrity.
    training_file.close()
    testing_file.close()


# fold is an integer indicating the testing fold number
def read_fold_file(fold):
    global training_entries
    global testing_entries
    global number_of_attributes

    # Read Testing Fold
    testing_file = open("fold" + str(fold), "r")

    for line in testing_file:

        if line[:4] == "fold":
            continue

        attributes = line.rstrip('\n').split(",")
        number_of_attributes = len(attributes) - 1

        for index in range(0, number_of_attributes):
            attributes[index] = float(attributes[index])

        testing_entries.append(attributes)

    testing_file.close()

    # Read Training Folds
    for index in range(1, 11):

        if index == fold:
            continue

        training_file = open("fold" + str(index), "r")

        # Reading entries.
        for line in training_file:

            if line[:4] == "fold":
                continue

            attributes = line.rstrip('\n').split(",")
            number_of_attributes = len(attributes) - 1

            for index in range(0, number_of_attributes):
                attributes[index] = float(attributes[index])

            training_entries.append(attributes)

        # Closing file for data integrity.
        training_file.close()


#                               #tutu
#                               #tutu
# k-nearest neighbor algorithm. #tutu
#                               #tutu
#                               #tutu

# Calculate Euclidean Distance given two entry.
# ARGUMENT: Two list of attributes.
# RETURN: A float value indicates Euclidean Distance.
def get_euclidean(first_entry, second_entry):
    sum_of_squared_attributes = 0.0

    for index in range(0, number_of_attributes):
        sum_of_squared_attributes += (first_entry[index] - second_entry[index]) ** 2

    return math.sqrt(sum_of_squared_attributes)


# Get k nearest neighbor given a entry and k number.
# ARGUMENT: A list of attributes and an integer.
# RETURN: A list of index of entry that is nearest.
def get_k_nearest_neighbor(entry, k):
    sorted_entries = []
    distances = []
    training_entries_copy = list(training_entries)

    for training_entry in training_entries:
        distances.append(get_euclidean(entry, training_entry))

    minimum_index = 0

    for run in range(0, k):
        for index in range(0, len(training_entries_copy)):
            if distances[index] < distances[minimum_index]:
                minimum_index = index

        if len(training_entries_copy) != 0:
            sorted_entries.append(training_entries_copy[minimum_index])
            distances.pop(minimum_index)
            training_entries_copy.pop(minimum_index)
            minimum_index = 0

    return sorted_entries


# K Nearest Neighbor Classification
# ARGUMENT: k number of nearest neighbor.
# RETURN: NOTHING.
def knn_classification(k):
    actual_results = []
    for entry in testing_entries:
        number_of_yes = 0
        number_of_no = 0
        nearest_neighbor = get_k_nearest_neighbor(entry, k)

        for neighbor in nearest_neighbor:
            if neighbor[number_of_attributes] == "yes":
                number_of_yes += 1
            else:
                number_of_no += 1

        if number_of_yes > number_of_no or number_of_yes == number_of_no:
            if algorithm[-2:] == "NN":
                print("yes")
            actual_results.append("yes")
        else:
            if algorithm[-2:] == "NN":
                print("no")
            actual_results.append("no")

    return actual_results


#                               #tutu
#                               #tutu
#     Naive Bayes Algorithm.    #tutu
#                               #tutu
#                               #tutu

# Naive Bayes algorithm
# ARGUMENT: NONE.
# RETURN: Nothing
def naive_bayes_classification():
    standard_deviation_yes = []
    mean_yes = []
    probability_yes = 1

    standard_deviation_no = []
    mean_no = []
    probability_no = 1

    actual_results = []

    for attribute_column in range(0, number_of_attributes):
        value = []
        for entry in training_entries:
            if entry[number_of_attributes] == "yes":
                value.append(entry[attribute_column])
        standard_deviation_yes.append(statistics.stdev(value))
        mean_yes.append(statistics.mean(value))
        probability_yes = float(len(value)) / float(len(training_entries))

    for attribute_column in range(0, number_of_attributes):
        value = []
        for entry in training_entries:
            if entry[number_of_attributes] == "no":
                value.append(entry[attribute_column])
        standard_deviation_no.append(statistics.stdev(value))
        mean_no.append(statistics.mean(value))
        probability_no = float(len(value)) / float(len(training_entries))

    conditional_probability_yes = 1
    conditional_probability_no = 1

    for entry in testing_entries:
        for attribute_column in range(0, number_of_attributes):
            conditional_probability_yes *= (1 / (
                    standard_deviation_yes[attribute_column] * math.sqrt(2 * math.pi))) * math.exp(-(
                    ((entry[attribute_column] - mean_yes[attribute_column]) ** 2) / (
                    2 * (standard_deviation_yes[attribute_column] ** 2))))
            conditional_probability_no *= (1 / (
                    standard_deviation_no[attribute_column] * math.sqrt(2 * math.pi))) * math.exp(-(
                    ((entry[attribute_column] - mean_no[attribute_column]) ** 2) / (
                    2 * (standard_deviation_no[attribute_column] ** 2))))
        conditional_probability_yes *= probability_yes
        conditional_probability_no *= probability_no

        if conditional_probability_yes > conditional_probability_no or conditional_probability_yes == conditional_probability_no:
            if algorithm == "NB":
                print("yes")
            actual_results.append("yes")
        elif conditional_probability_no > conditional_probability_yes:
            if algorithm == "NB":
                print("no")
            actual_results.append("no")

        conditional_probability_yes = 1
        conditional_probability_no = 1

    return actual_results


def validate_set_generator():
    folds = []

    for index in range(0, 10):
        folds.append([])

    yes_entries = []
    no_entries = []
    is_yes = True
    is_no = False

    for entry in training_entries:
        if entry[number_of_attributes] == "yes":
            yes_entries.append(entry)
        else:
            no_entries.append(entry)

    while True:
        for fold in range(0, 10):
            if is_yes:
                if len(yes_entries) == 0:
                    is_yes = False
                    is_no = True
                else:
                    folds[fold].append(yes_entries[0])
                    yes_entries.pop(0)

            if is_no:
                if len(no_entries) == 0:
                    is_yes = True
                    is_no = False
                else:
                    folds[fold].append(no_entries[0])
                    no_entries.pop(0)

        is_no = not is_no
        is_yes = not is_yes

        if len(yes_entries) == 0 and len(no_entries) == 0:
            break

    for index in range(0, 10):
        file_name = "fold" + str(index + 1)
        file = open(file_name, "w+")
        file.write(file_name + "\n")
        for fold in folds[index]:
            for entry in fold:
                if entry == fold[-1]:
                    file.write(str(entry) + "\n")
                else:
                    file.write(str(entry) + ",")
        file.close()

    for index in range(0, 10):
        num_yes = 0
        num_no = 0
        for entry in folds[index]:
            if entry[number_of_attributes] == "yes":
                num_yes += 1
            else:
                num_no += 1


def validate_knn(k):
    global training_entries
    global testing_entries

    errors = []

    for test_fold in range(0, 10):
        read_fold_file(test_fold + 1)
        expected_results = []
        error_results = 0

        for entry in testing_entries:
            expected_results.append(entry[number_of_attributes])

        actual_results = knn_classification(k)

        for index in range(0, len(expected_results)):
            if actual_results[index] != expected_results[index]:
                error_results += 1

        errors.append(float(error_results) / len(expected_results))

        training_entries = []
        testing_entries = []

    sum_of_errors = 0
    for error in errors:
        sum_of_errors += error

    print("Accuracy for {} neighbors is {}. ".format(k, 1 - (sum_of_errors / 10)))


def validate_nb():
    global training_entries
    global testing_entries

    errors = []

    for test_fold in range(0, 10):
        read_fold_file(test_fold + 1)
        expected_results = []
        error_results = 0

        for entry in testing_entries:
            expected_results.append(entry[number_of_attributes])

        actual_results = naive_bayes_classification()

        for index in range(0, len(expected_results)):
            if actual_results[index] != expected_results[index]:
                error_results += 1

        errors.append(float(error_results) / len(expected_results))

        training_entries = []
        testing_entries = []

    sum_of_errors = 0
    for error in errors:
        sum_of_errors += error

    print("Accuracy for Naive Bayes is {}. ".format(1 - (sum_of_errors / 10)))


if algorithm == "NB":
    read_single_file()
    naive_bayes_classification()

elif algorithm == "VGE":
    read_single_file()
    validate_set_generator()

elif algorithm == "VLKN":
    validate_knn(1)
    validate_knn(3)
    validate_knn(10)
    validate_knn(50)

elif algorithm == "VLNB":
    validate_nb()
else:
    read_single_file()
    k_neighbors = int(algorithm[:-2])
    knn_classification(k_neighbors)

    # Running TIme
    # Accuracy
    # For report

