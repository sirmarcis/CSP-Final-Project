import numpy as np
from new_algorithm import build_heur_arr
from matrix import build_matrix_from_arr


def build_unmatched_elts_list(pref_order_list):
	unmatched_elts_list = []
	curr_elt = 0
	while curr_elt < len(pref_order_list):
		unmatched_elts_list.append(curr_elt)
		curr_elt+=1
	return unmatched_elts_list

def build_proposal_dict_list(pref_order_list):
	proposal_dict_list = []
	curr_elt = 0
	while curr_elt < len(pref_order_list):
		proposal_dict_list.append([])
		curr_elt+=1
	return proposal_dict_list

def build_empty_final_matrix_arr(sys_pref_order_list):
	empty_final_matrix_arr = []
	for final_elt in sys_pref_order_list:
		empty_final_matrix_arr.append(build_heur_arr(len(final_elt)))
	return empty_final_matrix_arr

def get_best_unmatched_user(curr_sys_elt, sys_pref_order_list, user_pref_order_list, matched_user_elts_dict, proposal_dict_list):
	curr_sys_pref_order = sys_pref_order_list[curr_sys_elt]
	curr_user_elt = 0
	best_user_elt = 0
	best_sys_pref_val = 0
	return_sys_to_matching = None
	found_match_p = False
	for curr_sys_pref_val in curr_sys_pref_order:
		if curr_sys_pref_val > best_sys_pref_val and curr_user_elt not in proposal_dict_list[curr_sys_elt]: # make sure porposal is best and unique
			best_sys_pref_val = curr_sys_pref_val
			best_user_elt = curr_user_elt
		curr_user_elt+=1
	if best_user_elt in matched_user_elts_dict: # if the user already is matched
		curr_user_pref_order = user_pref_order_list[best_user_elt]
		old_sys_match_elt = matched_user_elts_dict[best_user_elt]
		if curr_user_pref_order[curr_sys_elt] > curr_user_pref_order[old_sys_match_elt]: # if the user prefs the new sys over the old
			matched_user_elts_dict[best_user_elt] = curr_sys_elt
			return_sys_to_matching = old_sys_match_elt
			found_match_p = True
		proposal_dict_list[curr_sys_elt].append(best_user_elt)
	else: # new unique matching
		matched_user_elts_dict[best_user_elt] = curr_sys_elt
		proposal_dict_list[curr_sys_elt].append(best_user_elt)
		found_match_p = True
	return found_match_p, return_sys_to_matching

def run_gale_shapley(sys_matrix, user_matrix):
	sys_pref_order_list = sys_matrix.tolist() # same as regular matrix in 2d array form
	user_pref_order_list = np.swapaxes(user_matrix,0,1).tolist()
	# system pref order represented in rows (sys = men in GS paradigm)
	# user pref order represented in cols (user = women in GS paradigm)
	unmatched_sys_elts = build_unmatched_elts_list(sys_pref_order_list)
	proposal_dict_list = build_proposal_dict_list(sys_pref_order_list)
	matched_user_elts_dict = {} # (key=user_elt : value=sys_elt)
	while len(unmatched_sys_elts) > 0:
		for curr_sys_elt in unmatched_sys_elts:
			found_match_p, return_sys_to_matching = get_best_unmatched_user(curr_sys_elt, sys_pref_order_list, user_pref_order_list, matched_user_elts_dict, proposal_dict_list)
			if found_match_p:
				unmatched_sys_elts.remove(curr_sys_elt)
			if return_sys_to_matching != None:
				unmatched_sys_elts.append(return_sys_to_matching)
	final_matrix_arr = build_empty_final_matrix_arr(sys_pref_order_list)
	for user_elt in matched_user_elts_dict:
		sys_elt = matched_user_elts_dict[user_elt]
		final_matrix_arr[sys_elt][user_elt] = 1
	final_matrix = build_matrix_from_arr(final_matrix_arr)
	return final_matrix