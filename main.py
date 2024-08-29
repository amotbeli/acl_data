from bs4 import BeautifulSoup
import requests
import json

def main():
    try:
        with open("acl_data.json", "r", encoding="utf8") as file:
            acl_data = json.load(file)
            existing_count = acl_data[-1]["id"]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        acl_data = []
        existing_count = 0

    print("Entries done (out of 15828):", existing_count)
    offset = int(input("Enter offset: "))
    count = int(input("Enter count: "))

    response = requests.get(f"http://118.185.210.241:8001/cgi-bin/koha/opac-search.pl?&limit=mc-itemtype%2Cphr%3ATAMIL&offset={offset}&sort_by=relevance&count={count}").text
    soup = BeautifulSoup(response, "lxml")

    book_count = offset

    book_details = soup.find_all("td", class_="bibliocol")
    for book_detail in book_details:
        book_count += 1
        try:
            book_title = book_detail.find("a", class_="title").text.strip()
        except AttributeError:
            book_title = "No information"
        try:
            book_authors = book_detail.find("ul", class_="author resource_list").text.strip()
        except AttributeError:
            book_authors = "No information"
        try:
            book_publishers = book_detail.find("span", class_="publisher_name").text.strip()
        except AttributeError:
            book_publishers = "No information"

        book_data = {}

        book_data["id"] = book_count
        book_data["title"] = book_title
        book_data["authors"] = book_authors
        book_data["publishers"] = book_publishers

        acl_data.append(book_data)

        with open("acl_data.json", "w", encoding="utf8") as file:
            #ensure_ascii parameter is kept False to make the JSON file readable for Tamil
            json.dump(acl_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()