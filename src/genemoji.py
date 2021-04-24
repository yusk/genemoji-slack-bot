import random

from PIL import Image, ImageDraw, ImageFont


def pillow_char_offset(x_pos: int,
                       y_pos: int,
                       x_end_pos: int,
                       y_end_pos: int,
                       char: str,
                       init_fontsize: int,
                       font_filepath: str,
                       color="#000"):
    ratio = 10
    img = Image.new('RGBA', (x_end_pos * ratio, y_end_pos * ratio), None)
    draw = ImageDraw.Draw(img)

    length = x_end_pos * ratio - x_pos
    height = y_end_pos * ratio - y_pos
    out_text_size = (length + 1, height + 1)
    font_size_offset = 0
    font = None

    while length < out_text_size[0] or height < out_text_size[1]:
        font_size = init_fontsize - font_size_offset
        font = ImageFont.truetype(font_filepath, font_size * ratio)
        out_text_size = draw.textsize(char, font=font)
        font_size_offset += 1

    img = Image.new('RGBA', (x_end_pos * ratio, font_size * ratio), None)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, fill=color, font=font)

    return img.resize((x_end_pos, y_end_pos))


def get_concat_v(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def generate_random_color():
    return '#{:02X}{:02X}{:02X}'.format(
        *[random.randint(0, 255) for _ in range(3)])


def make_img_for_slack(char, font, color=None):
    if color is None:
        color = generate_random_color()
    return pillow_char_offset(0, 0, 128, 128, char, 200, font, color=color)


def make_img_for_slack2(char, font, color=None):
    if color is None:
        color = generate_random_color()
    if '\n' in char:
        chars = char.split('\n')
    elif len(char) >= 4:
        sep = -(-len(char) // 2)
        chars = [char[0:sep], char[sep:]]
    else:
        chars = [char]
    img = None
    for char in chars:
        if img is None:
            img = make_img_for_slack(char, font, color=color)
        else:
            img2 = make_img_for_slack(char, font, color=color)
            img = get_concat_v(img, img2)

    return img.resize((128, 128))
