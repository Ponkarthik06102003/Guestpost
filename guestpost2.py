import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_traffic_and_domain_authority(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    monthly_traffic = None
    for elem in soup.select('div.fr-command.fr-element.fr-view'):
        if 'Monthly traffic' in elem.text:
            monthly_traffic = elem.text.strip().replace('Monthly traffic:', '').strip()
            break

    domain_authority = None
    for elem in soup.select('div.fr-command.fr-element.fr-view'):
        if 'Domain Authority Score' in elem.text:
            domain_authority = elem.text.strip().replace('Domain Authority Score:', '').strip()
            break

    return monthly_traffic, domain_authority


def get_guest_posts(topic):
    search_url = f'https://www.google.com/search?q={topic} "write for us" -site:pinterest.* -site:linkedin.*'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    search_results = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(search_results.text, 'html.parser')
    guest_posts = []

    for g in soup.find_all('div', class_='g'):
        a = g.find('a')
        link = a['href']
        title = g.find('h3').text
        if 'write for us' in title.lower():
            try:
                res = requests.get(link)
                soup = BeautifulSoup(res.text, 'html.parser')
                guest_post_url = None
                for elem in soup.find_all('a', href=True):
                    if 'guest-post' in elem['href'] or 'write-for-us' in elem['href']:
                        guest_post_url = elem['href']
                        break
                monthly_traffic, domain_authority = get_traffic_and_domain_authority(link)
                if not monthly_traffic:
                    monthly_traffic = 'Not found'
                if not domain_authority:
                    domain_authority = 'Not found'
                guest_posts.append({
                    'Blog Site': title,
                    'Blog Guest Post Link': guest_post_url,
                    'Blog Monthly Traffic': monthly_traffic,
                    'Domain Authority Score': domain_authority
                })
            except:
                pass
    return guest_posts


def main():
    topic = input('Enter the topic to search for guest posts: ')
    guest_posts = get_guest_posts(topic)
    df = pd.DataFrame(guest_posts)
    df.to_excel('guest_posts.xlsx', index=False)
    print(f"Data saved in 'guest_posts.xlsx' file.")


if __name__ == '__main__':
    main()
