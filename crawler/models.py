# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BrandConceptKeyword(models.Model):
    concept_id = models.AutoField(primary_key=True)
    brand_info = models.ForeignKey('BrandInfo', models.DO_NOTHING, blank=True, null=True)
    brand_dic = models.ForeignKey('BrandDic', models.DO_NOTHING, blank=True, null=True)
    keyword_info = models.ForeignKey('KeywordInfo', models.DO_NOTHING, blank=True, null=True)
    method_info = models.ForeignKey('MethodInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'brand_concept_keyword'


class BrandDic(models.Model):
    brand_dic_id = models.AutoField(primary_key=True)
    brand_similar = models.CharField(unique=True, max_length=50)
    brand_info = models.ForeignKey('BrandInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'brand_dic'


class BrandInfo(models.Model):
    brand_info_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=100)
    brand_url = models.CharField(max_length=200)
    brand_country = models.CharField(max_length=10)
    brand_description = models.TextField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    platform_info = models.ForeignKey('PlatformInfo', models.DO_NOTHING, blank=True, null=True)
    sizecom_user = models.ForeignKey('SizecomUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'brand_info'

    def __str__(self):
        return "%s: %s %s" % (self.brand_name, self.brand_url, self.platform_info)


class BrandTrackingInfo(models.Model):
    brand_tracking_info_id = models.AutoField(primary_key=True)
    brand_info = models.ForeignKey(BrandInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'brand_tracking_info'


class CategoryDic(models.Model):
    category_dic_id = models.AutoField(primary_key=True)
    category_similar = models.CharField(max_length=50)
    category_info = models.ForeignKey('CategoryInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'category_dic'

    def __str__(self):
        return "%s | category_info: %s" % (self.category_similar, self.category_info)


class CategoryInfo(models.Model):
    category_info_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=20)

    class Meta:
        # managed = False
        db_table = 'category_info'

    def __str__(self):
        return "%s" % self.category_name


class CategorySizePartDic(models.Model):
    category_size_part_dic_id = models.AutoField(primary_key=True)
    category_size_part_similar = models.CharField(max_length=50)
    category_size_part_info = models.ForeignKey('CategorySizePartInfo', models.DO_NOTHING, blank=True, null=True)
    category_info = models.ForeignKey(CategoryInfo, models.DO_NOTHING, blank=True, null=True)
    category_dic = models.ForeignKey(CategoryDic, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'category_size_part_dic'

    def __str__(self):
        return "%s | category_size_part_info: %s" % (self.category_size_part_similar, self.category_size_part_info)


class CategorySizePartInfo(models.Model):
    category_size_part_info_id = models.AutoField(primary_key=True)
    category_size_part_name = models.CharField(max_length=50)
    category_info = models.ForeignKey(CategoryInfo, models.DO_NOTHING, blank=True, null=True)
    category_dic = models.ForeignKey(CategoryDic, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'category_size_part_info'

    def __str__(self):
        return "%s | category_info: %s" % (self.category_size_part_name, self.category_info)


class GenderDic(models.Model):
    gender_dic_id = models.AutoField(primary_key=True)
    gender_similar = models.CharField(unique=True, max_length=20, blank=True, null=True)
    gender_info = models.ForeignKey('GenderInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'gender_dic'


class GenderInfo(models.Model):
    gender_info_id = models.AutoField(primary_key=True)
    gender_name = models.CharField(unique=True, max_length=20, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'gender_info'


class ImagePathInfo(models.Model):
    image_path_info_id = models.AutoField(primary_key=True)
    image_path_type = models.CharField(unique=True, max_length=20, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'image_path_info'


class KeywordDic(models.Model):
    keyword_dic_id = models.AutoField(primary_key=True)
    keyword_similar = models.CharField(unique=True, max_length=50)
    keyword_info = models.ForeignKey('KeywordInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'keyword_dic'


class KeywordInfo(models.Model):
    keyword_info_id = models.AutoField(primary_key=True)
    keyword_name = models.CharField(unique=True, max_length=50)
    sizecom_user = models.ForeignKey('SizecomUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'keyword_info'


class MethodInfo(models.Model):
    method_info_id = models.AutoField(primary_key=True)
    method_type = models.CharField(unique=True, max_length=50)

    class Meta:
        # managed = False
        db_table = 'method_info'


class PlatformDic(models.Model):
    platform_dic_id = models.AutoField(primary_key=True)
    platform_similar = models.CharField(unique=True, max_length=50)
    platform_info = models.ForeignKey('PlatformInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'platform_dic'


class PlatformInfo(models.Model):
    platform_info_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(unique=True, max_length=50)
    platform_url = models.CharField(unique=True, max_length=200)
    platform_country = models.CharField(max_length=10)
    platform_description = models.TextField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    sizecom_user = models.ForeignKey('SizecomUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'platform_info'

    def __str__(self):
        return "%s: %s" % (self.platform_name, self.platform_url)


class PriceTrackingInfo(models.Model):
    price_tracking_info_id = models.AutoField(primary_key=True)
    discount_price = models.FloatField()
    update_date = models.DateTimeField(blank=True, null=True)
    product_info = models.ForeignKey('ProductInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'price_tracking_info'


class ProductConceptKeyword(models.Model):
    concept_id = models.AutoField(primary_key=True)
    product_info = models.ForeignKey('ProductInfo', models.DO_NOTHING, blank=True, null=True)
    keyword_info = models.ForeignKey(KeywordInfo, models.DO_NOTHING, blank=True, null=True)
    method_info = models.ForeignKey(MethodInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'product_concept_keyword'


class ProductImage(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    image_path = models.TextField()
    product_info = models.ForeignKey('ProductInfo', models.DO_NOTHING, blank=True, null=True)
    image_path_info = models.ForeignKey(ImagePathInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'product_image'


class ProductInfo(models.Model):
    product_info_id = models.AutoField(primary_key=True)
    product_no = models.CharField(max_length=200, blank=True, null=True)
    product_name = models.CharField(max_length=200)
    product_url = models.CharField(max_length=200)
    manufacture_date = models.DateTimeField(blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    soldout_date = models.DateTimeField(blank=True, null=True)
    original_price = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)
    category_info = models.ForeignKey(CategoryInfo, models.DO_NOTHING, blank=True, null=True)
    category_dic = models.ForeignKey(CategoryDic, models.DO_NOTHING, blank=True, null=True)
    sub_category_info = models.ForeignKey('SubCategoryInfo', models.DO_NOTHING, blank=True, null=True)
    sub_category_dic = models.ForeignKey('SubCategoryDic', models.DO_NOTHING, blank=True, null=True)
    gender_info = models.ForeignKey(GenderInfo, models.DO_NOTHING, blank=True, null=True)
    brand_info = models.ForeignKey(BrandInfo, models.DO_NOTHING, blank=True, null=True)
    brand_dic = models.ForeignKey(BrandDic, models.DO_NOTHING, blank=True, null=True)
    platform_info = models.ForeignKey(PlatformInfo, models.DO_NOTHING, blank=True, null=True)
    sizecom_user = models.ForeignKey('SizecomUser', models.DO_NOTHING, blank=True, null=True)
    gender_dic = models.ForeignKey(GenderDic, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'product_info'

    def __str__(self):
        return "%s: %s %s / %s %s" % (self.product_name, self.product_url, self.brand_info, self.original_price, self.discount_price)


class ProductReview(models.Model):
    product_review_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    sizecom_user = models.ForeignKey('SizecomUser', models.DO_NOTHING, blank=True, null=True)
    product_info = models.ForeignKey(ProductInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'product_review'


class RoleInfo(models.Model):
    role_info_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=20)

    class Meta:
        # managed = False
        db_table = 'role_info'


class SearchStream(models.Model):
    search_stream_id = models.AutoField(primary_key=True)
    search_date = models.DateTimeField(blank=True, null=True)
    sizecom_user = models.ForeignKey('SizecomUser', models.DO_NOTHING, blank=True, null=True)
    product_info = models.ForeignKey(ProductInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_stream'


class SizeFitInfo(models.Model):
    size_fit_info_id = models.AutoField(primary_key=True)
    size_fit_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'size_fit_info'


class SizeFitLabelInfo(models.Model):
    size_fit_label_info_id = models.AutoField(primary_key=True)
    size_fit_label_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'size_fit_label_info'


class SizeInfo(models.Model):
    size_info_id = models.AutoField(primary_key=True)
    size_value = models.CharField(max_length=20)
    size_unit = models.CharField(max_length=20)
    product_info = models.ForeignKey(ProductInfo, models.DO_NOTHING, blank=True, null=True)
    size_standard = models.ForeignKey('SizeStandard', models.DO_NOTHING, blank=True, null=True)
    category_size_part_info = models.ForeignKey(CategorySizePartInfo, models.DO_NOTHING, blank=True, null=True)
    category_size_part_dic = models.ForeignKey(CategorySizePartDic, models.DO_NOTHING, blank=True, null=True)
    sub_category_size_part_info = models.ForeignKey('SubCategorySizePartInfo', models.DO_NOTHING, blank=True, null=True)
    sub_category_size_part_dic = models.ForeignKey('SubCategorySizePartDic', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'size_info'

    def __str__(self):
        return "%s %s %s" % (self.size_unit, self.size_value, self.product_info.product_name)


class SizeStandard(models.Model):
    size_standard_id = models.AutoField(primary_key=True)
    size_standard_name = models.CharField(unique=True, max_length=20)

    class Meta:
        # managed = False
        db_table = 'size_standard'
#
#
# class SizeStandardFormula(models.Model):
#     size_standard_formular_id = models.AutoField(primary_key=True)
#     formula = models.TextField()
#     size_standard_to = models.ForeignKey(SizeStandard, models.DO_NOTHING, db_column='size_standard_to', blank=True,
#                                          null=True)
#     size_standard_from = models.ForeignKey(SizeStandard, models.DO_NOTHING, db_column='size_standard_from', blank=True,
#                                            null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'size_standard_formula'


class SizecomUser(models.Model):
    sizecom_user_id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    birth = models.DateTimeField()
    reg_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    role_info = models.ForeignKey(RoleInfo, models.DO_NOTHING, blank=True, null=True)
    gender_info = models.ForeignKey(GenderInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'sizecom_user'


class SubCategoryDic(models.Model):
    sub_category_dic_id = models.AutoField(primary_key=True)
    sub_category_similar = models.CharField(max_length=50)
    sub_category_info = models.ForeignKey('SubCategoryInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'sub_category_dic'

    def __str__(self):
        return "%s | sub_category_info: %s" % (self.sub_category_similar, self.sub_category_info)


class SubCategoryInfo(models.Model):
    sub_category_info_id = models.AutoField(primary_key=True)
    sub_category_name = models.CharField(unique=True, max_length=20)
    category_info = models.ForeignKey(CategoryInfo, models.DO_NOTHING, blank=True, null=True)
    category_dic = models.ForeignKey(CategoryDic, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'sub_category_info'

    def __str__(self):
        return "%s | category_info: %s" % (self.sub_category_name, self.category_info)


class SubCategorySizePartDic(models.Model):
    sub_category_size_part_dic_id = models.AutoField(primary_key=True)
    sub_category_size_part_similar = models.CharField(max_length=50)
    sub_category_size_part_info = models.ForeignKey('SubCategorySizePartInfo', models.DO_NOTHING, blank=True, null=True)
    sub_category_info = models.ForeignKey(SubCategoryInfo, models.DO_NOTHING, blank=True, null=True)
    sub_category_dic = models.ForeignKey(SubCategoryDic, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'sub_category_size_part_dic'

    def __str__(self):
        return "%s | sub_category_size_part_info: %s" % (self.sub_category_size_part_similar, self.sub_category_size_part_info)


class SubCategorySizePartInfo(models.Model):
    sub_category_size_part_info_id = models.AutoField(primary_key=True)
    sub_category_size_part_name = models.CharField(max_length=50)
    sub_category_info = models.ForeignKey(SubCategoryInfo, models.DO_NOTHING, blank=True, null=True)
    sub_category_dic = models.ForeignKey(SubCategoryDic, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'sub_category_size_part_info'

    def __str__(self):
        return "%s | sub_category_info: %s" % (self.sub_category_size_part_name, self.sub_category_info)

# class UserBodyProfile(models.Model):
#     user_body_profile_id = models.AutoField(primary_key=True)
#     height = models.FloatField(blank=True, null=True)
#     weight = models.FloatField(blank=True, null=True)
#     reg_date = models.DateTimeField(blank=True, null=True)
#     size_standard = models.ForeignKey(SizeStandard, models.DO_NOTHING, blank=True, null=True)
#     weight_standard = models.ForeignKey('WeightStandard', models.DO_NOTHING, blank=True, null=True)
#     sizecom_user = models.ForeignKey(SizecomUser, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'user_body_profile'
#
#
# class UserCategorySizeProfile(models.Model):
#     user_size_profile_id = models.AutoField(primary_key=True)
#     size_value = models.CharField(max_length=20)
#     reg_date = models.DateTimeField(blank=True, null=True)
#     category_size_part_info = models.ForeignKey(CategorySizePartInfo, models.DO_NOTHING, blank=True, null=True)
#     category_info = models.ForeignKey(CategoryInfo, models.DO_NOTHING, blank=True, null=True)
#     user_body_profile = models.ForeignKey(UserBodyProfile, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'user_category_size_profile'


# class UserSizeLog(models.Model):
#     user_size_log_id = models.AutoField(primary_key=True)
#     reg_date = models.DateTimeField(blank=True, null=True)
#     sizecom_user = models.ForeignKey(SizecomUser, models.DO_NOTHING, blank=True, null=True)
#     size_info = models.ForeignKey(PlatformInfo, models.DO_NOTHING, blank=True, null=True)
#     platform_info = models.ForeignKey(PlatformInfo, models.DO_NOTHING, blank=True, null=True)
#     brand_info = models.ForeignKey(BrandInfo, models.DO_NOTHING, blank=True, null=True)
#     product_info = models.ForeignKey(PlatformInfo, models.DO_NOTHING, blank=True, null=True)
#     size_fit_label_info = models.ForeignKey(SizeFitLabelInfo, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'user_size_log'


# class UserSubCategorySizeProfile(models.Model):
#     user_size_profile_id = models.AutoField(primary_key=True)
#     size_value = models.CharField(max_length=20)
#     reg_date = models.DateTimeField(blank=True, null=True)
#     sub_category_size_part_info = models.ForeignKey(SubCategorySizePartInfo, models.DO_NOTHING, blank=True, null=True)
#     sub_category_info = models.ForeignKey(SubCategoryInfo, models.DO_NOTHING, blank=True, null=True)
#     user_body_profile = models.ForeignKey(UserBodyProfile, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'user_sub_category_size_profile'
#
#
# class WeightStandard(models.Model):
#     weight_standard_id = models.AutoField(primary_key=True)
#     weight_standard_name = models.CharField(unique=True, max_length=20)
#
#     class Meta:
#         managed = False
#         db_table = 'weight_standard'
#
#
# class WeightStandardFormula(models.Model):
#     weight_standard_formula_id = models.AutoField(primary_key=True)
#     formula = models.TextField()
#     weight_standard_to = models.ForeignKey(WeightStandard, models.DO_NOTHING, db_column='weight_standard_to',
#                                            blank=True, null=True)
#     weight_standard_from = models.ForeignKey(WeightStandard, models.DO_NOTHING, db_column='weight_standard_from',
#                                              blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'weight_standard_formula'
