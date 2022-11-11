from email import header
from urllib import response
import requests
import json
import csv
import numpy as np
import pandas as pd
nhasach_url = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=48&include=advertisement&aggregations=2&trackity_id=7ac7bd0c-d274-5d0e-12e8-2c461a9e0820&category=8322&page=1&urlKey=nha-sach-tiki"
product_url = "https://tiki.vn/api/v2/products/{}"
rating_url  = "https://tiki.vn/api/v2/reviews?product_id={}&include=comments&page=1&limit=-1&top=true&spid=162201946&seller_id=1"

product_id_file = "./data/product-id.txt"
product_file = "./data/product.txt"
product_file2 = "./data/product-detail.txt"
rating_file = "./data/rating.csv"

def crawl_product_id():
    product_list =np.array([])
    i = 1
    while(i < 22):
        payload = {}
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

        params = {
            'page': i
        }
        response = requests.request(
            "GET", nhasach_url, headers=headers, data=payload, params=params
        )
        print(response)
        print("page", i)
        y = response.json()
        print(len(y["data"]))
        for j in range(len(y["data"])):
            idproduct = y["data"][j]['id']
            product_list = np.append(product_list, [idproduct], axis=0)
        i += 1
    product_list = product_list.astype(int)
    print('product_list', product_list)
    print('len(product_list)', len(product_list))
    return product_list

def write_csv_file(data_matrix, file_path, mode='a'):
    df = pd.DataFrame(data=data_matrix)
    df.to_csv(file_path, sep='\t', header=None, index=None, mode=mode)


def read_matrix_file(file_path):
    f = pd.read_csv(
        file_path, sep='\t', encoding='utf-8', header=None
    )
    f = f.to_numpy()
    return f

def crawl_product(product_list):
    product_detail_list = np.array(
        [['id', 'name', 'original_price', 'price', 'productset_group_name', 'review_count', 'categories']]
    )
    print('product_detail_list', product_detail_list)
    for product_id in product_list:
        id = -1
        name = -1
        original_price = -1
        price = -1
        productset_group_name = -1
        review_count = -1
        categories = -1
        print("product_id", product_id)
        payload = {}
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

        response = requests.get(product_url.format(product_id), headers=headers, data=payload)
        y = response.json()
        if (response.status_code == 200):
            id = y['id']
            name = y['name']
            original_price = y['original_price']
            price = y['price']
            productset_group_name = y['productset_group_name']
            review_count = y['review_count']
            categories = y['categories']['name']
        product_detail_list = np.append(
            product_detail_list, [[id, name, original_price, price, productset_group_name, review_count, categories]]
        )
    return product_detail_list

def crawl_rating(product_list):
    for product_id in product_list:
        userid = -1
        itemid = -1
        rating = -1
        timestamp = -1
        comment = -1
        i = 1
        print("product_id", product_id)
        payload = {}
        params = {"page": i}
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

        response = requests.get(rating_url.format(product_id), headers=headers, data=payload, params=params)
        print("response", response)
        y = response.json()
        total_page = y["paging"]["last_page"]
        if (y["paging"]["total"] > 0):
            while (i <= total_page):
                payload = {}
                params = {"page":i}
                headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

                res = requests.get(rating_url.format(product_id), headers=headers, data=payload, params=params)
                x = res.json()
                for j in range(len(x["data"])):
                    userid = x["data"][j]['customer_id']
                    itemid =product_id
                    rating = x["data"][j]['rating']
                    timestamp = x["data"][j]['create_at']
                    comment = x["data"][j]['cintent']
                    rating_list = np.array(
                        [[userid, itemid, rating, timestamp, comment]]
                    )
                    write_csv_file(rating_list, rating_file, mode='a')
                i += 1
    return 1    



product_list =crawl_product_id()
write_csv_file(product_list, product_id_file, mode='w')
product_list = read_matrix_file(product_id_file).flatten()
product_detail_list = crawl_product(product_list)
write_csv_file(product_detail_list, product_file2, mode='w')
rating_list = crawl_rating(product_list)