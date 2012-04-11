# -*- coding: utf-8 -*- 

# Where the index is stored
index_location = "index.pkl"

# Webpages to crawl
root_web_pages = ["http://www.gastronomias.com/receitas/molhos.htm",
				  "http://www.gastronomias.com/receitas/entradas.htm", 
				  "http://www.gastronomias.com/receitas/sopas.htm",
				  "http://www.gastronomias.com/receitas/peixes.htm",
				  "http://www.gastronomias.com/receitas/carnes.htm",
				  "http://www.gastronomias.com/diabetes/inicio.htm"]

# Ignored in order to acquire more accurate results
ignored_prepositions = ["sem", "com", "que", "III", "dos", "sem", "das", 
						"gua", "cor", "etc", "leo", "lim", "bom", "grs", 
						"1lt", "5dl", "caf", "htm", "sua", "boa", "pes",	
						"car", "bem", "mso", "New", "afr", "mas", "seu",
						"ria", "10g", "cru", "nem", "mal", "ser", "kgs", 
						"80g", "mam", "end", "caj", "mae", "pau", "50g", 
						"por", "fac", "uma", "fcs", "iii", "num", "Pur", 
						"afr", "nio", "reg", "gim", "bas", "lio", "dio",
						"www", "ver", "for", "aos", "ais", "8cm", "2lt", 
						"fio", "pur", "vel", "dea", "tri", "Lim", "nia", 
						"del", "via", "aux", "Aji", "1dl", "lts", "nas", 
						"ras", "1kg", "0pt", "peq", "20g", "cie", "l00", 
						"fra", "che", "30g", "toa", "nea", "rad", "cio", 
						"mil", "Pat", "fil", "Can", "dip", "duo", "pil", 
						"neo", "2dl", "vol", "mix", "xer", "gra", "sao", 
						"lua", "Uma", "2kg", "tro", "per", "feu", "aba", 
						"vez", "60g", "4kg", "zia", "Bom", "img", "src", 
						"gif", "eir", "5kg", "pct", "nos", "dls", "lhe", 
						"dnt", "ltr", "Kgs", "bac", "meu", "amp", "4dl", 
						"gor", "uns", "1cm", "1oo", "Dcl", "Del", "cia", 
						"emb", "5gr", "cos", "red", "Grs", "1Kg", "3Kg", 
						"zia", "70g", "tem", "pra", "fim", "dia", "cox", 
						"dar", "pat", "esp", "dua", "End", "sto", "coq", 
						"vin", "Fac", "veu", "bia", "de4", "due", "90g", 
						"tem", "pac", "4ou", "Ing", "vea", "liq", "und", 
						"ter", "Doc", "2Kg", "Bas", "5Kg", "alm", "beb", 
						"ado", "2Kg", "Com", "Ado", "cil"]
			
# Number of results presented for each query			
results_per_query = 20

# Browser path - needed to open the recipes! (open is enough for MAC users)
browser_command="open "



# For string cleaning and format!
import external
import re

# For system calls
import os

# For index storing
import pickle


# Gets the webpage content
def get_page(url):
	try:
		import urllib
	#	print url
		return urllib.urlopen(url).read()
	except:
		return ""


# Removes all the accents from the letters
def process_diacritics(word):
	ret = ""
	for letter in word:
		ret += external.latin1_to_ascii(letter)

	return ret


# Removes all the white spaces inside the sentences
def clean_whites(sentence):
	sentence = process_diacritics(sentence)
	sentence = sentence.lower()
	words = split_words(sentence)
	ret = ""
	for word in words:
		ret += word + " "
	return ret.strip()


# Splits all the words in a sentence
def split_words(sentence):
	return re.split('\W+', sentence)
		

# Gets the next recipe, for all the format: "<a href="http://www.gastronomias.com/receitas/rec2742.htm">Sonhos de Batata</a>"
def get_next_recipe_v1(content, index):
	pattern = 'href="http://www.gastronomias.com/receitas/rec'
	
	# Get the url
	beginning = content[index:].find(pattern) + index
	
	# Pattern not found... :(
	if beginning-index == -1:
		return "", "", -1
	
	beginning += content[beginning:].find('"') + 1
	end = content[beginning:].find('"') + beginning
	url = content[beginning:end]
	
	# Get the name
	beginning = end + content[end:].find('>') + 1
	end = content[beginning:].find('<') + beginning
	name = content[beginning:end]
	
	return url.strip(), clean_whites(name), end
	
	
# Gets the next recipe, for all the format: "<a href="rec3203.htm">Sonhos de Abóbora com Ervas Aromáticas</a>"
def get_next_recipe_v2(content, index):
	prefix = 'http://www.gastronomias.com/receitas/'
	pattern = 'href="rec'
	return get_next_recipe_vX(content, index, prefix, pattern)
	

# Gets the next recipe, for all the format: "<a href="diab11.htm">Coelho com Mostarda</a>"
def get_next_recipe_v3(content, index):
	prefix = 'http://www.gastronomias.com/diabetes/'
	pattern = 'href="diab'
	return get_next_recipe_vX(content, index, prefix, pattern)


