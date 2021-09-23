import re
from collections import OrderedDict
import os
import codecs

class DxfNotFoundError(Exception):
	pass

class WrongFileFormatError(Exception):
	pass

class NoDxfIssuesFoundError(Exception):
	pass

class DxfFixer:
	def __init__(self):
		pass

	# build string from error throwing lines
	def collectString(self, start_i, lines):
		collected_string = ""
		for i in range(start_i, len(lines)):
			collected_string += lines[i].strip()
			if re.match(r"\D\n", lines[i+1]) == None:
				break
		return(collected_string, i)

	def restore(self, dxf_path):
		if dxf_path.split(".")[-1] != "dxf":
			raise WrongFileFormatError("Not .dxf")
			
		if not os.path.exists(dxf_path):
			raise DxfNotFoundError("Wrong file path")

		with codecs.open(dxf_path, 'r', encoding="UTF-8") as dxf:
			lines = dxf.readlines()

		for i in range(len(lines)):
			lines[i] = lines[i].replace("\r", "")
			
		indices_to_pop = []

		# parse lines, restore broken lines and collect error lines indices
		for i in range(0, len(lines) - 1):
			if (re.match(r"\D\n", lines[i]) != None) and (re.match(r"\D\n", lines[i+1]) != None):
				start_i = i
				collect = self.collectString(start_i, lines)
				lines[start_i] = collect[0] + "\n"
				indices_to_pop += [(i + 1) for i in range(start_i, collect[1])]

		# a clutch to drop duplicated indices
		indices_to_pop = list(OrderedDict.fromkeys(indices_to_pop))

		# if no error indices found -> raise this
		if len(indices_to_pop) == 0:
			raise NoDxfIssuesFoundError("No dxf issues found with given rules")

		# delete error indices
		deleted = 0
		for i in indices_to_pop:
			lines.pop(i - deleted)
			deleted += 1

		# add copyright thingy cause why not
		lines[1] = lines[1].strip() + ". Restored by RestoreDxf https://github.com/lulwhat/RestoreDxf\n"

		# add restored postfix to filename
		restored_filename = os.path.basename(dxf_path).split(".")
		restored_filename[-1] = " (restored)." + restored_filename[-1]
		restored_filename = os.path.dirname(dxf_path) + "/" +  "".join(restored_filename)
			
		# write lines back to file
		with codecs.open(restored_filename, 'w', encoding="UTF-8") as dxf:
			for line in lines:
				dxf.write(line)