import re

'''
Reads a KSP array from a text file and copies all values from it into a list in sequential order
'''
def parse_ksp_array(file):
	ksp_array = []
	ksp_values = []
	with open(file, 'r') as ksp_file:
		ksp_array = ksp_file.readlines()
	
	regex = r'%([\w\d]+)\s*\[\s*(\d+)\s*\]\s*:=\s*(-*\d+)'
	for line in ksp_array:
		match=re.match(regex, line)
		if match:
			ksp_values.append(match.group(3))
	return ksp_values
	
'''
Scales the values of the parsed KSP array for a new minimum and maximum setting
and stores those values into a new list
'''	
def scale_array(values, min, max):
	old_range = int(values[-1]) - int(values[0])
	range = max - min
	new_values = []
	for i,v in enumerate(values):
		if i == 0:
			new_values.append(int(min))
		else:
			ratio = (int(values[i]) - int(values[i-1])) / old_range
			new_values.append(int(new_values[i-1] + ratio * range))
	return new_values

'''
Takes a list of values and formats it for a KSP array, saving it to disk where you choose
'''	
def output_array(new_values, file_path, array_name):
	with open(file_path, 'w') as file:
		file.write("declare %" + array_name + "[" + str(len(new_values)) + "]\n")
		for i,v in enumerate(new_values):
			file.write("%" + array_name + "[" + str(i) + "] := " + str(v) + "\n")

array_values = parse_ksp_array('c:/users/patrick/desktop/log_list_forward.txt')
new_values = scale_array(array_values, 0, 630000)
output_array(new_values, 'scaled_array.txt', 'log_array_group_vol')
