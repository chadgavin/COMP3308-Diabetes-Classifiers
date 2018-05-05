import sys
import math
import statistics
import scipy
import time

start_time = time.time()
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
            print("yes")
        else:
            print("no")


#                               #tutu
#                               #tutu
#     Naive Bayes algorithm.    #tutu
#                               #tutu
#                               #tutu

# Probability of Class Yes
# ARGUMENT: NONE.
# RETURN: A float value indicating probability.
def probability_of_yes():
    probability = 1

    for attribute_column in range(0, number_of_attributes):
        value = []
        for entry in training_entries:
            if entry[number_of_attributes] == "yes":
                value.append(entry[attribute_column])
        statistics.stdev(value)
        statistics.mean(value)

    return probability


print("--- %s seconds ---" % (time.time() - start_time))
