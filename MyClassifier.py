import sys
import math

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
    training_entries_copy = training_entries

    for training_entry in training_entries:
        distances.append(get_euclidean(entry, training_entry))

    minimum_index = 0

    for run in range(0, k):
        for index in range(0, len(training_entries_copy)):
            if distances[index] <= distances[minimum_index]:
                minimum_index = index
        if len(training_entries_copy) is not 0:
            sorted_entries.append(training_entries_copy[minimum_index])
            distances.pop(minimum_index)
            training_entries_copy.pop(minimum_index)
            minimum_index = 0

    return sorted_entries


for entry in get_k_nearest_neighbor(training_entries[0], 10):
    print(entry)
