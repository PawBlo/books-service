import requests
from lxml import html
import os
class Scraper:
    def __init__(self, isbn):
        self.isbn = isbn
    def create_url(self):
        return f"https://www.poczytaj.pl/index.php?akcja=pokaz_ksiazki&szukaj={self.isbn}&kategoria_szukaj=cala_oferta&id=best&limit=10"
    def get_info(self):
        response = requests.get(self.create_url())
        # print(response.text)
        img_xpath = "/html/body/div/main/div[5]/div[1]/a/img"
        title_xpath = "/html/body/div/main/div[5]/div[2]/div[2]/h3/a"
        author_xpath = "/html/body/div/main/div[5]/div[2]/div[1]"
        tree = html.fromstring(response.text)
        img = tree.xpath(img_xpath)
        # print(img)
        if img:
            print(img[0].get('data-src'))
            img_url = img[0].get('data-src')
            response = requests.get(img_url)
            path_img = f"{self.isbn}.jpg"
            if response.status_code == 200:
                with open(f"./media/cover_images/{self.isbn}.jpg", 'wb') as file:
                    file.write(response.content)
                print("Grafika została zapisana jako obraz.jpg")
            else:
                print(f"Nie udało się pobrać grafiki. Kod statusu: {response.status_code}")
        # print(tree.xpath(title_xpath))
        title = tree.xpath(title_xpath)[0].get('title')
        author = tree.xpath(author_xpath)[0].text
        return f"{self.isbn}.jpg", title, author
# s = Scraper("9788395965371")
# print(s.get_info())