# Gets the next recipe, for all the format: "<a href="cock0796.htm">Batido de Framboesa e Laranja</a>"
def get_next_recipe_v4(content, index):
	prefix = 'http://www.gastronomias.com/diabetes/'
	pattern = 'href="cock'
	return get_next_recipe_vX(content, index, prefix, pattern)
	

# Gets the next recipe, for all the format: "<a href="doce0801.htm">"Biscotli" de Morango</a>"
def get_next_recipe_v5(content, index):
	prefix = 'http://www.gastronomias.com/diabetes/'
	pattern = 'href="doce'
	return get_next_recipe_vX(content, index, prefix, pattern)
		
		
# Gets the next recipe, for all the format: "<a href="doce0801.htm">"Biscotli" de Morango</a>"
def get_next_recipe_vX(content, index, prefix, pattern):
	# Get the url
	beginning = content[index:].find(pattern) + index

	# Pattern not found... :(
	if beginning-index == -1:
		return "", "", -1

	beginning += content[beginning:].find('"') + 1
	end = content[beginning:].find('"') + beginning
	url = content[beginning:end]

	# Get the name
	beginning = end + content[end:].find('>') + 1
	end = content[beginning:].find('<') + beginning
	name = content[beginning:end]

	return prefix+url.strip(), clean_whites(name), end
		
		
# Checks if a word is an ignorable prepositions.
def accept_word(word):
	if len(word) < 3:
		return False
		
	if word in ignored_prepositions:
		return False
	
	# Ignoring numbers
	try:
		int(word)
		return False
	except:
		
		#if len(word) < 4:
		#	print word
		
		return True
	

# Adds a set of words to the index. Attaches the respective url.
def add_content_to_index(words, title, url, index):
	for word in words:
		if accept_word(word):
			if word in index:
				add = True
				
				# To prevent different names for the same url!
				for url_info in index[word]:
					if url_info[1] == url:
						add = False
						break
				
				if add:
					index[word].append([title, url])
			else:
				index[word] = [[title, url]]

	
# Gets the ingredients and adds them to the index
def add_ingredients_to_index(url, title, index):
	content = get_page(url)
	ingredients = 'Ingredientes'
	
	# Get the ingredients position
	ingredients_position = content.find(ingredients)
	
	# Ingredients not found... :(
	if ingredients_position == -1:
		return
	
	beg_list = "<ul>"
	beg_list_position = content[ingredients_position:].find(beg_list) + ingredients_position
	
	end_list = "</ul>"
	end_list_position = content[ingredients_position:].find(end_list) + ingredients_position
	
	pivot = beg_list_position
	
	while True:
		init_ingredient = '<li><font'
		end_ingredient = '</font>'
		
		pos = content[pivot:].find(init_ingredient)
		if pos == -1 or pos + pivot < beg_list_position or pos + pivot > end_list_position:
			break
			
		init_ingredient_pos = content[pivot:].find(init_ingredient) + pivot + len(init_ingredient) + 1
		init_ingredient_pos += content[init_ingredient_pos:].find(">") + 1
		
		end_ingredient_pos = content[pivot:].find(end_ingredient) + pivot
		
		ingredient = content[init_ingredient_pos:end_ingredient_pos]
		add_content_to_index(split_words(ingredient), title, url, index)
		
		pivot = end_ingredient_pos + 1
	
	
# Adds the content of a recipe to the index. Adds the title and the ingredients.
def add_to_index(title, url, index):
	add_content_to_index(split_words(title), title, url, index)
	add_ingredients_to_index(url, title, index)


# Crawls the webpaces for the titles and ingredients
def recipe_crawler(index):
	for web_page_address in root_web_pages:
		content = get_page(web_page_address)

		# GET in the v1 format!
		i = 0
		while i != -1:
			url, name, i = get_next_recipe_v1(content, i)
			add_to_index(name, url, index)
	
		# GET in the v2 format!
		i = 0
		while i != -1:
			url, name, i = get_next_recipe_v2(content, i)
			add_to_index(name, url, index)
			
		# GET in the v3 format!
		i = 0
		while i != -1:
			url, name, i = get_next_recipe_v3(content, i)
			add_to_index(name, url, index)

		# GET in the v4 format!
		i = 0
		while i != -1:
			url, name, i = get_next_recipe_v4(content, i)
			add_to_index(name, url, index)

		# GET in the v4 format!
		i = 0
		while i != -1:
			url, name, i = get_next_recipe_v4(content, i)
			add_to_index(name, url, index)


# Prints the initial lookup message.
def print_initial_message():
	os.system("clear")
	print "<><><><><><><><><><><><><><><><><><>"
	print "<><><>   Welcome to reciPY!   <><><>"
	print "<><><><><><><><><><><><><><><><><><>"
	print ""
	print "---- Sample Usage ----"
	print ""
	print "< Recipe Name / Ingredients > : Bacalhau com Natas, Cebola, Azeite"
	print "< Exclude > : Cenoura"
	print ""
	print "---- Sample Usage ----"


