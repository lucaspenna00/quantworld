import pandas as pd
import numpy as np
import itertools
import csv
import os
import time
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import urllib
import datetime as dt
import yahooquery as yf
import os
from os import listdir
from os.path import isfile, join

def rename_equities():
	df = pd.read_csv("db_funds_tracker/summarize/DB_Fundos.csv")
	df.replace('BMGB11', 'BMGB4', inplace=True)
	df.replace('PCAR4 ', 'PCAR3', inplace=True)
	df.replace('NATU3', 'NTCO3', inplace=True)
	df.replace('ESTC3', 'YDUQ3', inplace=True)
	df.replace('TBLE3', 'EGIE3', inplace=True)
	df.replace('BVMF3', 'B3SA3', inplace=True)
	df.replace('SUZB5', 'SUZB3', inplace=True)
	df.replace('RUMO3', 'RAIL3', inplace=True)
	df.replace('KROT3', 'COGN3', inplace=True)
	df.replace('ALSC3', 'ALSO3', inplace=True)
	df.replace('ALLL3', 'RAIL3', inplace=True)
	df.to_csv("db_funds_tracker/summarize/DB_Fundos.csv")

def update_equities():
	valid_tickers = pd.read_csv("db_funds_tracker/input/valid_tickers.csv")
	valid_tickers = valid_tickers['tickers'].tolist()
	for ticker in valid_tickers:
	    if os.path.exists('equities_data/'+ticker+'.csv'):
	        pass
	    else:
	        print(ticker)
	        yf.Ticker(ticker+".SA").history(period='max').to_csv("equities_data/"+ticker+".csv")
	        time.sleep(3)

#INTERNAL
def identify_ticker(CD_ATIVO):

	if 'XXXX' in CD_ATIVO:
		return CD_ATIVO

	if "-" in CD_ATIVO:
		list = CD_ATIVO.split(" - ")
	elif "/" in CD_ATIVO:
		list = CD_ATIVO.split("/")
	else:
		list = []
		list.append(CD_ATIVO)

	for item in list:
		if item[-1:] == "T":
			item = item[:-1]
			termo = "Termo "
		elif item[-2:] == "-":
			item = item[:-2]
			termo = ""
		else:
			termo = ""
		if len(item) == 5 or len(item) == 6:
			if ((item[:4].isalpha() or item[:4] == "B3SA") and item[4-len(item):].isnumeric()) or item == "ENMA3B":
				return termo + item
	return "ERRO: " + CD_ATIVO

