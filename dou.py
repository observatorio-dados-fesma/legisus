
from requests import get
from re import findall
from json import loads, dump
from datetime import datetime

class Dou(object):	
	
	def get_data_dou_saude(self, date: str):
	
		'''format date: %d-%m-%Y'''

		try:

			url = f'https://www.in.gov.br/leiturajornal?org=Minist%C3%A9rio%20da%20Sa%C3%BAde&data={date}#daypicker'
		
			data = get(url).text
		
			text_data = findall(r'<script id="params" type="application/json">\n\t(.*?)\n', data)[0]
		
			return loads(text_data)

		except:

			return [{
    					'pubName': 'DO1',
    					'urlTitle': 'https://link.com',
    					'numberPage': '116',
    					'subTitulo': '',
    					'titulo': '',
    					'title': 'Sem Leis Publicadas Hoje',
    					'pubDate': '01/01/2023',
    					'content': 'Sem Leis Publicadas Hoje',
    					'editionNumber': '159',
    					'hierarchyLevelSize': 2,
    					'artType': 'Portaria',
    					'pubOrder': 'DO100046:00001:00000:00000:00000:00000:00000:00000:00000:00000:00054:00009',
    					'hierarchyList': ['Teste'],
    					'hierarchyStr': 'Minist\u00e9rio da Sa\u00fade/Gabinete da Ministra'
  					}]

	def tidy_data(self, date):

		data = self.get_data_dou_saude(date = date)['jsonArray']

		data = [i for i in data if i['hierarchyList'][0] == 'Ministério da Saúde']

		data = [{k: v for k,v in i.items() if k != 'hierarchyList'} for i in data]

		return data

	def save_data(self, date: str):

		with open(f'S:/04. FUNDO ESTADUAL DE SAÚDE/05. ANO 2023/1. Controle Financeiro/07. Recurso Federal/03. Painéis/Imagens e Outros/diario_dia.json', 'w') as file:
		
			dump(self.tidy_data(date = date), file, indent = 2)

dou = Dou()

hoje = datetime.now().strftime('%d-%m-%Y')

dou.save_data(date = hoje)
