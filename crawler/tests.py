from crawler.crawler_musinsa import MusinsaCrawler
from crawler.crawler_uniqlo import UniqloCrawler

import unittest
musinsa = None
uniqlo = None
musinsa_test_brand_name_list = ['MUSINSA STANDARD', '8SECONDS', 'ROMANTICPIRATES', '5252BYOIOI', 'GROOVE RHYME',
                                'COVERNAT', 'DRAW FIT']


def build_crawler(platform_name, debug_level=0):
    global musinsa, uniqlo
    if platform_name == 'Musinsa': # Musinsa
        musinsa = MusinsaCrawler(debug_level)
    elif platform_name == 'Uniqlo':
        uniqlo = UniqloCrawler(debug_level)


def test_brand_update(platform_name):
    if platform_name == musinsa.name: # Musinsa
        return musinsa.update_brand_list()


def test_get_brand_dic(platform_name):
    if platform_name == musinsa.name: # Musinsa
        return musinsa.get_brand_dic()


def test_get_brand_main_url_dic(platform_name, brand_dic):
    if platform_name == musinsa.name: # Musinsa
        return musinsa.get_brand_main_url_dic(brand_dic)


def test_get_product_url_dic(platform_name, brand_main_url_list):
    if platform_name == musinsa.name: # Musinsa
        return musinsa.get_product_url_dic(brand_main_url_list)


def test_get_product_detail(platform_name, overlap_chk, product_url_list):
    if platform_name == musinsa.name: # Musinsa
        musinsa.get_product_detail(overlap_chk, product_url_list)


def test_whole_crawler_work_flow(platform_name, overlap_chk):
    build_crawler(platform_name)
    test_brand_update(platform_name)
    brand_dic = test_get_brand_dic(platform_name)
    brand_main_url_dic = test_get_brand_main_url_dic(platform_name, brand_dic)
    product_url_dic = test_get_product_url_dic(platform_name, brand_main_url_dic)
    test_get_product_detail(platform_name, overlap_chk, product_url_dic)


# class MusinsaCrawlerTest(unittest.TestCase):
#     musinsa = MusinsaCrawler(0)
#     brand_dict = None
#     brand_main_url_list = None
#     product_url_list = None
#
#     def test_update_brand_list(self):
#         cnt = musinsa.update_brand_list()
#         self.assertIsNotNone(cnt)
#
#     def test_get_brand_list(self, brand_name_list):
#         self.brand_dict = musinsa.get_brand_list(brand_name_list)
#         self.assertIsNotNone(self.brand_dict)
#
#     def test_get_brand_main_url_list(self):
#         self.brand_main_url_list = musinsa.get_brand_main_url_list(self.brand_dict)
#         self.assertIsNotNone(self.brand_main_url_list)
#
#     def test_get_product_url_list(self):
#         self.product_url_list = musinsa.get_product_url_list(self.brand_main_url_list)
#         self.assertIsNotNone(self.product_url_list)
#
#
# if __name__ == '__main__':
#     import django
#
#     django.setup()
#     unittest.main()
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