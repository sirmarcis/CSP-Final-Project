import numpy as np
import random
import os, sys



def save_matricies(matrix_str_arr):
	"""Save randomly generated matricies to seperate files"""
	matrix_cntr = 0
	for curr_matrix_str in matrix_str_arr:
		matrix_filename = "Example Matrices/matrix_" + str(matrix_cntr) + ".txt"
		with open(matrix_filename, 'w') as writefile:
			writefile.write(curr_matrix_str)
		matrix_cntr+=1

def read_matricies():
	"""Load in all previously written to file matricies"""
	matrix_arr = []
	curr_dirpath = os.getcwd()
	for subdir, dirs, files in os.walk(curr_dirpath + '/Example Matrices'):
		for curr_file in files:
			curr_filepath = curr_dirpath + '/Example Matrices/' + curr_file
			with open(curr_filepath, 'r') as open_file:
				for line in open_file:
					if len(line) > 0:
						curr_matrix = np.matrix(line)
						matrix_arr.append(curr_matrix)
	return matrix_arr

def build_arr_of_size(arr_size):
	curr_arr_cntr = 1
	the_arr = []
	while curr_arr_cntr <= arr_size:
		the_arr.append(curr_arr_cntr)
		curr_arr_cntr+=1
	return the_arr

def convert_arr_to_str(curr_arr):
	the_str = ''
	for arr_elt in curr_arr:
		the_str+= str(arr_elt) + ' '
	return the_str.rstrip()

def gen_random_matrix(row_len, col_len):
	curr_row_cntr = 1
	matrix_str = ''
	while curr_row_cntr <= row_len:
		curr_row = build_arr_of_size(col_len)
		random.shuffle(curr_row)
		curr_row_str = convert_arr_to_str(curr_row)
		if curr_row_cntr != row_len:
			matrix_str += (curr_row_str + ';')
		else:
			matrix_str += curr_row_str
		curr_row_cntr+=1
	return np.matrix(matrix_str), matrix_str

def gen_multi_matricies(num_matricies, matrix_row_len, matrix_col_len):
	cur_mat_cntr = 0
	matrix_arr = []
	matrix_str_arr = []
	while cur_mat_cntr < num_matricies:
		curr_matrix, curr_matrix_str = gen_random_matrix(matrix_row_len, matrix_col_len)
		matrix_arr.append(curr_matrix)
		matrix_str_arr.append(curr_matrix_str)
		cur_mat_cntr+=1
	return matrix_arr, matrix_str_arr

def main():
	if len(sys.argv) > 1:
		if len(sys.argv) == 4:
			if sys.argv[1] == "--newMatricies" or sys.argv[1] == "-N":
				row_len = int(sys.argv[2])
				col_len = int(sys.argv[3])
				print "generating new matricies of dimensions [", row_len, ", ", col_len, "] ..."
				rand_matricies, rand_matrix_str_arr = gen_multi_matricies(2,4,4)
				print "System matrix:"
				print rand_matricies[0]
				print "User matrix:"
				print rand_matricies[1]
				save_matricies(rand_matrix_str_arr)
				return
		print "Error: usage; should be '$ main.py [--newMatricies/-N] [rowLen] [colLen]'", len(sys.argv)
	else:
		print "using old matricies from files..."
		old_matricies = read_matricies()
		print "System matrix:"
		print old_matricies[0]
		print "User matrix:"
		print old_matricies[1]
	

if __name__ == '__main__':
	main()