# Bitcoin Puzzle Bruteforce (Multithreaded)

## Introduction
This program has for goal to bruteforce the following puzzle :
https://privatekeyfinder.io/bitcoin-puzzle/

## Installation
This script is written, in python3
To use this script, you'll need to install git and pip.
Then, run this command to install all required libraries.
```shell
pip3 install -r requirements.txt
```

## Run it
As it is a verry long process, I strongly recommand you to run this command with nohup
```shell
nohup python3 puzzle.py &
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

# Private key range in which you want to search the address (the private key will automatically be completed with 0 before ex: 00[...]00ffffffffffffffff)
start = "8000000000000000"
end = "ffffffffffffffff"
```

## Donations
If this program help you or if it make you win some money here is my BTC address.. We never know ;)
bc1qpst40fj88652akszrr2w2unfwl37kgdm5d7pfj