#external
def summarize_eqt_pos():

	df_CVM_4 = pd.read_csv("db_funds_tracker/summarize/CVM_DB_4.csv")
	df_CVM_4 = df_CVM_4[(df_CVM_4.TP_APLIC == 'Ações')]
	df_CVM_4 = df_CVM_4[['CNPJ_FUNDO', 'DT_COMPTC', 'QT_POS_FINAL','VL_MERC_POS_FINAL', 'CD_ATIVO']]

	df_CVM_8 = pd.read_csv("db_funds_tracker/summarize/CVM_DB_8.csv")
	df_CVM_8 = df_CVM_8[(df_CVM_8.TP_APLIC == 'Ações')]
	df_CVM_8 = df_CVM_8[['CNPJ_FUNDO', 'DT_COMPTC', 'QT_POS_FINAL','VL_MERC_POS_FINAL', 'DS_ATIVO']]
	df_CVM_8.rename(columns = {'DS_ATIVO':'CD_ATIVO'}, inplace=True)

	df_DB_Fundos = pd.concat([df_CVM_4, df_CVM_8])

	for i in range(0, df_DB_Fundos.shape[0]):
		if df_DB_Fundos['CD_ATIVO'].isna().iloc[i] == True:
			df_DB_Fundos['CD_ATIVO'].iloc[i] = 'XXXX' + str(i)

	df_DB_Fundos['QT_POS_FINAL'].fillna(value=0, inplace=True)

	df_DB_Fundos = df_DB_Fundos.groupby(['CNPJ_FUNDO', 'DT_COMPTC', 'CD_ATIVO'], as_index = False).agg({"QT_POS_FINAL": "sum", "VL_MERC_POS_FINAL": 'sum'})

	df_funds_list = pd.read_csv("db_funds_tracker/input/funds_list.csv",encoding='ISO-8859-1', names = ['CNPJ_FUNDO', 'NOME_FUNDO', 'NOME_GESTOR'])
	df_DB_PLs = pd.read_csv('db_funds_tracker/summarize/CVM_DB_0.csv', encoding='ISO-8859-1')


	df_DB_Fundos = pd.merge(df_DB_Fundos, df_funds_list, on = 'CNPJ_FUNDO', how='left')
	df_DB_PLs = df_DB_PLs[['CNPJ_FUNDO', 'DT_COMPTC', 'VL_PATRIM_LIQ']]

	array_CD_ATIVO = df_DB_Fundos['CD_ATIVO'].unique()
	array_DT_COMPTC = df_DB_Fundos['DT_COMPTC'].unique()
	array_NOME_GESTOR = df_funds_list['NOME_GESTOR'].unique()

	df_DB_Fundos['CD_ATIVO'] = df_DB_Fundos['CD_ATIVO'].apply(identify_ticker)

	df_DB_Fundos = pd.merge(df_DB_Fundos, df_DB_PLs, on=['CNPJ_FUNDO', 'DT_COMPTC'], how='left')

	array_CD_ATIVO = df_DB_Fundos['CD_ATIVO'].unique()

	for atv in array_CD_ATIVO:
		if atv[:5]=='ERRO:':
			print("Deleting -> "+atv)
			df_DB_Fundos = df_DB_Fundos[df_DB_Fundos['CD_ATIVO'] != atv]

	array_CD_ATIVO = df_DB_Fundos['CD_ATIVO'].unique()
	arrays = [array_DT_COMPTC, array_NOME_GESTOR, array_CD_ATIVO]

	df_aux = pd.DataFrame(list(itertools.product(*arrays)), columns = ['DT_COMPTC', 'NOME_GESTOR', 'CD_ATIVO'])

	df_DB_PLs = pd.merge(df_DB_PLs, df_funds_list, on='CNPJ_FUNDO', how='left')

	print(df_DB_Fundos.shape)

	def get_weight(row):
		if row['VL_PATRIM_LIQ']>0:
			return row['VL_MERC_POS_FINAL']/row['VL_PATRIM_LIQ']
		else:
			return 0

	df_DB_Fundos['%PL'] = df_DB_Fundos.apply(get_weight, axis=1)
	df_DB_Fundos['Price'] = -1

	df_DB_Fundos = df_DB_Fundos[['DT_COMPTC', 'NOME_GESTOR', 'NOME_FUNDO', 'CNPJ_FUNDO', 'CD_ATIVO', 'QT_POS_FINAL', 'VL_MERC_POS_FINAL', 'VL_PATRIM_LIQ', '%PL', 'Price']]

	df_DB_Gestoras = df_DB_Fundos.groupby(['DT_COMPTC', 'NOME_GESTOR', 'CD_ATIVO'], as_index=False).agg({'QT_POS_FINAL':'sum', 'VL_MERC_POS_FINAL':'sum'})
	df_DB_Gestoras = pd.merge(df_aux, df_DB_Gestoras, on=['DT_COMPTC', 'NOME_GESTOR', 'CD_ATIVO'], how='left')
	df_DB_Gest_PLs = df_DB_PLs.groupby(['DT_COMPTC', 'NOME_GESTOR'], as_index=False).agg({"VL_PATRIM_LIQ":'sum'})
	df_DB_Gestoras = pd.merge(df_DB_Gestoras, df_DB_Gest_PLs, on=['NOME_GESTOR', 'DT_COMPTC'], how='left')
	df_DB_Gestoras["%PL"] = df_DB_Gestoras.apply(lambda row: row['VL_MERC_POS_FINAL']/row['VL_PATRIM_LIQ'] if row['VL_PATRIM_LIQ']>0 else 0, axis=1)

	df_DB_Gestoras['QT_POS_FINAL'] = df_DB_Gestoras['QT_POS_FINAL'].fillna(0)
	df_DB_Gestoras['VL_MERC_POS_FINAL'] = df_DB_Gestoras['VL_MERC_POS_FINAL'].fillna(0)
	df_DB_Gestoras['%PL'] = df_DB_Gestoras['%PL'].fillna(0)
	df_DB_Gestoras['Price'] = -1

	df_DB_Gestoras = df_DB_Gestoras[['DT_COMPTC', 'NOME_GESTOR', 'CD_ATIVO', 'QT_POS_FINAL', 'VL_MERC_POS_FINAL', 'VL_PATRIM_LIQ', '%PL', 'Price']]
	df_DB_PLs = df_DB_PLs[['CNPJ_FUNDO', 'NOME_FUNDO', 'NOME_GESTOR', 'DT_COMPTC', 'VL_PATRIM_LIQ']]

	array_DB_Ativos = df_DB_Fundos['CD_ATIVO'].unique()
	array_DB_Ativos.sort()		
	df_DB_Ativos = pd.DataFrame()
	df_DB_Ativos['CD_ATIVO'] = array_DB_Ativos

	df_DB_Datas = pd.DataFrame()
	array_DT_COMPTC.sort()
	df_DB_Datas['DT_COMPTC'] = array_DT_COMPTC

	df_DB_Fundos['DT_COMPTC'] = df_DB_Fundos['DT_COMPTC'].astype('datetime64[ns]')
	df_DB_Gestoras['DT_COMPTC'] = df_DB_Gestoras['DT_COMPTC'].astype('datetime64[ns]')
	df_DB_PLs['DT_COMPTC'] = df_DB_PLs['DT_COMPTC'].astype('datetime64[ns]')
	df_DB_Datas['DT_COMPTC'] = df_DB_Datas['DT_COMPTC'].astype('datetime64[ns]')

	try:
		df_DB_Fundos.to_csv("db_funds_tracker/summarize/DB_Fundos.csv")
		print('DB_Fundos.csv was succesfully saved!')
	except:
		print("Error to create DB_Fundos.csv!")

	try:
		df_DB_Gestoras.to_csv("db_funds_tracker/summarize/DB_Gestoras.csv")
		print('DB_Fundos.csv was succesfully saved!')
	except:
		print("Error to create DB_Gestoras.csv!")

	try:
		df_DB_PLs.to_csv("db_funds_tracker/summarize/DB_PLs.csv")
		print('DB_PLs.csv was succesfully saved!')
	except:
		print("Error to create DB_PLs.csv!")

	try:
		df_DB_Ativos.to_csv("db_funds_tracker/summarize/DB_Ativos.csv")
		print('df_DB_Ativos.csv was succesfully saved!')
	except:
		print("Error to create DB_Ativos.csv!")

	try:
		df_DB_Datas.to_csv("db_funds_tracker/summarize/DB_Datas.csv")
		print('DB_Datas.csv was succesfully saved!')
	except:
		print("Error to create DB_Datas.csv!")

