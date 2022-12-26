from django.shortcuts import render
import snowflake.connector
from transformers import pipeline
from snowflake.connector.pandas_tools import pd_writer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk
import pandas as pd
import json
import re
# import snowflake.connector as sl
# from cleantext import remove_emoji
import emoji

def extract_hash_tags(text):
   return list(set(re.findall(r"#(\w+)", str.lower(text))))


def extract_user(text):
   return list(set(re.findall(r"@(\w+)"), text))


def clean_tweet(content):
   clean_content = re.sub('#(\w+)', '', content)
   clean_content = re.sub('@(\w+)', '', clean_content)
   clean_content = re.sub('# (\w+)', '', clean_content)
   clean_content = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                          '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', clean_content)
   clean_content = re.sub('\n', '', clean_content)
   clean_content = str.strip(clean_content)

   clean_content = give_emoji_free_text(clean_content)

   return clean_content


def sentiment_analysis(tweetContent):
   sentiment = ''
   clean_content = clean_tweet(tweetContent)
   analysis = TextBlob(tweetContent)
   score = SentimentIntensityAnalyzer().polarity_scores(clean_content)
   neg = score['neg']
   neu = score['neu']
   pos = score['pos']
   comp = score['compound']

   if neg > pos:
      sentiment = 'negative'
   elif pos > neg:
      sentiment = 'positive'
   else:
      sentiment = 'neutral'

   return sentiment

def give_emoji_free_text(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.EMOJI_DATA]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text

def sentiment_analysis_pipeline(text):
   clean_text = clean_tweet(text)
   sentiment_pipeline = pipeline("sentiment-analysis")
   result = sentiment_pipeline(clean_text)
   sentiment = str.lower(result[0]['label'])
   score = result[0]['score']
   return sentiment

def index(request):
    if request.method == "POST":
      # topic = request.POST["topic"]
      # ctx = snowflake.connector.connect(
      #    user='hoangnb2501',
      #    password='Hoang2501',
      #    account='jq26585.southeast-asia.azure',
      #    warehouse='WH1',
      #    database='TWITTER',
      #    schema='PUBLIC'
      # )
      # nltk.download('vader_lexicon')
      # cur = ctx.cursor()
      # sql = f"select TWEETID, CONTENT, SENTIMENT from TWITTER_TEST_2 where SENTIMENT is null and topic = '{topic}';"
      # tweets = cur.execute(sql).fetchall()
      # for i, t in enumerate(tweets):
      #    sentiment = sentiment_analysis(t[1])
      #    updatedSql = f"update TWITTER_TEST_2 set SENTIMENT = '{sentiment}' where TWEETID = '{t[0]}'"
      #    cur.execute(updatedSql)
      # params = {'places_data': "Phan lop thanh cong"}
      return render(request, "index.html", {})
    return render(request, 'home.html')
   
