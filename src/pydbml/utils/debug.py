DEBUG = True  # toggle this on/off


def debug(title: str, data):
    if DEBUG:
        print(f"\n--- DEBUG: {title} ---")
        print(data)