## test_suite.py
## written by Anders Maraviglia

import numpy as np
import random, os, sys

from matrix import gen_multi_matricies
from new_algorithm import run_new_algorithm, build_heur_arr
from gale_shapley import run_gale_shapley, build_proposal_dict_list

def compute_utility(matrix1, matrix2):
	"""Called by run_large_scale_tests, gets the utility of matrix 1 based on matrix 2"""
	# matrix 2 should be a result matrix
	matrix1_list = matrix1.tolist()
	matrix2_list = matrix2.tolist()
	tot_utility = 0
	row_cntr = 0
	for m1_row_list in matrix1_list: # take all the utilities of the matches, aka non-zero values, based on matrix2
		col_cntr = 0
		for m1_elt in m1_row_list:
			if matrix2_list[row_cntr][col_cntr] != 0:
				tot_utility += m1_elt
			col_cntr+=1
		row_cntr +=1
	return tot_utility

def print_matrices(matrix_list):
	for curr_matrix in matrix_list:
		print curr_matrix

def run_large_scale_tests(sys_matrices, user_matrices, max_matches, tab_p = False, extended_p = False):
	"""Called by main and run_full_test_set, runs GS and new algoirithms on the input matrix system and user sets"""
	curr_matrix_cntr = 0
	avg_a1_sys_utility = 0
	avg_a1_user_utility = 0
	avg_gs_sys_utility = 0
	avg_gs_user_utility = 0
	avg_a1_rev_sys_utility = 0
	avg_a1_rev_user_utility = 0
	while curr_matrix_cntr < len(sys_matrices): # good luck understanding any of this (NEEDS REFACTORING)
		curr_sys_matrix = sys_matrices[curr_matrix_cntr]
		curr_user_matrix = user_matrices[curr_matrix_cntr]
		#curr_a1_result_matrix = run_new_algorithm(curr_sys_matrix, curr_user_matrix, max_matches)
		curr_a1_result_matrix = run_new_algorithm(np.swapaxes(curr_user_matrix,0,1), np.swapaxes(curr_sys_matrix,0,1), max_matches)
		curr_gs_result_matrix = run_gale_shapley(curr_sys_matrix, curr_user_matrix, max_matches)
		#print_matrices([curr_sys_matrix, curr_user_matrix, curr_gs_result_matrix])
		curr_a1_rev_result_matrix = run_new_algorithm(np.swapaxes(curr_user_matrix,0,1), np.swapaxes(curr_sys_matrix,0,1), max_matches, reverse_order_p = True)
		curr_a1_sys_utility = compute_utility(np.swapaxes(curr_sys_matrix,0,1), curr_a1_result_matrix)
		avg_a1_sys_utility += curr_a1_sys_utility
		curr_a1_user_utility = compute_utility(np.swapaxes(curr_user_matrix,0,1), curr_a1_result_matrix)
		avg_a1_user_utility+=curr_a1_user_utility
		curr_gs_sys_utility = compute_utility(curr_sys_matrix, curr_gs_result_matrix)
		avg_gs_sys_utility+=curr_gs_sys_utility
		curr_gs_user_utility = compute_utility(curr_user_matrix, curr_gs_result_matrix)
		avg_gs_user_utility+=curr_gs_user_utility
		curr_a1_rev_sys_utility = compute_utility(np.swapaxes(curr_sys_matrix,0,1), curr_a1_rev_result_matrix)
		avg_a1_rev_sys_utility += curr_a1_rev_sys_utility
		curr_a1_rev_user_utility = compute_utility(np.swapaxes(curr_user_matrix,0,1), curr_a1_rev_result_matrix)
		avg_a1_rev_user_utility += curr_a1_rev_user_utility
		curr_matrix_cntr+=1		
	avg_a1_sys_utility = avg_a1_sys_utility/curr_matrix_cntr
	avg_a1_user_utility = avg_a1_user_utility/curr_matrix_cntr
	avg_gs_sys_utility = avg_gs_sys_utility/curr_matrix_cntr
	avg_gs_user_utility = avg_gs_user_utility/curr_matrix_cntr
	avg_a1_rev_sys_utility = avg_a1_rev_sys_utility/curr_matrix_cntr
	avg_a1_rev_user_utility = avg_a1_rev_user_utility/curr_matrix_cntr
	tab_char = ""
	if tab_p:
		tab_char = "\t"
	else:
		print "gale shapley: average System utility:", avg_gs_sys_utility, ", average combined user utility:", avg_gs_user_utility
		print "new algorithm: average System utility:", avg_a1_sys_utility, ", average combined user utility:", avg_a1_user_utility
		print "new algorithm (reverse pref. order): average system utility:", avg_a1_rev_sys_utility, ", average combined user utility:", avg_a1_rev_user_utility
	if extended_p:
		return [avg_gs_sys_utility, avg_gs_user_utility, avg_a1_sys_utility, avg_a1_user_utility, avg_a1_rev_sys_utility, avg_a1_rev_user_utility]
	else:
		return [avg_gs_sys_utility, avg_gs_user_utility, avg_a1_sys_utility, avg_a1_user_utility]

