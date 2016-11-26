import numpy as np
from matrix import build_matrix_from_arr

def build_heur_arr(arr_len):
	heur_arr = []
	arr_cntr = 0
	while arr_cntr < arr_len:
		heur_arr.append(0)
		arr_cntr+=1
	return heur_arr

def build_finished_rows_dict(num_elts):
	finished_rows_dict = {}
	curr_elt = 0
	while curr_elt < num_elts:
		finished_rows_dict[curr_elt] = []
		curr_elt+=1
	return finished_rows_dict

def build_pref_order_arr(heur_arr):
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

def run_sys_pref_col_heuristic(sys_matrix, user_matrix, max_matches):
	sys_matrix_list = sys_matrix.tolist() # use just the list version of the matrix for the moment
	user_matrix_list = user_matrix.tolist()
	sys_col_heur_arr = build_heur_arr(len(sys_matrix_list[0]))
	for curr_row in sys_matrix_list: # go over each row
		sys_matrix_col_cntr = 0
		for mat_elt in curr_row: # go over each element in the current row
			sys_col_heur_arr[sys_matrix_col_cntr] += mat_elt
			sys_matrix_col_cntr+=1
	finished_user_rows_dict = build_finished_rows_dict(len(user_matrix_list))
	col_pref_order_arr = build_pref_order_arr(sys_col_heur_arr) # replace with a simple sort() call.... wtf dude...
	inverse_finished_matrix_arr = build_heur_arr(len(sys_matrix_list))
	for col_pref_elt in col_pref_order_arr: # for each column preference, in order, go over user matrix
		curr_user_row_elt = 0
		best_user_row_elt = 0
		best_user_pref = 0
		curr_finished_matrix_col = build_heur_arr(len(user_matrix_list[0]))
		for curr_user_matrix_row in user_matrix_list: # pick most preferred column choice, based on user preference
			curr_user_pref = curr_user_matrix_row[col_pref_elt]
			if curr_user_pref > best_user_pref and len(finished_user_rows_dict[curr_user_row_elt]) < max_matches:
				if col_pref_elt not in finished_user_rows_dict[curr_user_row_elt]:
					best_user_pref = curr_user_pref
					best_user_row_elt = curr_user_row_elt
			curr_user_row_elt+=1
		finished_user_rows_dict[best_user_row_elt].append(col_pref_elt)
		curr_finished_matrix_col[best_user_row_elt] = 1
		inverse_finished_matrix_arr[col_pref_elt] = curr_finished_matrix_col
	finished_matrix = np.swapaxes(build_matrix_from_arr(inverse_finished_matrix_arr), 0,1)
	return finished_matrix