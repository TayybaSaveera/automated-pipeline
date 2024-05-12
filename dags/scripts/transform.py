def clean_news_data(articles):
    """Cleans text data in articles for processing."""
    cleaned_data = []
    for article in articles:
        cleaned_data.append({
            'title': article['title'].replace('!', ''),
            'url': article['link'],
            'summary': article['description'].replace(';', ',')
        })
    return cleaned_data
