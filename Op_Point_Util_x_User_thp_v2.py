#from sklearn.cluster import KMeans
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt

data1=pd.read_excel('Base_Dimensionamento_C1_decong..xlsx', sheet_name='Sheet1')

def op_point(f,b,bw): 
        
        Layer=data1[data1['Fornecedor'].isin([f])&data1['BW'].isin([bw])&data1['Banda'].isin([b])]
        Layer=Layer.reset_index(drop=True)
        Mov_avg_input= Layer[['User Thp','Utilization']]
        Mov_avg_input=Mov_avg_input.sort_values(by=['Utilization'])
        Mov_avg_output=Mov_avg_input.rolling(window=15).mean().dropna()
        Mov_avg_output[['Fornecedor','Banda','BW']]=Layer[['Fornecedor','Banda','BW']]
        return Mov_avg_output

x=0
f_ser=Series(data1.Fornecedor.unique())
bw_ser=Series(data1.BW.unique())
b_ser=Series(data1.Banda.unique())
for i in f_ser.index:
    f=f_ser[i]
    for j in b_ser.index:
        b=b_ser[j]
        for k in bw_ser.index:
            bw=bw_ser[k]
            Layer=data1[data1['Fornecedor'].isin([f])&data1['BW'].isin([bw])&data1['Banda'].isin([b])]
            if Layer.count()[1]>0:
                a=op_point(f,b,bw)
                a.to_csv('file_{}.csv'.format(x))
                x=x+1
files=[]
for i in range(x):
    files.append('file_{}.csv'.format(i))
result = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
result_5M=result[np.logical_and(result['User Thp']>4500,result['User Thp']<5500)]
result_3M=result[np.logical_and(result['User Thp']>2700,result['User Thp']<3300)]
pivot_5m=result_5M.pivot_table(columns=['Fornecedor'],index=['Banda','BW'],values=['Utilization'])
pivot_3m=result_3M.pivot_table(columns=['Fornecedor'],index=['Banda','BW'],values=['Utilization'])
result.to_excel('OP_Points.xlsx',sheet_name='Sheet1',startrow=0)
pivot_3m.to_excel('OP_Points_3m.xlsx',sheet_name='Sheet1',startrow=0)
pivot_5m.to_excel('OP_Points_5m.xlsx',sheet_name='Sheet1',startrow=0)
