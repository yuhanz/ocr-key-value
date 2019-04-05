import pytesseract
from PIL import Image
from itertools import groupby
import numpy as np


# schema = [u'level', u'page_num', u'block_num', u'par_num', u'line_num', u'word_num', u'left', u'top', u'width', u'height', u'conf', u'text']

LINE_INDEX = 4
CONF_INDEX = -2
WORD_INDEX = -1
LEFT_INDEX = -6
WIDTH_INDEX = -4

def processingOneLineOfWords(words, joinThreshold = 5):
    wordDistanceArr = map(lambda p: p[1][LEFT_INDEX] - (p[0][LEFT_INDEX] + p[0][WIDTH_INDEX]), zip(words, words[1:]))
    shouldSplit = list((np.array(wordDistanceArr) > joinThreshold) + 0)
    phraseIds = reduce(lambda s,x: s + [x+s[-1]] , shouldSplit, [0])
    # print(phraseIds)
    wordGroups = [map(lambda p: p[0], it) for k, it in groupby(zip(words, phraseIds), lambda p: p[1])]

    return map(lambda arr: arr[0][0:WORD_INDEX] + [' '.join(map(lambda w: w[WORD_INDEX], arr))], wordGroups)



def extract_data(img_file_path):
    data = pytesseract.image_to_data(Image.open(img_file_path))
    # print(data)
    arrays = map(lambda s: s.split('\t'), data.split('\n'))[1:]
    words = map(lambda arr: arr[0:6] + map(lambda i: int(i), arr[6:-1]) + [arr[-1]], arrays)
    words = filter(lambda arr: arr[CONF_INDEX] >0 and arr[WORD_INDEX], words)
    #lines = [' '.join(map(lambda arr: arr[-1], it)) for k, it in groupby(words, lambda arr: ','.join(arr[0:5]))]
    lines = [processingOneLineOfWords(map(lambda x: x, it)) for k, it in groupby(words, lambda arr: ','.join(arr[0:5]))]
    return [lines]

[lines] = extract_data('/tmp/1.png')

# print(data)
keyValues = dict(map(lambda line: [line[0][WORD_INDEX], line[1][WORD_INDEX] if len(line) >= 2 else ''], lines))
print(keyValues)