#EXTERNAL
def update(yr_i = 2005, yr_f = 2019, m_f=12):
	path = os.path.dirname(os.path.abspath(__file__))
	for r, d, f in os.walk(path + '/db_funds_tracker/'):
		for file in f:
			if file[:7] == 'cda_fi_':
				if os.path.exists('db_funds_tracker/' + file):
					os.remove('db_funds_tracker/' + file)

	for yr in range(yr_i, yr_f+1):
		if yr == yr_f:
			update_yr(yr, m_f)
		else:
			update_yr(yr, 12)

		for r, d, f in os.walk(path):
			for file in f:
				if file[:10] == 'cda_fi_PL_':
					os.rename("db_funds_tracker/cda_fi_PL_"+file[10:], 'db_funds_tracker/cda_fi_BLC_0_'+file[10:])

#INTERNO
def update_yr(yr, m_f):

	if yr < 2018:
		print('Downloading ' + str(yr) + ' CVM CDA databases...')
		download_zip('http://dados.cvm.gov.br/dados/FI/DOC/CDA/DADOS/HIST/cda_fi_'+str(yr)+'.zip')
	else:
		for m in range(1, m_f+1):
			print("Downloading "+str(yr)+' CVM CDA databases...')
			download_zip('http://dados.cvm.gov.br/dados/FI/DOC/CDA/DADOS/cda_fi_'+str(yr)+'{:02d}'.format(m)+'.zip')
	print('\nDatabases successfully updated!\n')

#INTERNO
def download_zip(link):
	url = urlopen(link)
	with ZipFile(BytesIO(url.read())) as my_zip_file:
		my_zip_file.extractall('db_funds_tracker')
