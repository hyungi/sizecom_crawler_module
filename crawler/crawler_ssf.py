from crawler.crawler_interface import PlatformCrawler
from crawler.models import *
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import json
from datetime import timezone, datetime


class SsfCrawler(PlatformCrawler):
    """
    현재 class 내부에서 static 으로 존재 해야 하는 변수와 그렇지 않은 변수가 혼재되어 있음
    static => url, product_info_list, save_data, women_last_crawled, men_last_crawled
    non_static => brndNm, godNo, dpos, godName, size_data, product_url
    """

    def __init__(self, debug_level, name='SSF', url='http://www.ssfshop.com'):
        super().__init__(debug_level, name, url)
        self.platform_info = None
        self.product_info = None
        self.brand_info = None
        self.category_size_part_info = None
        self.category_size_part_dic = None
        self.sub_category_size_part_info = None
        self.sub_category_size_part_dic = None
        self.gender_info = None

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        self.driver = webdriver.Chrome('/Users/seonghyeongi/python_projects/crawler/crawler/chromedriver', chrome_options=options)
        self.dspBrndDic = {}    # {brand_name: brandShopId}

        try:
            self.platform_info = PlatformInfo.objects.get(platform_name=self.name)
            self.logger.debug('Success|get platform_info: ' + str(self.platform_info))
        except PlatformInfo.DoesNotExist:
            self.platform_info = PlatformInfo.objects.create(platform_name=self.name, platform_url=self.url)
            self.logger.debug('Success|create platform_info: ' + str(self.platform_info))
        except Exception as e:
            self.logger.error('Unexpected Fail|get platform_info: ' + self.url + ' Cause: ' + str(e))

        self.driver.get(self.url + '/selectAllBrandList')
        page_source = self.driver.find_element_by_id('tab11').get_attribute('innerHTML')
        tab_bs = BeautifulSoup(page_source, 'html.parser')
        a_list = tab_bs.find_all('a')
        for a in a_list:
            self.dspBrndDic[a.attrs.get('ctgrynm')] = a.attrs.get('brndshopid')
        self.driver.quit()
        self.logger.info('Success|' + str(self.dspBrndDic))

    def _get_brandShopNo(self, brand_name):
        try:
            req = requests.get('http://www.ssfshop.com/selectDspCtgryBrand.json?dspBrndId=' + self.dspBrndDic.get(brand_name))
            text = json.loads(req.text)
            brandShopNo = dict(text)
            dspCtgryNo = brandShopNo.get("dspCtgryBrand").get("dspCtgryNo")
        except Exception as e:
            self.logger.error('Unexpected Fail|' + brand_name + ' Cause: ' + str(e))
            dspCtgryNo = None
        return dspCtgryNo

    def update_brand_list(self):
        # self.url + '/' + brand_name + '/main?' +
        # 'brandShopNo=' + self.get_brandShopNo(brand_name) + 'brndShopId=' + self.dspBrndDic.get(brand_name)
        _crawled_brand_set = set(self.dspBrndDic.keys())

        try:
            _current_brand_set = set(BrandInfo.objects.filter(platform_info=self.platform_info).values_list('brand_name', flat=True))
        except BrandInfo.DoesNotExist:
            _current_brand_set = ()
        _new_brand_list = list(_crawled_brand_set.difference(_current_brand_set))
        _new_brand_dic = {}
        for _new_brand_name in _new_brand_list:
            # _new_brand_main_url = self.url + '/' + _new_brand_name + '/main?brandShopNo=' + self._get_brandShopNo(_new_brand_name) + '&brndShopId=' + self.dspBrndDic.get(_new_brand_name)
            _new_brand_main_url = self.url + '/ssfshop/main?brandShopNo=' + self._get_brandShopNo(_new_brand_name) + '&brndShopId=' + self.dspBrndDic.get(_new_brand_name)
            _new_brand_dic.update({_new_brand_name: _new_brand_main_url})

        self.logger.debug('Success|make_new_brand_dic: ' + str(_new_brand_dic))

        for _brand_name in _new_brand_dic:
            _brand_url = _new_brand_dic.get(_brand_name)
            model_instance = BrandInfo(
                brand_name=_brand_name, brand_url=_brand_url, platform_info=self.platform_info
            )
            model_instance.save()
            self.logger.debug('Success|update brand_info: ' + str(model_instance.brand_name))

        return len(_new_brand_list)

    def get_brand_dic(self, brand_name_list=['Balenciaga', 'Beanpole Men', 'A COLD WALL']):
        """
        :param brand_name_list: 이 리스트가 존재 한다면 해당 브랜드들만 크롤링한다. 기본값은 특정 브랜드 리스트
        :return brand_dic: {brand_name: brand_url} 로 구성된 dictionary 를 return 한다
        """
        brand_info = dict(BrandInfo.objects.filter(platform_info=self.platform_info).values_list('brand_name', 'brand_url'))
        if brand_name_list is not None:
            brand_dic = {}
            for brand_name in brand_name_list:
                brand_dic.update({brand_name: brand_info.get(brand_name)})
            return brand_dic
        else:
            return brand_info

    def get_brand_main_url_dic(self, brand_dic):
        brand_main_url_dic = {}
        for _brand_name in brand_dic.keys():
            brand_main_url_list = []
            brand_url = brand_dic.get(_brand_name)
            brand_url = brand_url.split('main?')[0]
            try:
                women_main_url = brand_url + 'Women/list?dspCtgryNo=SFMA41&brandShopNo=' + self._get_brandShopNo(_brand_name) + '&brndShopId=' + self.dspBrndDic.get(_brand_name)
                men_main_url = brand_url + 'Men/list?dspCtgryNo=SFMA42&brandShopNo=' + self._get_brandShopNo(_brand_name) + '&brndShopId=' + self.dspBrndDic.get(_brand_name)
            except TypeError:
                continue
            w_last_page_no, m_last_page_no = 1, 1
            try:
                w_last_page_no = self.get_page_html(women_main_url).select_one('#page_last').attrs.get('pageno')
                self.logger.debug('Success: ' + women_main_url)
            except AttributeError:
                w_last_page_no = 1
            except Exception as e:
                self.logger.error('Unexpected error: ' + women_main_url + ' Cause: ' + str(type(e).__name__))

            try:
                m_last_page_no = self.get_page_html(men_main_url).select_one('#page_last').attrs.get('pageno')
                self.logger.debug('Success: ' + men_main_url)
            except AttributeError:
                m_last_page_no = 1
            except Exception as e:
                self.logger.error('Unexpected error: ' + men_main_url + ' Cause: ' + str(type(e).__name__))

            for idx in range(1, int(w_last_page_no) + 1):
                brand_main_url_list.append(women_main_url + '&currentPage=' + str(idx))

            for idx in range(1, int(m_last_page_no) + 1):
                brand_main_url_list.append(men_main_url + '&currentPage=' + str(idx))
            brand_main_url_dic.update({_brand_name: brand_main_url_list})

        return brand_main_url_dic

    def get_product_url_dic(self, brand_main_url_dic):
        _product_url_dic = {}
        for _brand_name in brand_main_url_dic.keys():
            product_url_list = []
            for brand_main_url in brand_main_url_dic.get(_brand_name):
                try:
                    product_li_list = self.get_page_html(brand_main_url).find('ul', id='dspGood').find_all('li')
                except AttributeError:
                    self.logger.info('No product info: ' + brand_main_url)
                    continue
                for product_li in product_li_list:
                    prdno = product_li.attrs.get('data-prdno')
                    if brand_main_url.find('/Women') == -1:
                        product_url_list.append(brand_main_url.split('/Men')[0] + '/' + prdno + '/good')
                        self.logger.debug('Success|' + brand_main_url.split('/Men')[0] + '/' + prdno + '/good')
                    else:
                        product_url_list.append(brand_main_url.split('/Women')[0] + '/' + prdno + '/good')
                        self.logger.debug('Success|' + brand_main_url.split('/Women')[0] + '/' + prdno + '/good')
            product_url_list = list(set(product_url_list))
            _product_url_dic.update({_brand_name: product_url_list})

        return _product_url_dic

    def get_product_detail(self, overlap_chk, product_url_dic):
        # TODO: 클래스 단에서 저장할 필요가 있는 정보는 아닐지?
        self.product_info = ProductInfo.objects.filter(platform_info=self.platform_info)
        self.brand_info = BrandInfo.objects.filter(platform_info=self.platform_info)

        self.category_size_part_info = CategorySizePartInfo.objects.all()
        self.category_size_part_dic = CategorySizePartDic.objects.all()
        self.sub_category_size_part_info = SubCategorySizePartInfo.objects.all()
        self.sub_category_size_part_dic = SubCategorySizePartDic.objects.all()
        self.gender_info = GenderInfo.objects.all()

        for _brand_name in product_url_dic.keys():
            _brand_info = self.get_brand_info(_brand_name)
            for _product_url in product_url_dic.get(_brand_name):
                product_info = self.product_info.filter(product_url=_product_url)
                if product_info.exists() and overlap_chk is True:
                    product_source = self.get_page_html(_product_url)
                    _price, _discount_price = self.get_product_price(_product_url, product_source)
                    if _discount_price is not None:
                        product_info.discount_price = _discount_price
                        product_info.update()
                        PriceTrackingInfo.objects.create(
                            discount_price=_discount_price, update_date=datetime.now(), product_info=product_info.get()
                        )
                    self.logger.debug('Success|product_info already exist: ' + str(product_info))
                    continue

                else:
                    product_source = self.get_page_html(_product_url)
                    size_info = self.get_size_table(_product_url, product_source)
                    _gender_info, _gender_dic = self.get_gender_info(_product_url, product_source)
                    _product_name = self.get_product_name(_product_url, product_source)
                    _product_no = self.get_product_no(_product_url, product_source)
                    _product_description = self.get_product_description(_product_url, product_source)
                    _sub_category_info, _sub_category_dic = self.get_sub_category_info_and_dic(_product_url, product_source)
                    _price, _discount_price = self.get_product_price(_product_url, product_source)

                    try:
                        product_info = ProductInfo.objects.create(
                            product_name=_product_name, product_url=_product_url, product_description=_product_description,
                            product_no=_product_no, brand_info=_brand_info, platform_info=self.platform_info,
                            original_price=_price, discount_price=_discount_price, gender_info=_gender_info,
                            sub_category_info=_sub_category_info, sub_category_dic=_sub_category_dic
                        )
                        self.logger.debug('Success|create product_info: ' + str(product_info.product_url))
                    except Exception as e:
                        self.logger.error('Unexpected Fail|create or get product_info: ' + _product_url + ' Cause: ' + str(e))
                        continue
                # _img_url_list = self.get_image_list(_product_url, product_source)
                # product_image = ProductImage.objects.filter(product_info=product_info)
                #
                # for img_url in _img_url_list:
                #     try:
                #         # 똑같은 주소가 아니라면 업데이트
                #         product_image.filter(image_path=img_url)
                #     except ProductImage.DoesNotExist:
                #         ProductImage.objects.create(
                #             product_info=product_info,
                #             image_path=img_url,
                #         )
                #         self.logger.debug('Success|create product image: ' + str(img_url))

                    if size_info is None:
                        self.logger.info('no size data')
                    else:
                        self.save_size_table(_product_url, None, _sub_category_dic, size_info)

    def save_size_table(self, product_url, category_dic, sub_category_dic, _size_info):
        """
        class 에 저장된 정보를 db 로 옮기는 작업
        """
        product_info = ProductInfo.objects.get(product_url=product_url)
        try:
            size_unit_list = _size_info.pop('사이즈')
        except KeyError:
            size_unit_list = ['Free']
        size_part_list = list(_size_info.keys())
        # size_info 에서 product_info 기준으로 검색 되는것이 있으면 중복으로 체크하고 넘어가기
        for size_part_name in size_part_list:

            try:
                _size_standard_info = SizeStandard.objects.get(size_standard_name="cm")
                self.logger.debug('Success|get_size_standard_info: ' + str(_size_standard_info))
            except SizeStandard.DoesNotExist:
                _size_standard_info = SizeStandard.objects.create(size_standard_name="cm")
                self.logger.debug('Success|create_size_standard_info: ' + str(_size_standard_info))
            except Exception as e:
                _size_standard_info = None
                self.logger.info('Fail|create_or_get_size_standard_info: ' + product_url + ' Cause: ' + str(e))

            # _category_size_part_info, _category_size_part_dic = self.get_category_size_part_info_and_dic(size_part_name, category_dic)
            _sub_category_size_part_info, _sub_category_size_part_dic = self.get_sub_category_size_part_info_and_dic(size_part_name, sub_category_dic)

            size_value_partial_list = list(_size_info.get(size_part_name))
            for idx, size_value in enumerate(size_value_partial_list):
                if size_value == "":
                    size_value = None
                # 중복이면 업데이트
                try:
                    _size_info_res = SizeInfo.objects.get(
                        size_unit=size_unit_list[idx], product_info=product_info, size_standard=_size_standard_info,
                        # category_size_part_info=_category_size_part_info,
                        # category_size_part_dic=_category_size_part_dic,
                        sub_category_size_part_info=_sub_category_size_part_info,
                        sub_category_size_part_dic=_sub_category_size_part_dic
                    )
                    _size_info_res.size_value = size_value
                    _size_info_res.save()
                    self.logger.debug('Success|update size_info: ' + str(_size_info_res))
                except SizeInfo.DoesNotExist:
                    # 없으면 새로 만들기
                    try:
                        _size_info_res = SizeInfo.objects.create(
                            size_unit=size_unit_list[idx], size_value=size_value, product_info=product_info,
                            size_standard=_size_standard_info,
                            # category_size_part_info=_category_size_part_info,
                            # category_size_part_dic=_category_size_part_dic,
                            sub_category_size_part_info=_sub_category_size_part_info,
                            sub_category_size_part_dic=_sub_category_size_part_dic
                        )
                        self.logger.debug('Success|create size_info: ' + str(_size_info_res))
                    except Exception as e:
                        self.logger.info('Fail|create size_info' + product_url + ' Cause: ' + str(e))
                except Exception as e:
                    self.logger.error('Fail|' + product_url + ' Cause: ' + str(e))

    def get_size_table(self, product_url, product_source):
        try:
            size_div = product_source.find("div", class_="data_size")
        except AttributeError as e:
            self.logger.info('Fail|get size_div: ' + product_url + ' Cause: ' + str(e))
            return None
        except Exception as e:
            self.logger.error('Unexpected Fail|get size_div: ' + product_url + ' Cause: ' + str(e))
            return None
        try:
            table = size_div.find("table", class_="tbl_info")
        except AttributeError as e:
            self.logger.info('Fail|get size_table: ' + product_url + ' Cause: ' + str(e))
            return None
        except Exception as e:
            self.logger.error('Unexpected Fail|get size_table: ' + product_url + ' Cause: ' + str(e))
            return None

        # table = soup.find("table")
        size_data = {}
        if table is None:
            if size_div.find('table') is not None:
                try:
                    table = size_div.find('table')
                    headings = [td.get_text(strip=True) for td in table.find('tr').find_all('td')]
                    headings[0] = '사이즈'
                    _list = []
                    for td in [tr.find_all('td') for tr in table.find_all('tr')[1:]]:
                        text_data = [inner_td.get_text(strip=True) for inner_td in td]
                        _list.append(text_data)
                    for idx, heading in enumerate(headings):
                        data_list = [info[idx] for info in _list]
                        size_data[heading] = data_list
                except Exception as e:
                    self.logger.info('Fail|get size_data: ' + product_url + ' Cause: ' + str(e))
                    return None

            elif product_source.find('table', class_='size_info') is not None:
                try:
                    table = product_source.find('table', class_='size_info')
                    headings = [th.get_text(strip=True) for th in table.find('tr').find_all('th')]
                    tbody = table.find_all('tr')[1:]
                    _list = []
                    for tr in tbody:
                        td_list = tr.find_all('td')
                        if len(td_list) is not len(headings):
                            continue
                        _list.append([td.get_text(strip=True) for td in td_list])
                    for idx, heading in enumerate(headings):
                        data_list = [info[idx] for info in _list]
                        size_data[heading] = data_list
                except Exception as e:
                    self.logger.info('Fail|get size_data: ' + product_url + ' Cause: ' + str(e))
                    return None

        else:
            try:
                headings = [th.get_text() for th in table.find("tbody").find_all("th")]
                for index, row in enumerate(table.find_all("tr")):
                    data_list = []
                    for td in row.find_all("td"):
                        data_list.append(td.get_text())
                    size_data[headings[index]] = data_list
            except Exception as e:
                self.logger.info('Fail|get size_data: ' + product_url + ' Cause: ' + str(e))
                return None

        if size_data == {}:
            size_data = None
        return size_data

    def get_product_price(self, product_url, product_source):
        _price, _discount_price = None, None
        try:
            _discount_price, _price  = product_source.find('div', class_='price').find('em').get_text().split('\xa0')
            self.logger.debug('Success: ' + _price + ', ' + _discount_price)
        except ValueError:
            _price = product_source.find('div', class_='price').find('em').get_text()
            self.logger.debug('Success: ' + _price)
        except Exception as e:
            self.logger.error('Unexpected Fail: ' + product_url + ' Cause: ' + str(e))
            return None, None

        ret_price = 0
        for idx in range(len(_price)):
            try:
                tmp_value = int(_price[idx])
                ret_price *= 10
                ret_price += tmp_value
            except ValueError:
                continue

        ret_sale_price = 0
        try:
            for idx in range(len(_discount_price)):
                try:
                    tmp_value = int(_discount_price[idx])
                    ret_sale_price *= 10
                    ret_sale_price += tmp_value
                except ValueError:
                    continue
        except Exception:
            # 세일 가격이 없는 경우
            ret_sale_price = None

        return ret_price, ret_sale_price

    def get_product_name(self, product_url, product_source):
        _name = None
        try:
            _name = product_source.find('h1', id='goodDtlTitle').get_text(strip=True)
            self.logger.debug('Success: ' + _name)
        except AttributeError:
            self.logger.info('Fail: ' + product_url)
        except Exception as e:
            self.logger.error('Unexpected Fail: ' + product_url + ' Cause: ' + str(e))
        return _name

    def get_product_no(self, product_url, product_source):
        _no = None
        try:
            _no = product_source.select_one('h3.brand > small').get_text(strip=True)
            self.logger.debug('Success: ' + _no)
        except AttributeError:
            self.logger.info('Fail: ' + product_url)
        except Exception as e:
            self.logger.error('Unexpected Fail: ' + product_url + ' Cause: ' + str(e))

        return _no

    def get_gender_info(self, product_url, product_source):
        try:
            _gender_name = product_source.select_one('#location > span:nth-child(2) > a:nth-child(1)').get_text(strip=True)
            self.logger.debug('Success|get gender_name: ' + str(_gender_name))
        except Exception as e:
            self.logger.info('Fail|get_gender_name: ' + product_url + ' Cause: ' + str(e.args))
            return self.gender_info.filter(gender_info_id=3).get(), None

        try:
            _gender_dic = GenderDic.objects.get(gender_similar=_gender_name.upper())
            _gender_info = _gender_dic.gender_info
            self.logger.debug('Success|get gender_dic: ' + str(_gender_dic))
        except GenderDic.DoesNotExist:
            _gender_dic = GenderDic.objects.create(gender_similar=_gender_name.upper())
            _gender_info = self.gender_info.filter(gender_info_id=3).get()
            self.logger.debug('Success|create gender_dic: ' + str(_gender_dic))
        except Exception as e:
            _gender_dic = GenderDic.objects.create(gender_similar=_gender_name.upper())
            _gender_info = self.gender_info.filter(gender_info_id=3).get()
            self.logger.info('Fail|get_or_create gender_dic: ' + product_url + ' Cause: ' + str(e))

        return _gender_info, _gender_dic

    def get_product_description(self, product_url, product_source):
        ret_desc = product_source.find('div', class_='write_txt')
        if ret_desc is not None:
            ret_desc = ret_desc.get_text(strip=True)
        return ret_desc

    def get_brand_info(self, brand_name):
        try:
            brand_info = self.brand_info.filter(brand_name=brand_name).get()
            self.logger.debug('Success|' + brand_info.brand_url)
        except BrandInfo.DoesNotExist:
            self.logger.info('Fail|BrandInfo does not exist' + brand_name)
            self.update_brand_list()
            brand_info = self.brand_info.filter(brand_name=brand_name).get()
        except Exception as e:
            self.logger.error('Unexpected Fail|' + brand_name + str(e))
            brand_info = None

        return brand_info

    def get_category_info_and_dic(self, product_url, product_source):
        pass

    def get_sub_category_info_and_dic(self, product_url, product_source):
        sub_category_name = ""
        try:
            spans = product_source.find('section', id='location').find_all('span')[-2:]
        except Exception as e:
            return None, None
        for span in spans:
            sub_category_name += span.get_text(strip=True) + " "
        _sub_category_name = sub_category_name.rstrip()

        try:
            _sub_category_dic = SubCategoryDic.objects.get(sub_category_similar=_sub_category_name)
            _sub_category_info = _sub_category_dic.sub_category_info
            self.logger.debug('Success|get_sub_category_dic: ' + _sub_category_dic.sub_category_similar)
        except SubCategoryDic.DoesNotExist:
            _sub_category_dic = SubCategoryDic.objects.create(sub_category_similar=_sub_category_name)
            _sub_category_info = _sub_category_dic.sub_category_info
            self.logger.debug('Success|create_sub_category_dic: ' + _sub_category_dic.sub_category_similar)
        except Exception as e:
            self.logger.info('Fail|get_or_create_sub_category_dic and _info: ' + _sub_category_name + ' Cause: ' + str(e))
            return None, None
        return _sub_category_info, _sub_category_dic

    def get_image_list(self, product_url, product_source):
        '.goods_detail > p:nth-child(5)'
        ret_list = []
        # bs = BeautifulSoup(product_source, 'html.parser')
        # bs.

        return ret_list

    def get_category_size_part_info_and_dic(self, size_part_name, category_dic):
        category_size_part_querySet = self.category_size_part_dic.filter(category_size_part_similar=size_part_name)
        self.logger.debug(category_size_part_querySet)
        if category_size_part_querySet is not None:
            try:
                for size_part_dic in category_size_part_querySet:
                    # CategorySizePartDic
                    size_part_info = size_part_dic.category_size_part_info

                    if size_part_info.category_info == category_dic.category_info:
                        self.logger.debug('Success|get_category_size_part_dic: ' + str(size_part_dic))
                        return size_part_info, size_part_dic
            except Exception as e:
                self.logger.error('Fail|get_category_size_part_dic: ' + str(category_size_part_querySet) + ', Cause: ' + str(e))

        size_part_info = None
        # size_part_info = CategorySizePartInfo.objects.create(
        #     category_size_part_name=size_part_name, category_info=category_dic.category_info,
        #     category_dic=category_dic
        # )
        # self.logger.debug('Success|create_category_size_part_info: ' + str(size_part_info))
        size_part_dic = CategorySizePartDic.objects.create(
            category_size_part_similar=size_part_name, category_size_part_info=size_part_info
        )
        self.logger.debug('Success|create_category_size_part_dic: ' + str(size_part_dic))
        return size_part_info, size_part_dic

    def get_sub_category_size_part_info_and_dic(self, size_part_name, sub_category_dic):
        sub_category_size_part_querySet = self.sub_category_size_part_dic.filter(sub_category_size_part_similar=size_part_name)
        self.logger.debug(sub_category_size_part_querySet)
        if sub_category_size_part_querySet is not None:
            try:
                for size_part_dic in sub_category_size_part_querySet:
                    # SubCategorySizePartDic
                    size_part_info = size_part_dic.sub_category_size_part_info

                    if size_part_info.sub_category_info == sub_category_dic.sub_category_info:
                        self.logger.debug('Success|get_sub_category_size_part_dic: ' + str(size_part_dic))
                        return size_part_info, size_part_dic
            except Exception as e:
                self.logger.error('Fail|get_sub_category_size_part_dic: ' + str(sub_category_size_part_querySet) + ', Cause: ' + str(e))
        size_part_info = None
        # size_part_info = SubCategorySizePartInfo.objects.create(
        #     sub_category_size_part_name=size_part_name, sub_category_info=sub_category_dic.sub_category_info,
        #     sub_category_dic=sub_category_dic
        # )
        # self.logger.debug('Success|create_sub_category_size_part_info: ' + str(size_part_info))
        size_part_dic = SubCategorySizePartDic.objects.create(
            sub_category_size_part_similar=size_part_name, sub_category_size_part_info=size_part_info
        )
        self.logger.debug('Success|create_sub_category_size_part_dic: ' + str(size_part_dic))
        return size_part_info, size_part_dic

    def get_review_html(self, product_url, product_source):
        pass

'''
from crawler.crawler_ssf import SsfCrawler
crawler = SsfCrawler(0)
crawler.update_brand_list()
brand_dic = crawler.get_brand_dic()
brand_main_url_dic = crawler.get_brand_main_url_dic(brand_dic)
product_url_dic = crawler.get_product_url_dic(brand_main_url_dic)
crawler.get_product_detail(False, product_url_dic)
'''