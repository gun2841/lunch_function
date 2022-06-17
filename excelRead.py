import pandas as pd
filename ='./menu.xlsx'

df = pd.read_excel(filename, sheet_name="Sheet1",engine='openpyxl')

for i,row in df.iterrows():
    print(row)