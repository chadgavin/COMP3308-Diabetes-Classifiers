import sys

# Getting arguments
training_file = sys.argv[1]
testing_file = sys.argv[2]
algorithm = sys.argv[3]

# A set of entries for which each entry is made up of another list with corresponding attributes.
training_entries = []
testing_entries = []

# Reading training entries.
def readTrainingEntries():
