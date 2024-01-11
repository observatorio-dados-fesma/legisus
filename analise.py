
import json
import nltk

from nltk.probability import FreqDist
from collections import Counter
from os import listdir
from shutil import copy
from re import findall, search
from datetime import datetime

nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('portuguese')

saude_stopwords = [
	'saúde', 'gm', 'ms', 'portaria', 'r', 'art', 'ministério', 'secretário',
	'diário', 'oficial', 'pr', 'resolução', 'ltda', '_', 'considerando',
	'ac', 'ro', 'rr', 'am', 'pa', 'ap', 'to', 
	'ba', 'se', 'pe', 'al', 'rn',
	'pi', 'ce', 'ms', 'mt', 'go', 'df', 'sp', 
	'mg', 'rj', 'es', 'sc', 'rs', 'pr', 'pb',
	'n', 's'
]

d = {
	' GM/MS': '', ' GM/GM': '', 'GMMS': '',
	' Nº': '', ' nº': '',
	'-RE n': '', '-RE': '', '-RDC': '', '-RE N': '',
	'/HSFE/MS/N': '', '-': '', '(*)': '',
	'd': '', 'de': '', '-re': '',
	'ï¿½ï¿½': 'ÇÃ', '4': '', 'Nº': '', '0': '', 'TRIA': 'TARIA', 'ÇAO': 'ÇÃO'
}

class LegiSus:

	def read(self):

		files = listdir('coleta/')

		data = []

		for i in files:

			with open(f'''coleta/{i}''', 'r') as file:
	
				data.append((i[:-5], json.load(file)))
	
		return dict([i for i in data if len(i[1]) > 0])

	def tag(self, text):

		sw = stopwords + saude_stopwords

		if text != None:

			text = [i for i in findall(r'\b[A-zÀ-úü]+\b', text.lower()) if i not in sw]

			l = FreqDist(text).most_common(4)

			return ' '.join([i[0] for i in l])

		else:

			return text

	def replace_names(self, text):

		for i, j in d.items():
			
			if text != None:

				text = text.split(' ')[0].split('/')[0]

				text = text.replace(i, j).upper()

				# print(text)

				return text

			else:

				return text

	def describe(self):

		data = self.read()

		x = []

		for i in data.keys():

			for j in data.get(i):

				try:

					s = {k: v for k, v in j.items() if k in ['titulo', 'ementa', 'url', 'texto_principal', 'texto_completo']}

					s['data'] = f'''{i[0:2]}/{i[2:4]}/{i[-4:]}'''

					x.append(s)

				except:
	
					pass

		for i in x:

			i['tipo'] = self.replace_names(i['titulo'])

			i['tag'] = self.tag(text = i['texto_principal'])

			try:

				if search('Maranh|MARANH| MA ', i['texto_principal']) != None:
	
					i['has_ma'] = True
	
				else:
	
					i['has_ma'] = False

			except:

				i['has_ma'] = False

		for i in x:

			try:

				if i['tipo'] == 'PORTARIA':

					if search('Média e Alta Complexidade|Atenção Especializada|SAMU', i['texto_completo']) != None or search('Média e Alta Complexidade|Atenção Especializada|SAMU', i['ementa']) != None:

						i['grupo'] = 'Média e Alta Complexidade'

					elif search('aquisição de equipamentos', i['texto_completo']) != None or search('aquisição de equipamentos', i['ementa']) != None:

						i['grupo'] = 'Equipamentos'

					elif search('recursos financeiros de capital|execução de obras', i['texto_completo']) != None or search('recursos financeiros de capital|execução de obras', i['ementa']) != None:

						i['grupo'] = 'Obras'

					elif search('Atenção Primária', i['texto_completo']) != None or search('Atenção Primária', i['ementa']) != None:

						i['grupo'] = 'Atenção Primária'

					elif search('Assistência Farmacêutica', i['texto_completo']) != None or search('Assistência Farmacêutica|PNAISP|CBAF|CEAF', i['ementa']) != None:

						i['grupo'] = 'Assistência Farmacêutica'

					elif search('Vigilância em Saúde|Vigilância Sanitária|Vigilância Epidemiológica', i['texto_completo']) != None or search('Vigilância em Saúde|Vigilância Sanitária|Vigilância Epidemiológica', i['ementa']) != None:

						i['grupo'] = 'Vigilância em Saúde'

					elif search('Gestão do SUS', i['texto_completo']) != None or search('Gestão do SUS', i['ementa']) != None:

						i['grupo'] = 'Gestão do SUS'

					else:

						i['grupo'] = 'Grupo não identificado'

				else:

					i['grupo'] = 'Sem grupo'

			except:

				i['grupo'] = 'Grupo não identificado'

			i.pop('texto_principal', None)

			i.pop('texto_completo', None)

		details = {
			'qtd_normativos': len(x),
			'tipos': dict(Counter([i['tipo'] for i in x])),
		}

		return x, details

ls = LegiSus()

data, det = ls.describe()

with open('dados.json', 'w', encoding = 'utf-8') as file:

	json.dump(data, file, indent = 2, ensure_ascii = False)

copy(
	'C:/Users/jersiton.matos/Documents/envs/leg/dados.json', 
	'S:/05. FUNDO ESTADUAL DE SAÚDE/06. ANO 2024/1. Controle Financeiro/11. Painéis Gerenciais - PBI/01. Painel Legislação do SUS'
)
