#%%
from bs4 import BeautifulSoup
import re

# https://3g.dxy.cn/newh5/view/pneumonia
path = 'C:/Users/Administrator/Desktop/2019/datasource.html'
htmlfile = open(path, 'r', encoding='utf-8')
htmlhandle  = htmlfile.read()
#print(htmlpage)
soup = BeautifulSoup(htmlhandle, 'lxml')



target = soup.find(id="getAreaStat")
with open("data.txt","w") as f:
        f.write(tagget.string)

# https://blog.csdn.net/y_silence_/article/details/79411618
province = re.findall(r"\bp\S*e\b", target.string)

if province:
    print(province)

else:
    print('not match')