import requests
from bs4 import BeautifulSoup as bs, Comment
import pandas as pd

# URL of the webpage
url = 'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats'

# Send request and get the page content
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'})
soup = bs(r.content, 'html.parser')

# Labels to delete
labels_to_delete = [
    ['Rk', 'G+A', 'PK', 'PKatt', 'npxG+xAG', 'Matches'],
    ['Rk', 'MP', 'Starts', 'Min', 'Matches'],
    [],
    ['Rk', 'Matches'],
    ['Rk', 'Matches'],
    ['Rk', 'Att', 'Matches'],
    ['Rk', 'Matches'],
    ['Rk', 'Matches'],
    ['Rk', 'Matches'],
    ['Rk', 'MP', 'Min', 'Mn/MP', 'Min%', 'Matches', '+/-', '+/-90', 'On-Off'],
    ['Rk', 'CrdY', 'CrdR', '2CrdY', 'Int', 'TklW', 'PKwon', 'PKcon', 'Matches']
]

# Gather links
data = []
for item in soup.find('p', class_='listhead').find_next('ul').find_all('li'):
    title = item.text.strip()
    link = 'https://fbref.com' + item.find('a')['href']
    data.append({'title': title, 'link': link})

# Function to fetch comments from URL
def get_url(url):
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    return comments

# Function to extract table data
def get_info(comments, columns_to_delete):
    table = None
    for comment in comments:
        if 'table_container' in comment:
            table = bs(comment, 'html.parser')

    if table:
        if_table = table.find('table', {'class': 'stats_table'})

        headers_list = []
        headers = if_table.find_all('tr', attrs={'class': 'thead'})

        for header in headers:
            cols = header.find_all('th')
            for col in cols:
                headers_list.append(col.text.strip())
            break

        rows = []
        for row in if_table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                if 'data-stat' in th.attrs:
                    value = th.text.strip() 
                try:
                    # Kiểm tra xem giá trị có chứa dấu phẩy hay không và chuyển đổi
                    if ',' in value:
                        value = float(value.replace(',', '.'))*1000 # Chuyển đổi thành float
                    else:
                        value = int(value) if value.isdigit() else float(value)  # Chuyển đổi thành int hoặc float
                except ValueError:
                    # Nếu không thể chuyển đổi, giữ lại giá trị gốc
                    pass
                    if value == '':
                        value = 0
                row_data.append(value)

            if len(row_data) == len(headers_list) and row_data != headers_list:
                rows.append(row_data)

        df = pd.DataFrame(rows, columns=headers_list)
        
        # Keep only the last 3 characters in 'Nation' for country codes
        if 'Nation' in df.columns:
            df['Nation'] = df['Nation'].str[-3:]

        # Remove unnecessary columns
        df = df.drop(columns=[col for col in columns_to_delete if col in df.columns])

        return df

# Get tables and remove unnecessary columns
dataframes = [get_info(get_url(data[i]['link']), labels_to_delete[i]) for i in range(len(data)) if i != 2]

df = dataframes[0]

for data_frame in dataframes[1:]:
    df = pd.merge(df, data_frame, on=['Player', 'Nation', 'Pos' , 'Squad', 'Age', '90s', 'Born'], how='outer')


df = df[df['90s'] >= 1]  

df = df.sort_values(by=['Player', 'Age'], ascending=[True, False])

df.to_csv('results.csv', sep=';', index=False)

