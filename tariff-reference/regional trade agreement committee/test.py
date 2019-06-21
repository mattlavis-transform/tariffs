import re
para = "more than 9,5kg but less than 12.993kg"
p = re.sub("([0-9]),([0-9])", "\\1.\\2", para)
print (p)