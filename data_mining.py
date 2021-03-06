import numpy as np
from nltk.corpus import stopwords

data_file_name = 'data_set_aminar_dblp.v11/dblp_papers_v11.txt'
#data_file_name = 'data_set_aminar_dblp.v11/sample_of_dblp_papers_v11.txt'
no_of_sample = 1000

stop_words = set(stopwords.words('english'))
unwanted_chars = ['-', '(', ')', '_', '\\', ',', '.', "'", '"', ':', ':', '%']

def get_next_word(this_paper):
	global j
	this_word = ''
	while j < len(this_paper) and this_paper[j] != '"':
		j = j + 1
	j = j + 1
	while j < len(this_paper) and this_paper[j] != '"':
		if(this_paper[j] == '\\'):
			j = j + 1
		if(this_paper[j] == '.') or (this_paper[j] == ','):
			j = j + 1
			continue
		this_word = this_word + this_paper[j]
		j = j + 1
	j = j + 1
	return this_word

class Authors:
	def __init__(self):
		self.name = ''
		self.identity = ''
		self.org = ''

class Venue:
	def __init__(self):
		self.identity = ''
		self.raw = ''

class Fos:
	def __init__(self):
		self.name = ''
		self.w = 0.0

class Indexed_abstract:
	def __init__(self):
		self.IndexLength = 0
		self.InvertedIndex = []

class Word_index:
	def __init__(self):
		self.word = ''
		self.index = []

class Paper:
	def __init__(self):
		self.identity = ''
		self.title = ''
		self.authors = []
		self.authors_name_list = []
		self.venue = Venue()
		self.year = 0
		self.keywords = []
		self.fos = []
		self.fos_list = []
		self.references = []
		self.n_citation = 0
		self.page_start = ''
		self.page_end = ''
		self.doc_type = ''
		self.lang = ''
		self.publisher = ''
		self.volume = ''
		self.issue = ''
		self.issn = ''
		self.isbn = ''
		self.doi = ''
		self.pdf = ''
		self.url = []
		self.abstract = ''
		self.indexed_abstract = Indexed_abstract()
		self.word_with_frequency = {}

