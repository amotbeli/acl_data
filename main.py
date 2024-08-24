from bs4 import BeautifulSoup
import requests

def main():
    response = requests.get("http://118.185.210.241:8001/cgi-bin/koha/opac-search.pl?&limit=mc-itemtype%2Cphr%3ATAMIL&offset=0&sort_by=relevance&count=1000").text
    soup = BeautifulSoup(response, "lxml")

    book_count = 0

    book_details = soup.find_all("td", class_="bibliocol")
    for book_detail in book_details:
        book_count += 1
        try:
            book_title = book_detail.find("a", class_="title").text.strip()
        except:
            book_title = "No information"
        try:
            book_authors = book_detail.find("ul", class_="author resource_list").text.strip()
        except:
            book_authors = "No information"
        try:
            book_publishers = book_detail.find("span", class_="publisher_name").text.strip()
        except AttributeError:
            book_publishers = "No information"
        with open("acl_data.txt", "a", encoding="utf8") as file:
            acl_data = f"""book number: {book_count}
            title: {book_title}
            authors: {book_authors}
            publishers: {book_publishers}\n\n"""
            file.write(acl_data)

if __name__ == "__main__":
    main()