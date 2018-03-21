# coding=utf-8
from PIL import Image


# Set the i-th bit of v to x
def set_bit(n, i, x):
    mask = 1 << i
    n &= ~mask
    if x:
        n |= mask
    return n


# image object, see https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
# payload object
def encode(img, watermark):
    (img_w, img_h) = img.size
    (watermark_w, watermark_h) = watermark.size

    img_bitmap = img.getdata()
    watermark_bitmap = watermark.getdata()

    img_out = Image.new('RGBA', (img_w, img_h))
    img_out_bitmap = img_out.getdata()

    for x in range(img_w):
        for y in range(img_h):
            (img_r, img_g, img_b, img_a) = img_bitmap.getpixel((x, y))
            watermark_x = x % watermark_w
            watermark_y = y % watermark_h
            bit = 1 if watermark_bitmap.getpixel((watermark_x, watermark_y)) else 0
            img_r = set_bit(img_r, 0, bit)
            img_g = set_bit(img_g, 0, bit)
            img_b = set_bit(img_b, 0, bit)
            img_a = set_bit(img_a, 0, bit)
            img_out_bitmap.putpixel((x, y), (img_r, img_g, img_b, img_a))
    return img_out


def main():
    img = Image.open("/Users/chan/Documents/github/cloacked-pixel/tiger-1526704_1280.png")
    watermark = Image.open("/Users/chan/Documents/github/cloacked-pixel/watermark.png")
    out = encode(img, watermark)
    out.save("/Users/chan/Documents/github/cloacked-pixel/out.png", "PNG")


if __name__ == '__main__':
    main()
