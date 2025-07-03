import requests

def get_image(url, tittle):
    normal_url = f"https://sxodim.com{url}"
    # 2. Send HTTP GET request
    response = requests.get(normal_url)

    # 3. Raise an exception if the download failed (status codes 4xx/5xx)
    response.raise_for_status()

    # 4. Write the binary content to a local file
    with open(f"image\{tittle}.jpg", "wb") as f:
        f.write(response.content)