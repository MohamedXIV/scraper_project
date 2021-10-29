from os import link
import qrcode
from helpers import Helpers


def makeQrcode(data: str, path: str = None):
    qr = qrcode.QRCode(version=1, box_size=20, border=5)

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    if path is not None:
        img.save(path)
    return img

  
url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"
path = './data/qrcodes/'

wiki_table = Helpers.getTable(url, False)
Helpers.getHyperlinks(wiki_table)
links = Helpers.static_final_links
#print(links)

previous_value = 0

print('Saving Images....')
for idx, link in enumerate(links):
  save_path = f"{path}{idx}.png"
  makeQrcode(f"https://ar.wikipedia.org{link[0]}", save_path)
  Helpers.simpleLoading(len(links), idx)