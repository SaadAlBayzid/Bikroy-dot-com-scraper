#Import necessary modules

from typing import Counter
from bs4 import BeautifulSoup
import requests
import csv
import warnings

#create new csv file to store data after scraping
file = open('phone_data.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
 
# write title of data
writer.writerow(['Phone Model','City','Price'])
headers = {'Accept-Language': 'en-US,en;q=0.8'}

#function to do the scraping
def scraper_bikroy_dot_com():
    for page_number in range(1,1000):#change range 
        source=requests.get('https://bikroy.com/en/ads/bangladesh/electronics?sort=date&order=desc&buy_now=0&urgent=0&page='+str(page_number),headers=headers).text
        soup=BeautifulSoup(source,'lxml')
        test=soup.find_all('a', attrs={'class':'card-link--3ssYv gtm-ad-item'})
                                                            
        for data in test:
            model=data.text.strip().split(')')
            city = data.find('div', {'class' : 'description--2-ez3'})
            city_clean= city.text.strip().split(',')
            price= data.find('div', {'class' : 'price--3SnqI color--t0tGX'})
            price_clean=price.text.strip().split(' ')
            count=0
            for name in model:
                    phone_model= name.strip().split('(')
                    if count%2 == 0 and len(price_clean)>1:
                        print(phone_model[0]+' could be purchased from city '+ city_clean[0].strip() + 'which costs ' + price_clean[1])
                        writer.writerow([phone_model[0], city_clean[0].strip(), price_clean[1]])
                        count+=1
                        
                    else:
                        continue

try:
    if __name__ == '__main__':
        scraper_bikroy_dot_com()
        
except:
    warnings.warn('Check the code again',stacklevel=2)