def gen_new_sys_user_matrices(num_matrices, row_len, col_len, rand_matrix_str_arr = [], tab_p = False):
	"""Called by main and run_full_test_set, randomly generates num_matrices matrices of dimensions row_len and col_len"""
	if not tab_p:
		print "generating new matricies of dimensions [", row_len, ", ", col_len, "] ..."
	rand_matricies, rand_matrix_str_arr = gen_multi_matricies(num_matrices,row_len,col_len)
	sys_matrices = rand_matricies[:len(rand_matricies)/2]
	user_matrices = [np.swapaxes(x,0,1) for x in rand_matricies[len(rand_matricies)/2:]]
	return sys_matrices, user_matrices

def make_centered_num_str(curr_num, str_len):
	"""Called by run_full_test_set, helper function to build nice printable numer strings"""
	num_str = str(curr_num)
	space_str = " " * ((str_len - len(num_str))/2)
	final_str = space_str + num_str + space_str
	if len(final_str) != str_len:
		final_str += " " 
	return final_str

def run_full_test_set(extended_p = False):
	"""Called by main, runs all tests whose parameters are listed in test_list"""
	test_list = [[4,4,2], [4,4,2], [5,5,2], [6,6,3], [7,7,3], [8,8,4], [9,9,4], [10,10,5]]
	intro_line = "Matrix Dimensions and Algorithm | Max Matches | Average System Utility | Social Welfare Utility | Num Matrices per Agent"
	row_sep_line_str = "-"*len(intro_line)
	num_matrices_str = make_centered_num_str(100, 23)
	print intro_line
	print row_sep_line_str
	for curr_matrix_dimension_list in test_list:
		curr_row_len = curr_matrix_dimension_list[0]
		curr_col_len = curr_matrix_dimension_list[1]
		curr_max_matches = curr_matrix_dimension_list[2]
		curr_sys_matrices, curr_user_matrices = gen_new_sys_user_matrices(200, curr_row_len, curr_col_len, tab_p = True)
		if extended_p:
			utilities_list = run_large_scale_tests(curr_sys_matrices, curr_user_matrices, curr_max_matches, tab_p = True, extended_p = True)
		else:
			utilities_list = run_large_scale_tests(curr_sys_matrices, curr_user_matrices, curr_max_matches, tab_p = True)
		matrix_dim_str1 = "[" + str(curr_row_len) + ", " + str(curr_col_len) + "] GS"
		matrix_dim_str2 = "[" + str(curr_row_len) + ", " + str(curr_col_len) + "] New Alg."
		max_matches_str = make_centered_num_str(curr_max_matches, 13)
		gs_sys_str = make_centered_num_str(utilities_list[0], 24)
		gs_user_str = make_centered_num_str(utilities_list[1], 24) 
		a1_sys_str = make_centered_num_str(utilities_list[2], 24)
		a1_user_str = make_centered_num_str(utilities_list[3], 24)
		print matrix_dim_str1 + " "*(32-len(matrix_dim_str1)) + "|" + max_matches_str + "|" + gs_sys_str + "|" + gs_user_str + "|" + num_matrices_str
		print matrix_dim_str2 + " "*(32-len(matrix_dim_str2)) + "|" + max_matches_str + "|" + a1_sys_str + "|" + a1_user_str + "|" + num_matrices_str
		if extended_p:
			matrix_dim_str3 = "[" + str(curr_row_len) + ", " + str(curr_col_len) + "] New Alg. (rev)"
			a1_rev_sys_str = make_centered_num_str(utilities_list[4], 24)
			a1_rev_user_str = make_centered_num_str(utilities_list[5], 24)
			print matrix_dim_str3 + " "*(32-len(matrix_dim_str3)) + "|" + max_matches_str + "|" + a1_rev_sys_str + "|" + a1_rev_user_str + "|" + num_matrices_str
		print row_sep_line_str