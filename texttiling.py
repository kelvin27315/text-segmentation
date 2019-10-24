from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import MeCab
import os

def wakathi(text):
    m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    all_words = []
    sentence_parse_words = []
    for sent in text.splitlines():
        words_in_sentence = []
        words = m.parse(sent).splitlines()
        for word in words:
            if word != "EOS":
                words_in_sentence.append(word.split("\t")[0])
                all_words.append(word.split("\t")[0])
        sentence_parse_words.append(words_in_sentence)
    all_words = list(set(all_words))
    return(sentence_parse_words, all_words)

def make_hyo(all_words, parsed_text):
    hyo = pd.DataFrame(0, index = list(range(len(parsed_text))), columns = all_words)
    for i,sentence in enumerate(parsed_text):
        for word in sentence:
            hyo.iloc[i,:].loc[word] += 1
    return(hyo)

def cos_simi(hyo,windowsize,all_words):
    ruiji = [list(range(windowsize,len(hyo)+1-windowsize)), [0]*(len(hyo)+1-windowsize*2)]
    for num, i in enumerate(tqdm(range(windowsize-1,len(hyo)-windowsize))):
        Lwindow = pd.DataFrame(0, columns = all_words, index = [0])
        Rwindow = pd.DataFrame(0, columns = all_words, index = [0])
        for j in range(windowsize):
            Lwindow += hyo.iloc[i-j,:]
            Rwindow += hyo.iloc[i+1+j,:]
        ruiji[1][num] = np.dot(Lwindow.iloc[0,:],Rwindow.iloc[0,:]) / (np.linalg.norm(Lwindow.iloc[0,:]) * np.linalg.norm(Rwindow.iloc[0,:]))
    return(ruiji)

def drow_graph(ruiji,windowsize,text_file_path):
    if text_file_path == "text/chumonno_oi_ryoriten.txt":
        text_name = "注文の多い料理店"
    elif text_file_path == "text/gingatetsudou_no_yoru.txt":
        text_name = "銀河鉄道の夜"
    elif text_file_path == "text/maihime.txt":
        text_name = "舞姫"
    else:
        text_name = "NTTの例文"
    plt.figure(figsize=(8,5),dpi=100)
    plt.plot(ruiji[0],ruiji[1])
    plt.title("-TextTiling- file: "+text_name+", W.size: " + str(windowsize))
    plt.savefig("pic/" +text_name+ "_"+str(windowsize)+"texttiling.png")
    plt.close()

if __name__ == "__main__":
    #file_path = "text/chumonno_oi_ryoriten.txt"
    file_path = "text/gingatetsudou_no_yoru.txt"
    #file_path = "text/maihime.txt"
    #file_path = "text/test.txt"
    with open(file_path, "r") as f:
        text = f.read()
    parsed_text, all_words = wakathi(text)
    hyo = make_hyo(all_words, parsed_text)
    for windowsize in range(1,15):
        ruiji = cos_simi(hyo,windowsize,all_words)
        drow_graph(ruiji,windowsize,file_path)