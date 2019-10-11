from urllib.request import Request, urlopen, URLError
from bs4 import BeautifulSoup
from nltk import regexp_tokenize
from nltk.corpus import stopwords


class Scraping:

    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

    def get_text_from_url(self, url):
        """
        :param url: takes a single url as "https://example.com"
        :return: uncleaned list of words from the url
        """
        try:
            req = Request(url, headers=self.header)
            page = urlopen(req)
            soup = BeautifulSoup(page, "lxml")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            return text
        except ValueError:
            # Remplacer par un log
            print("Value error")
        except URLError:
            print("Url error")

class Preprocessor:
    
    def tokenize(self, raw_text):
        results = []
        pattern = r"\s|[\.,;\(\)\[\]\/\~\%\!\:\_\…\?\=\‘\’\&\-\“\”\•\©\—\<\>\»\\\$\£\€\®\*\@]"
        if raw_text:
            results = regexp_tokenize(raw_text, pattern=pattern, gaps=True)
        return results


def from_url_to_vector(url):
    scraper = Scraping()
    preproc = Preprocessor()
    url_content = scraper.get_text_from_url(url)
    tokenized_text = preproc.tokenize(url_content)
    stopWords = set(stopwords.words('english'))
    cleaned_text = [word for word in tokenized_text if word not in stopWords]

    return cleaned_text


if __name__ == "__main__":
    url = "https://towardsdatascience.com/what-does-an-ideal-data-scientists-profile-look-like-7d7bd78ff7ab"
    elements = from_url_to_vector(url)

    with open('result.txt','w') as f:
        f.write(" ".join(elements))