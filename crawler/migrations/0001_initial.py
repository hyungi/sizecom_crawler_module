# Generated by Django 2.2.1 on 2019-07-27 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchStream',
            fields=[
                ('search_stream_id', models.AutoField(primary_key=True, serialize=False)),
                ('search_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'search_stream',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SizeFitInfo',
            fields=[
                ('size_fit_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('size_fit_name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'size_fit_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SizeFitLabelInfo',
            fields=[
                ('size_fit_label_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('size_fit_label_name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'size_fit_label_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BrandDic',
            fields=[
                ('brand_dic_id', models.AutoField(primary_key=True, serialize=False)),
                ('brand_similar', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'brand_dic',
            },
        ),
        migrations.CreateModel(
            name='BrandInfo',
            fields=[
                ('brand_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('brand_name', models.CharField(max_length=100)),
                ('brand_url', models.CharField(max_length=200)),
                ('brand_country', models.CharField(max_length=10)),
                ('brand_description', models.TextField(blank=True, null=True)),
                ('reg_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'brand_info',
            },
        ),
        migrations.CreateModel(
            name='CategoryDic',
            fields=[
                ('category_dic_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_similar', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'category_dic',
            },
        ),
        migrations.CreateModel(
            name='CategoryInfo',
            fields=[
                ('category_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'category_info',
            },
        ),
        migrations.CreateModel(
            name='CategorySizePartDic',
            fields=[
                ('category_size_part_dic_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_size_part_similar', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'category_size_part_dic',
            },
        ),
        migrations.CreateModel(
            name='CategorySizePartInfo',
            fields=[
                ('category_size_part_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_size_part_name', models.CharField(max_length=50)),
                ('category_dic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategoryDic')),
                ('category_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategoryInfo')),
            ],
            options={
                'db_table': 'category_size_part_info',
            },
        ),
        migrations.CreateModel(
            name='GenderInfo',
            fields=[
                ('gender_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('gender_name', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ],
            options={
                'db_table': 'gender_info',
            },
        ),
        migrations.CreateModel(
            name='ImagePathInfo',
            fields=[
                ('image_path_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('image_path_type', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ],
            options={
                'db_table': 'image_path_info',
            },
        ),
        migrations.CreateModel(
            name='KeywordInfo',
            fields=[
                ('keyword_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword_name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'keyword_info',
            },
        ),
        migrations.CreateModel(
            name='MethodInfo',
            fields=[
                ('method_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('method_type', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'method_info',
            },
        ),
        migrations.CreateModel(
            name='PlatformInfo',
            fields=[
                ('platform_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('platform_name', models.CharField(max_length=50, unique=True)),
                ('platform_url', models.CharField(max_length=200, unique=True)),
                ('platform_country', models.CharField(max_length=10)),
                ('platform_description', models.TextField(blank=True, null=True)),
                ('reg_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'platform_info',
            },
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('product_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_no', models.CharField(blank=True, max_length=200, null=True)),
                ('product_name', models.CharField(max_length=200)),
                ('product_url', models.CharField(max_length=200)),
                ('manufacture_date', models.DateTimeField(blank=True, null=True)),
                ('product_description', models.TextField(blank=True, null=True)),
                ('reg_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('soldout_date', models.DateTimeField(blank=True, null=True)),
                ('original_price', models.FloatField(blank=True, null=True)),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('brand_dic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.BrandDic')),
                ('brand_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.BrandInfo')),
                ('category_dic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategoryDic')),
                ('category_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategoryInfo')),
                ('gender_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.GenderInfo')),
                ('platform_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.PlatformInfo')),
            ],
            options={
                'db_table': 'product_info',
            },
        ),
        migrations.CreateModel(
            name='RoleInfo',
            fields=[
                ('role_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'role_info',
            },
        ),
        migrations.CreateModel(
            name='SizeStandard',
            fields=[
                ('size_standard_id', models.AutoField(primary_key=True, serialize=False)),
                ('size_standard_name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'size_standard',
            },
        ),
        migrations.CreateModel(
            name='SubCategoryDic',
            fields=[
                ('sub_category_dic_id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_category_similar', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'sub_category_dic',
            },
        ),
        migrations.CreateModel(
            name='SubCategoryInfo',
            fields=[
                ('sub_category_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_category_name', models.CharField(max_length=20, unique=True)),
                ('category_dic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategoryDic')),
                ('category_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategoryInfo')),
            ],
            options={
                'db_table': 'sub_category_info',
            },
        ),
        migrations.CreateModel(
            name='SubCategorySizePartInfo',
            fields=[
                ('sub_category_size_part_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_category_size_part_name', models.CharField(max_length=50)),
                ('sub_category_dic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SubCategoryDic')),
                ('sub_category_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SubCategoryInfo')),
            ],
            options={
                'db_table': 'sub_category_size_part_info',
            },
        ),
        migrations.CreateModel(
            name='SubCategorySizePartDic',
            fields=[
                ('sub_category_size_part_dic_id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_category_size_part_similar', models.CharField(max_length=50)),
                ('sub_category_size_part_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SubCategorySizePartInfo')),
            ],
            options={
                'db_table': 'sub_category_size_part_dic',
            },
        ),
        migrations.AddField(
            model_name='subcategorydic',
            name='sub_category_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SubCategoryInfo'),
        ),
        migrations.CreateModel(
            name='SizeInfo',
            fields=[
                ('size_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('size_value', models.CharField(max_length=20)),
                ('size_unit', models.CharField(max_length=20)),
                ('category_size_part_dic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategorySizePartDic')),
                ('category_size_part_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategorySizePartInfo')),
                ('product_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.ProductInfo')),
                ('size_standard', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SizeStandard')),
                ('sub_category_size_part_dic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SubCategorySizePartDic')),
                ('sub_category_size_part_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SubCategorySizePartInfo')),
            ],
            options={
                'db_table': 'size_info',
            },
        ),
        migrations.CreateModel(
            name='SizecomUser',
            fields=[
                ('sizecom_user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=50)),
                ('birth', models.DateTimeField()),
                ('reg_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('gender_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.GenderInfo')),
                ('role_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.RoleInfo')),
            ],
            options={
                'db_table': 'sizecom_user',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('product_review_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(blank=True, null=True)),
                ('reg_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('product_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.ProductInfo')),
                ('sizecom_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SizecomUser')),
            ],
            options={
                'db_table': 'product_review',
            },
        ),
        migrations.AddField(
            model_name='productinfo',
            name='sizecom_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SizecomUser'),
        ),
        migrations.AddField(
            model_name='productinfo',
            name='sub_category_dic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SubCategoryDic'),
        ),
        migrations.AddField(
            model_name='productinfo',
            name='sub_category_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SubCategoryInfo'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('product_image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image_path', models.TextField()),
                ('image_path_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.ImagePathInfo')),
                ('product_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.ProductInfo')),
            ],
            options={
                'db_table': 'product_image',
            },
        ),
        migrations.CreateModel(
            name='ProductConceptKeyword',
            fields=[
                ('concept_id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.KeywordInfo')),
                ('method_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.MethodInfo')),
                ('product_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.ProductInfo')),
            ],
            options={
                'db_table': 'product_concept_keyword',
            },
        ),
        migrations.CreateModel(
            name='PriceTrackingInfo',
            fields=[
                ('price_tracking_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('discount_price', models.FloatField()),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('product_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.ProductInfo')),
            ],
            options={
                'db_table': 'price_tracking_info',
            },
        ),
        migrations.AddField(
            model_name='platforminfo',
            name='sizecom_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SizecomUser'),
        ),
        migrations.CreateModel(
            name='PlatformDic',
            fields=[
                ('platform_dic_id', models.AutoField(primary_key=True, serialize=False)),
                ('platform_similar', models.CharField(max_length=50, unique=True)),
                ('platform_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.PlatformInfo')),
            ],
            options={
                'db_table': 'platform_dic',
            },
        ),
        migrations.AddField(
            model_name='keywordinfo',
            name='sizecom_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SizecomUser'),
        ),
        migrations.CreateModel(
            name='KeywordDic',
            fields=[
                ('keyword_dic_id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword_similar', models.CharField(max_length=50, unique=True)),
                ('keyword_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.KeywordInfo')),
            ],
            options={
                'db_table': 'keyword_dic',
            },
        ),
        migrations.CreateModel(
            name='GenderDic',
            fields=[
                ('gender_dic_id', models.AutoField(primary_key=True, serialize=False)),
                ('gender_similar', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('gender_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.GenderInfo')),
            ],
            options={
                'db_table': 'gender_dic',
            },
        ),
        migrations.AddField(
            model_name='categorysizepartdic',
            name='category_size_part_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategorySizePartInfo'),
        ),
        migrations.AddField(
            model_name='categorydic',
            name='category_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.CategoryInfo'),
        ),
        migrations.CreateModel(
            name='BrandTrackingInfo',
            fields=[
                ('brand_tracking_info_id', models.AutoField(primary_key=True, serialize=False)),
                ('brand_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.BrandInfo')),
            ],
            options={
                'db_table': 'brand_tracking_info',
            },
        ),
        migrations.AddField(
            model_name='brandinfo',
            name='platform_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.PlatformInfo'),
        ),
        migrations.AddField(
            model_name='brandinfo',
            name='sizecom_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.SizecomUser'),
        ),
        migrations.AddField(
            model_name='branddic',
            name='brand_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.BrandInfo'),
        ),
        migrations.CreateModel(
            name='BrandConceptKeyword',
            fields=[
                ('concept_id', models.AutoField(primary_key=True, serialize=False)),
                ('brand_dic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.BrandDic')),
                ('brand_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.BrandInfo')),
                ('keyword_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.KeywordInfo')),
                ('method_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='crawler.MethodInfo')),
            ],
            options={
                'db_table': 'brand_concept_keyword',
            },
        ),
    ]
