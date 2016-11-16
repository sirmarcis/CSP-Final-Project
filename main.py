import numpy as np
import random
import os, sys

from matrix import gen_multi_matricies, save_matricies, read_matricies




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