class Collection:
	def __init__(self):
		self.collection_size = no_of_sample
		self.paper = []
		self.attributes = {}

	def print_data(self):
		for i in self.paper:
			print('identity : ' + i.identity)
			print('title : ' + i.title)
			print('authors :')
			for j in i.authors:
				print('\tname : ' + j.name + '\tidentity : ' + j.identity + '\torg : ' + j.org)
			print('keywords :')
			for j in i.keywords:
				print('\t' + j)
			print('fos :')
			for j in i.fos:
				print('\tname : ' + j.name + '\tw : ' + str(j.w))
			print('references :')
			for j in i.references:
				print('\t' + j)
			print('venue :')
			print('\traw : ' + i.venue.raw + '\tidentity : ' + i.venue.identity)
			print('year : ' + str(i.year))
			print('n_citation : ' + str(i.n_citation))
			print('page_start : ' + i.page_start)
			print('page_end : ' + i.page_end)
			print('doc_type : ' + i.doc_type)
			print('lang : ' + i.lang)
			print('publisher : ' + i.publisher)
			print('volume : ' + i.volume)
			print('issue : ' + i.issue)
			print('issn : ' + i.issn)
			print('isbn : ' + i.isbn)
			print('doi : ' + i.doi)
			print('pdf : ' + i.pdf)
			print('url :')
			for j in i.url:
				print('\t' + j)
			print('indexed_abstract :')
			print('\tIndexLength : ' + str(i.indexed_abstract.IndexLength))
			print('\tInvertedIndex : ')
			for j in i.indexed_abstract.InvertedIndex:
				print('\t\tword : ' + j.word, end = '')
				print('\t\tIndex : ', end = '')
				for k in j.index:
					print(str(k), end = ',')
				print()
			print('\n')

	def read_data(self):
		global j
		input_file = open(data_file_name, "r")
		for i in range(0, self.collection_size):
			this_paper = input_file.readline()
			print(i)
			#print(this_paper + '\n')
			paper = Paper()
			j = 0;
			if(this_paper == ''):
				self.collection_size = i;
				break
			while j < len(this_paper):
				this_word = get_next_word(this_paper)
				if this_word in self.attributes:
					key = self.attributes[this_word]
					if(key == 0):
						paper.identity = get_next_word(this_paper)
					elif(key == 1):
						paper.title = get_next_word(this_paper)
					elif(key == 2):
						while j < len(this_paper) and this_paper[j + 1] != ']':
							temp = Authors()
							j = j + 1
							while j < len(this_paper) and this_paper[j] != '}':
								temp1 = get_next_word(this_paper)
								if(temp1 == 'name'):
									temp.name = get_next_word(this_paper)
									temp.name = temp.name.lower()
								elif(temp1 == 'id'):
									temp.identity = get_next_word(this_paper)
								elif(temp1 == 'org'):
									temp.org = get_next_word(this_paper)
							flag = 0
							for x in paper.authors:
								if(x.identity == temp.identity):
									flag = 1
									break
							if(flag == 0):
								paper.authors.append(temp)
								paper.authors_name_list.append(temp.name)
					elif(key == 3):
						while j < len(this_paper) and this_paper[j] != '}':
							temp = get_next_word(this_paper)
							if(temp == 'id'):
								paper.venue.identity = get_next_word(this_paper)
							elif(temp == 'raw'):
								paper.venue.raw = get_next_word(this_paper)
					elif(key == 4):
						j = j + 2
						temp = ''
						while j < len(this_paper) and this_paper[j] >= '0' and this_paper[j] <= '9':
							temp = temp + this_paper[j]
							j = j + 1
						paper.year = int(temp)
					elif(key == 5):
						if(this_paper[j + 3] != ']'):
							while j < len(this_paper) and this_paper[j] != ']':
								paper.keywords.append(get_next_word(this_paper))
					elif(key == 6):
						while j < len(this_paper) and this_paper[j + 1] != ']':
							temp = Fos()
							j = j + 1
							while j < len(this_paper) and this_paper[j] != '}':
								temp1 = get_next_word(this_paper)
								if(temp1 == 'name'):
									temp.name = get_next_word(this_paper)
									temp.name = temp.name.lower()
								elif(temp1 == 'w'):
									j = j + 2
									temp2 = ''
									while j < len(this_paper) and ((this_paper[j] >= '0' and this_paper[j] <= '9') or this_paper[j] == '.'):
										temp2 = temp2 + this_paper[j]
										j = j + 1
									temp.w = float(temp2)
							paper.fos.append(temp)
							if temp.name not in paper.fos_list:
								paper.fos_list.append(temp.name)
					elif(key == 7):
						if(this_paper[j + 3] != ']'):
							while j < len(this_paper) and this_paper[j] != ']':
								paper.references.append(get_next_word(this_paper))
					elif(key == 8):
						j = j + 2
						temp = ''
						while j < len(this_paper) and this_paper[j] >= '0' and this_paper[j] <= '9':
							temp = temp + this_paper[j]
							j = j + 1
						paper.n_citation = int(temp)
					elif(key == 9):
						paper.page_start = get_next_word(this_paper)
					elif(key == 10):
						paper.page_end = get_next_word(this_paper)
					elif(key == 11):
						paper.doc_type = get_next_word(this_paper)
					elif(key == 12):
						paper.lang = get_next_word(this_paper)
					elif(key == 13):
						paper.publisher = get_next_word(this_paper)
						paper.publisher = paper.publisher.lower()
					elif(key == 14):
						paper.volume = get_next_word(this_paper)
					elif(key == 15):
						paper.issue = get_next_word(this_paper)
					elif(key == 16):
						paper.issn = get_next_word(this_paper)
					elif(key == 17):
						paper.isbn = get_next_word(this_paper)
					elif(key == 18):
						paper.doi = get_next_word(this_paper)
					elif(key == 19):
						paper.pdf = get_next_word(this_paper)
					elif(key == 20):
						while j < len(this_paper) and this_paper[j] != ']':
							paper.url.append(get_next_word(this_paper))
					elif(key == 21):
						paper.abstract = get_next_word(this_paper)
					elif(key == 22):
						get_next_word(this_paper)
						j = j + 2
						temp = ''
						while j < len(this_paper) and this_paper[j] >= '0' and this_paper[j] <= '9':
							temp = temp + this_paper[j]
							j = j + 1
						paper.indexed_abstract.IndexLength = int(temp)
						get_next_word(this_paper)
						while j < len(this_paper) and this_paper[j + 1] != '}':
							temp1 = Word_index()
							temp1.word = get_next_word(this_paper)
							temp1.word = temp1.word.lower()
							temp1.word = ''.join(i for i in temp1.word if not i in unwanted_chars)
							j = j + 3
							temp2 = ''
							while j < len(this_paper) and this_paper[j] != ']':
								if(this_paper[j] == ','):
									temp1.index.append(temp2)
									temp2 = ''
									j = j + 1
								else:
									temp2 = temp2 + this_paper[j]
								j = j + 1
							temp1.index.append(temp2)
							paper.indexed_abstract.InvertedIndex.append(temp1)
						for x in paper.indexed_abstract.InvertedIndex:
							if x.word.isalpha() and (x.word not in stop_words):
								if x.word not in paper.word_with_frequency:
									paper.word_with_frequency[x.word] = len(x.index)
								else:
									paper.word_with_frequency[x.word] += len(x.index)
			self.paper.append(paper)
		input_file.close()

	def map_attributes_to_interger(self):
		self.attributes['id'] = 0
		self.attributes['title'] = 1
		self.attributes['authors'] = 2
		self.attributes['venue'] = 3
		self.attributes['year'] = 4
		self.attributes['keywords'] = 5
		self.attributes['fos'] = 6
		self.attributes['references'] = 7
		self.attributes['n_citation'] = 8
		self.attributes['page_start'] = 9
		self.attributes['page_end'] = 10
		self.attributes['doc_type'] = 11
		self.attributes['lang'] = 12
		self.attributes['publisher'] = 13
		self.attributes['volume'] = 14
		self.attributes['issue'] = 15
		self.attributes['issn'] = 16
		self.attributes['isbn'] = 17
		self.attributes['doi'] = 18
		self.attributes['pdf'] = 19
		self.attributes['url'] = 20
		self.attributes['abstract'] = 21
		self.attributes['indexed_abstract'] = 22

