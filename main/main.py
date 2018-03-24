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

    ## 检查水印是不是二值图片(只有黑白两种颜色的图片)
    if not cmp(watermark.mode, 'P') and not cmp(watermark.mode, 'L'):
        raise RuntimeError("invalid argument, watermark must be a binary image")

    img_bitmap = img.getdata()
    watermark_bitmap = watermark.getdata()

    img_out = Image.new(img.mode, (img_w, img_h))
    img_out_bitmap = img_out.getdata()

    print "start write"
    # 遍历原图中的每一个像素
    for x in range(img_w):
        for y in range(img_h):
            pixel = img_bitmap.getpixel((x, y))
            
            # 读取水印中的每一个像素，取模是为了防止读取位置超过水印的宽高
            # 比如5 % 2 取模的结果永远不会超过2
            watermark_x = x % watermark_w
            watermark_y = y % watermark_h
            # 得出要对原图的每个颜色分量写的值（比如黑色就写0，白色就写1）
            bit = 1 if watermark_bitmap.getpixel((watermark_x, watermark_y)) else 0
            new_pixel = []

            # 原图如果是个彩色图，通常返回(R, G, B, A)的元组，但是如果是黑白图就是一个像素
            if isinstance(pixel, Iterable):
                # (R, G, B, A)的元组每个channel进行写值，即在0位写0或1
                for channel in pixel:
                    new_pixel.append(set_bit(channel, 0, bit))
            else:
                new_pixel.append(set_bit(pixel, 0, bit))
            # 再输出到输出图片里
            img_out_bitmap.putpixel((x, y), tuple(new_pixel))
    return img_out


if __name__ == '__main__':
    # test png
    img = Image.open("../tiger-1526704_1280.png")
    watermark = Image.open("../watermark.png")
    out = encode(img, watermark)
    out.save("../png_out.png", img.format)

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
    # with open('../F100011059.jpg', 'rb') as content_file:
    #     content = content_file.read()
    #     img = Image.open(StringIO.StringIO(content))
    #     img.show()
