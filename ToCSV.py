#%%
from bs4 import BeautifulSoup
import requests
import re
import sys
import os 
import calendar;
import time;
ts = calendar.timegm(time.gmtime())

def main(path):
    # obtain html from website to txt
    url='https://3g.dxy.cn/newh5/view/pneumonia'
    response=requests.get(url)
    response.encoding = "UTF-8"
    soup = BeautifulSoup(response.text,'lxml')
    target = soup.find(id="getAreaStat").text

    file = open(str(ts)+".txt","w")
    file.write(target)
    file.close()

    provinceShortNamepot=[]
    confirmedCountpot=[]
    suspectedCountpot=[]
    curedCountpot=[]
    deadCountpot=[]
    commentpot=[]
    citiespot=[]
    cityNamepot=[]

    # read from txt file
    f = open(path+str(ts)+".txt", "r")
    raw = f.read()

    r = re.finditer('provinceShortName',raw)
    for i in r:
        provinceShortNamepot.append(i.span())
    r = re.finditer('confirmedCount',raw)
    for i in r:
        confirmedCountpot.append(i.span())
    r = re.finditer('suspectedCount',raw)
    for i in r:
        suspectedCountpot.append(i.span())
    r = re.finditer('curedCount',raw)
    for i in r:
        curedCountpot.append(i.span())
    r = re.finditer('deadCount',raw)
    for i in r:
        deadCountpot.append(i.span())
    r = re.finditer('cityName',raw)
    for i in r:
        cityNamepot.append(i.span())
    r = re.finditer('cities',raw)
    for i in r:
        citiespot.append(i.span())

    # 用类的坐标找开始和结束符的位置并算出长度
    # for province
    provinceShortName=[]
    # province & cities
    confirmedCount=[]
    # province & cities
    suspectedCount=[]
    # province & cities
    curedCount=[]
    # province & cities
    deadCount=[]
    # for cities
    cityName=[]
    cities=[]

    char_cities_start='['
    char_cities_end=']'
    char_start=':'
    char_end=','

    for pot in provinceShortNamepot:
        startPos=raw[pot[1]:].find(char_start)
        endPos=raw[pot[1]:].find(char_end)
        provinceShortName.append(raw[pot[1]+startPos+2:pot[1]+endPos-1])
    for pot in confirmedCountpot:
        startPos=raw[pot[1]:].find(char_start)
        endPos=raw[pot[1]:].find(char_end)
        confirmedCount.append(raw[pot[1]+startPos+1:pot[1]+endPos])
    for pot in suspectedCountpot:
        startPos=raw[pot[1]:].find(char_start)
        endPos=raw[pot[1]:].find(char_end)
        suspectedCount.append(raw[pot[1]+startPos+1:pot[1]+endPos])
    for pot in curedCountpot:
        startPos=raw[pot[1]:].find(char_start)
        endPos=raw[pot[1]:].find(char_end)
        curedCount.append(raw[pot[1]+startPos+1:pot[1]+endPos])
    for pot in deadCountpot:
        startPos=raw[pot[1]:].find(char_start)
        endPos=raw[pot[1]:].find(char_end)
        deadCount.append(raw[pot[1]+startPos+1:pot[1]+endPos])
    for pot in cityNamepot:
        startPos=raw[pot[1]:].find(char_start)
        endPos=raw[pot[1]:].find(char_end)
        cityName.append(raw[pot[1]+startPos+1:pot[1]+endPos])
    for pot in citiespot:
        startPos=raw[pot[1]:].find(char_cities_start)
        endPos=raw[pot[1]:].find(char_cities_end)
        cities.append(raw[pot[1]+startPos:pot[1]+endPos])

    #记录各省有几个城市
    CitiesOfProvince=[]
    for province in cities:
        CitiesOfProvince.append(province.count('cityName'))
    #把相应的城市按顺序与省排在一起
    ProvinceName=[]
    for i in range(len(provinceShortName)):
        ProvinceName.append(provinceShortName[i])
        if CitiesOfProvince[i] != 0:
            for city in range(CitiesOfProvince[i]):
                ProvinceName.append(cityName[city])
            for city in range(CitiesOfProvince[i]):
                del cityName[0]

    # 写入CSV
    from pandas import DataFrame
    deadCount = [re.sub("\D", "", file) for file in deadCount]
    virus = {'Province&City': ProvinceName,
            'Confirmed':confirmedCount,
            'Suspected':suspectedCount,
            'Cured':curedCount,
            'Dead':deadCount
            }
    df = DataFrame(virus, columns= ['Province&City','Confirmed','Suspected','Cured','Dead'])
    export_csv = df.to_csv (r''+path+str(ts)+'.csv', index = None, header=True, encoding='utf-8-sig')

path="C:/Users/Administrator/Desktop/WuHan_19nCov-master/"
main(path)


# %%
