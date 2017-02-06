from bs4 import BeautifulSoup
import requests
class common_methods():

    def __init__(self):
        self.agent = requests.session()

    def page_to_soup(self,page):
        soup = BeautifulSoup(page.content)
        return soup

    def get_page(self,url):
        content = self.agent.get(url)
        return content

    def post_page(self,url,post):
        content = self.agent.post(url,post)
        return content
