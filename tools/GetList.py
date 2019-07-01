import requests
from bs4 import BeautifulSoup as BS


class List:
    def get_dict():
        url = "https://www.sprakradet.no/sprakhjelp/Skriverad/Avloeysarord/"
        page = requests.get(url)
        soup = BS(page.text, "html.parser")
        word_table = soup.find("tbody")
        word_table_breakdown = word_table.find_all("tr")
        word_table_dict = []

        for row in word_table_breakdown:
            if Work.check(row):
                row_dict = []
                for line in row.find_all('td'):
                    dict_friendly = line.get_text()
                    row_dict.append(dict_friendly)
                word_table_dict.append(row_dict)
            else:
                pass
        return word_table_dict

    def dict_to_json():
        gen_dict = List.get_dict()
        json = {}
        for uncompressed_dict in gen_dict:
            bad_word = uncompressed_dict[0]
            replace_word = uncompressed_dict[1]
            json[bad_word] = replace_word
        return json


class Work:

    def check(row):
        for line in row.find_all("td", {"valign": "top", "align": "left"}):
            if line.find("h2") or line is None:
                return False
            elif line.get_text() == " " or line.get_text() == "Til toppen":
                return False
            else:
                return True
