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
	tot_utility = 0
	row_cntr = 0
	for m1_row_list in matrix1_list: # take all the utilities of the matches, aka non-zero values, based on matrix2
		col_cntr = 0
		for m1_elt in m1_row_list:
			#print "comparing", matrix1_list[row_cntr][col_cntr], "to", matrix2_list[row_cntr][col_cntr]
			if matrix2_list[row_cntr][col_cntr] != 0:
				tot_utility += m1_elt
			col_cntr+=1
		row_cntr +=1
	return tot_utility

def print_matrices(matrix_list):
	for curr_matrix in matrix_list:
		print curr_matrix

def run_large_scale_tests(sys_matrices, user_matrices, max_matches):
	curr_matrix_cntr = 0
	avg_a1_sys_utility = 0
	avg_a1_user_utility = 0
	avg_gs_sys_utility = 0
	avg_gs_user_utility = 0
	avg_a1_rev_sys_utility = 0
	avg_a1_rev_user_utility = 0
	while curr_matrix_cntr < len(sys_matrices):
		curr_sys_matrix = sys_matrices[curr_matrix_cntr]
		curr_user_matrix = user_matrices[curr_matrix_cntr]
		#curr_a1_result_matrix = run_sys_pref_col_heuristic(curr_sys_matrix, curr_user_matrix, max_matches)
		curr_a1_result_matrix = run_sys_pref_col_heuristic(np.swapaxes(curr_user_matrix,0,1), np.swapaxes(curr_sys_matrix,0,1), max_matches)
		curr_gs_result_matrix = run_gale_shapley(curr_sys_matrix, curr_user_matrix)
		print_matrices([curr_sys_matrix, curr_user_matrix, curr_gs_result_matrix])
		curr_a1_rev_result_matrix = run_sys_pref_col_heuristic(np.swapaxes(curr_user_matrix,0,1), np.swapaxes(curr_sys_matrix,0,1), max_matches, reverse_order_p = True)
		curr_a1_sys_utility = compute_utility(curr_sys_matrix, curr_a1_result_matrix)
		avg_a1_sys_utility += curr_a1_sys_utility
		curr_a1_user_utility = compute_utility(curr_user_matrix, curr_a1_result_matrix)
		avg_a1_user_utility+=curr_a1_user_utility
		curr_gs_sys_utility = compute_utility(curr_sys_matrix, curr_gs_result_matrix)
		avg_gs_sys_utility+=curr_gs_sys_utility
		curr_gs_user_utility = compute_utility(curr_user_matrix, curr_gs_result_matrix)
		avg_gs_user_utility+=curr_gs_user_utility
		curr_a1_rev_sys_utility = compute_utility(curr_sys_matrix, curr_a1_rev_result_matrix)
		avg_a1_rev_sys_utility += curr_a1_rev_sys_utility
		curr_a1_rev_user_utility = compute_utility(curr_user_matrix, curr_a1_rev_result_matrix)
		avg_a1_rev_user_utility += curr_a1_rev_user_utility
		curr_matrix_cntr+=1		
	avg_a1_sys_utility = avg_a1_sys_utility/curr_matrix_cntr
	avg_a1_user_utility = avg_a1_user_utility/curr_matrix_cntr
	avg_gs_sys_utility = avg_gs_sys_utility/curr_matrix_cntr
	avg_gs_user_utility = avg_gs_user_utility/curr_matrix_cntr
	avg_a1_rev_sys_utility = avg_a1_rev_sys_utility/curr_matrix_cntr
	avg_a1_rev_user_utility = avg_a1_rev_user_utility/curr_matrix_cntr
	print "gale shapley: average System utility:", avg_gs_sys_utility, ", average combined user utility:", avg_gs_user_utility
	print "new algorithm: average System utility:", avg_a1_sys_utility, ", average combined user utility:", avg_a1_user_utility
	print "new algorithm (reverse pref. order): average system utility:", avg_a1_rev_sys_utility, ", average combined user utility:", avg_a1_rev_user_utility

def main():
	sys_matrix = None
	user_matrix = None
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
					print "generating new matricies of dimensions [", row_len, ", ", col_len, "] ..."
					rand_matricies, rand_matrix_str_arr = gen_multi_matricies(num_matrices,row_len,col_len)
					sys_matrices = rand_matricies[:len(rand_matricies)/2]
					user_matrices = [np.swapaxes(x,0,1) for x in rand_matricies[len(rand_matricies)/2:]]
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
	#result_matrix = run_sys_pref_col_heuristic(sys_matrix, user_matrix, max_matches)
	#print "New algorithm result matrix:"
	#print result_matrix
	#gs_result_matrix = run_gale_shapley(sys_matrix, user_matrix)
	#print "Gale Shapley result matrix:"
	#print gs_result_matrix
	#a1_sys_utility = compute_utility(sys_matrix, result_matrix)
	#print "sys utility:", a1_sys_utility

if __name__ == '__main__':
	main()