#EXTERNO
def summarize(yr_i=2005, yr_f=2019, m_f=12):
	for db in range(9):
		cvm_db=[]
		for yr in range(yr_i, yr_f+1):
			if yr == yr_i and yr != yr_f:
				cvm_db = cvm_db + summarize_db_yr(db, yr, 12)
			elif yr == yr_i and yr == yr_f:
				cvm_db = cvm_db + summarize_db_yr(db, yr, m_f)
			elif yr == yr_f:
				cvm_db = cvm_db + summarize_db_yr(db, yr, m_f)[1:]
			else:
				cvm_db = cvm_db + summarize_db_yr(db, yr, 12)[1:]

		with open('db_funds_tracker/summarize/CVM_DB_'+str(db)+'.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerows(cvm_db)
			print('\nCVM_DB_'+str(db)+'.csv was sucessfuly saved!\n')
#interno
def summarize_db_yr(db, yr, m_f):
	with open('db_funds_tracker/input/funds_list.csv', encoding='ISO-8859-1') as funds_file:
		funds_list = csv.reader(funds_file, delimiter=',')
		cnpj_list=[]
		for fund in funds_list:
			cnpj_list.append(fund[0])
	cvm_db=[]
	if yr < 2018:
		print("Summarizing CVM #"+str(db)+" database from "+ str(yr) + '...')
		try:
			with open('db_funds_tracker/cda_fi_BLC_'+str(db)+'_'+str(yr)+'.csv', encoding='ISO-8859-1') as cvm_file:
				cvm_csv = csv.reader(cvm_file, delimiter=';')
				cvm_db.append(next(cvm_csv, None))
				for cvm_data in cvm_csv:
					if cvm_data[1] in cnpj_list:
						cvm_db.append(cvm_data)
		except:
			print("File does not exists!")

	else:
		for m in range(1, m_f+1):
			print("Summarizing CVM # "+str(db)+' database from '+str(yr)+'/'+'{:02d}'.format(m) + '...')
			try:
				with open('db_funds_tracker/cda_fi_BLC_'+str(db)+'_'+str(yr)+'{:02d}'.format(m)+'.csv', encoding='ISO-8859-1') as cvm_file:
					cvm_csv = csv.reader(cvm_file, delimiter=';')
					if m == 1:
						cvm_db.append(next(cvm_csv, None))
					for cvm_data in cvm_csv:
						if cvm_data[1] in cnpj_list:
							cvm_db.append(cvm_data)
			except:
				print(' File does not exists!')

	print("    Appended " + str(len(cvm_db)) + ' lines')
	return cvm_db

# externo
def update_INF(yr_i=2005, yr_f=2019, m_f=12):
	path = os.path.dirname(os.path.abspath(__file__))
	for r, d, f in os.walk(path+'/db_funds_tracker/'):
		for file in f:
			if file[:4] == 'inf_':
				if os.path.exists('db_funds_tracker/'+file):
					os.remove('db_funds_tracker/'+file)
	for yr in range(yr_i, yr_f+1):
		if yr == yr_f:
			update_INF_yr(yr, m_f)
		else:
			update_INF_yr(yr, 12)
#interno
def update_INF_yr(yr, m_f):
	if yr < 2017:
		print("Downloading "+str(yr)+ ' CVM INF databases...')
		download_zip('http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/HIST/inf_diario_fi_'+str(yr)+'.zip')
	else:
		for m in range(1, m_f+1):
			print("Downloading "+str(yr)+"/"+'{:02d}'.format(m)+' CVM INF databases...')
			urllib.request.urlretrieve('http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_'
				+str(yr)+'{:02d}'.format(m) + ".csv", 'db_funds_tracker/inf_diario_fi_'+str(yr)+'{:02d}'.format(m)+'.csv')
	print("\n Databases succesfully updated!\n")

#EXTERNO
def summarize_INF():

	with open('db_funds_tracker/input/funds_list.csv', encoding='ISO-8859-1') as funds_file:
		funds_list = csv.reader(funds_file, delimiter=',')
		cnpj_list = []
		for fund in funds_list:
			cnpj_list.append(fund[0])

	mypath='db_funds_tracker/'
	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	inf_diario_files = []
	for file in files:
	    if 'inf_diario_fi_' in file:
	        inf_diario_files.append(file)

	df_final = pd.DataFrame()
	for file in inf_diario_files:
	    df = pd.read_csv('db_funds_tracker/'+file, sep=';', parse_dates=['DT_COMPTC'])
	    df = df[df['CNPJ_FUNDO'].isin(cnpj_list)]
	    df_final = df_final.append(df)
	df_final = df_final.sort_values(by='DT_COMPTC', ascending=True)

	df_final.to_csv("db_funds_tracker/summarize/CVM_INF_DIARIO.csv", index=False)

	print('\nCVM_INF_DIARIO.csv was succesfully saved!\n')











