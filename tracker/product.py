import requests
from bs4 import BeautifulSoup
import threading
from typing import Callable, List, Dict, Any

OnChangeCallback = Callable[[Dict[str, Any], Dict[str, Any], List[str]], None]

class Product:
    TITLE_SELECTOR = "h1#title"
    PRICE_SELECTOR = "span.priceToPay > span:nth-child(2)"
    IMG_SELECTOR = "img#landingImage"

    TRACKED_PRODUCTS = {}

    def __init__(self, title: str, price: str, img_url: str, url: str, on_change_funcs: List[OnChangeCallback] = None):
        self.title = title
        self.price = price
        self.img_url = img_url
        self.url = url
        self.on_change_funcs = on_change_funcs or []

    @staticmethod
    def get_product_info(url: str) -> Dict[str, str]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/135.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        return {
            "title": soup.select_one(Product.TITLE_SELECTOR).text.strip(),
            "price": soup.select_one(Product.PRICE_SELECTOR).text.strip().replace("\n", ""),
            "img_url": soup.select_one(Product.IMG_SELECTOR).get("src").strip(),
            "url": url
        }

    @classmethod
    def track_product_amazon(cls, url: str, interval: float = 5.0, on_change_funcs: List[OnChangeCallback] = None):
        product_info = cls.get_product_info(url)
        product_obj = cls(**product_info, on_change_funcs=on_change_funcs)
        product_obj.track_product(interval)
        return product_obj

    def track_product(self, interval: float = 5.0):
        """Start recurring tracking."""
        def recurring_update():
            self.update()
            # Reschedule the next call
            timer = threading.Timer(interval, recurring_update)
            Product.TRACKED_PRODUCTS[self] = timer
            timer.start()

        recurring_update()  # Start first call

    def untrack_product(self):
        timer = Product.TRACKED_PRODUCTS.get(self)
        if timer:
            timer.cancel()
            del Product.TRACKED_PRODUCTS[self]

    def update(self):
        new_info = self.get_product_info(self.url)
        changed_keys = []

        if new_info["title"] != self.title:
            changed_keys.append("title")
        if new_info["price"] != self.price:
            changed_keys.append("price")
        if new_info["img_url"] != self.img_url:
            changed_keys.append("img_url")

        if changed_keys:
            before = self.json
            for changed_key in changed_keys:
                self.__setattr__(changed_key, new_info[changed_key])
            after = self.json

            for func in self.on_change_funcs:
                func(before, after, changed_keys)

    @staticmethod
    def cancel_all_threads():
        for thread in Product.TRACKED_PRODUCTS.values():
            thread.cancel()

    @property
    def json(self):
        return {"title": self.title, "price": self.price, "url": self.url, "img_url": self.img_url}

    def __str__(self):
        return f"Product(title='{self.title}', price={self.price})"
