import collections
from kakao import overlapped_data,make_map,get_menu
from tqdm import tqdm
import pandas as pd
import numpy as np

loc_x , loc_y = 126.898242, 37.530774
keyword = '음식점'
# 시작 좌표
start_x = 126.891
start_y = 37.529
next_x = 0.001
next_y = 0.001
num_x = 14
num_y = 8
print("검색 시작")
overlapped_result = overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y)
print("검색 종료")
# 중복 제거
results = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in overlapped_result)))
X = []
Y = []
stores = []
road_address = []
place_url = []
ID = []
category = []
for place in results:
    X.append(float(place['x']))
    Y.append(float(place['y']))
    stores.append(place['place_name'])
    road_address.append(place['road_address_name'])
    place_url.append(place['place_url'])
    ID.append(place['id'])
    category.append(place['category_name'])
    ar = np.array([ID, stores, X, Y, category,road_address, place_url]).T
    df = pd.DataFrame(ar, columns=['ID', 'stores', 'X', 'Y','category', 'road_address', 'place_url'])
print('total_reuslt_number = ', len(df))
print("메뉴가져오기 시작")
menus = get_menu(ID)
print("메뉴가져오기 종료")
#make_map(df,loc_y,loc_x)
df.to_excel("./menu.xlsx")