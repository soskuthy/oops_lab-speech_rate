main_dir$ = "/Users/soskuthy/Documents/Research/data/xling-corpus/forced_aligned/taiwanese_mandarin"

Create Strings as directory list... dir_list 'main_dir$'
dir_list_index = selected()

dir_list_len = Get number of strings

for i to dir_list_len
	select 'dir_list_index'
	sub_dir$ = Get string... 'i'
	dir$ = main_dir$ + "/" + sub_dir$
	search_string$ = "'dir$'" + "/*.TextGrid"
	Create Strings as file list... file_list 'search_string$'
    file_list_index = selected()
	file_list_len = Get number of strings
	for t to file_list_len
		select 'file_list_index'
		file_name$ = Get string... 't'
		file_path$ = "'dir$'" + "/" + file_name$
		Read from file... 'file_path$'
		Remove tier... 1
		Duplicate tier... 2 3 tones
		Replace interval texts: 2, 1, 0, "(.*)[0-9]", "\1", "Regular Expressions" 
		Replace interval texts: 3, 1, 0, ".*([0-9])", "\1", "Regular Expressions"
		Replace interval texts: 3, 1, 0, "^[^0-9]+$", "", "Regular Expressions"
		Replace interval texts: 3, 1, 0, "([0-9])", "t\1", "Regular Expressions"
		Set tier name... 1 word
		Set tier name... 2 phone
		#interval_no = Get number of intervals... 3
		#c = 1
		#prev_text = 1
		#for v to interval_no
		#	v_text$ = Get label of interval... 3 v
		#	if v_text$="" and prev_text=0
		#		remove_time[c] = Get start time of interval... 3 v
		#		c = c + 1
		#	endif
		#	prev_text=0
		#	if not v_text$=""
		#		prev_text=1
		#	endif
		#endfor
		#for v from 1 to c-1
		#	removal_time = remove_time[v]
		#	Remove boundary at time... 3 'removal_time'
		#endfor
		Save as text file... 'file_path$'
	endfor
endfor