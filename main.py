import numpy as np
import random
import os, sys

from matrix import gen_multi_matricies, save_matricies, read_matricies
from new_algorithm import run_sys_pref_col_heuristic
from gale_shapley import run_gale_shapley

def main():
	sys_matrix = None
	user_matrix = None
	if len(sys.argv) > 1:
		if len(sys.argv) == 4:
			if sys.argv[1] == "--newMatricies" or sys.argv[1] == "-N":
				row_len = int(sys.argv[2])
				col_len = int(sys.argv[3])
				print "generating new matricies of dimensions [", row_len, ", ", col_len, "] ..."
				rand_matricies, rand_matrix_str_arr = gen_multi_matricies(2,4,4)
				rand_matricies[1] = np.swapaxes(rand_matricies[1],0,1)
				print "System matrix:"
				print rand_matricies[0]
				sys_matrix = rand_matricies[0]
				print "User matrix:"
				print rand_matricies[1]
				user_matrix = rand_matricies[1]
				save_matricies(rand_matrix_str_arr)
			else:
				print "Error: usage; should be '$ main.py [--newMatricies/-N] [rowLen] [colLen]'"
		else:
			print "Error: usage; should be '$ main.py [--newMatricies/-N] [rowLen] [colLen]'"
	else:
		print "using old matricies from files..."
		old_matricies = read_matricies()
		old_matricies[1] = np.swapaxes(old_matricies[1],0,1)
		print "System matrix:"
		print old_matricies[0]
		sys_matrix = old_matricies[0]
		print "User matrix:"
		print old_matricies[1]
		user_matrix = old_matricies[1]
	result_matrix = run_sys_pref_col_heuristic(sys_matrix, user_matrix)
	print "New algorithm result matrix:"
	print result_matrix
	gs_result_matrix = run_gale_shapley(sys_matrix, user_matrix)
	print "Gale Shapley result matrix:"
	print gs_result_matrix

if __name__ == '__main__':
	main()