## main.py
## written by Anders Maraviglia

import numpy as np
import random, os, sys

from matrix import save_matricies, read_matricies
from test_suite import gen_new_sys_user_matrices, run_large_scale_tests, run_full_test_set

def main():
	max_matches = 1
	load_old_matricies = True
	sys_matrices = []
	user_matrices = []
	if len(sys.argv) > 1:
		if len(sys.argv) >= 5:
			if sys.argv[1] == "--newMatricies" or sys.argv[1] == "-N":
				row_len = int(sys.argv[2])
				col_len = int(sys.argv[3])
				num_matrices = int(sys.argv[4])
				if num_matrices % 2 == 0:
					rand_matrix_str_arr = []
					sys_matrices, user_matrices = gen_new_sys_user_matrices(num_matrices, row_len, col_len, rand_matrix_str_arr = rand_matrix_str_arr)
					print "Num system matrix:", len(sys_matrices)
					print "Num user matrix:", len(user_matrices)
					save_matricies(rand_matrix_str_arr)
					load_old_matricies = False
				else:
					print "Error: num requested matrices should be even"
					return 
			else:
				print "Error: usage; should be '$ main.py [--newMatricies/-N] [rowLen] [colLen] [numMatrices]'"
				return
			if len(sys.argv) == 7:
				if sys.argv[5] == "--maxMatches" or sys.argv[5] == "-M":
					max_matches = int(sys.argv[6])
			elif load_old_matricies:
				print "Error: usage; should be '$ main.py [--newMatricies/-N] [rowLen] [colLen] [numMatrices] [--maxMatches/-M] [maxMatches]'"
				return
		if len(sys.argv) == 3:
			if sys.argv[1] == "--maxMatches" or sys.argv[1] == "-M":
				max_matches = int(sys.argv[2])
			elif (sys.argv[1] ==  "--runTestSet" or sys.argv[1] == "-R") and sys.argv[2] == "--extended":
				print "running full (extended) test set"
				load_old_matricies = False
				run_full_test_set(extended_p = True)
				return
		elif len(sys.argv) == 2:
			if sys.argv[1] == "--runTestSet" or sys.argv[1] == "-R":
				print "running full test set"
				load_old_matricies = False
				run_full_test_set()
				return 
		elif load_old_matricies:
			print "Error: usage; should be '$ main.py [--maxMatches/-M] [maxMatches]'"
			return	
	if load_old_matricies:
		print "using old matricies from files..."
		old_matricies = read_matricies()
		sys_matrices = old_matricies[:len(old_matricies)/2]
		user_matrices = [np.swapaxes(x,0,1) for x in old_matricies[len(old_matricies)/2:]]
		print "Num system matrix:", len(sys_matrices)
		print "Num user matrix:", len(user_matrices)
	run_large_scale_tests(sys_matrices, user_matrices, max_matches)

if __name__ == '__main__':
	main()