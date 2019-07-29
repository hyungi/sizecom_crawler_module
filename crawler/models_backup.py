# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         # managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         # managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         # managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         # managed = False
#         db_table = 'auth_user'

#
# class AuthUserGroups(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         # managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         # managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


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
    brand_similar = models.CharField(max_length=50)
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
    reg_date = models.DateTimeField(blank=True, null=True, default=datetime.now())
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
        return "%s %s" % (self.category_similar, self.category_info)


class CategoryInfo(models.Model):
    category_info_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)

    class Meta:
        # managed = False
        db_table = 'category_info'

    def __str__(self):
        return "%s" % self.category_name


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#
#     class Meta:
#         # managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         # managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)

#
# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         # managed = False
#         db_table = 'django_migrations'


class GenderDic(models.Model):
    gender_dic_id = models.AutoField(primary_key=True)
    gender_similar = models.CharField(max_length=20, blank=True, null=True)
    gender_info = models.ForeignKey('GenderInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'gender_dic'


class GenderInfo(models.Model):
    gender_info_id = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=20)

    class Meta:
        # managed = False
        db_table = 'gender_info'


class ImagePathInfo(models.Model):
    image_path_info_id = models.AutoField(primary_key=True)
    image_path_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'image_path_info'


class KeywordDic(models.Model):
    keyword_dic_id = models.AutoField(primary_key=True)
    keyword_similar = models.CharField(max_length=50)
    keyword_info = models.ForeignKey('KeywordInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'keyword_dic'


class KeywordInfo(models.Model):
    keyword_info_id = models.AutoField(primary_key=True)
    keyword_name = models.CharField(max_length=50)
    sizecom_user = models.ForeignKey('SizecomUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'keyword_info'


class MethodInfo(models.Model):
    method_info_id = models.AutoField(primary_key=True)
    method_type = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = 'method_info'


class PlatformDic(models.Model):
    platform_dic_id = models.AutoField(primary_key=True)
    platform_similar = models.CharField(max_length=50)
    platform_info = models.ForeignKey('PlatformInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'platform_dic'


class PlatformInfo(models.Model):
    platform_info_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(max_length=50)
    platform_url = models.CharField(max_length=200)
    platform_country = models.CharField(max_length=10)
    platform_description = models.TextField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True, default=datetime.now())
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
    reg_date = models.DateTimeField(blank=True, null=True, default=datetime.now())
    update_date = models.DateTimeField(blank=True, null=True)
    soldout_date = models.DateTimeField(blank=True, null=True)
    category_info = models.ForeignKey(CategoryInfo, models.DO_NOTHING, blank=True, null=True)
    category_dic = models.ForeignKey(CategoryDic, models.DO_NOTHING, blank=True, null=True)
    sub_category_info = models.ForeignKey('SubCategoryInfo', models.DO_NOTHING, blank=True, null=True)
    sub_category_dic = models.ForeignKey('SubCategoryDic', models.DO_NOTHING, blank=True, null=True)
    gender_info = models.ForeignKey(GenderInfo, models.DO_NOTHING, blank=True, null=True)
    brand_info = models.ForeignKey(BrandInfo, models.DO_NOTHING, blank=True, null=True)
    brand_dic = models.ForeignKey(BrandDic, models.DO_NOTHING, blank=True, null=True)
    platform_info = models.ForeignKey(PlatformInfo, models.DO_NOTHING, blank=True, null=True)
    sizecom_user = models.ForeignKey('SizecomUser', models.DO_NOTHING, blank=True, null=True)
    original_price = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)

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


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=20)

    class Meta:
        # managed = False
        db_table = 'role'


class SearchStream(models.Model):
    search_stream_id = models.AutoField(primary_key=True)
    search_date = models.DateTimeField(blank=True, null=True)
    sizecom_user = models.ForeignKey('SizecomUser', models.DO_NOTHING, blank=True, null=True)
    product_info = models.ForeignKey(ProductInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'search_stream'


class SizeInfo(models.Model):
    size_info_id = models.AutoField(primary_key=True)
    size_value = models.CharField(max_length=20)
    size_unit = models.CharField(max_length=20)
    product_info = models.ForeignKey(ProductInfo, models.DO_NOTHING, blank=True, null=True)
    size_standard = models.ForeignKey('SizeStandard', models.DO_NOTHING, blank=True, null=True)
    size_part_info = models.ForeignKey('SizePartInfo', models.DO_NOTHING, blank=True, null=True)
    size_part_dic = models.ForeignKey('SizePartDic', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'size_info'

    def __str__(self):
        return "%s %s %s %s" % (self.size_unit, self.size_value, self.product_info.product_name, self.size_part_dic.size_part_info)


class SizePartDic(models.Model):
    size_part_dic_id = models.AutoField(primary_key=True)
    size_part_similar = models.CharField(max_length=50)
    size_part_info = models.ForeignKey('SizePartInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'size_part_dic'

    def __str__(self):
        return "%s %s" % (self.size_part_similar, self.size_part_info)


class SizePartInfo(models.Model):
    size_part_info_id = models.AutoField(primary_key=True)
    size_part_name = models.CharField(max_length=50)
    category_info = models.ForeignKey(CategoryInfo, models.DO_NOTHING, blank=True, null=True)
    category_dic = models.ForeignKey(CategoryDic, models.DO_NOTHING, blank=True, null=True)
    sub_category_info = models.ForeignKey('SubCategoryInfo', models.DO_NOTHING, blank=True, null=True)
    sub_category_dic = models.ForeignKey('SubCategoryDic', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'size_part_info'

    def __str__(self):
        return "%s %s" % (self.size_part_name, self.category_dic)


class SizeStandard(models.Model):
    size_standard_id = models.AutoField(primary_key=True)
    size_standard_name = models.CharField(max_length=20)

    class Meta:
        # managed = False
        db_table = 'size_standard'

    def __str__(self):
        return "%s" % self.size_standard_name


# class SizeStandardFormula(models.Model):
#     size_standard_formular_id = models.AutoField(primary_key=True)
#     formula = models.TextField()
#     size_standard_to = models.ForeignKey(SizeStandard, models.DO_NOTHING, db_column='size_standard_to', blank=True, null=True)
#     size_standard_from = models.ForeignKey(SizeStandard, models.DO_NOTHING, db_column='size_standard_from', blank=True, null=True)
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
    role = models.ForeignKey(Role, models.DO_NOTHING, blank=True, null=True)
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
        return "%s %s" % (self.sub_category_similar, self.sub_category_info)


class SubCategoryInfo(models.Model):
    sub_category_info_id = models.AutoField(primary_key=True)
    sub_category_name = models.CharField(max_length=20)
    category_info = models.ForeignKey(CategoryInfo, models.DO_NOTHING, blank=True, null=True)
    category_dic = models.ForeignKey(CategoryDic, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'sub_category_info'

    def __str__(self):
        return "%s %s" % (self.sub_category_name, self.category_dic)