# Prints the exit informative message.
def print_exit_informative_exit():
	print ""
	print ""
	print "< type 'exit' + ENTER to terminate the lookup >"
	print ""
	print ""
	
	
# Prints the exit message.
def print_exit_message():
	print ""
	print ""
	print "<><><><><><><><><><><><><><><><><><>"
	print "<><>   Thank you! Come again!   <><>"
	print "<><><>   Have a good meal!    <><><>"
	print "<><><><><><><><><><><><><><><><><><>"
	print ""


# Prints the results message.
def print_results_message():
	print ""
	print ""
	print "------------"
	print "-- Results:"
	print ""
	
	
# Prints the query message.
def print_query_message():
	print "------------"
	print "-- Query:"
	print ""
	

# Prints the navigation panel.
def print_navigation_panel():
	print ""
	print ""
	print "--------------------"
	print "-- Navigation Panel:"
	print ""
	print "> n : show next page."
	print "> exit : execute other query."
	print "> #id : open recipe in your browser."
	print ""


# Reads the lookup parameters from the shell.
def read_lookup_parameters():
	print_query_message()
	
	ingredients = raw_input('< Recipe Name / Ingredients > : ')
	if ingredients == "exit":
		return -1, "", ""
			
	exclude = raw_input('< Exclude > : ')
	if exclude == "exit":
		return -1, "", ""
	
	return 1, ingredients, exclude


# Searches the index for the words
def lookup_urls_for(search_parameters, index):
	parameters = split_words(search_parameters)
	ret = {}
	
	for parameter in parameters:
		p = clean_whites(parameter)
		if accept_word(p) and p in index:
			for url_info in index[p]:
				if p in ret:
					ret[p].append(url_info)
				else:
					ret[p] = [url_info]
	
	return ret
	
	
# Navigates through the results of the query
def result_navigation_loop(results, ingredients, exclude):
	current_page = 0
	total_pages = len(results) / results_per_query
	
	if len(results) % results_per_query != 0:
		total_pages = round(total_pages+0.5)
	
	while True:
		os.system("clear")
		print_query_message()
		print '< Recipe Name / Ingredients > : ' + ingredients
		print '< Exclude > : ' + exclude
		print_results_message()
		
		if total_pages > 0:
			print "( page " + str(current_page+1) + " of " + str(int(total_pages)) + ")"
		else:
			print "(no page found)"
			
		print ""
	
		from_id = current_page * results_per_query
		to_id = from_id + results_per_query
		
		i = from_id
		for result in results[from_id:to_id]:
			print "[" + str(i+1) + "] " + result["name"] #+ "  (" + result["url"] + ")"
			i += 1
			
		# Navigate through the results
		print_navigation_panel()
		while True:
			op = raw_input("Operation: ")
		
			if op == "exit":
				return
			elif op == "n":
				current_page = (current_page + 1) % total_pages
				current_page = int(current_page)
				break
			else:
				try:
					i = int(op)
					if i > 0 and i <= len(results):
						os.system(browser_command + results[i-1]["url"])
					else:
						print ""
						print "ERROR: invalid #id!"
						print ""
				except:
					continue # Not a valid integer


# Gets the index, in the results for the url 'url'	
def get_index_for_url(results, url):
	i = 0
	for r in results:
		if r["url"] == url:
			return i
		i += 1
	return -1


# Lookup routine. Allows to look for recipes.
# results = {name: X, url: Y, relevance: Z}
def lookup_loop(index):
	print_initial_message()
	print_exit_informative_exit()
	
	while True:
		status, ingredients, exclude = read_lookup_parameters()
		if status == -1:
			break
		
		results = []
		ingredients_results = lookup_urls_for(ingredients, index)
		exclude_results = lookup_urls_for(exclude, index)
		
		for r in ingredients_results:
			for url_unit in ingredients_results[r]:
				excl = False
				
				for er in exclude_results:
					if url_unit in exclude_results[er]:
						excl = True
						break
				
				if not excl:
					j =  get_index_for_url(results, url_unit[1])
					if j == -1:
						new_result = {}
						new_result["name"] = url_unit[0]
						new_result["url"] = url_unit[1]
						new_result["relevance"] = 1
						results.append(new_result)
					else:
						results[j]["relevance"] += 1
		
		# Sort results according to relevance ( most relevant first! )
		results = sorted(results, key=lambda k: k['relevance'], reverse=True) 
		
		result_navigation_loop(results, ingredients, exclude)
		os.system("clear")		
		print_exit_informative_exit()
			
	print_exit_message()


# Loads the index from a file
def load_index():
	try:
		pkl_file = open(index_location, 'rb')
		index = pickle.load(pkl_file)
		pkl_file.close()
		return index
	except:
		return None
	

# Writes the index to a file
def save_index(index):
	try:
		output = open(index_location, 'wb')
		pickle.dump(index, output)
		output.close()
	except:
		return # Do nothing








# main() :D


index = load_index()

if index == None:
	index = {}
	recipe_crawler(index)
	save_index(index)
	
lookup_loop(index)