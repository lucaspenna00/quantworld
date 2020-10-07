import yahooquery as yf
import pandas as pd
import time 
import numpy as np

ativos = pd.read_csv("lista_tickers_b3.csv")
ativos = ativos['ticker'].unique()

ativos_aux = []
free_float = []

for ativo in ativos:

	print(ativo)

	try:

		aux1 = yf.Ticker(ativo+".SA")

		free_float.append(aux1.key_stats[ativo+".SA"]['floatShares'])

	except:

		print("Erro")

		free_float.append(np.nan)

	ativos_aux.append(ativo)

	time.sleep(5)

final_ff = pd.DataFrame()
final_ff['ticker'] = ativos_aux
final_ff['freefloat'] = free_float

final_ff.to_csv("free_floats.csv")





