import time
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import string

def scraper_live_hindustan(city,date_from,date_to):
    news_articles_root='https://www.livehindustan.com'
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    times = []
    start = False
    titles = []
    contents = []
    page = 1
    start_date = pd.to_datetime(date_from).date()
    end_date = pd.to_datetime(date_to).date()
    start = True
    while start:
        print(start)
        markup = requests.get(news_articles_root + '/uttar-pradesh/'+city+'/news-'+str(page),headers = agent).text
        soup = BeautifulSoup(markup, "lxml")
        links = soup.find_all('h4',{'class':'hindustan-link'})
        dates = soup.find_all('div',{'class':'list-time-tags tags-list'})

        for i in range(0,len(links)):
            news_link = links[i].find('a',href = True)['href'] 
            news_title = links[i].find('a',href = True)['title'].replace('\xa0',' ')
            news_date = dates[i].find('span').get_text()
            news_markup = requests.get(news_articles_root + news_link,headers = agent).text
            news_soup = BeautifulSoup(news_markup, "lxml")
            news_div_content = news_soup.find('div',{'class':'story-page-content'})
            news_content = news_div_content.get_text().replace('\xa0',' ')
            n = pd.to_datetime(news_date).date()

            if n < start_date:
                start = False
                break
            if n > end_date:
                continue

            times.append(news_date)
            titles.append(news_title)
            contents.append(news_content)
            print(news_date)
        page+=1
    print('Out')
    news = {'Time':times,'Title':titles,'Content':contents}
    df = pd.DataFrame(news,columns = ['Time','Title','Content'])

    time = df['Time']
    dates = []
    for i in time:
        date = pd.to_datetime(i).date()
        dates.append(date)
    df = df.drop(['Time'],axis = 1)
    content = df['Content']
    df = df.drop(['Content'],axis = 1)
    df['Headline'] = df['Title']
    df['Content'] = content
    df = df.drop(['Title'],axis = 1)
    df['Date'] = dates
    
    stopword = ['','[',']','-','"','?','अंदर','अत','अदि','अप','अपना','अपनि','अपनी','अपने','अभि','अभी','आदि','आप','इंहिं','इंहें','इंहों','इतयादि','इत्यादि','इन','इनका','इन्हीं','इन्हें','इन्हों','इस','इसका','इसकि','इसकी','इसके','इसमें','इसि','इसी','इसे','उंहिं','उंहें','उंहों','उन','उनका','उनकि','उनकी','उनके','उनको','उन्हीं','उन्हें','उन्हों','उस','उसके','उसि','उसी','उसे','एक','एवं','एस','एसे','ऐसे','ओर','और','कइ','कई','कर','करता','करते','करना','करने','करें','कहते','कहा','का','काफि','काफ़ी','कि','किंहें','किंहों','कितना','किन्हें','किन्हों','किया','किर','किस','किसि','किसी','किसे','की','कुछ','कुल','के','को','कोइ','कोई','कोन','कोनसा','कौन','कौनसा','गया','घर','जब','जहाँ','जहां','जा','जिंहें','जिंहों','जितना','जिधर','जिन','जिन्हें','जिन्हों','जिस','जिसे','जीधर','जेसा','जेसे','जैसा','जैसे','जो','तक','तब','तरह','तिंहें','तिंहों','तिन','तिन्हें','तिन्हों','तिस','तिसे','तो','था','थि','थी','थे','दबारा','दवारा','दिया','दुसरा','दुसरे','दूसरे','दो','द्वारा','न','नहिं','नहीं','ना','निचे','निहायत','नीचे','ने','पर','पहले','पुरा','पूरा','पे','फिर','बनि','बनी','बहि','बही','बहुत','बाद','बाला','बिलकुल','भि','भितर','भी','भीतर','मगर','मानो','मे','में','यदि','यह','यहाँ','यहां','यहि','यही','या','यिह','ये','रखें','रवासा','रहा','रहे','ऱ्वासा','लिए','लिये','लेकिन','व','वगेरह','वरग','वर्ग','वह','वहाँ','वहां','वहिं','वहीं','वाले','वुह','वे','वग़ैरह','संग','सकता','सकते','सबसे','सभि','सभी','साथ','साबुत','साभ','सारा','से','सो','हि','ही','हुअ','हुआ','हुइ','हुई','हुए','हे','हें','है','हैं','हो','होता','होति','होती','निकला','वालों','मैं','होते','पहुँचकर','गये','कराया', 'जाएगा','जाएगी','पहुंच','रहने','देखने','मिला','कहीं-कहीं','बता', 'दें','लाना','लोगों ','जिसमें','पाएंगे','यूं','आगे','मिलते','पहुंची','देखा', 'जिसमे','होना','कराने','लगाना', 'होगा','कराएं', 'होगा','देना','होगी','चाहता', 'उसकी','लगतार','अब','जाने', 'समझे','बताया', 'कहना','देखते', 'हुये','रही','पहुचा','रहेगी','होने','रह','आ','दे','वाला', 'मिल','रख','करा','चल','ले','ला', 'चाहिए','देखा।','गई','दी','उसने','देखें','लिया','लेकर','करेंगे','इनसे','पूरी','बिना','हर', 'आने-जाने','निकले','शुरू','देख','अन्य','लोग','देते','पहुंचे','लगाने','गए','उन्होंने']
    count=1
    for j in np.arange(0,len(df['Content'])):
        if(j!=3221 or j!=3400 or j!= 3457):
            df['Content'][j]=str(df['Content'][j])
            p=[]
            print(count)
            count=count+1
            df['Content'][j]=re.sub('[.,+,-,*,|,।,:,{,},\,/,<,>,$,&,(,),#,;,\u200d,\u200b,=,_]', ' ', df['Content'][j])
            df['Content'][j]=re.sub('[0-9]', ' ', df['Content'][j])
            df['Content'][j]=re.sub('[A-Z]', ' ', df['Content'][j])
            df['Content'][j]=re.sub('[a-z]', ' ', df['Content'][j])
            df['Content'][j]=df['Content'][j].replace("\n","")
            df['Content'][j]= df['Content'][j].split()
            for w in df['Content'][j]:
                if w not in stopword:
                    p.append(w)
                    df['Content'][j]= ' '.join(p)
                    df['Content'] = df['Content'].str.replace('[{}]'.format(string.punctuation), '')
                    df['Headline'] = df['Headline'].str.replace('[{}]'.format(string.punctuation), '')
                    df.to_csv(city.capitalize()+'_LiveHindustan.csv',index= False)
