import requests
import pandas as pd
import time

def get_reviews(product_id, max_pages=5):
    reviews = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for page in range(1, max_pages+1):
        url = f"https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=/product/{product_id}/reviews?page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Ошибка на странице {page}")
            break
        data = response.json()
        try:
            items = data['widgetStates']['webReviewList']['reviews']
            for item in items:
                reviews.append({
                    'text': item['text'],
                    'rating': item['rating'],
                    'authorName': item['authorName'],
                    'createdAt': item['createdAt']
                })
        except KeyError:
            print(f"Нет отзывов на странице {page}")
            break
        time.sleep(1)
    return reviews

def get_reviews_for_products(product_ids, label, max_pages=5):
    all_reviews = []
    for pid in product_ids:
        reviews = get_reviews(pid, max_pages)
        for review in reviews:
            review['product_id'] = pid
            review['category'] = label
        all_reviews.extend(reviews)
        print(f"Собрано {len(reviews)} отзывов для товара {pid}")
    return all_reviews

women_ids = [1131621478, 2030177793, 277013878, 287889610]
men_ids = [218820548, 186894245, 2033971623, 2038415935]

women_reviews = get_reviews_for_products(women_ids, label="Women", max_pages=5)
men_reviews = get_reviews_for_products(men_ids, label="Men", max_pages=5)

df_reviews = pd.DataFrame(women_reviews + men_reviews)
df_reviews.to_csv('data/ozon_reviews.csv', index=False)
print("Файл ozon_reviews.csv сохранен.")
