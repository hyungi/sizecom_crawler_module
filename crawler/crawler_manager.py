from .crawler_musinsa import MusinsaCrawler
from .crawler_ssf import SsfCrawler
from .crawler_uniqlo import UniqloCrawler
from .models import CategoryDic, SubCategoryDic, CategorySizePartDic, SubCategorySizePartDic, CategoryInfo, SubCategoryInfo, CategorySizePartInfo, SubCategorySizePartInfo


class CrawlerManager:
    # TODO: receive_category_dic_info method 기준으로 view 에 넘길 정보 다시 정리
    def __init__(self, debug_level=0):
        self.musinsa_crawler = MusinsaCrawler(debug_level)
        self.uniqlo_crawler = UniqloCrawler(debug_level)
        self.ssf_crawler = SsfCrawler(debug_level)
        self.category_info = CategoryInfo.objects.all().values()
        self.category_dic = CategoryDic.objects.filter(category_info=None).values()
        self.sub_category_info = SubCategoryInfo.objects.all().values()
        self.sub_category_dic = SubCategoryDic.objects.filter(sub_category_info=None).values()
        self.category_size_part_info = CategorySizePartInfo.objects.all().values()
        self.category_size_part_dic = CategorySizePartDic.objects.filter(category_size_part_info=None).values()
        self.sub_category_size_part_info = SubCategorySizePartInfo.objects.all().values()
        self.sub_category_size_part_dic = SubCategorySizePartDic.objects.filter(sub_category_size_part_info=None).values()
        self.reload_database()
        self.crawler_name_list = ['무신사', '유니클로', 'SSF']

    def reload_database(self):
        self.category_info = CategoryInfo.objects.all().values()
        self.category_dic = CategoryDic.objects.filter(category_info=None).values()
        self.sub_category_info = SubCategoryInfo.objects.all().values()
        self.sub_category_dic = SubCategoryDic.objects.filter(sub_category_info=None).values()
        self.category_size_part_info = CategorySizePartInfo.objects.all().values()
        self.category_size_part_dic = CategorySizePartDic.objects.filter(category_size_part_info=None).values()
        self.sub_category_size_part_info = SubCategorySizePartInfo.objects.all().values()
        self.sub_category_size_part_dic = SubCategorySizePartDic.objects.filter(sub_category_size_part_info=None).values()

    def run_crawler(self, crawler_name, overlap_chk=True):
        """
        :param crawler_name: 동작하고자 하는 크롤러의 이름
        :return: 크롤러가 정상동작함: True, 크롤러 이름 | 그렇지 않다면: False, 크롤러 이름, 성공한 단계 까지의 변수, 오류 / False, 존재하는 크롤러의 이름 리스트
        성공한 단계 까지의 변수를 return 하는 이유는 크롤러를 각 단계별로 다시 돌리는 시간이 많이 걸리기 때문에 성공한 단계 까지는 저장을 해서
        다시 크롤러를 돌릴 수 있도록 한다.
        """
        manager, brand_dic, brand_main_url_dic, product_url_dic = None, None, None, None
        result = {"status": False}
        if crawler_name not in self.crawler_name_list:
            result["error"] = "crawler_doesn't exist"
            result["error_msg"] = str(self.crawler_name_list)
            return result
        if crawler_name == '무신사' or crawler_name.lower() == 'musinsa':
            result['crawler_name'] = 'musinsa'
            manager = self.musinsa_crawler
        elif crawler_name == '유니클로' or crawler_name.lower() == 'uniqlo':
            result['crawler_name'] = 'uniqlo'
            manager = self.uniqlo_crawler
        elif crawler_name == 'SSF' or crawler_name.lower() == 'ssf':
            result['crawler_name'] = 'ssf'
            manager = self.ssf_crawler
        try:
            manager.update_brand_list()
            brand_dic = manager.get_brand_dic()
            brand_main_url_dic = manager.get_brand_main_url_dic(brand_dic)
            product_url_dic = manager.get_product_url_dic(brand_main_url_dic)
            manager.get_product_detail(overlap_chk, product_url_dic)
            result['status'] = True
            return result
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__str__()
            if product_url_dic is not None:
                result["partial_result"] = product_url_dic
                result["error_point"] = "Fail to get product_detail"
                return result
            elif brand_main_url_dic is not None:
                result["partial_result"] = brand_main_url_dic
                result["error_point"] = "Fail to get product_url_dic"
                return result
            elif brand_dic is not None:
                result["partial_result"] = brand_dic
                result["error_point"] = "Fail to get brand_main_url_dic"
                return result

    def run_crawler_partially(self, crawler_name, overlap_chk, error_point, partial_result):
        """
        이걸 그냥 run_crawler에서 같이 동작하게 할수 있지 않을까? 그리고 error_point 에서 크롤러를 다시 돌린다고 해서 무조건 성공한다는 보장이 없음
        error 발생시 해당 지점을 계속 확인하고 다시 돌릴수 있도록 만들어주면 좋을듯
        :param crawler_name:
        :param overlap_chk:
        :param error_point:
        :param partial_result:
        :return:
        """
        manager, brand_dic, brand_main_url_dic, product_url_dic = None, None, None, None
        result = {"status": False}
        if crawler_name == '무신사' or crawler_name.lower() == 'musinsa':
            result['crawler_name'] = 'musinsa'
            manager = self.musinsa_crawler
        elif crawler_name == '유니클로' or crawler_name.lower() == 'uniqlo':
            result['crawler_name'] = 'uniqlo'
            manager = self.uniqlo_crawler
        elif crawler_name == 'SSF' or crawler_name.lower() == 'ssf':
            result['crawler_name'] = 'ssf'
            manager = self.ssf_crawler

        try:
            if error_point is "Fail to get product_detail":
                product_url_dic = partial_result
                manager.get_product_detail(overlap_chk, product_url_dic)
                result['status'] = True
            elif error_point is "Fail to get product_url_dic":
                brand_main_url_dic = partial_result
                product_url_dic = manager.get_product_url_dic(brand_main_url_dic)
                manager.get_product_detail(overlap_chk, product_url_dic)
                result['status'] = True
            elif error_point is "Fail to get brand_main_url_dic":
                brand_dic = manager.get_brand_dic()
                brand_main_url_dic = manager.get_brand_main_url_dic(brand_dic)
                product_url_dic = manager.get_product_url_dic(brand_main_url_dic)
                manager.get_product_detail(overlap_chk, product_url_dic)
                result['status'] = True
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__str__()
            if product_url_dic is not None:
                result["partial_result"] = product_url_dic
                result["error_point"] = "Fail to get product_detail"
            elif brand_main_url_dic is not None:
                result["partial_result"] = brand_main_url_dic
                result["error_point"] = "Fail to get product_url_dic"
            elif brand_dic is not None:
                result["partial_result"] = brand_dic
                result["error_point"] = "Fail to get brand_main_url_dic"

        return result

    def get_brand_dic(self):
        result = {"status": False}

        try:
            brand_dic = {}
            brand_dic.update({'Musinsa': self.musinsa_crawler.get_brand_dic()})
            brand_dic.update({'Uniqlo': self.uniqlo_crawler.get_brand_dic()})
            brand_dic.update({'SSF': self.ssf_crawler.get_brand_dic()})
            result['brand_dic'] = str(brand_dic)
            result["status"] = True
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__str__()

        return result

    def get_current_crawler_list(self):
        return self.crawler_name_list

    #TODO: in-memory caching을 할 필요가 있을까? manager init 할때 한번에 로드해서 관리가 편할수 있음 : 어차피 동작을 할때마다 DB에 접근을 해야하는데 의미가 없다.
    def send_category_dic_and_info(self):
        result = {"status": False}
        try:
            dic = {'category_dic': list(self.category_dic)}
            info = {'category_info': list(self.category_info)}
            result['dic'] = dic
            result['info'] = info
            result["status"] = True
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__str__()
        return result

    def send_sub_category_dic_and_info(self):
        result = {"status": False}
        try:
            dic = {'sub_category_dic': list(self.sub_category_dic)}
            info = {'sub_category_info': list(self.sub_category_info)}
            result['dic'] = dic
            result['info'] = info
            result["status"] = True
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__str__()
        return result

    def send_category_size_part_dic_and_info(self):
        result = {"status": False}
        try:
            dic = {'category_size_part_dic': list(self.category_size_part_dic)}
            info = {'category_size_part_info': list(self.category_size_part_info)}
            result['dic'] = dic
            result['info'] = info
            result["status"] = True
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__str__()
        return result

    def send_sub_category_size_part_dic_and_info(self):
        result = {"status": False}
        try:
            dic = {'sub_category_size_part_dic': list(self.sub_category_size_part_dic)}
            info = {'sub_category_size_part_info': list(self.sub_category_size_part_info)}
            result['dic'] = dic
            result['info'] = info
            result["status"] = True
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__str__()
        return result

    def receive_category_dic_info(self, dic_pk, info_pk):
        # TODO: dic을 업데이트 한 뒤 result 결과에 반영을 할지? 한다면 json 화 고려(get으로 받아온 object는 json으로 바꾸기 힘다) : 하지 않는다면 성공 여부만 return
        result = {"status": False}
        try:
            info = CategoryInfo.objects.get(pk=info_pk)
            dic = CategoryDic.objects.filter(pk=dic_pk)
            dic.update(category_info=info)
            result["status"] = True
            self.reload_database()
            # result["info"] = info
            # result["dic"] = dic
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__name__
        return result

    def receive_sub_category_dic_info(self, dic_pk, info_pk):
        result = {"status": False}
        try:
            info = SubCategoryInfo.objects.get(pk=info_pk)
            dic = SubCategoryDic.objects.get(pk=dic_pk)
            dic.update(sub_category_info=info)
            result["status"] = True
            self.reload_database()
            # result["info"] = info
            # result["dic"] = dic
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__name__
        return result

    def receive_category_size_part_dic_info(self, dic_pk, info_pk):
        result = {"status": False}
        try:
            info = CategorySizePartInfo.objects.get(pk=info_pk)
            dic = CategorySizePartDic.objects.get(pk=dic_pk)
            dic.update(category_size_part_info=info)
            result["status"] = True
            self.reload_database()
            # result["info"] = info
            # result["dic"] = dic
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__name__
        return result

    def receive_sub_category_size_part_dic_info(self, dic_pk, info_pk):
        result = {"status": False}
        try:
            info = SubCategorySizePartInfo.objects.get(pk=info_pk)
            dic = SubCategorySizePartDic.objects.get(pk=dic_pk)
            dic.update(sub_category_size_part_info=info)
            result["status"] = True
            self.reload_database()
            # result["info"] = info
            # result["dic"] = dic
        except Exception as e:
            result["error"] = e
            result["error_msg"] = e.__name__
        return result
