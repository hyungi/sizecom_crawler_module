from crawler.crawler_interface import PlatformCrawler
from crawler.models import *
from datetime import datetime


class MusinsaCrawler(PlatformCrawler):
    # TODO: Test Code 작성 >> 핵심 method 별로 외부 접근시 동작 확인이 가능한 정도 / manager class 작성 필요
    # TODO: error logging 하는 class 설계

    def get_review_html(self, product_url, product_source):
        pass

    def __init__(self, debug_level, name='Musinsa', url='https://store.musinsa.com'):
        super().__init__(debug_level, name, url)
        self.size_info = {}
        self.platform_info = None
        self.product_info = None
        self.brand_info = None
        self.category_size_part_info = None
        self.category_size_part_dic = None
        self.sub_category_size_part_info = None
        self.sub_category_size_part_dic = None
        self.gender_info = None
        self.size_standard = ""

        try:
            self.platform_info = PlatformInfo.objects.get(platform_name=self.name)
        except PlatformInfo.DoesNotExist:
            self.platform_info = PlatformInfo.objects.create(platform_name=self.name, platform_url=self.url)
        except Exception as e:
            self.logger.error('Unexpected Fail|get platform_info: ' + self.url + ' Cause: ' + str(e))

    def update_brand_list(self):
        """
        DB에 저장된 brand 들을 불러와 set 형태로 저장한 뒤 크롤링한 brand_set 과 비교하여 새롭게 추가된 브랜드만 db에 업데이트 한다.
        :return _cnt_new_brand_list:업데이트한 BrandInfo 의 갯수를 return 한다
        """
        # 1. 브랜드 list 를 먼저 긁어온다
        # 브랜드 list 를 긁어온뒤, db 에서 브랜드 list 를 또한 가져와서 비교 한다음 없는 친구만 update 하기
        # 2. 완성한 브랜드 리스트를 바탕으로 해당 브랜드별 상세  페이지를 얻어낸다. 품절 옵션 추가.
        # https://store.musinsa.com/app/brand/goods_list/{brandname}?brand_code={brandname}&page=1&ex_soldout=Y

        _brand_list_url = self.url + '/app/contents/brandshop'
        _crawled_brand_dict = {}
        try:
            _brand_detail_url_list = self.get_page_html(_brand_list_url).find_all('li', attrs={'class': 'brand_li'})

            for brand_detail in _brand_detail_url_list:
                _crawled_brand_dict.update(
                    {brand_detail.find('a').get_text(strip=True): self.url + brand_detail.find('a', href=True)['href']}
                )

            _crawled_brand_set = set([brand_detail.find('a').get_text(strip=True) for brand_detail in _brand_detail_url_list])
            _current_brand_set = set(BrandInfo.objects.filter(platform_info=self.platform_info).values_list('brand_name', flat=True))
            _new_brand_list = list(_crawled_brand_set.difference(_current_brand_set))
            self.logger.debug('Success|number of new_brand_list: ' + str(len(_new_brand_list)))
        except Exception as e:
            _new_brand_list = []
            self.logger.error('Fail|make _new_brand_list: ' + str(e))

        try:
            for _brand_name in _new_brand_list:
                _brand_url = _crawled_brand_dict.get(_brand_name).strip()
                # 바로 생성하는 케이스 > 인스턴스 만들고 save 하는 것으로 변경
                model_instance = BrandInfo(
                    brand_name=_brand_name, brand_url=_brand_url, platform_info=self.platform_info
                )
                model_instance.save()
                self.logger.debug('Success|update brand_info: ' + str(model_instance.brand_name))

            _cnt_new_brand_list = len(_new_brand_list)
            self.logger.debug('Success|number of update BrandInfo: ' + str(_cnt_new_brand_list))

        except Exception as e:
            self.logger.debug('Fail|update BrandInfo: ' + str(e))
            _cnt_new_brand_list = None

        return _cnt_new_brand_list

    def get_brand_dic(self, brand_name_list=['MUSINSA STANDARD', '5252BYOIOI', 'ROMANTICPIRATES', 'GROOVE RHYME', 'COVERNAT', 'DRAW FIT']):
        """
        :param brand_name_list: 이 리스트가 존재 한다면 해당 브랜드들만 크롤링한다. 기본값은 특정 브랜드 리스트
        :return brand_dic: {brand_name: brand_url} 로 구성된 dictionary 를 return 한다
        """
        brand_info = dict(BrandInfo.objects.filter(platform_info=self.platform_info).values_list('brand_name','brand_url'))
        if brand_name_list is not None:
            brand_dic = {}
            for brand_name in brand_name_list:
                brand_dic.update({brand_name: brand_info.get(brand_name)})
            return brand_dic
        else:
            return brand_info

    def get_brand_main_url_dic(self, brand_dic):
        """
        :param brand_dic: brand_dic 바탕으로 각 브랜드별 상세 페이지를 얻어낸다. 품절 옵션 추가.
        https://store.musinsa.com/app/brand/goods_list/{brand_name}?brand_code={brand_name}&page=1&ex_soldout=Y
        :return brand_main_url_list: 각 브랜드별 품절 옵션이 추가된 모든 페이지 url 을 return 한다.
        """
        brand_main_url_dic = {}
        for _brand_name in brand_dic.keys():
            brand_main_url_list = []
            brand_url = brand_dic.get(_brand_name)
            page_list = []
            try:
                page_list = self.get_page_html(brand_url).find(
                    'div', attrs={'class': 'pagination'}
                ).find_all('a', attrs={'class': 'paging-btn'})
                self.logger.debug('Success|get page_list of brand / number of page_list: ' + str(len(page_list) - 4))
            except Exception as e:
                self.logger.info('Fail|make page_list of brand: ' + _brand_name + ', ' + brand_url + str(e.args))

            total_list = [page.get_text(strip=True) for page in page_list][2:-2]
            if len(total_list) < 1:
                self.logger.debug('brand has no products ' + brand_url)
            else:
                for list_num in total_list:
                    brand_main_url_list.append(brand_url + '?page=' + list_num + '&ex_soldout=Y')
            brand_main_url_dic.update({_brand_name: brand_main_url_list})
        return brand_main_url_dic

    def get_product_url_dic(self, brand_main_url_dic):
        """
        :param brand_main_url_dic: 각 브랜드별 품절 옵션이 추가된 모든 페이지의 url을 바탕으로 모든 페이지의 product_url을 추출한다.
        :return: product_url_dic
        """
        _product_url_dic = {}
        for _brand_name in brand_main_url_dic.keys():
            _product_url_list = []
            for brand_main_url in brand_main_url_dic.get(_brand_name):
                link_bs = self.get_page_html(brand_main_url).select('#searchList > li > div.li_inner > div.list_img > a')
                for link in link_bs:
                    _product_url_list.append(self.url + link.get("href"))
            _product_url_list = list(set(_product_url_list))
            _product_url_dic.update({_brand_name: _product_url_list})
        return _product_url_dic

    def get_product_detail(self, overlap_chk, product_url_dic):
        # brand_main_url_list = self.get_product_url_list()
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
                    _price, _sale_price = self.get_product_price(_product_url, product_source)
                    if _sale_price is not None:
                        product_info.discount_price = _sale_price
                        product_info.update()
                        PriceTrackingInfo.objects.create(
                            discount_price=_sale_price, update_date=datetime.now(), product_info=product_info.get()
                        )
                    self.logger.debug('Success|product_info already exist: ' + str(product_info.product_url))
                    continue

                else:
                    product_source = self.get_page_html(_product_url)
                    self.size_info = self.get_size_table(_product_url, product_source)
                    _gender_info, _gender_dic = self.get_gender_info(_product_url, product_source)
                    _product_name = self.get_product_name(_product_url, product_source)
                    _product_no = self.get_product_no(_product_url, product_source)
                    _product_description = self.get_product_description(_product_url, product_source)
                    _category_info, _category_dic = self.get_category_info_and_dic(_product_url, product_source)
                    _sub_category_info, _sub_category_dic = self.get_sub_category_info_and_dic(_product_url, product_source, _category_dic)
                    _price, _sale_price = self.get_product_price(_product_url, product_source)

                    try:
                        product_info = ProductInfo.objects.create(
                            product_name=_product_name, product_url=_product_url, product_description=_product_description,
                            product_no=_product_no, brand_info=_brand_info, original_price=_price, discount_price=_sale_price,
                            category_info=_category_info, category_dic=_category_dic, sub_category_info=_sub_category_info,
                            sub_category_dic=_sub_category_dic, platform_info=self.platform_info, gender_info=_gender_info
                        )
                        self.logger.debug('Success|create product_info: ' + str(product_info.product_url))
                    except Exception as e:
                        self.logger.error('Unexpected Fail|create or get product_info: ' + _product_url + ' Cause: ' + str(e))
                        continue

                    _img_url_list = self.get_image_list(_product_url, product_source)
                    product_image = ProductImage.objects.filter(product_info=product_info)

                    for img_url in _img_url_list:
                        try:
                            # 똑같은 주소가 아니라면 업데이트
                            product_image.filter(image_path=img_url)
                        except ProductImage.DoesNotExist:
                            ProductImage.objects.create(
                                product_info=product_info,
                                image_path=img_url,
                            )
                            self.logger.debug('Success|create product image: ' + str(img_url))

                    if self.size_info is None:
                        self.logger.info('no size data')
                    else:
                        self.save_size_table(product_info, _category_dic, _sub_category_dic)

    def save_size_table(self, product_info, category_dic, sub_category_dic):
        """
        class 에 저장된 정보를 db 로 옮기는 작업
        """
        _size_info = self.size_info
        size_unit_list = _size_info.pop('사이즈')
        size_part_list = list(_size_info.keys())

        for size_part_name in size_part_list:
            try:
                _size_standard_info = SizeStandard.objects.get(size_standard_name=self.size_standard)
                self.logger.debug('Success|get_size_standard_info: ' + str(_size_standard_info))
            except SizeStandard.DoesNotExist:
                _size_standard_info = SizeStandard.objects.create(size_standard_name=self.size_standard)
                self.logger.debug('Success|create_size_standard_info: ' + str(_size_standard_info))
            except Exception as e:
                _size_standard_info = None
                self.logger.info('Fail|create_or_get_size_standard_info: ' + product_info.product_url + ' Cause: ' + str(e))

            _category_size_part_info, _category_size_part_dic = self.get_category_size_part_info_and_dic(size_part_name, category_dic)
            _sub_category_size_part_info, _sub_category_size_part_dic = self.get_sub_category_size_part_info_and_dic(size_part_name, sub_category_dic)

            size_value_partial_list = list(_size_info.get(size_part_name))
            for idx, size_value in enumerate(size_value_partial_list):
                if size_value == "":
                    size_value = None
                # 중복이면 업데이트
                try:
                    _size_info_res = SizeInfo.objects.get(
                        size_unit=size_unit_list[idx], product_info=product_info,
                        size_standard=_size_standard_info,
                        category_size_part_info=_category_size_part_info,
                        category_size_part_dic=_category_size_part_dic,
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
                            category_size_part_info=_category_size_part_info,
                            category_size_part_dic=_category_size_part_dic,
                            sub_category_size_part_info=_sub_category_size_part_info,
                            sub_category_size_part_dic=_sub_category_size_part_dic
                        )
                        self.logger.debug('Success|create size_info: ' + str(_size_info_res))
                    except Exception as e:
                        self.logger.info('Fail|create size_info: ' + product_info.product_url + 'Cause: ' + str(e))
                except Exception as e:
                    self.logger.info('Fail|get size_info: ' + product_info.product_url + ' Cause: ' + str(e))

    def get_brand_info(self, brand_name):
        try:
            brand_info = self.brand_info.filter(brand_name=brand_name).get()
            self.logger.debug('Success|' + brand_info.brand_url)
        except BrandInfo.DoesNotExist:
            self.logger.info('Fail|BrandInfo does not exist' + brand_name)
            self.update_brand_list()
            brand_info = self.brand_info.filter(brand_name=brand_name).get()
        except Exception as e:
            self.logger.info('Unexpected Fail|' + brand_name + str(e))
            brand_info = None

        return brand_info

    def get_category_info_and_dic(self, product_url, product_source):
        try:
            _category_name = product_source.select_one('.item_categories').find_all('a')[1].get_text(strip=True)
            self.logger.debug('Success|get category_name: ' + str(_category_name))
        except Exception as e:
            self.logger.info('Fail|get category_name: ' + product_url + ' Cause: ' + str(e))
            return None, None

        try:
            _category_dic = CategoryDic.objects.get(category_similar=_category_name)
            _category_info = _category_dic.category_info
            self.logger.debug('Success|get_category_dic: ' + _category_dic.category_similar)
        except CategoryDic.DoesNotExist:
            _category_info = CategoryInfo.objects.create(category_name=_category_name)
            _category_dic = CategoryDic.objects.create(
                category_similar=_category_name, category_info=_category_info
            )
            self.logger.debug('Success|create_category_dic: ' + _category_dic.category_similar)
        except Exception as e:
            self.logger.info(
                'Fail|get_or_create_category_dic and _info: ' + _category_name + ' Cause: ' + str(e))
            return None, None
        return _category_info, _category_dic

    def get_sub_category_info_and_dic(self, product_url, product_source, category_dic):
        try:
            _sub_category_name = product_source.select_one('.item_categories').find_all('a')[2].get_text(strip=True)
            self.logger.debug('Success|get_sub_category_name: ' + str(_sub_category_name))
        except Exception as e:
            self.logger.info('Fail|get get_sub_category_name: ' + product_url + ' Cause: ' + str(e))
            return None, None

        try:
            _sub_category_dic = SubCategoryDic.objects.get(sub_category_similar=_sub_category_name)
            _sub_category_info = _sub_category_dic.sub_category_info
            if _sub_category_info.category_info is None:
                _sub_category_info.category_info = category_dic.category_info
            if _sub_category_info.category_dic is None:
                _sub_category_info.category_dic = category_dic
            _sub_category_info.save()
            self.logger.debug('Success|get_sub_category_dic: ' + _sub_category_dic.sub_category_similar)
        except SubCategoryDic.DoesNotExist:
            _sub_category_info = SubCategoryInfo.objects.create(
                sub_category_name=_sub_category_name, category_info=category_dic.category_info, category_dic=category_dic
            )
            _sub_category_dic = SubCategoryDic.objects.create(
                sub_category_similar=_sub_category_name, sub_category_info=_sub_category_info
            )
            self.logger.debug('Success|create_sub_category_dic: ' + _sub_category_dic.sub_category_similar)
        except Exception as e:
            self.logger.info('Fail|get_or_create_sub_category_dic and _info: ' + _sub_category_name + ' Cause: ' + str(e))
            return None, None
        return _sub_category_info, _sub_category_dic

    def get_image_list(self, product_url, product_source):
        ret_list = []
        img_bs_list = product_source.select_one('#detail_view')
        if img_bs_list is None:
            return ret_list
        else:
            img_bs_list = img_bs_list.find_all('img')
        # file_name = os.getcwd() + file_name
        for idx, img_bs in enumerate(img_bs_list):
            img_url = img_bs['src'][2:]
            img_url = img_url[img_url.find('//') + 1:]
            if img_url[0] == '/':
                img_url = img_url[1:]
            ret_list.append(img_url)
            # urllib.request.urlretrieve(img_url, file_name + '_' + str(idx) + '.jpg')
        self.logger.debug('in update_image - img_url_list: ' + str(ret_list))
        return ret_list

    def get_size_table(self, product_url, product_source):
        size_table = product_source.find('table', class_='table_th_grey')
        if size_table is None:
            # self.logger.info('no size data')
            return size_table
        try:
            self.size_standard = size_table.find('th').get_text(strip=True)
            self.logger.debug('Success|get size_standard ' + self.size_standard)
        except AttributeError:
            # 사이즈 조견표가 아닌 정보가 들어있는 경우임
            self.logger.info('Fail|get size_standard')
            return None
        except Exception as e:
            self.logger.info('Fail|get size_standard, Cause ' + str(e))
            return None

        headings = []
        thead = size_table.find_all('th', class_='item_val')
        tbody = []
        try:
            headings = [th.get_text(strip=True) for th in thead]
            headings.insert(0, '사이즈')
            self.logger.debug('Success|get headings ' + str(headings))
            # headings
            tbody = size_table.find('tbody').find_all('tr')[2:]
        except Exception as e:
            self.logger.info('Fail|get headings ' + product_url + ' Cause: ' + str(e.args))
        _list = []
        for tb in tbody:
            tb_list = tb.find_all()
            _list.append([tl.get_text() for tl in tb_list])
        ret_data = {}
        for idx, heading in enumerate(headings):
            data_list = [info[idx] for info in _list]
            ret_data[heading] = data_list
        return ret_data

    def get_product_price(self, product_url, product_source):
        try:
            price = product_source.select_one('#goods_price').text.strip()
            self.logger.debug('Success|get_original_price ' + price)
            ret_price = 0
            for idx in range(len(price)):
                try:
                    tmp_value = int(price[idx])
                    ret_price *= 10
                    ret_price += tmp_value
                except ValueError:
                    continue

            try:
                sale_price = product_source.select_one('#sale_price').text.strip()
                self.logger.info('Success|get_sale_price: ' + sale_price)
                ret_sale_price = 0
                for idx in range(len(sale_price)):
                    try:
                        tmp_value = int(sale_price[idx])
                        ret_sale_price *= 10
                        ret_sale_price += tmp_value
                    except ValueError:
                        continue
            except AttributeError:
                # 세일 가격이 없는 경우
                ret_sale_price = None

            return ret_price, ret_sale_price

        except Exception as e:
            self.logger.info('Fail|get_product_price ' + product_url + ' Cause: ' + str(e))
            return None, None

    def get_product_name(self, product_url, product_source):
        try:
            name = product_source.find('span', class_="product_title").get_text(strip=True)
            return name
        except Exception as e:
            self.logger.info('Fail|' + product_url + ' Cause: ' + str(e))
            return None

    def get_product_no(self, product_url, product_source):
        try:
            # TODO: class id가 있는건 class id 를 통해 긁어오자 selector 말고
            no = product_source.find('div', class_='explan_product product_info_section').find('p', class_='product_article_contents').get_text(strip=True)
            no = no[no.find('/') + 1:]
            self.logger.debug('Success|' + no)
            return no
        except Exception as e:
            self.logger.info('Fail|' + product_url + ' Cause: ' + str(e))
            return None

    def get_gender_info(self, product_url, product_source):
        try:
            _gender_name = product_source.select_one('.txt_gender').get_text(strip=True)
        except Exception as e:
            self.logger.info('Fail|get_gender_name: ' + product_url + ' Cause: ' + str(e))
            return self.gender_info.filter(gender_info_id=3).get(), None

        try:
            _gender_dic = GenderDic.objects.get(gender_similar=_gender_name)
            _gender_info = _gender_dic.gender_info
            self.logger.debug('Success|get gender_dic: ' + str(_gender_dic))
        except GenderDic.DoesNotExist:
            _gender_dic = GenderDic.objects.create(gender_similar=_gender_name)
            _gender_info = self.gender_info.filter(gender_info_id=3).get()
            self.logger.debug('Success|create gender_dic: ' + str(_gender_dic))
        except Exception as e:
            _gender_dic = GenderDic.objects.create(gender_similar=_gender_name)
            _gender_info = self.gender_info.filter(gender_info_id=3).get()
            self.logger.info('Fail|get_or_create gender_dic:' + product_url + ' Cause: ' + str(e))

        return _gender_info, _gender_dic

    def get_product_description(self, product_url, product_source):
        ret_desc = product_source.select_one('#detail_view')
        if ret_desc is not None:
            ret_desc = ret_desc.get_text(strip=True)
        return ret_desc

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

        size_part_info = CategorySizePartInfo.objects.create(
            category_size_part_name=size_part_name, category_info=category_dic.category_info,
            category_dic=category_dic
        )
        self.logger.debug('Success|create_category_size_part_info: ' + str(size_part_info))
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

        size_part_info = SubCategorySizePartInfo.objects.create(
            sub_category_size_part_name=size_part_name, sub_category_info=sub_category_dic.sub_category_info,
            sub_category_dic=sub_category_dic
        )
        self.logger.debug('Success|create_sub_category_size_part_info: ' + str(size_part_info))
        size_part_dic = SubCategorySizePartDic.objects.create(
            sub_category_size_part_similar=size_part_name, sub_category_size_part_info=size_part_info
        )
        self.logger.debug('Success|create_sub_category_size_part_dic: ' + str(size_part_dic))
        return size_part_info, size_part_dic


# TODO: business logic 상 필요한 기능을 만들기 위해 위의 method 들을 조합해야 한다는 것을 고려하자
'''
dict_sample = {
    'Top':
        {
            product_name:
                {
                    '사이즈': ['XS', 'S', 'M', 'L', 'XL']
                    ...
                }
        }

}
from crawler.crawler_musinsa import MusinsaCrawler
crawler = MusinsaCrawler(0)
crawler.update_brand_list()
brand_dic = crawler.get_brand_dic()
brand_main_url_dic = crawler.get_brand_main_url_dic(brand_dic)
product_url_dic = crawler.get_product_url_dic(brand_main_url_dic)
crawler.get_product_detail(False, product_url_dic)
'''