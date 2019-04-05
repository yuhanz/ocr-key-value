import pytesseract
from PIL import Image
from itertools import groupby


# schema = [u'level', u'page_num', u'block_num', u'par_num', u'line_num', u'word_num', u'left', u'top', u'width', u'height', u'conf', u'text']

LINE_INDEX = 4
CONF_INDEX = -2
WORD_INDEX = -1

def extract_data(img_file_path):
    data = pytesseract.image_to_data(Image.open(img_file_path))
    arrays = map(lambda s: s.split('\t'), data.split('\n'))[1:]
    words = map(lambda arr: arr[0:6] + map(lambda i: int(i), arr[6:-1]) + [arr[-1]], arrays)
    words = filter(lambda arr: arr[CONF_INDEX] >0 and arr[WORD_INDEX], words)
    lines = [' '.join(map(lambda arr: arr[-1], it)) for k, it in groupby(words, lambda arr: ','.join(arr[0:5]))]
    return [words, lines]

print(extract_data('/tmp/1.png'))

