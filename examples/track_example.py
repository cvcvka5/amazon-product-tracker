from tracker.product import Product
import time

def on_change(before, after, changed_keys):
    print(f"Change detected! Keys: {changed_keys}")
    print(f"Before: {before}")
    print(f"After: {after}\n")

if __name__ == "__main__":
    url = "https://www.amazon.de/dp/B0B1V5ZP3F"  # Example Amazon product
    product = Product.track_product_amazon(url, interval=10, on_change_funcs=[on_change])