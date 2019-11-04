from abc import *
from .logger import Logger

'''
HOW TO RUN selenium-chrome ON NON-DISPLAY env
1. apt-get install chromium-browser
2. apt-get install xvfb
3. pip install pyvirtualdisplay
4. Call pyvirtualdisplay.Display befroe using selenium
5. Don't forget to use Chromedriver ver.0.73 for linux64
'''


class Crawler(metaclass=ABCMeta):
    """
    extends by platform
    e.g. Musinsa_Crawler
    """
    platform_url = None
    platform_name = None
    logger = None

    @abstractmethod
    def __init__(self, debug_level, name, url):
        self.name = name
        self.url = url
        _logger = Logger(name, debug_level)
        self.logger = _logger.set_logger()

    @abstractmethod
    def show_dev_info(self, date="2019.04.02"):
        '''
        show platform basic info
        :param date: String; the last update date for maintenance, should update manually
        :return: None
        '''
        print("Name: {name}\n" \
              "Url: {url}\n" \
              "Last update : {date}".format(name=self.name, url=self.url, date=date))

    @staticmethod
    def get_page_html(page_url):
        '''
        get html string of the page with bs4
        :param page_url: String
        :return: String
        '''
        import requests
        from bs4 import BeautifulSoup
        _page_source = requests.get(page_url)
        _page_source.encoding = 'utf-8'  # 한글이 깨져서 encoding 추가
        page_source = _page_source.text
        return BeautifulSoup(page_source, 'html.parser')


class PlatformCrawler(Crawler):
    @abstractmethod
    def __init__(self, debug_level, name, url):
        super().__init__(debug_level, name, url)

    def show_dev_info(self, date="2019.04.02"):
        super(date)

    @abstractmethod
    def update_brand_list(self):
        pass

    @abstractmethod
    def get_brand_dic(self, brand_name_list):
        '''
        get all brand urls of the platform
        :return: Dictionary; key: brand_name, value: brand_url
        '''
        pass

    @abstractmethod
    def get_brand_main_url_dic(self, brand_dict):
        """

        :param brand_dict:
        :return brand_main_url_list:
        """

    @abstractmethod
    def get_product_url_dic(self, brand_main_url_list):
        '''
        get all product urls of the platform
        :return product_url_list:
        '''
        pass

    @abstractmethod
    def get_product_detail(self, overlap_check, product_url_list):
        '''
        get product detail of given product_url_list

        '''
        pass

    @abstractmethod
    def get_product_price(self, product_url, product_source):
        '''
        get product price of given product_url
        :param product_url: String
        :return product price: String

        '''
        pass

    @abstractmethod
    def get_product_name(self, product_url, product_source):
        '''
        get product name of given product_url
        :param product_url: String
        :return product name: String

        '''
        pass

    @abstractmethod
    def get_product_no(self, product_url, product_source):
        '''
        get product number of given product_url
        :param product_url: String
        :return product name: String

        '''
        pass

    @abstractmethod
    def get_review_html(self, product_url, product_source):
        '''
        get review Html of given product_url
        :param product_url: String
        :return product name: String
        '''
        pass


class CommunityCrawler(Crawler):
    @abstractmethod
    def __init__(self, name, url):
        super(name, url)

    @abstractmethod
    def showDevInfo(self, date="2019.04.02"):
        super(date)

    @abstractmethod
    def getPageHtml(self, page_url):
        super(page_url)

    pass