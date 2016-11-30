import numpy as np
from new_algorithm import build_heur_arr
from matrix import build_matrix_from_arr


def build_unmatched_elts_dict(pref_order_list):
	unmatched_elts_dict = {}
	curr_elt = 0
	while curr_elt < len(pref_order_list):
		unmatched_elts_dict[curr_elt] = 0
		curr_elt+=1
	return unmatched_elts_dict

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

def get_best_unmatched_user(curr_sys_elt, sys_pref_order_list, user_pref_order_list, matched_user_elts_dict, proposal_dict_list, max_matches):
	curr_sys_pref_order = sys_pref_order_list[curr_sys_elt]
	curr_user_elt = 0
	best_user_elt = 0
	best_sys_pref_val = 0
	return_sys_to_matching = None
	found_match_p = False
	has_proposal_p = False
	for curr_sys_pref_val in curr_sys_pref_order:
		if curr_sys_pref_val > best_sys_pref_val and curr_user_elt not in proposal_dict_list[curr_sys_elt]: # make sure porposal is best and unique
			best_sys_pref_val = curr_sys_pref_val
			best_user_elt = curr_user_elt
			has_proposal_p = True
		curr_user_elt+=1
	if has_proposal_p:
		if best_user_elt in matched_user_elts_dict: # if the user already is matched
			if len(matched_user_elts_dict[best_user_elt]) < max_matches: # we can just add the match to the list
				matched_user_elts_dict[best_user_elt].append(curr_sys_elt)
				matched_user_elts_dict[best_user_elt].sort()
				found_match_p = True
			else: # we need to see if we must replace an old match
				curr_user_pref_order = user_pref_order_list[best_user_elt]
				for curr_old_sys_match_elt in matched_user_elts_dict[best_user_elt]:
					#old_sys_match_elt = matched_user_elts_dict[best_user_elt]
					if curr_user_pref_order[curr_sys_elt] > curr_user_pref_order[curr_old_sys_match_elt]: # if the user prefs the new sys over the old
						matched_user_elts_dict[best_user_elt].remove(curr_old_sys_match_elt)
						matched_user_elts_dict[best_user_elt].append(curr_sys_elt)
						matched_user_elts_dict[best_user_elt].sort()
						return_sys_to_matching = curr_old_sys_match_elt
						found_match_p = True
						proposal_dict_list[curr_sys_elt].append(best_user_elt)
						return found_match_p, return_sys_to_matching, has_proposal_p
		else: # new unique matching
			matched_user_elts_dict[best_user_elt] = [curr_sys_elt]
			found_match_p = True
		proposal_dict_list[curr_sys_elt].append(best_user_elt)
	return found_match_p, return_sys_to_matching, has_proposal_p

def run_gale_shapley(sys_matrix, user_matrix, max_matches):
	## A COMPLETE MANY TO MANY MATCHING DOES NOT ALWAYS EXIST
	sys_pref_order_list = sys_matrix.tolist() # same as regular matrix in 2d array form
	user_pref_order_list = np.swapaxes(user_matrix,0,1).tolist()
	# system pref order represented in rows (sys = men in GS paradigm)
	# user pref order represented in cols (user = women in GS paradigm)
	unmatched_sys_elts = build_unmatched_elts_list(sys_pref_order_list)
	sys_elt_match_cntr_dict = build_unmatched_elts_dict(sys_pref_order_list)
	proposal_dict_list = build_proposal_dict_list(sys_pref_order_list)
	matched_user_elts_dict = {} # (key=user_elt : value=sys_elt)
	while len(unmatched_sys_elts) > 0:
		for curr_sys_elt in unmatched_sys_elts: # a system is proposing to a user
			num_matches = sys_elt_match_cntr_dict[curr_sys_elt]
			remove_curr_sys_elt_p = False
			while num_matches < max_matches:
				found_match_p, return_sys_to_matching, has_proposal_p = get_best_unmatched_user(curr_sys_elt, sys_pref_order_list, user_pref_order_list, matched_user_elts_dict, proposal_dict_list, max_matches)
				if found_match_p or not has_proposal_p:
					remove_curr_sys_elt_p = True
					sys_elt_match_cntr_dict[curr_sys_elt]+=1
				if return_sys_to_matching != None:
					sys_elt_match_cntr_dict[return_sys_to_matching] -=1
					if return_sys_to_matching not in unmatched_sys_elts: # remove old match
						unmatched_sys_elts.append(return_sys_to_matching)
				num_matches+=1
			if remove_curr_sys_elt_p:
				#print "found_match_p:", found_match_p, ", has_proposal_p", has_proposal_p
				#print "unmatched_sys_elts:", unmatched_sys_elts, ", curr_sys_elt:", curr_sys_elt
				unmatched_sys_elts.remove(curr_sys_elt)
	final_matrix_arr = build_empty_final_matrix_arr(sys_pref_order_list)
	for user_elt in matched_user_elts_dict:
		for curr_sys_match_elt in matched_user_elts_dict[user_elt]:
			final_matrix_arr[curr_sys_match_elt][user_elt] = 1
	final_matrix = build_matrix_from_arr(final_matrix_arr)
	return final_matrix