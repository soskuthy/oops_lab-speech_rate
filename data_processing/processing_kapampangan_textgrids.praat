main_dir$ = "/Users/soskuthy/Documents/Research/data/xling-corpus/forced_aligned/kapampangan"

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
		Set tier name... 1 word
		Set tier name... 2 phone
		interval_n = Get number of intervals... 2
		seg_1$ = Get label of interval... 2 1
		for intv from 2 to interval_n
			seg_2$ = Get label of interval... 2 'intv'
			if seg_1$=="d" and seg_2$=="ʒ"
				Remove left boundary... 2 'intv'
				interval_n = interval_n - 1
				intv = intv - 1
			endif
			if seg_1$=="t" and seg_2$=="ʃ"
				Remove left boundary... 2 'intv'
				interval_n = interval_n - 1
				intv = intv - 1
			endif
			seg_1$ = seg_2$
		endfor
		Save as text file... 'file_path$'
	endfor
endfor