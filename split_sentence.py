import re
import sys
import os
from tqdm import tqdm

def Process(sentences,s_type):
    """
    いらない部分を取り除く
    """
    if s_type == "Sentence":
        #。で改行
        sentences = re.sub("。","。\n",sentences)
    #頭の改行を削除
    sentences = sentences[1:-1]
    #空白の行を削除
    sentences = re.sub("\n+","\n",sentences)
    #全部の行にの末尾に\nが来るようにした
    sentences += "\n"
    return(sentences)

if __name__ == "__main__":
    s_types = ["Sentence"]
    for s_type in s_types:
        print(s_type + "の準備をしています")
        file_paths = ["text/chumonno_oi_ryoriten.txt","text/gingatetsudou_no_yoru.txt","text/maihime.txt"]
        for file_path in tqdm(file_paths):
            with open(file_path, "r") as f:
                sentences = f.read()
            sentences = Process(sentences,s_type)
            #記事の保存
            file_path += "test.txt"
            with open(file_path, "w") as f:
                f.write(sentences)