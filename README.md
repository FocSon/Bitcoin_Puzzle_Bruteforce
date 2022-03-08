# Bitcoin Puzzle Bruteforce

## Introduction
This program has for goal to bruteforce the following puzzle :
https://privatekeyfinder.io/bitcoin-puzzle/

## Installation
To use this script, you'll need to install git and pip.
Then, run this command to install all required libraries.
```shell
pip install -r requirements.txt
```

## Parameters
I've designed it to be multithreaded and very flexible.
There is some parameters at the beginning of the cade than you can modify in order to make the process answer to your needs.

```python
# Parameters :

# If you don't need to recreate the dataset, set it to False
need_setup_dataset = True

# Number of thread (max 2 per core, more will be useless)
nb_thread_max = 3

# Number of address that a unique thread will have to process (WARNING : the lower this value is, the bigger the dataset will be)
addr_per_thread = 7000000000

#Number of temp file to create (the higher this value is, the lower RAM is used)
num_of_temp_file = 100

#The searched address
pub_addr_searched = "16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN"

# Range in wich you want to search the address
start = "8000000000000000"
end = "ffffffffffffffff"
```
