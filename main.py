import numpy as np
import random
import os, sys

from matrix import gen_multi_matricies, save_matricies, read_matricies
from new_algorithm import run_sys_pref_col_heuristic, build_heur_arr
from gale_shapley import run_gale_shapley, build_proposal_dict_list

def compute_utility(matrix1, matrix2):
	# matrix 2 should be a result matrix
	matrix1_list = matrix1.tolist()
	matrix2_list = matrix2.tolist()
	row_cntr = 0
	col_average_matrix_list = build_proposal_dict_list(matrix1_list)
	col_averages = build_heur_arr(len(matrix1_list))
	num_col_avg_vals = build_heur_arr(len(matrix1_list))
	for m1_row_list in matrix1_list:
		col_cntr = 0
		for m1_elt in m1_row_list:
			#print "comparing", matrix1_list[row_cntr][col_cntr], "to", matrix2_list[row_cntr][col_cntr]
			if matrix2_list[row_cntr][col_cntr] != 0:
				col_average_matrix_list[row_cntr].append(m1_elt)
			else:
				col_average_matrix_list[row_cntr].append(0)
			col_cntr+=1
		row_cntr +=1
	for curr_row in col_average_matrix_list:
		col_cntr = 0
		for curr_elt in curr_row:
			if curr_elt != 0:
				col_averages[col_cntr] += curr_elt
				num_col_avg_vals[col_cntr]+=1
			col_cntr+=1
		print curr_row
	tot_utility = 0
	col_cntr = 0
	for col_val in col_averages:
		tot_utility += (col_val / num_col_avg_vals[col_cntr])
		col_cntr+=1
	return tot_utility

def main():
	sys_matrix = None
	user_matrix = None
	max_matches = 1
	load_old_matricies = True
	if len(sys.argv) > 1:
		if len(sys.argv) >= 4:
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
				load_old_matricies = False
			else:
				print "Error: usage; should be '$ main.py [--newMatricies/-N] [rowLen] [colLen]'"
				return
			if len(sys.argv) == 6:
				if sys.argv[4] == "--maxMatches" or sys.argv[4] == "-M":
					max_matches = int(sys.argv[5])
			else:
				print "Error: usage; should be '$ main.py [--newMatricies/-N] [rowLen] [colLen] [--maxMatches/-M] [maxMatches]'"
				return
		if len(sys.argv) == 3:
			if sys.argv[1] == "--maxMatches" or sys.argv[1] == "-M":
				max_matches = int(sys.argv[2])
		elif load_old_matricies:
			print "Error: usage; should be '$ main.py [--maxMatches/-M] [maxMatches]'"
			return	
	if load_old_matricies:
		print "using old matricies from files..."
		old_matricies = read_matricies()
		old_matricies[1] = np.swapaxes(old_matricies[1],0,1)
		print "System matrix:"
		print old_matricies[0]
		sys_matrix = old_matricies[0]
		print "User matrix:"
		print old_matricies[1]
		user_matrix = old_matricies[1]
	result_matrix = run_sys_pref_col_heuristic(sys_matrix, user_matrix, max_matches)
	print "New algorithm result matrix:"
	print result_matrix
	gs_result_matrix = run_gale_shapley(sys_matrix, user_matrix)
	print "Gale Shapley result matrix:"
	print gs_result_matrix
	a1_sys_utility = compute_utility(sys_matrix, result_matrix)
	print "sys utility:", a1_sys_utility

if __name__ == '__main__':
	main()