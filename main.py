from newsapi import NewsApiClient
import newspaper
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import time
#from twilio.rest import Client
import keys
#Download all neccasary


#My API key
api_key = '7ed8a560a327445692c65686accbbfc0'
newsapi = NewsApiClient(api_key=api_key)

# This gets a list of the top headlines
def get_top_headlines(country='us', category='general', num_articles=1):
    top_headlines = newsapi.get_top_headlines(country=country, category=category, page_size=num_articles)
    articles = top_headlines['articles']
    print('Number of articles', len(articles))
    return articles

#This prints an entire article
def print_full_article(title, url):
    print(f"\nTitle: {title}")
    print("\nFull Article Content:")

    try:
        article = newspaper.Article(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        article.download()
        #time.sleep(2)  # Add a delay of 2 seconds
        article.parse()
        full_content = article.text
        print(full_content)
    except newspaper.article.ArticleException as e:
        print(f"Error downloading article: {e}")


def get_full_article(title, url):

    article = newspaper.Article(url, headers={'User-Agent': 'your-user-agent-string'})
    article.download()
    #time.sleep(0.5)
    article.parse()
    full_content = article.text

    return full_content

def generate_summary(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  #Num sentances you want
    return " ".join([str(sentence) for sentence in summary])

def print_summary(articles):
     
     for article in articles:
        title = article['title']
        url = article['url']
        text = get_full_article(title, url)
        summary = generate_summary(text)
        print(summary)

def get_summary(articles):
     
     for article in articles:
        title = article['title']
        url = article['url']
        text = get_full_article(title, url)
        summary = generate_summary(text)
        return summary


def send_summary(articles):
     
     for article in articles:
        title = article['title']
        url = article['url']
        text = get_full_article(title, url)
        summary = generate_summary(text)
        send_message(summary)

def print_all_articles(articles):
     
     for article in articles:
        title = article['title']
        url = article['url']
        print_full_article(title, url)

def send_message(message_text):
    client = Client(keys.account_sid, keys.auth_token)
    message = client.messages.create(
        body = message_text,
        from_ = keys.twilio_number,
        to = keys.target_number
    )
    print("Message sent")


def main():
    country = 'ca'  # Change this to the desired country code
    category = 'general'  # Change this to the desired news category

    num_articles = 1  # Change this to the desired number of articles

    articles = get_top_headlines(country, category, num_articles)
    
    #print_summary(articles)

    #print_all_articles(articles)

    #send_summary(articles)
    
   
if __name__ == "__main__":
    main()
