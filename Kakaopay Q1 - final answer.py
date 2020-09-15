#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib
import seaborn as sns
from scipy import stats
import numpy as np

# TO DO:
# 1. '더치페이 요청에 때한 응답률이 높을수록 더치페이 서비스를 더 많이 사용한다' 통계적 검정
# 가정: '요청 응답률'이란, 더치페이 요청 수신자가 받은 모든 요청건 대비 status가 sent (송금완료) 또는 check (송금 후 요청자 확인완료) 상태인 요청 비율을 말한다


# In[2]:


#upload data
data = pd.read_csv('dutchpay_claim_detail.csv')
data.head()


# In[3]:


data.describe()


# In[4]:


data[data['claim_amount']==0].head()


# In[5]:


#0원 송금 요청에 대해 수신자가 응답할 필요가 없다고 판단하여, 요청 응답률 계산에서 제외했습니다
data = data[data['claim_amount']>0]
data.describe()


# In[6]:


# status가 CLAIM이 아닌 요청건들을 '성공'으로 정의했습니다
# 이걸 요청 받은 유저가 받은 모든 요청건과 비교해서 '응답률'을 계산합니다
claims_per_receiver = data.groupby('recv_user_id')['claim_id'].nunique()
success_per_receiver = data[data['status']!='CLAIM'].groupby('recv_user_id')['claim_id'].nunique()
receiver_data = pd.merge(claims_per_receiver, success_per_receiver, on='recv_user_id', how='left', suffixes=('_all', '_success'))
receiver_data.head(10)


# In[7]:


receiver_data = receiver_data.fillna(0)
receiver_data['response_rate'] = 100.0*receiver_data['claim_id_success']/receiver_data['claim_id_all']
receiver_data.index.names = ['user_id']
receiver_data.head(10)


# In[8]:


receiver_data.describe()


# In[9]:


# 이제 요청 받은 유저들이 더치페이 요청 이력이 얼마나 있는지를 알아봅니다
claimer_data = pd.read_csv('dutchpay_claim.csv')
claimer_data.head()


# In[11]:


# claims 데이터에서 요청 유저별로 group해서 유저당 요청건을 산출합니다
claims_per_user = claimer_data.groupby('claim_user_id').claim_id.nunique()
claims_per_user.index.names = ['user_id']
df = pd.merge(receiver_data, claims_per_user, on='user_id', how='left')
df


# In[12]:


df = df.fillna(0)


# In[16]:


# 응답률과 요청건간의 상관관계 계수(correlation coefficient)를 계산합니다
a = np.array(df['response_rate'])
b = np.array(df['claim_id'])
r = np.corrcoef(a, b)
r


# In[ ]:


# 상관관계 계수가 0.26임으로 매우 약한 상관관계에 속합니다

