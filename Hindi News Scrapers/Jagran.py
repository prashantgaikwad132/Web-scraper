#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import string


def request_url(link):
    response=requests.get(link)
    news=response.content
    soup=BeautifulSoup(news,'html5lib')
    return soup;



def scraper_jagran(districts,d1,d2):
    d1=pd.to_datetime(d1).date()
    d2=pd.to_datetime(d2).date()
    root_url="https://www.jagran.com/local/uttar-pradesh_"
    
    for i in districts:

        title_list=[]
        news_content=[]
        news_date=[]

        add_city=["agra","aligarh","allahabad","amroha","bareilly","gorakhpur","jhansi",
                      "kanpur","lucknow","meerut","moradabad","varanasi"]
        exceptions=["chandauli","ghaziabad","ghazipur","jaunpur","hathras","fatehpur","muzaffarnagar","noida","rampur","sitapur","sultanpur","azamgarh","unnao"]

        if i in add_city:
            i=i

        

        curr_page=1
        check=True
        first_date_found=False

        while(check):
            if i in exceptions:
                link=root_url+i+"-news-hindi-"+"page"+str(curr_page)+".html"
            else:
                link=root_url+i+"-city-news-hindi-"+"page"+str(curr_page)+".html"
            print(link)

            #request url
            soup=request_url(link)

            news=soup.find('ul',class_='topicList')
            link=news.find_all('a',href=True)   
            
            
            
            #0 to len-1
            for n in np.arange(0,len(link)):
                    

                temp="https://www.jagran.com"+link[n]['href']
                

                #request url for link of article
                print(str(n+1)+": "+temp)                
                soup_article=request_url(temp)

                #datetime
                datetime=soup_article.find_all('div', class_='dateInfo')
                
                only_date=datetime[1].get_text()[19:30] 
                d=pd.to_datetime(only_date).date()
                
                if(d<=d2 and d>=d1):
                    first_date_found=True
                    print("----Date Found-----",d)
                    news_date.append(d)

                    #title of the article
                    title=soup_article.find('h1').text
                    title_list.append(title)



                    body=soup_article.find('div', class_="articleBody")
                    p=body.find_all('p')

                    list_paragraph=[]
                    for m in np.arange(0,len(p)-2):
                        paragraph=p[m].text
                        list_paragraph.append(paragraph)
                        final_article=" ".join(list_paragraph)
                    news_content.append(final_article.strip())
                elif(first_date_found):
                    print("----Date not found: Termination----",d)
                    check=False
                    break
                else:
                    print("----Starting date not found----",d)

            curr_page=curr_page+1
            print("\n")


        df= pd.DataFrame({'Headline': title_list,'Content': news_content,'Date':news_date})
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
                        df.to_csv(i.capitalize()+'_Jagran.csv',index= False)