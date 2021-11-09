main_dir$ = "/Users/soskuthy/Documents/Research/data/xling-corpus/forced_aligned/korean"

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
		Save as text file... 'file_path$'
	endfor
endfor