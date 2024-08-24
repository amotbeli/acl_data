from bs4 import BeautifulSoup
import requests

def main():
    response = requests.get("http://118.185.210.241:8001/cgi-bin/koha/opac-search.pl?&limit=mc-itemtype%2Cphr%3ATAMIL&offset=0&sort_by=relevance&count=200").text
    soup = BeautifulSoup(response, "lxml")

    book_detail = soup.find("td", class_="bibliocol")
    book_title = book_detail.find("a", class_="title").text
    print(book_title)

if __name__ == "__main__":
    main()