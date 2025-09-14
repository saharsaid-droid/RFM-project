import pandas as pd
import numpy as np 
from datetime import datetime
import matplotlib.pyplot as plt


import plotly.graph_objects as go

import seaborn as sns

dataset = pd.read_csv("C:/Users/dell/Downloads/50000 Sales Records.csv")
df = pd.DataFrame(dataset)
print(df.head())

print(df.shape)
df.info()

#order_date'  => convert to date time to use to recency
#Total Revenue => use to manotry 
#frequency => order_id'

print(df.duplicated().any())



df["Order Date"] = pd.to_datetime(df['Order Date'], format="%m/%d/%Y")
# print(df.head())
present_time = datetime.now()
print(present_time)





rfm = df.groupby("Order ID").agg({"Order Date":lambda date :(present_time- date.max()).days,
                                  "Order ID": lambda num : len(num),
                                  "Total Revenue" : lambda price : price.sum()})

# print(rfm.head())


rfm.columns = ["Recency", "Frequency", "Monetary"]
# rfm.info()
print(rfm.nunique())




rfm['r_quartile'] = pd.qcut(rfm['Recency'], 4, labels=['4', '3', '2', '1'], duplicates='drop')
rfm['f_quartile'] = pd.qcut(rfm['Frequency'], 1, labels=[ '1'], duplicates='drop')
rfm['m_quartile'] = pd.qcut(rfm['Monetary'], 4, labels=['4', '3', '2', '1'], duplicates='drop')
print(rfm.head())

rfm["RFM_Score"] = rfm.r_quartile.astype(str) + rfm.f_quartile.astype(str) +rfm.m_quartile.astype(str)
print(rfm.head())

rfm[rfm['RFM_Score']=='111'].sort_values('Monetary',ascending=False).head()
rfm["RFM_Score"] = rfm['RFM_Score'].astype(int)
segment_labels = ['High-Value', 'Mid-Value','Low-Value']
rfm['Value_Segment'] = pd.qcut(rfm['RFM_Score'], q=3, labels=segment_labels)
print(rfm.head())



plt.figure(figsize=(10, 6)) # Set the figure size
ax = rfm.Value_Segment.value_counts().sort_values().plot(kind='bar', color=sns.color_palette("pastel"))
ax.set_title('Value Segment Distribution', fontsize=16) 
ax.set_xlabel('Value Segment', fontsize=14)
ax.set_ylabel('Count', fontsize=14)
ax.grid(axis='y', linestyle='--', alpha=0.7)
 
for p in ax.patches:
   ax.annotate(f'{int(p.get_height())}',
      (p.get_x() + p.get_width() / 2., p.get_height()),
      ha='center', va='bottom', fontsize=12)
 # Show the plot
plt.show()


segment_scores = rfm.groupby('Value_Segment')[['Recency', 'Frequency','Monetary']].mean().reset_index()
 # Create a grouped bar chart to compare segment scores
fig = go.Figure()
 # Add bars for Recency score
fig.add_trace(go.Bar(x=segment_scores['Value_Segment'],
 y=segment_scores['Recency'],
 name='Recency Score',
 marker_color='rgb(158,202,225)'
 ))
 # Add bars for Frequency score
fig.add_trace(go.Bar(x=segment_scores['Value_Segment'],
 y=segment_scores['Frequency'],
 name='Frequency Score',
 marker_color='rgb(94,158,217)'
))


# Add bars for Monetary score
fig.add_trace(go.Bar(
 x=segment_scores['Value_Segment'],
 y=segment_scores['Monetary'],
 name='Monetary Score',
 marker_color='rgb(32,102,148)'
 ))
 # Update the layout
fig.update_layout(
title='Comparison of RFM Segments based on Recency, Frequency, and MonetaryScores',
 xaxis_title='RFM Segments',
 yaxis_title='Score',
 barmode='group',
 showlegend=True
 )
 # Show the plot
fig.show()








