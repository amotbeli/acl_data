from bs4 import BeautifulSoup
import requests

def main():
    response = requests.get("http://118.185.210.241:8001/cgi-bin/koha/opac-search.pl?&limit=mc-itemtype%2Cphr%3ATAMIL&offset=0&sort_by=relevance&count=200").text
    soup = BeautifulSoup(response, "lxml")

    book_detail = soup.find("td", class_="bibliocol")
    book_title = book_detail.find("a", class_="title").text
    book_authors = book_detail.find("ul", class_="author resource_list").text
    try:
        book_publishers = book_detail.find("span", class_="publisher_name").text
    except AttributeError:
        book_publishers = "No information"
    print(book_title)
    print(book_authors)
    print(book_publishers)

if __name__ == "__main__":
    main()