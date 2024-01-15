import random


def get_shuffled_names(correct_name, incorrect_name):
    print(incorrect_name)
    names = [correct_name, incorrect_name]

    random.shuffle(names)

    return names