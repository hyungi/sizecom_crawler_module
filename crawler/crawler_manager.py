from crawler.crawler_musinsa import MusinsaCrawler
from crawler.crawler_ssf import SsfCrawler
from crawler.crawler_uniqlo import UniqloCrawler
from crawler.models import CategoryDic, SubCategoryDic, CategorySizePartDic, SubCategorySizePartDic, CategoryInfo, SubCategoryInfo, CategorySizePartInfo, SubCategorySizePartInfo


class CrawlerManager:
    def __init__(self, debug_level=0):
        self.musinsa_crawler = MusinsaCrawler(debug_level)
        self.uniqlo_crawler = UniqloCrawler(debug_level)
        self.ssf_crawler = SsfCrawler(debug_level)
        self.crawler_name_list = ['무신사', '유니클로', 'SSF']

    def run_crawler(self, crawler_name):
        """
        :param crawler_name: 동작하고자 하는 크롤러의 이름
        :return: 크롤러가 정상동작함: True, 크롤러 이름 | 그렇지 않다면: False, 오류 또는 존재하는 크롤러의 이름 리스트
        """
        if crawler_name == '무신사' or crawler_name.lower() == 'musinsa':
            try:
                self.musinsa_crawler.update_brand_list()
                brand_dic = self.musinsa_crawler.get_brand_dic()
                brand_main_url_dic = self.musinsa_crawler.get_brand_main_url_dic(brand_dic)
                product_url_dic = self.musinsa_crawler.get_product_url_dic(brand_main_url_dic)
                self.musinsa_crawler.get_product_detail(False, product_url_dic)
                return True, crawler_name
            except Exception as e:
                return False, e
        elif crawler_name == '유니클로' or crawler_name.lower() == 'uniqlo':
            try:
                self.uniqlo_crawler.update_brand_list()
                brand_dic = self.uniqlo_crawler.get_brand_dic(None)
                brand_main_url_dic = self.uniqlo_crawler.get_brand_main_url_dic(brand_dic)
                product_url_dic = self.uniqlo_crawler.get_product_url_dic(brand_main_url_dic)
                self.uniqlo_crawler.get_product_detail(False, product_url_dic)
                return True, crawler_name
            except Exception as e:
                return False, e
        elif crawler_name == 'SSF' or crawler_name.lower() == 'ssf':
            try:
                self.ssf_crawler.update_brand_list()
                brand_dic = self.ssf_crawler.get_brand_dic()
                brand_main_url_dic = self.ssf_crawler.get_brand_main_url_dic(brand_dic)
                product_url_dic = self.ssf_crawler.get_product_url_dic(brand_main_url_dic)
                self.ssf_crawler.get_product_detail(False, product_url_dic)
                return True, crawler_name
            except Exception as e:
                return False, e
        else:
            print('크롤러 이름을 다시 확인해주세요')
            return False, self.crawler_name_list

    def get_brand_dic(self):
        brand_dic = {}
        brand_dic.update({'Musinsa': self.musinsa_crawler.get_brand_dic()})
        brand_dic.update({'Uniqlo': self.uniqlo_crawler.get_brand_dic()})
        brand_dic.update({'SSF': self.ssf_crawler.get_brand_dic()})
        return brand_dic

    def get_current_crawler_list(self):
        return self.crawler_name_list

    def send_category_dic_and_info(self):
        # mapping 대상인 dic list
        dic_list = {}
        dic_list.update({'category_dic': CategoryDic.objects.filter(category_info=None)})
        dic_list.update({'sub_category_dic': SubCategoryDic.objects.filter(sub_category_info=None)})
        dic_list.update({'category_size_part_dic': CategorySizePartDic.objects.filter(category_size_part_info=None)})
        dic_list.update({'sub_category_size_part_dic': SubCategorySizePartDic.objects.filter(sub_category_size_part_info=None)})

        # 유저가 보고 매핑해줄 info list
        info_list = {}
        info_list.update({'category_info': CategoryInfo.objects.all()})
        info_list.update({'sub_category_info': SubCategoryInfo.objects.all()})
        info_list.update({'category_size_part_info': CategorySizePartInfo.objects.all()})
        info_list.update({'sub_category_size_part_info': SubCategorySizePartInfo.objects.all()})

        return dic_list, info_list

    def receive_category_dic_info(self, category, dic, info):
        if category == 'category':
            dic.update(category_info=info)
        elif category == 'sub_category':
            dic.update(sub_category_info=info)
        elif category == 'category_size_part_dic':
            dic.update(category_size_part_info=info)
        elif category == 'sub_category_size_part_dic':
            dic.update(sub_category_size_part_info=info)
        # TODO
        """
        drop down 메뉴로 info 가 매핑이 안된 dic list 보여주고 해당 dic 의 카테고리에 맞는(category, subcategory, category_sizepart,
        subcategory_sizepart 등) info 를 다음 drop down 메뉴에 보여주고, 사용자가 선택을 한뒤 submit 을 하면 서버에서 그걸 받아서
        처리하는 방향으로 하면 될듯
        """
