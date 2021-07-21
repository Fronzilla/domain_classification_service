import cloudscraper

from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36 '
                  '(compatible; Googlebot/2.1; +https://www.google.com/bot.html)'
}


def scrap_data(url_: str, length=1500) -> str:
    """
    По переданному url попытаемся определить его описание
    :param url_: Целевой url
    :param length: Длина возвращаемой строки
    :return:
    """
    try:
        if not url_.startswith('http'):
            url_ = 'http://' + url_

        r = scraper.get(url_, headers=HEADERS)

        if r.apparent_encoding != r.encoding:  # если явная кодировка != кодировки от запроса - перекодируем
            r.encoding = r.apparent_encoding

        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('title').text
        description = soup.find('meta', attrs={'name': 'description'})

        if "content" in str(description):
            description = description.get("content")
        else:
            description = ""

        h1_all, h2_all, h3_all = str(), str(), str()

        h1 = soup.find_all('h1')
        h1_all = ""

        # дальше - итеративно перебираем каждые заголовки в поисках содержимого
        for x in range(len(h1)):
            if x == len(h1) - 1:
                h1_all = h1_all + h1[x].text
            else:
                h1_all = h1_all + h1[x].text + ". "

        paragraphs_all = ""
        paragraphs = soup.find_all('p')

        for x in range(len(paragraphs)):
            if x == len(paragraphs) - 1:
                paragraphs_all = paragraphs_all + paragraphs[x].text
            else:
                paragraphs_all = paragraphs_all + paragraphs[x].text + ". "

        h2 = soup.find_all('h2')

        for x in range(len(h2)):
            if x == len(h2) - 1:
                h2_all = h2_all + h2[x].text
            else:
                h2_all = h2_all + h2[x].text + ". "

        h3 = soup.find_all('h3')
        h3_all = ""

        for x in range(len(h3)):
            if x == len(h3) - 1:
                h3_all = h3_all + h3[x].text
            else:
                h3_all = h3_all + h3[x].text + ". "

        description = str(title) + " " + str(description) + " " + str(h1_all) + " " + str(h2_all) + " " + str(
            h3_all) + " " + str(paragraphs_all)

        # ограничиваем длину строки до 1500 символов
        description = str(description)[0:length] if length else str(description)

        return description

    except Exception as r:
        print(r)
        return str()
