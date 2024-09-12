from bs4 import BeautifulSoup
import requests
import json
import time

def main():
    try:
        with open("acl_data.json", "r", encoding="utf8") as file:
            acl_data = json.load(file)
            existing_count = acl_data[-1]["id"]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        acl_data = []
        existing_count = 0

    print("Entries done (out of 15845):", existing_count)
    offset = int(input("Enter offset: "))
    count = int(input("Enter count: "))

    response = requests.get(f"http://118.185.210.241:8001/cgi-bin/koha/opac-search.pl?&limit=mc-itemtype%2Cphr%3ATAMIL&offset={offset}&sort_by=relevance&count={count}").text
    soup = BeautifulSoup(response, "lxml")

    book_id = offset

    books = soup.find_all("td", class_="bibliocol")
    for book in books:
        time.sleep(2)
        book_id += 1
        book_href = book.find("a", class_="title").get("href")
        book_url = "http://118.185.210.241:8001"+book_href
        response_in = requests.get(book_url).text
        soup_in = BeautifulSoup(response_in, "lxml")
        book_details = soup_in.find("div", class_="record")
        try:
            title = book_details.find("h1", class_="title").text.strip()
        except AttributeError:
            title = "No information"
        try:
            authors = book_details.find("span", property="name").text.strip()
        except AttributeError:
            authors = "No information"
        try:
            publishers = book_details.find("span", class_="publisher_name").text.strip()
        except AttributeError:
            publishers = "No information"
        try:
            publisher_place = book_details.find("span", class_="publisher_place").text.strip()
        except AttributeError:
            publisher_place = "No information"
        try:
            publisher_date = book_details.find("span", class_="publisher_date").text.strip()
        except AttributeError:
            publisher_date = "No information"
        try:
            edition = book_details.find("span", property="bookEdition").text.strip()
        except AttributeError:
            edition = "No information"
        try:
            page_numbers = book_details.find("span", property="description").text.strip()
        except AttributeError:
            page_numbers = "No information"
        try:
            isbn = book_details.find("span", property="isbn").text.strip()
        except AttributeError:
            isbn = "No information"
        try:
            alt_name = book_details.find("span", property="alternateName").text.strip()
        except AttributeError:
            alt_name = "No information"
        try:
            subject = book_details.find("a", class_="subject").text
        except AttributeError:
            subject = "No information"
        
        book_data = {}
        book_data["id"] = book_id
        book_data["title"] = title
        book_data["alt title"] = alt_name
        book_data["authors"] = authors
        book_data["publishers"] = publishers
        book_data["published place"] = publisher_place
        book_data["published date"] = publisher_date
        book_data["edition"] = edition
        book_data["page numbers"] = page_numbers
        book_data["isbn"] = isbn
        book_data["subject"] = subject

        acl_data.append(book_data)
        count -= 1
        print(f"Entries left in this iteration: {count}")
        with open("acl_data.json", "w", encoding="utf8") as file:
            #ensure_ascii parameter is kept False to make the JSON file readable for Tamil
            json.dump(acl_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()