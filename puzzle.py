import os
import ecdsa
import binascii
import hashlib
import base58
import random
import time
import codecs
import multiprocessing
from cryptotools.BTC import PrivateKey, Address

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



nomber_ite = int((int(end, 16) - int(start, 16))/addr_per_thread)

def hash160(hex_str):
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(hex_str)
    rip.update( sha.digest() )
    return rip.hexdigest()  # .hexdigest() is hex ASCII

def get_addr(private_key):
	Private_key = bytes.fromhex(private_key)

	signing_key = ecdsa.SigningKey.from_string(Private_key, curve = ecdsa.SECP256k1)
	verifying_key = signing_key.get_verifying_key()
	public_key = bytes.fromhex("04") + verifying_key.to_string()
	public_key = public_key.hex()

	if (ord(bytearray.fromhex(public_key[-2:])) % 2 == 0):
		pubkey_compressed = '02'
	else:
		pubkey_compressed = '03'
	pubkey_compressed += public_key[2:66]
	hex_str = bytearray.fromhex(pubkey_compressed)

	# Obtain key:

	key_hash = '00' + hash160(hex_str)

	# Obtain signature:

	sha = hashlib.sha256()
	sha.update( bytearray.fromhex(key_hash) )
	checksum = sha.digest()
	sha = hashlib.sha256()
	sha.update(checksum)
	checksum = sha.hexdigest()[0:8]

	return str(base58.b58encode( bytes(bytearray.fromhex(key_hash + checksum))))

def thread_f(start_l, thread_no):
	# Progress bar
	progress = -0.01

	for e in range(0, addr_per_thread) :
		# Show progress (can be disabled)
		if e%(addr_per_thread/10000) == 0:
			progress += 0.01
			f = open("nohup.out", "a")
			f.write(str(thread_no) + " => " + str(progress) + "%\n")
			f.close()

		# Getting the current private key
		current = ""
		for e in range(64 - len(start_l)):
			current = current + "0"
		current = current + str(hex(int(start_l,16) + e)[2:])

		#Searching the address associated
		addrp2pkh = (get_addr(current)[2:])[:-1]

		# If you find the result, it will be written in this file 
		if(addrp2pkh == pub_addr_searched):
			f = open("result.txt", "a")
			f.write(current)
			f.close()
			print("found")

	return

def setup_dataset(from_file_no = 0, to_file_no = num_of_temp_file):
	# Create a dataset and shuffle it
	# If you have a memory error in this part, you can increase the value of the num_of_temp_file variable

	print("Seting up dataset ..")

	from_addr = int(start, 16) + addr_per_thread * from_file_no
	to_addr = int(start, 16) + addr_per_thread * to_file_no

	files = []
	for e in range(from_file_no, to_file_no):
		files.append(open("todo_" + str(e) + ".txt", "w"))

	for e in range(from_addr, to_addr, addr_per_thread):
		files[int((e-from_addr)/addr_per_thread)%num_of_temp_file].write(hex(e)[2:]+"\n")

	for e in range(0, to_file_no-from_file_no):
		files[e].close()

	print("Done !\n")


def shuffle_dataset(from_file_no = 0, to_file_no = num_of_temp_file):
	# We shuffle each temp file and we join them into one bigger file

	print("Shuffling")

	file_list = [e for e in range(from_file_no, to_file_no)]

	# We shuffle each file
	for e in range(from_file_no, to_file_no):
		file = open("todo_" + str(e) + ".txt", "r")
		content = file.read().split("\n")
		file.close()

		random.shuffle(content)
		file = open("todo_" + str(e) + ".txt", "w")
		for line in content:
			file.write(line + "\n")
		file.close()

def join_dataset(from_file_no = 0, to_file_no = num_of_temp_file):
	# We create a list of open files

	file_iterators = []
	for file in range(from_file_no, to_file_no):
		file_iterators.append(open("todo_" + str(file) + ".txt"))

	# We randomly read these values and apend it to the main file
	todo_file = open("todo.txt", "w")
	while len(file_iterators) > 0:
		file_iterator = file_iterators[random.randint(0, len(file_iterators)-1)]
		try:
			line = next(file_iterator)

			if line == "\n":
				continue

			todo_file.write(line)
		except Exception as e:
			# If the file is empty
			file_iterator.close()
			file_iterators.remove(file_iterator)

	todo_file.close()

	for e in range(from_file_no, to_file_no):
		# We remove temp files
		os.remove("todo_" + str(e) + ".txt")

	print("Done !")

if __name__ == "__main__":
	thread_l = []

	if need_setup_dataset:
		for e in range(nb_thread_max):
			from_file_no = int(e * (num_of_temp_file/nb_thread_max))
			to_file_no = int((e+1) * (num_of_temp_file/nb_thread_max))
			x = multiprocessing.Process(target=setup_dataset, args=(from_file_no, to_file_no,))
			x.start()
			thread_l.append(x)

		for e in thread_l:
			e.join()

		thread_l = []
		for e in range(nb_thread_max):
			from_file_no = int(e * (num_of_temp_file/nb_thread_max))
			to_file_no = int((e+1) * (num_of_temp_file/nb_thread_max))
			x = multiprocessing.Process(target=shuffle_dataset, args=(from_file_no, to_file_no,))
			x.start()
			thread_l.append(x)

		for e in thread_l:
			e.join()

		thread_l = []
		join_dataset()


	todo_f = open("todo.txt", 'r')
	count = 0

	for count in range(0, nomber_ite+1):
		line = next(todo_f)[:-1]

		if len(thread_l) != nb_thread_max:
			print(count, "/", nomber_ite)
			x = multiprocessing.Process(target=thread_f, args=(line,len(thread_l),))
			x.start()
			thread_l.append(x)

		else:
			for x in thread_l:
				x.join()
			thread_l = []
			count-=1
