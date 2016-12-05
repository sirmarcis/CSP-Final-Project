## new_algorithm.py
## written by Anders Maraviglia
##
## Algorithm Description:
## We have two matrices as input to the main function, run_new_algorithm, which are sys_matrix and user_matrix.
## The user_matrix represents the preferences of the agents being proposed to.
## The sys_matrix represents the preferences of the agents doing the proposing.
## Proposal order is determined by taking the sum of the utilities for each column in the user_matrix, which basically acts as a
## "user desirability" with respect to users, and from this a list of systems is created, sorted by "desirability" in decending
## order.  From this, each system then picks max_matches of their highest rated (avalible) users.  Note that each system and user
## can have at most max_matches at any given time, but each system and user does not necessaraly have max_matches at the end
## of the matching process.  
##
## Runtime Complexity: 
## It is O(m*n^2), where n is the number of user or system agents, and m is the max matches we are trying to make.
## This is the case because we go over the entire user matrix once to get the hauristic to determine proposal order, O(n^2), 
## from there we sort the preference list, O(n), and iterate over it, and for each iteration going over the current system 
## preference list (of size n) m times to find a best avalible match, O(n*m*n).  Combining these runtimes we get 
## O(n^2) + O(n) + O(n*m*n) = O((n^2)+n+m*n^2) = O(n+2*m*n^2), which simplifies to O(m*n^2).

import numpy as np
from matrix import build_matrix_from_arr

def build_heur_arr(arr_len):
	"""Called by run_new_algorithm and populate_sys_col_heur_arr"""
	heur_arr = []
	arr_cntr = 0
	while arr_cntr < arr_len:
		heur_arr.append(0)
		arr_cntr+=1
	return heur_arr

def build_finished_rows_dict(num_elts):
	"""Called by run_new_algorithm"""
	finished_rows_dict = {}
	curr_elt = 0
	while curr_elt < num_elts:
		finished_rows_dict[curr_elt] = []
		curr_elt+=1
	return finished_rows_dict

def build_pref_order_arr(heur_arr):
	"""Called by run_new_algorithm"""
	pref_order_arr = []
	while len(pref_order_arr) < len(heur_arr):
		heur_elt = 0
		best_heur_elt = 0
		best_heur_val = 0
		for curr_heur_val in heur_arr:
			if curr_heur_val > best_heur_val and heur_elt not in pref_order_arr:
				best_heur_val = curr_heur_val
				best_heur_elt = heur_elt
			heur_elt+=1
		pref_order_arr.append(best_heur_elt)
	return pref_order_arr

def populate_sys_col_heur_arr(sys_matrix_list):
	"""Called by run_new_algorithm"""
	sys_col_heur_arr = build_heur_arr(len(sys_matrix_list[0]))
	for curr_row in sys_matrix_list: # go over each row
		sys_matrix_col_cntr = 0
		for mat_elt in curr_row: # go over each element in the current row
			sys_col_heur_arr[sys_matrix_col_cntr] += mat_elt
			sys_matrix_col_cntr+=1
	return sys_col_heur_arr

def build_finished_matrix_arr(matrix_list):
	"""Called by run_new_algorithm"""
	finished_matrix_arr = []
	matrix_row_len = len(matrix_list[0])
	matrix_elt = 0
	while matrix_elt < len(matrix_list):
		crr_finished_matrix_row = [0 for elt in matrix_list[matrix_elt]]
		finished_matrix_arr.append(crr_finished_matrix_row)
		matrix_elt+=1
	return finished_matrix_arr

def print_matrix_list(matrix_list):
	"""Function used for testing"""
	for matrix_row in matrix_list:
		print matrix_row

def run_new_algorithm(user_matrix, sys_matrix, max_matches, reverse_order_p=False):
	"""Called by run_large_scale_tests in main.py, runs the greedy algorithm. 
	user_matrix is the preference list matrix of the agents being proposed to,
	sys_matrix is the preference list matrix of the proposing agents.  
	Refer to the top of the file for an algorithm description."""
	user_matrix_list = user_matrix.tolist() # use just the list version of the matrix for the moment
	sys_matrix_list = sys_matrix.tolist()
	sys_col_heur_arr = populate_sys_col_heur_arr(user_matrix_list)
	finished_user_rows_dict = build_finished_rows_dict(len(sys_matrix_list))
	col_pref_order_arr = build_pref_order_arr(sys_col_heur_arr)
	if reverse_order_p:
		col_pref_order_arr.reverse()
	inverse_finished_matrix_arr = build_finished_matrix_arr(user_matrix_list)
	for col_pref_elt in col_pref_order_arr: # for each column preference, in order, go over user matrix
		num_matches = 0
		while num_matches < max_matches: # find max_matches for each column preference
			curr_user_row_elt = 0 # position of the current system in the user matrix
			best_user_row_elt = 0 # position of the best system match in the user matrix
			best_user_pref = 0 # the actual utility value of the current best system match in the user matrix
			match_found_p = False # to ensure we actually find a match (not garunteed)
			for curr_user_matrix_row in sys_matrix_list: # pick most preferred column choice, based on user preference
				curr_user_pref = curr_user_matrix_row[col_pref_elt]
				if curr_user_pref > best_user_pref and len(finished_user_rows_dict[curr_user_row_elt]) < max_matches:
					if col_pref_elt not in finished_user_rows_dict[curr_user_row_elt]:
						best_user_pref = curr_user_pref
						best_user_row_elt = curr_user_row_elt
						match_found_p = True
				curr_user_row_elt+=1
			if match_found_p:
				finished_user_rows_dict[best_user_row_elt].append(col_pref_elt)
				inverse_finished_matrix_arr[col_pref_elt][best_user_row_elt] = 1 # counterintuitive, ik..
			num_matches+=1
	finished_matrix = np.swapaxes(build_matrix_from_arr(inverse_finished_matrix_arr), 0,1)
	return finished_matrix