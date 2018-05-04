import sys

# Getting arguments
training_file_name = sys.argv[1]
testing_file_name = sys.argv[2]
algorithm = sys.argv[3]

# A set of entries for which each entry is made up of another list with corresponding attributes.
training_entries = []
testing_entries = []

# Open files
training_file = open(training_file_name, "r")
testing_file = open(testing_file_name, "r")

# Reading training entries.
for line in training_file:
    training_entries.append(line.rstrip('\n').split(","))
