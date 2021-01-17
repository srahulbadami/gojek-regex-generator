import random
import sys

# MAX = sys.maxsize
MAX = 1
class RegexGen:
	def __init__(self, regex, qnt):
		self.qnt = qnt
		self.regex = regex[1:-1]

	def genericParser(self, list_of_objs):
		num=1
		length = len(list_of_objs)
		new_str=''
		for i in range(num):
			random_number = random.randrange(length+1)
			if random_number == length:
				new_str += list_of_objs[0]
			else:
				new_str += list_of_objs[random_number]
		return new_str


	def quantifierGenericParser(self, list_of_objs, random_num):
		num=1
		length = len(list_of_objs)
		new_str=''
		for i in range(random_num):
			random_number = random.randrange(length+1)
			if random_number == length:
				new_str += list_of_objs[0]
			else:
				new_str += list_of_objs[random_number]
		return new_str

	def squareParser(self, string):
		post_string = ''
		pre_string = ''
		inside = False

		if '|' in string:
			bracket_open = False
			new_pattern = ''
			new_pattern_list = []
			
			outside = False
			for i in string:
				if i=='[':
					bracket_open = True
					new_pattern += i
				elif i==']':
					bracket_open = False
					new_pattern += i
				elif i=='|' and not bracket_open:
					outside = True
					new_pattern_list.append(new_pattern)
					new_pattern=''
				elif i=='|' and bracket_open:
					inside = True
					new_pattern += i
				else:
					new_pattern += i
			new_pattern_list.append(new_pattern)
			if outside==True:
				random_number = random.randrange(len(new_pattern_list))
				string = new_pattern_list[random_number]
				if '|' in string:
					return(string)
			if inside==True:
				if '[' in string and string.index('[')>0:
					pre_string = string.split('[')[0]
					string = '[' + string.split('[')[1]
				if ']' in string and string.index(']')+1<len(string):
					post_string = string.split(']')[1]
					string = string.split(']')[0] + ']'
				if string[0] == '[' and string[-1] == ']':
					string = string[1:-1]
				if '|' in string:
					new_str = string.split('|')
					random_number = random.randrange(len(new_str))
					string = new_str[random_number]
		if not inside:
			if '[' in string and string.index('[')>0:
				pre_string = string.split('[')[0]
				string = string.split('[')[1]
			if ']' in string and string.index(']')+1<len(string):
				pre_string = string.split(']')[1]
				string = string.split(']')[0]
		if string[0] == '[' and string[-1] == ']':
			string = string[1:-1]
		if len(string) == 1:
			return(pre_string + string + post_string)
		if '-' in string and len(string)==3:
			parsed = string.split('-')
			list_of_objs = []
			for i in range(ord(string[0]),ord(string[2])+1):
				list_of_objs.append(chr(i))
			string = self.genericParser(list_of_objs)
		if '-' in string and len(string)==4:
			if string[0] == '^':
				parsed = string.split('-')
				list_of_objs = []
				if ord(string[1]) >= 48 and ord(string[1]) <58:
					start_range = 48
					end_range = 58
				if ord(string[1]) >= 65 and ord(string[1]) <91:
					start_range = 65
					end_range = 91
				if ord(string[1]) >= 97 and ord(string[1]) <123:
					start_range = 97
					end_range = 123
				for i in range(start_range, ord(string[1])):
					list_of_objs.append(chr(i))
				for i in range(ord(string[3])+1, end_range):
					list_of_objs.append(chr(i))
				string = self.genericParser(list_of_objs)
			else:
				return (-1)
		else:
			string = self.genericParser(string)
		return pre_string + string + post_string

	def curlyParser(self, string):
		start = string.index('{') + 1
		end = string.index('}')
		quantifier = string[start:end]
		quantifier = quantifier.split(',')
		string = string[:start-1]
		string = string[1:-1]
		strng = ''
		if len(quantifier)>1:
			random_number = random.randint(int(quantifier[0]), int(quantifier[1]))
		else:
			random_number = random.randrange(int(quantifier[0]))
		for i in range(random_number):
			new_str = self.squareParser(string)
			if '|' in new_str:
				new_str = self.squareParser(new_str)
			strng+=new_str
		return strng
	
	def barParser(self, string):
		if '[' in string:
			string = string[1:-1]
		new_str = string.split('|')
		random_number = random.randrange(len(new_str))
		new_str = new_str[random_number]
		return new_str

	
	def genericCurlyParser(self, string):
		start = string.index('{') + 1
		end = string.index('}')
		quantifier = string[start:end]
		quantifier = quantifier.split(',')
		string = string[:start-1]
		strng = ''
		if len(quantifier)>1:
			random_number = random.randint(int(quantifier[0]), int(quantifier[1]))
		else:
			random_number = random.randrange(int(quantifier[0]))
		for i in range(random_number):
			strng+=string
		return strng

	def quantifierParser(self, string, type):
		if '[' in string:
			string = string[1:-1]
		if type=='*':
			random_number = random.randint(0, MAX)
		if type=='+':
			random_number = random.randint(1, MAX)
		if type=='?':
			random_number = random.randint(0, 1)
		if '-' in string and len(string)==3:
			parsed = string.split('-')
			list_of_objs = []
			for i in range(ord(string[0]),ord(string[2])):
				list_of_objs.append(chr(i))
			string = self.quantifierGenericParser(list_of_objs, random_number)
		else:
			string = self.quantifierGenericParser(string, random_number)
		return string

	def getListofPatterns(self, regex):
		
		special_symbol = False
		start=False
		strng=''
		index=0
		list_of_subpattern=[]
		for i in regex:
			if special_symbol:
				strng+=i
				if symbol=='?' or symbol=='+' or symbol =='*' or i=='}':
					special_symbol=False
					start=False
					list_of_subpattern.append(strng)
					strng=''
			elif i == ')' and start:
				strng+=i
				try:
					if regex[index+1]=='{':
						special_symbol=True
						symbol='{'
					elif regex[index+1]=='?':
						special_symbol=True
						symbol='?'
					elif regex[index+1]=='+':
						special_symbol=True
						symbol='+'
					elif regex[index+1]=='*':
						special_symbol=True
						symbol='*'
					else:
						start=False
						list_of_subpattern.append(strng)
						strng=''
				except:
					start=False
					# strng+=')'
					list_of_subpattern.append(strng)
					strng=''
			elif start:
				strng+=i
			elif i == '(':
				if len(strng)>0:
					list_of_subpattern.append(strng)
				strng='('
				start=True
			else:
				strng+=i
			index+=1
		list_of_subpattern.append(strng)

		new_list_of_subpattern = []
		for pattern in list_of_subpattern:
			if len(pattern)>0:
				if(pattern[0]!='('):
					new_list_of_subpattern.append('('+pattern+')')
				else:
					new_list_of_subpattern.append(pattern)
		list_of_subpattern = new_list_of_subpattern

		return list_of_subpattern

	def parseSubPattern(self, list_of_subpattern):
		strng=''
		start=False
		special_symbol = False
		symbol = ''
		index=0
		new_list_of_subpattern = []
		for pattern in list_of_subpattern:
			p = pattern
			if pattern[-1]=='}':
				cpystr = ''
				for i in pattern:
					if i=='{':
						break
					else:
						cpystr+=i
					# cpystr+=cpystr
				list_of_subpattern.insert(index+1,cpystr)
				list_of_subpattern[index] = cpystr
				p=cpystr
			if pattern[-1]=='?' or pattern[-1]=='+' or pattern[-1]=='*':
				pattern_str = pattern[-1]
				cpystr = ''
				for i in pattern:
					if i==pattern_str:
						break
					else:
						cpystr+=i
					# cpystr+=cpystr
				if pattern_str=='*':
					random_number = random.randint(0, MAX)
				if pattern_str=='+':
					random_number = random.randint(1, MAX)
				if pattern_str=='?':
					random_number = random.randint(0, 1)
				for i in range(0, random_number):
					list_of_subpattern.insert(index+1,cpystr)
				p=cpystr
			new_list_of_subpattern.append(p)
			index+=1

		
		for i in range(len(new_list_of_subpattern)):
			if new_list_of_subpattern[i][0]=='(':
				new_list_of_subpattern[i] = new_list_of_subpattern[i][1:-1]

		return new_list_of_subpattern
	def parseSubPatternAlternates(self, list_of_subpattern):
		index=0
		for pattern in list_of_subpattern:
			bracket_open = False
			new_pattern = ''
			new_pattern_list = []
			if '|' in pattern:
				# print(pattern)
				for i in pattern:
					if i=='[':
						bracket_open = True
						new_pattern += i
					elif i==']':
						bracket_open = False
						new_pattern += i
					elif i=='|' and not bracket_open:
						new_pattern += i
					else:
						new_pattern += i
				new_pattern_list.append(new_pattern)
				if(len(new_pattern_list)>0):
					random_number = random.randrange(len(new_pattern_list))
					list_of_subpattern[index] = new_pattern_list[random_number]
				# new_list_of_subpattern.append(new_pattern_list)
			index+=1
		return list_of_subpattern

	def parsePattern(self, list_of_subpattern):
		new_list_of_subpattern = []
		cstr = ''
		for pattern in list_of_subpattern:
			cstr = ''
			if '|' in pattern:
				new_list_of_subpattern.append(pattern)
			else:
				for sub in pattern:
					if sub=='[':
						new_list_of_subpattern.append(cstr)
						cstr='['
						continue
					cstr+=sub
				if len(cstr)>0:
					new_list_of_subpattern.append(cstr)
		return new_list_of_subpattern

	def parsePatternQuantifier(self, list_of_subpattern):
		list_of_strings = []
		start = False
		special_symbol = False
		symbol = ''
		for pattern in list_of_subpattern:
			index = 0
			strng=''
			if '|' in pattern:
				list_of_strings.append(pattern)
				continue
			for i in pattern:
				
				if special_symbol:
					strng+=i
					if i=='}':
						special_symbol=False
						symbol='{'
						start=False
						list_of_strings.append(strng)
						strng=''
					elif symbol=='*' or symbol=='+' or symbol=='?':
						special_symbol=False
						start=False
						list_of_strings.append(strng)
						strng=''
				elif i == ']' and start:
					strng+=']'
					try:
						if pattern[index+1]=='[':
							start=False
							list_of_strings.append(strng)
							strng=''
						else:
							if pattern[index+1]=='{':
								special_symbol=True
								symbol='{'
							elif pattern[index+1]=='?':
								special_symbol=True
								symbol='?'
							elif pattern[index+1]=='+':
								special_symbol=True
								symbol='+'
							elif pattern[index+1]=='*':
								special_symbol=True
								symbol='*'
							elif pattern[index+1]=='|':
								special_symbol=True
								symbol='|'
							else:
								start=False
								list_of_strings.append(strng)
								strng=''
					except:
						start=False
						list_of_strings.append(strng)
						strng=''
				elif start:
					strng+=i
				elif i == '[':
					if len(strng)>0:
						list_of_strings.append(strng)
					strng='['
					start=True
				else:
					strng+=i
				index+=1
			list_of_strings.append(strng)

		index=0
		for string in list_of_strings:
			if '|' in string:
				if string[-1]=='}':
					new_str = self.genericCurlyParser(string)
					parsed = ''
					new_list =[]
					for elem in new_str:
						if elem == '[':
							if len(parsed)>0:
								new_list.append(parsed)
							parsed = ''
						parsed+=elem
					new_list.append(parsed)
					new_str = ''
					for item in new_list:
						parsed = item[1:-1]
						parsed = parsed.split('|')
						random_number = random.randrange(len(parsed))
						new_str += parsed[random_number]
					list_of_strings[index] = new_str
			index+=1
		return list_of_strings

	def getSubPatterns(self, regex):
		list_of_subpattern = []
		
		list_of_subpattern = self.getListofPatterns(regex)  #Seperates SubPatterns in a Regex
		
		list_of_subpattern = self.parseSubPattern(list_of_subpattern) #Parses SubPattern Quantifiers
		
		# list_of_subpattern = self.parseSubPatternAlternates(list_of_subpattern) #Parses SubPattern's Alternate Branches
		
		list_of_subpattern = self.parsePattern(list_of_subpattern) #Parses the Patterns
		
		list_of_strings = self.parsePatternQuantifier(list_of_subpattern) #Parses Pattern's Quantifiers

		return list_of_strings

	def generate(self): #Parses and Generates Strings

		list_of_strings = self.getSubPatterns(self.regex) #Sub Patterns Generates a list of Patterns
		# We break the Regex into smaller Sub Patterns and then solve them seperately and finally putting them together. 
		# Priority -> () > {} > [] 
		# print(list_of_strings)
		generatedStrings = []
		for i in range(self.qnt):
			generatedString = ''
			for string in list_of_strings:
				if len(string)==0:
					continue
				elif string[-1] == '?':
					generatedString += self.quantifierParser(string[:-1], '?')
				elif string[-1] == '}':
					generatedString += self.curlyParser(string)
				elif string[-1] == ']':#Parses String Inside Square Brackets
					new_str = self.squareParser(string)
					if '|' in new_str: # Case when Choice inside square bracket
						new_str = self.squareParser(new_str)
					generatedString += new_str 
				elif string[-1] == '*':
					generatedString += self.quantifierParser(string[:-1], '*')
				elif string[-1] == '+':
					generatedString += self.quantifierParser(string[:-1], '+')
				elif '|' in string:
					generatedString += self.barParser(string)
				else:
					generatedString += string
			generatedStrings.append(generatedString)#No Pattern, Append as it is.
		print(generatedStrings)

# a = RegexGen('/(4[5|9])(:[0-5][0-9]|:[a-c]){2} (A|P)M/', 10)
reg = input("Enter Regex. Pattern -> /<regex>/\n")
a = RegexGen(reg, 10)
# a = RegexGen('/[^a-w]/', 10)
# a = RegexGen('/[+-]?[0-9]{1,16}[.][0-9]{1,6}/', 10)
# a = RegexGen('/(1[0|2]|0[1-9])(:[0-5][0-9]){2} (A|P)M/', 10)

# a = RegexGen('/[1-5]c/', 10)
# a = RegexGen('/(1[0-2]|0[1-9])(:[0-5][0-9]){2} (A|P)M/', 10)
a.generate()