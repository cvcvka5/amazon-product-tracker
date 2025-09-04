# 🛒 Amazon Product Tracker (Python)

A lightweight Python library to **track Amazon product changes** (price, title, image) using `requests` + `BeautifulSoup` with threaded intervals.

---

## Features
- Tracks **title, price, and image** of an Amazon product
- Uses **threading.Timer** for recurring updates
- Supports **multiple callbacks** on change
- Graceful shutdown on **Ctrl+C**

---

## Installation

```bash
git clone https://github.com/<your-username>/amazon-product-tracker.git
cd amazon-product-tracker
pip install -r requirements.txt
```

---

## Example Usage

```python
from tracker.product import Product
import time

def on_change(before, after, changed_keys):
    print(f"Changed: {changed_keys}")
    print(f"Before: {before}")
    print(f"After: {after}")

url = "https://www.amazon.de/dp/B0B1V5ZP3F"
product = Product.track_product_amazon(url, interval=10, on_change_funcs=[on_change])
```

---

#### LICENSE (MIT)