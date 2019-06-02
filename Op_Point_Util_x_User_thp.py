from sklearn.cluster import KMeans
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt

data1=pd.read_excel('Base_Dimensionamento_C1_decong..xlsx', sheet_name='Sheet1')

def op_point(f,b,bw): 
        
        Layer=data1[data1['Fornecedor'].isin([f])&data1['BW'].isin([bw])&data1['Banda'].isin([b])]
        Layer=Layer.reset_index(drop=True)
        if Layer.last_valid_index() < 100:
            n_clusters=Layer.last_valid_index()
        else:
            n_clusters=100
        clusData1 = Layer[['User Thp','Utilization']]
        kmeans1 = KMeans(n_clusters=n_clusters,random_state=0).fit(clusData1)
        df=pd.DataFrame(kmeans1.cluster_centers_,columns=(['User Thp','Utilization']))
        centroids=df.sort_values(by=['User Thp'])
        centroids[['Fornecedor','Banda','BW']]=Layer[['Fornecedor','Banda','BW']]
        return centroids
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
result.to_excel('OP_Points.xls',sheet_name='Sheet1',startrow=0)
