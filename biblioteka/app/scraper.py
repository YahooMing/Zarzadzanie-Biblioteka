import requests
from bs4 import BeautifulSoup

def fetch_external_reviews(book_title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    search_url = f'https://lubimyczytac.pl/szukaj?phrase={book_title}'
    search_response = requests.get(search_url, headers=headers)

    if search_response.status_code != 200:
        print(f"Error fetching search page: {search_response.status_code}")
        return []

    search_soup = BeautifulSoup(search_response.content, 'html.parser')
    book_link = search_soup.find('a', class_='authorAllBooks__singleTextTitle')

    if not book_link:
        print("No book link found")
        return []

    book_page_url = 'https://lubimyczytac.pl' + book_link['href']
    book_response = requests.get(book_page_url, headers=headers)

    if book_response.status_code != 200:
        print(f"Error fetching book page: {book_response.status_code}")
        return []

    book_soup = BeautifulSoup(book_response.content, 'html.parser')

    reviews = []
    review_elements = book_soup.find_all('div', class_='comment-cloud')

    if not review_elements:
        print("No review elements found")
        return []

    for element in review_elements:
        review_author = element.find('div', class_='reviewer-nick').text.strip()
        review_text = element.find('div', class_='comment-cloud__body relative').text.strip()
        review_rating_element = element.find('span', class_='big-number')
        if review_rating_element:
            review_rating = int(review_rating_element.text.strip())
        else:
            review_rating = None  # Lub inna wartość domyślna w przypadku braku oceny

        reviews.append(f"{review_author}:{review_rating} :{review_text}")

    return reviews

# Example call
#print(fetch_external_reviews("Harry Potter"))
