# from crawler.crawler_musinsa import *
# from ..crawler.crawler_uniqlo import UniqloCrawler
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'size_dot_comm_crawler_module.settings'
import django
django.setup()
import unittest
from crawler.crawler_musinsa import MusinsaCrawler
uniqlo = None
musinsa_test_brand_name_list = ['MUSINSA STANDARD', '8SECONDS', 'ROMANTICPIRATES', '5252BYOIOI', 'GROOVE RHYME',
                                'COVERNAT', 'DRAW FIT']


class MusinsaCrawlerTest(unittest.TestCase):
    musinsa = MusinsaCrawler(0)
    brand_dic = None
    brand_main_url_dic = None
    product_url_dic = None

    def test_update_brand_list(self):
        cnt = self.musinsa.update_brand_list()
        print(cnt)
        self.assertIsNotNone(cnt)

    def test_get_brand_dic(self):
        self.brand_dic = self.musinsa.get_brand_dic(musinsa_test_brand_name_list)
        print(self.brand_dic)
        self.assertIsNotNone(self.brand_dic)

    def test_get_brand_main_url_list(self):
        self.test_get_brand_dic()
        self.brand_main_url_dic = self.musinsa.get_brand_main_url_dic(self.brand_dic)
        print(self.brand_main_url_dic)
        self.assertIsNotNone(self.brand_main_url_dic)

    def test_get_product_url_dic(self):
        self.test_get_brand_dic()
        self.brand_main_url_dic = self.musinsa.get_brand_main_url_dic(self.brand_dic)
        self.product_url_dic = self.musinsa.get_product_url_dic(self.brand_main_url_dic)
        print(self.product_url_dic)
        self.assertIsNotNone(self.product_url_dic)


if __name__ == '__main__':
    unittest.main()
# 메인을 넣어야 하나?
# get_product_detail
# save_size_table
# get_brand_info
# get_category_info_and_dic
# get_sub_category_info_and_dic
# get_image_list
# get_size_table
# get_product_price
# get_product_name
# get_product_no
# get_gender_info
# get_product_description