import pandas as pd
from sklearn.cluster import KMeans


data = pd.read_csv('results.csv')


features = ['Min', 'Age', 'Won%']


data = data.dropna(subset=features)

num_clusters = 3 
kmeans = KMeans(n_clusters=num_clusters, random_state=42)

X = data[features]
data['cluster'] = kmeans.fit_predict(X)

group_names = {
    0: 'Nhóm 1: Cầu thủ xuất sắc',
    1: 'Nhóm 2: Cầu thủ trung bình',
    2: 'Nhóm 3: Cầu thủ kém'
}

data['group_name'] = data['cluster'].map(group_names)

grouped_data = data.groupby('group_name')[features].mean().reset_index()

sorted_grouped_data = grouped_data.sort_values(by='goals', ascending=False)

data.to_csv('results3.csv', index=False)
sorted_grouped_data.to_csv('sorted_groups.csv', index=False)
