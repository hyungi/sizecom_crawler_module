from crawler.crawler_interface import PlatformCrawler
from crawler.models import *


class UniqloCrawler(PlatformCrawler):

    def __init__(self, debug_level, name='Uniqlo', url='https://store-kr.uniqlo.com'):
        super().__init__(debug_level, name, url)
        self.category = {}          # 유니클로는 이렇게 할 필요가 있음
        self.sub_category = {}          # 유니클로는 이렇게 할 필요가 있음
        self.platform_info = None
        self.brand_info = None
        self.size_info = {}
        self.brand_name = name
        self.size_standard = ""

        try:
            self.platform_info = PlatformInfo.objects.get(platform_name=self.name)
            self.logger.debug('Success|get_platform_info')
        except PlatformInfo.DoesNotExist:
            self.platform_info = PlatformInfo.objects.create(platform_name=self.name, platform_url=self.url)
            self.logger.debug('Success|create_platform_info')
        except Exception as e:
            self.logger.error('Unexpected Fail|get platform_info: ' + self.url + ' Cause: ' + str(e))

        try:
            self.brand_info = BrandInfo.objects.get(brand_name=self.brand_name, brand_url=self.url + '/index.jsp', platform_info=self.platform_info)
            self.logger.debug('Success|get_brand_info')
        except BrandInfo.DoesNotExist:
            self.brand_info = BrandInfo.objects.create(brand_name=self.brand_name, brand_url=self.url + '/index.jsp', platform_info=self.platform_info)
            self.logger.debug('Success|create_brand_info')
        except Exception as e:
            self.brand_info = None
            self.logger.error('Unexpected Fail|get_or_create_brand_info, Cause: ' + str(e))

    def update_brand_list(self):
        pass

    def get_brand_dic(self, brand_name_list):
        """
        uniqlo doesn't need this method
        :return:
        """
        pass

    def get_brand_main_url_dic(self, brand_dict={'Uniqlo': 'https://store-kr.uniqlo.com/index.jsp'}):
        """
        uniqlo doesn't need this method
        :return "Uniqlo main url": https://store-kr.uniqlo.com/index.jsp
        """
        return dict({self.brand_info.brand_name: self.brand_info.brand_url})

    def get_product_url_dic(self, brand_main_url_dic={'Uniqlo': 'https://store-kr.uniqlo.com/index.jsp'}):
        """
        :param brand_main_url_dic: Uniqlo main url 하나만 담아서 전달
        카테고리 별 페이지로 접근하여 각 카테고리 내의 product_url_list 를 추출하고 category dict 에 해당 url 의 정보를 저장한다.
        :return product_url_list: 개별 product_url_list 를 return 한다.
        """
        url = brand_main_url_dic.get('Uniqlo')
        bs = self.get_page_html(url)
        all_info = []
        product_by_sub_category_dict = {}
        self.category = {}
        self.sub_category = {}
        product_url_list = []
        for idx in range(3, 7):
            all_info.append(bs.find_all("div", class_="gnb_2016_col col" + str(idx), limit=2))

        for partial_info in all_info:
            for info in partial_info[:2]:
                _category = info.find('h5').get_text(strip=True)
                for inner in info.find_all("a", href=True):
                    try:
                        bs = self.get_page_html(self.url + inner['href'])
                        _sub_category = inner.get_text(strip=True)
                        self.logger.debug('Success|get_sub_category')
                    except Exception as e:
                        bs = self.get_page_html(self.url + '/' + inner['href'])
                        _sub_category = inner.get_text(strip=True)
                        self.logger.info('Fail|get_sub_category: ' + self.url + '/' + inner['href'] + ' Cause: ' + str(e))

                    self.category.update({_sub_category: _category})
                    # self.logger.debug('category_main_list_url: ' + self.url + '/' + inner['href'])
                    product_by_sub_category_dict.update({_sub_category: bs.find_all('p', class_="tumb_img")})

                category_list = product_by_sub_category_dict.keys()

                for category in category_list:
                    for product in product_by_sub_category_dict.get(category):
                        try:
                            _product_url = self.url + product.find("a", href=True)['href']
                            self.sub_category.update({_product_url: category})
                            product_url_list.append(_product_url)
                            self.logger.debug('Success|get_category')
                        except Exception as e:
                            self.logger.info('Fail|get_category: ' + str(product) + ' Cause: ' + str(e))

        return {'Uniqlo': product_url_list}

    def get_product_detail(self, overlap_chk, product_url_dic):
        product_url_list = product_url_dic.get(self.name)
        for _product_url in product_url_list:
            # TODO: 개별 정보를 얻기 위해 접근하는 method 들인데, 각자 get_page_html 을 호출하고 있음, 사전에 한번만 호출하고 param 으로 넣어주는 것이 합리적이지 않을까?
            product_source = self.get_page_html(_product_url)
            _category_info, _category_dic = self.get_category_info_and_dic(_product_url, product_source)
            _sub_category_info, _sub_category_dic = self.get_sub_category_info_and_dic(_product_url, _category_dic)
            _product_name = self.get_product_name(_product_url, product_source)

            if overlap_chk is True and self.overlap_check(_product_url):
                self.logger.info('product info is exist')
                continue

            _price = self.get_product_price(_product_url, product_source)
            _product_no = self.get_product_no(_product_url, product_source)
            _product_description = self.get_product_description(_product_url, product_source)
            _gender_info, _gender_dic = self.get_gender_info(_product_url, product_source)

            try:
                # TODO: platform info 기준으로 product_info 를 뽑아놓고 filter 를 써보자
                _product_info = ProductInfo.objects.get(product_url=_product_url)
                if overlap_chk is True:
                    continue
                else:
                    if self.get_page_html(_product_url).select_one('#limitedPrice') is not None:
                        _product_info.discount_price = _price
                        _product_info.save()
                        PriceTrackingInfo.objects.create(
                            discount_price=_price, update_date=datetime.now(), product_info=_product_info
                        )
                    continue
            except ProductInfo.DoesNotExist:
                _product_info = ProductInfo.objects.create(
                    product_name=_product_name, product_url=_product_url, product_description=_product_description,
                    product_no=_product_no, brand_info=self.brand_info, original_price=_price,
                    category_info=_category_info, category_dic=_category_dic, sub_category_info=_sub_category_info,
                    sub_category_dic=_sub_category_dic, platform_info=self.platform_info, gender_info=_gender_info
                )
            except Exception as e:
                self.logger.error('Unexpected Fail|get_or_create_product_info' + _product_url + ' Cause: ' + str(e))
                continue
            try:
                _size_standard = SizeStandard.objects.get(size_standard_name='cm')
                self.logger.debug('Success|get_size_standard')
            except SizeStandard.DoesNotExist:
                _size_standard = SizeStandard.objects.create(size_standard_name='cm')
                self.logger.debug('Success|create_size_standard')
            except Exception as e:
                _size_standard = None
                self.logger.error('Unexpected Fail|get_or_create_size_standard: ' + _product_url + ' Cause: ' + str(e))

            _img_url_list = self.get_image_list(_product_url, product_source)
            product_image = ProductImage.objects.filter(product_info=_product_info)
            for img_url in _img_url_list:
                try:
                    # 똑같은 주소가 아니라면 업데이트
                    product_image.filter(image_path=img_url)
                except ProductImage.DoesNotExist:
                    ProductImage.objects.create(
                        product_info=_product_info,
                        image_path=img_url,
                    )
                    self.logger.debug('Success|create product image: ' + str(img_url))

            size_table_url = self._get_size_table_url(product_source)
            data = self.get_size_table(size_table_url)
            if data is not None:
                self.save_size_table(data, _product_info, _size_standard)

    def save_size_table(self, size_data, product_info, size_standard):
        size_unit_list = size_data.pop('사이즈')
        size_part_list = list(size_data.keys())

        for size_part in size_part_list:
            try:
                _size_part_dic = SizePartDic.objects.get(size_part_similar=size_part)
                self.logger.debug('Success|get')
            except SizePartDic.DoesNotExist:
                _size_part_dic = SizePartDic.objects.create(size_part_similar=size_part)
                self.logger.debug('Success|create')
            except Exception as e:
                _size_part_dic = None
                self.logger.error('Unexpected Fail|get_size_part_dic: ' + size_part + ' Cause: ' + str(e))

            size_value_partial_list = list(size_data.get(size_part))
            for idx, size_value in enumerate(size_value_partial_list):
                try:
                    _size_info_res = SizeInfo.objects.get(
                        size_unit=size_unit_list[idx], product_info=product_info, size_part_dic=_size_part_dic,
                        size_part_info=_size_part_dic.size_part_info, size_standard=size_standard
                    )
                    _size_info_res.size_value = size_value
                    _size_info_res.save()
                except SizeInfo.DoesNotExist:
                    SizeInfo.objects.create(
                        size_unit=size_unit_list[idx], size_value=size_value, product_info=product_info,
                        size_part_dic=_size_part_dic, size_part_info=_size_part_dic.size_part_info,
                        size_standard=size_standard
                    )
                except Exception as e:
                    self.logger.info('Unexpected Fail|save_size_info: ' + product_info.product_url + ' Cause: ' + str(e))
                    self.logger.info(size_data)

        self.logger.debug(str(size_data))

    def _get_size_table_url(self, product_source):
        try:
            bs = str(product_source)
            from_idx = bs.find('fn_viewSizeTable')
            bs = bs[from_idx:]
            from_idx = bs.find('"')
            bs = bs[from_idx + 1:]
            to_idx = bs.find('"')
            bs = bs[:to_idx]
            self.logger.debug('Success')
        except Exception as e:
            bs = None
            self.logger.info('Fail, Cause: ' + str(e))
        return bs
        """
            // 사이즈조견표
            fn_viewSizeTable = function() {
                var _left = (screen.width)/2 - 636/2 ;
                var _top = (screen.height)/2 - 654/2;
                    window.open(
                    "https://simage-kr.uniqlo.com/goods/31/11/73/73/sizeTable/413117_size.html",
                    "조견표","menubar=no,scrollbars=yes,resizable=yes,status=yes,width=636,height=654,top="+ _top + ",
                    left=" + _left + "");
            }
        """

    def get_size_table(self, table_url):
        try:
            soup = self.get_page_html(table_url)
            table_body = soup.find("tbody")
            headings = [th.text for th in table_body.find_all("th")]
            headings.insert(0, "사이즈")
            size_col = [th.text for th in soup.find("thead").find_all("th")][1:]
            ret_data = {headings[0]: size_col}
            for index, row in enumerate(table_body.find_all("tr")):
                data_list = [td.text for td in row.find_all("td")]
                ret_data.update({headings[index + 1]: data_list})
            self.logger.debug('Success')
        except Exception as e:
            ret_data = None
            self.logger.info('Fail: ' + table_url + ' Cause: ' + str(e))
        return ret_data

    def get_product_price(self, product_url, product_source):
        try:
            price = product_source.select_one('#salePrice').text.strip()
        except AttributeError as e:
            self.logger.info('Fail, Cause: ' + str(e))
            return None
        except Exception as e:
            self.logger.error('Unexpected Fail| ' + product_url + ' Cause: ' + str(e))
            return None

        ret_price = 0
        for idx in range(len(price)):
            try:
                tmp_value = int(price[idx])
                ret_price *= 10
                ret_price += tmp_value
            except Exception:
                continue

        return ret_price

    def get_category_info_and_dic(self, product_url, product_source):
        _sub_category_name = self.sub_category.get(product_url)
        _category_name = self.category.get(_sub_category_name)

        try:
            _category_dic = CategoryDic.objects.get(category_similar=_category_name)
            _category_info = _category_dic.category_info
            self.logger.debug('Success|get')
        except CategoryDic.DoesNotExist:
            _category_dic = CategoryDic.objects.create(category_similar=_category_name)
            _category_info = None
            self.logger.info('Success|create')
        except Exception as e:
            _category_info, _category_dic = None, None
            self.logger.info('Fail|get_or_create: ' + product_url + ' Cause: ' + str(e))

        return _category_info, _category_dic

    def get_sub_category_info_and_dic(self, product_url, category_dic):
        _sub_category_name = self.sub_category.get(product_url)
        self.logger.info('_sub_category_name  ' + _sub_category_name)
        try:
            _sub_category_dic = SubCategoryDic.objects.get(sub_category_similar=_sub_category_name)
            _sub_category_info = _sub_category_dic.sub_category_info
            self.logger.debug('Success|get')
        except SubCategoryDic.DoesNotExist:
            _sub_category_dic = SubCategoryDic.objects.create(sub_category_similar=_sub_category_name)
            _sub_category_info = None
            self.logger.info('Success|create')
        except Exception as e:
            _sub_category_info, _sub_category_dic = None, None
            self.logger.info('Unexpected Fail|get_or_create: ' + product_url + ' Cause: ' + str(e))

        return _sub_category_info, _sub_category_dic

    def get_product_name(self, product_url, product_source):
        try:
            name = product_source.select_one('#goodsNmArea').text.strip()
        except AttributeError as e:
            name = None
            self.logger.info('Fail|' + product_url + ' Cause: ' + str(e))
        except Exception as e:
            name = None
            self.logger.error('Unexpected Fail| ' + product_url + ' Cause: ' + str(e))
        return name

    def get_product_no(self, product_url, product_source):
        try:
            no = product_source.select_one('.number').text.split(':')[1].strip()
        except AttributeError as e:
            no = None
            self.logger.info('Fail|' + product_url + ' Cause: ' + str(e))
        except Exception as e:
            no = None
            self.logger.error('Unexpected Fail| ' + product_url + ' Cause: ' + str(e))
        return no

    def get_gender_info(self, product_url, product_source):
        try:
            _gender_name = product_source.select_one('.pathdetail').get_text(strip=True)
        except AttributeError as e:
            self.logger.info('Fail|' + product_url + ' Cause: ' + str(e))
            return None, None
        except Exception as e:
            self.logger.error('Unexpected Fail| ' + product_url + ' Cause: ' + str(e))
            return None, None

        try:
            _gender_dic = GenderDic.objects.get(gender_similar=_gender_name)
            _gender_info = _gender_dic.gender_info
            self.logger.debug('Success|get')
        except GenderDic.DoesNotExist:
            _gender_dic = GenderDic.objects.create(gender_similar=_gender_name)
            _gender_info = None
            self.logger.debug('Success|create')
        except Exception as e:
            _gender_dic = None
            _gender_info = None
            self.logger.info('Unexpected Fail|get_or_create gender_dic ' + product_url + ' Cause: ' + str(e))
        return _gender_info, _gender_dic

    def get_product_description(self, product_url, product_source):
        try:
            ret_desc = product_source.select_one('dl.spec:nth-child(1)').get_text(strip=True)
        except AttributeError as e:
            ret_desc = None
            self.logger.info('Fail|' + product_url + ' Cause: ' + str(e))
        except Exception as e:
            ret_desc = None
            self.logger.error('Unexpected Fail|' + product_url + ' Cause: ' + str(e))
        if ret_desc is not None:
            ret_desc = ret_desc[:ret_desc.find('※')]
        return ret_desc

    def overlap_check(self, product_url):
        try:
            ProductInfo.objects.get(product_url=product_url)
            self.logger.debug('Success|get')
            return True
        except ProductInfo.DoesNotExist:
            self.logger.debug('Success|create')
            return False
        except Exception as e:
            self.logger.error('Unexpected Fail|' + product_url + " this product is already overlapped in DB must be fixed" + str(e.args))
            return True

    def get_image_list(self, product_url, product_source):
        ret_list = []
        img_bs_list = product_source.find('ul', class_='prodThumbImgs')
        if img_bs_list is not None:
            img_bs_list = img_bs_list.find_all('a', href=True)
        for img_bs in img_bs_list:
            img_url = img_bs['href']
            ret_list.append(img_url)
        try:
            default_img = product_source.find('div', id='prodImgDefault').find('img')['src']
            ret_list.append(default_img)
        except Exception as e:
            self.logger.info('Fail|get_default_img ' + product_url + ' Cause: ' + str(e))

        self.logger.debug('in update_image - img_url_list: ' + str(ret_list))
        return ret_list

    def get_review_html(self, product_url, product_source):
        pass
