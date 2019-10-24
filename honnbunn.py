
import re
import os.path,glob

def main():
    download_text = "maihime.txt"
    text = convert(download_text)
    print(text)
    with open("maihime.txt", "w") as f:
        f.write(text)

def convert(download_text):
    binarydata = open(download_text, 'rb').read()
    text = binarydata.decode('shift_jis')

    # ルビ、注釈などの除去
    text = re.split(r'\-{5,}', text)[2]
    text = re.split(r'底本：', text)[0]
    text = re.sub(r'《.+?》', '', text)
    text = re.sub(r'［＃.+?］', '', text)
    text = text.strip()
    return text

if __name__ == "__main__":
    main()
