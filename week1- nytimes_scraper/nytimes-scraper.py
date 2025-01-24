import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

#getting information from NY Times Website
url = "https://nytimes.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')



#retrieving all relevant article links
links = soup.find_all('a', class_ = 'css-9mylee')

#initiating array 
article_array = []

#looking into every news link
for link in links:

    #retrieving text/headlines
    news_article = []
    news_article =link.find_all('p', class_=lambda x: x and (x.startswith('indicate-hover') or x.startswith('summary-class')))
    for i in range(len(news_article)):
        news_article[i] = news_article[i].text.strip()


    #filling in missing data
    if len(news_article) == 1:
        news_article.append(None)

    #articles without text and headline are discarded
    elif len(news_article) == 0:
        continue

    #appending link and date to data
    news_article.append(link.get('href'))
    news_article.append(datetime.now())
    article_array.append(news_article)



#I tried to scrape the news paper articles too, but run into captcha

# article_content = []
# for article in article_array:
#     response_article = requests.get(article[2])
#     soup_article = BeautifulSoup(response_article.content, 'html.parser')
#     paragraph_article = soup_article.find_all('p', class_= "css-at9mc1 evys1bk0")
#     article_content.append(news_article.text.strip()

#creating dataframe and save it as csv-file
news_df = pd.DataFrame(article_array)
news_df.columns=['Header','Subtitle','Link','Date']
news_df
news_df.to_csv('nytimes_articles.csv', mode = 'a', header = False, index = False)