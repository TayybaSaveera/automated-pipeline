import requests
from bs4 import BeautifulSoup


def get_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
    except requests.RequestException as error:
        return {'error': str(error)}

    soup = BeautifulSoup(response.content, 'html.parser')
    news_list = []

    for link in soup.find_all('a', attrs={'data-testid': ['external-anchor', 'internal-link']}):
        headline = link.find('h2', attrs={'data-testid': 'card-headline'})
        description = link.find('p', attrs={'data-testid': 'card-description'})
        if headline and description:
            news_list.append({
                'title': headline.text.strip(),
                'summary': description.text.strip(),
                'url': link['href'] if link['href'].startswith('http') else 'https://www.bbc.com' + link['href']
            })

    return news_list


def display_news():
    target_url = 'https://www.bbc.com'
    news = get_news(target_url)
    if 'error' in news:
        print(f"Error retrieving data: {news['error']}")
    else:
        for item in news:
            print(item['title'], item['url'], item['summary'])


if __name__ == "__main__":
    display_news()
