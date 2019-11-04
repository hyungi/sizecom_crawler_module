# Size Recommender
- Create a size profile using user information; Brands purchased by users, Size worn by users
- Recommend product of most suitable size or fit in comparison with size of specific product

#### Basic request form
```POST /${task}/${objective}/${by}/${using}```
- task: recommend, create
- objective: unit/product, size_profile
- by: category, sub_category
- using: product, size_profile

<br><br>

# Create size profile
Create a size profile using user information; Brands purchased by users, Size worn by users

- Create size profile by given category using products

    ```POST /create/size_profile/category```
    ```json
    {
      "category_info_id": 15,
      "gender_info_id": 1,
      "recent":true,
      "brand_info_id_list": [30, 15],
      "size_unit_list": ["XL", "XXL"]
    }
    ```

- Create size profile by given sub category using products

    ```POST /create/size_profile/sub_category```
    ```json
        {
          "sub_category_info_id": 21,
          "gender_info_id": 1,
          "recent":true,
          "brand_info_id_list": [30, 15],
          "size_unit_list": ["XL", "XXL"]
        }
    ```

<br><br>

## Recommend size unit
Recommend product of most suitable size among the given sizes of the product

- Recommend size unit by given category using size profile
> ```POST /recommend/unit/category/size_profile```

- Recommend size unit by given category using product
> ```POST /recommend/unit/category/product```

- Recommend size unit by given sub category using size profile
> ```POST /recommend/unit/sub_category/size_profile```

- Recommend size unit by given sub category using product
> ```POST /recommend/unit/sub_category/product```

<br><br>

## Reocmmend size fit
Recommend product of most suitable fit among the products

- Recommend size fit by given category using size profile
> ```POST /recommend/product/category/size_profile```

- Recommend size fit by given category using product
> ```POST /recommend/product/category/product```

- Recommend size fit by given sub category using size profile
```POST /recommend/product/sub_category/size_profile```

- Recommend size fit by given sub category using product
```POST /recommend/product/sub_category/product```