collection = Collection()
collection.map_attributes_to_interger()
collection.read_data()

name_set = {}
for i in range(0, len(collection.paper)):
	for author_name in collection.paper[i].authors:
		if author_name.name not in name_set:
			name_set[author_name.name] = [[i]]
		else:
			name_set[author_name.name].append([i])

count_a = 0
for x in name_set:
	if (len(name_set[x]) > 1):
		print(x + " " + str(len(name_set[x])))
		for y in name_set[x]:
			print(y[0], end = "||")
		list_of_co_authors = []
		list_of_fos = []
		list_of_years = []
		list_of_references = []
		list_of_lang = []
		list_of_publishers = []
		list_of_keywords = []
		keywords_with_frequency = {}
		print()
		for y in name_set[x]:
			for z in collection.paper[y[0]].authors_name_list:
				if (z != x) and (z not in list_of_co_authors):
					list_of_co_authors.append(z)
		for y in name_set[x]:
			for z in collection.paper[y[0]].fos_list:
				if (z not in list_of_fos) and (z != ''):
					list_of_fos.append(z)
		for y in name_set[x]:
			if (collection.paper[y[0]].year not in list_of_years) and (collection.paper[y[0]].year != 0):
				list_of_years.append(collection.paper[y[0]].year)
		for y in name_set[x]:
			for z in collection.paper[y[0]].references:
				if (z not in list_of_references) and (z != ''):
					list_of_references.append(z)
		for y in name_set[x]:
			if (collection.paper[y[0]].lang not in list_of_lang) and (collection.paper[y[0]].lang != ''):
				list_of_lang.append(collection.paper[y[0]].lang)
		for y in name_set[x]:
			if (collection.paper[y[0]].publisher not in list_of_publishers) and (collection.paper[y[0]].publisher != ''):
				list_of_publishers.append(collection.paper[y[0]].publisher)
		for y in name_set[x]:
			for z in collection.paper[y[0]].word_with_frequency:
				if z not in keywords_with_frequency:
					keywords_with_frequency[z] = collection.paper[y[0]].word_with_frequency[z]
				else:
					keywords_with_frequency[z] += collection.paper[y[0]].word_with_frequency[z]



		for z in keywords_with_frequency:
			if ((keywords_with_frequency[z] > 1) and (keywords_with_frequency[z] < (1.5 * len(name_set[x])))):
				if (z not in list_of_keywords) and (z != ''):
					list_of_keywords.append(z)
		#print(keywords_with_frequency)

		print("Co-authors : ", end = '')
		print(list_of_co_authors)
		print("fos : ", end = '')
		print(list_of_fos)
		print("years : ", end = '')
		print(list_of_years)
		print("references : ", end = '')
		print(list_of_references)
		print("lang : ", end = '')
		print(list_of_lang)
		print("publishers : ", end = '')
		print(list_of_publishers)
		print("keywords : ", end = '')
		print(list_of_keywords)

		feature_matrix = []
		for y in name_set[x]:
			feature_vector = []
			for z in list_of_co_authors:
				feature_vector.append(collection.paper[y[0]].authors_name_list.count(z))

			for z in list_of_fos:
				feature_vector.append(collection.paper[y[0]].fos_list.count(z))

			for z in list_of_years:
				if(z == collection.paper[y[0]].year):
					feature_vector.append(1)
				else:
					feature_vector.append(0)
				
			for z in list_of_references:
				feature_vector.append(collection.paper[y[0]].references.count(z))

			for z in list_of_lang:
				if(z == collection.paper[y[0]].lang):
					feature_vector.append(1)
				else:
					feature_vector.append(0)

			for z in list_of_publishers:
				if(z == collection.paper[y[0]].publisher):
					feature_vector.append(1)
				else:
					feature_vector.append(0)

			for z in list_of_keywords:
				if z in collection.paper[y[0]].word_with_frequency:
					feature_vector.append(collection.paper[y[0]].word_with_frequency[z])
				else:
					feature_vector.append(0)
			
			feature_matrix.append(feature_vector)
			print(feature_vector)
		feature_np_matrix = np.array(feature_matrix)
		#print(feature_np_matrix)

		#main algo
		freq = np.sum(feature_np_matrix, axis = 0)
		x_freq = np.sum(feature_np_matrix, axis = 1)
		#print(freq)
		#print(x_freq)
		p_x_f = feature_np_matrix / freq[None, :]
		#print("p_x_f")
		#print(p_x_f)
		p_f_x = feature_np_matrix / x_freq[:, None]
		#print("p_f_x")
		#print(p_f_x)
		p_x_x = np.matmul(p_x_f, p_f_x.T)
		print("p_x_x")
		print(p_x_x)

		l = 0.1

		while (len(name_set[x]) > 1):
			#keep_cluster_id = {}
			c_sys_matrix = np.zeros((feature_np_matrix.shape[0] ,len(name_set[x])))
			count = 0;
			for j in range(0, len(name_set[x])):
				for k in range(0, len(name_set[x][j])):
					#keep_cluster_id[count] = j
					c_sys_matrix[count][j] = 1
					count = count + 1
			#print(c_sys_matrix)

			cluster_vector = np.matmul(x_freq.T, c_sys_matrix)
			#print(cluster_vector.shape)

			#print(x_freq.shape)
			p_x_c = np.multiply((np.matmul(x_freq.reshape(len(x_freq ), 1), (1 / cluster_vector).reshape(1, len(cluster_vector)))), c_sys_matrix)
			#print(p_x_c)

			p_c_c = np.matmul(c_sys_matrix.T, np.matmul(p_x_x, p_x_c))
			print("p_c_c")
			print(p_c_c)

			merge = []
			max = 0
			row_index = 0
			column_index = 0
			for m in range(0, p_c_c.shape[0]):
				for n in range(0, p_c_c.shape[1]):
					if(m != n):
						if(max < p_c_c[m][n]):
							max = p_c_c[m][n]
							row_index = m
							column_index = n
			if(max > l):
				merge.append([row_index, column_index])
			if(len(merge) == 0):
				break
			else:
				for y in merge:
					name_set[x][row_index].extend(name_set[x][column_index])
					del name_set[x][column_index]
			#print(name_set[x])

		count_a = count_a + len(name_set[x])
		#print(name_set[x])
		print()
	else:
		count_a = count_a + 1
print(count_a)

for x in name_set:
	if (len(name_set[x]) > 1):
		print(x, end = " ")
		print(name_set[x])
	else:
		if (len(name_set[x][0]) > 1):
			print(x, end = " ")
			print(name_set[x])