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
  

def saveQRImages():
    links = Helpers.static_final_links
    print('Saving Images....')
    for idx, link in enumerate(links):
        save_path = f"{Helpers.qr_images_path}{idx}.png"
        makeQrcode(f"https://ar.wikipedia.org{link[0]}", save_path)
        Helpers.simpleLoading(len(links), idx)