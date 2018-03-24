# coding=utf-8
import StringIO
from collections import Iterable

import io
from PIL import Image


# Set the i-th bit of v to x
def set_bit(n, i, x):
    mask = 1 << i
    n &= ~mask
    if x:
        n |= mask
    return n


# image object, see https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
# watermark object
def encode(img, watermark):
    (img_w, img_h) = img.size
    (watermark_w, watermark_h) = watermark.size

    if not cmp(watermark.mode, 'P') and not cmp(watermark.mode, 'L'):
        raise RuntimeError("invalid argument, watermark must be a binary image")

    img_bitmap = img.getdata()
    watermark_bitmap = watermark.getdata()

    img_out = Image.new(img.mode, (img_w, img_h))
    img_out_bitmap = img_out.getdata()

    print "start write"
    for x in range(img_w):
        for y in range(img_h):
            pixel = img_bitmap.getpixel((x, y))
            watermark_x = x % watermark_w
            watermark_y = y % watermark_h
            bit = 1 if watermark_bitmap.getpixel((watermark_x, watermark_y)) else 0
            new_pixel = []
            if isinstance(pixel, Iterable):
                for channel in pixel:
                    new_pixel.append(set_bit(channel, 0, bit))
            else:
                new_pixel.append(set_bit(pixel, 0, bit))
            img_out_bitmap.putpixel((x, y), tuple(new_pixel))
    return img_out


if __name__ == '__main__':
    # test png
    # img = Image.open("../tiger-1526704_1280.png")
    # watermark = Image.open("../watermark.png")
    # out = encode(img, watermark)
    # out.save("../png_out.png", img.format)

    ## test jpg
    # img = Image.open("../F100011059.jpg")
    # watermark = Image.open("../watermark.png")
    # out = encode(img, watermark)
    # out.save("../jpg_out.jpg", img.format)

    ## test to bytes
    # img = Image.open("../F100011059.jpg")
    # watermark = Image.open("../watermark.png")
    # out = encode(img, watermark)
    # b = io.BytesIO()
    # out.save(b, img.format)
    # file = open("../jpg_raw_out.jpg", "w")
    # file.write(b.getvalue())
    # file.close()

    ## test from bytes 1
    # img = Image.open("../F100011059.jpg")
    # temp = Image.frombytes(img.mode, img.size, img.tobytes())
    # temp.show()

    ## test from bytes 2
    with open('../F100011059.jpg', 'rb') as content_file:
        content = content_file.read()
        img = Image.open(StringIO.StringIO(content))
        img.show()
