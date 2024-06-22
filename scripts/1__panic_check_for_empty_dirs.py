from __global_paths import *

import os

def count_empty_subdirectories(parent_directory):
    # List all subdirectories in the given parent directory
    subdirectories = [os.path.join(parent_directory, d) for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]

    # Count how many of these subdirectories are empty
    empty_count = sum(1 for subdir in subdirectories if not os.listdir(subdir))

    return empty_count

# Replace 'your_parent_directory' with the path to your parent directory
parent_directory = CLONE_REPOS_DIR
empty_subdirectories_count = count_empty_subdirectories(parent_directory)
print(f'Number of empty subdirectories: {empty_subdirectories_count}')