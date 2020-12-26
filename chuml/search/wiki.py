import os
import re
import html
from chuml.core import config

files = list(filter(
	lambda x: not x.startswith('.'),
	os.listdir(config.wiki_path)
))

def search(expresion):
	exp = re.compile(expresion)
	document = ['<div class=grep-block>']
	for file_name in files:
		file = open(wiki_path + "/" + file_name)
		for i, line in enumerate(file.readlines()):
			results = list(exp.finditer(line))
			if results:
				document.append('''
					<div class="grep-result">
					<a href=https://github.com/jarys/wiki/blob/master/{}#L{}>
						<span class="grep-file">{}:</span>
					</a>
					'''.format(file_name, i+1, file_name
						))
				delice = list(map(lambda x:x.span(), results))
				delice.append((-1, -1))
				document.append(html.escape(line[0:delice[0][0]]))
				for i in range(len(results)):
					document.append('''<span class=grep-color>{}</span>'''.format(
						html.escape(line[delice[i][0]:delice[i][1]])))
					document.append(html.escape(line[delice[i][1]:delice[i+1][0]]))
				document.append('</div>')
		file.close()
	
	document.append('</div>')

	return ''.join(document)

if __name__ == "__main__":
	import sys
	print(search(sys.argv[1]))



