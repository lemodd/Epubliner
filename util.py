from ebooklib import epub
from bs4 import BeautifulSoup
import ebooklib


# def retrieve(ainfo,epub_file):
#     for item in self.appinfo['books']:
#         if self.epub_file_path == item['bookname']:
#             print(item)




class EpubReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.book = self.load_epub()
        self.chapters = self.get_chapters()
        self.total = len(self.chapters)

    def load_epub(self):
        book = epub.read_epub(self.file_path)
        return book

    def get_chapters(self):
        chapters = []
        items = self.book.get_items()
        for item in self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            chapters.append(item)
        return chapters

    def get_chapter(self, i):
#         print(self.total)
        if i >= self.total:
            return "The book is over!"
        chapter = self.chapters[i]
        soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
        text = soup.get_text()
        
        return text
    
           
                
                
def rgb_to_hex(rgb):
    r, g, b = rgb
    hex_string = '#{:02X}{:02X}{:02X}'.format(r, g, b)
    return hex_string

def detect_language(text):
    """
    判断文本主要是中文还是英文
    
    参数:
        text (str): 要判断的文本
        
    返回:
        str: 'cn' - 如果文本主要是中文
             'en' - 如果文本主要是英文
             'mi' - 如果中英文混合比例接近
    """
    # 统计中文字符和英文字符的数量
    chinese_chars = 0
    english_chars = 0
    other_chars = 0
    
    for char in text:
        # 中文字符的Unicode范围
        if '\u4e00' <= char <= '\u9fff':
            chinese_chars += 1
        # 基本拉丁字母（英文）、数字和标点
        elif ord(char) < 128:
            english_chars += 1
        else:
            other_chars += 1
    
    total_relevant = chinese_chars + english_chars
    if total_relevant == 0:
        return 'Unknown'
    
    chinese_ratio = chinese_chars / total_relevant
    english_ratio = english_chars / total_relevant
    
    # 判断阈值可以调整
    if chinese_ratio > 0.4:
        return 'cn'
    else:
        return 'en'





import re

def extract_text_with_position(text, start, step):
    """
    从指定位置开始按步长提取文本，保证不拆分单词，遇到换行符则停止，并返回下次读取位置
    
    参数:
        text (str): 输入的英文文本
        start (int): 开始位置(从0开始计数)
        step (int): 步长(字符数)
    
    返回:
        tuple: (提取的文本片段, 下次读取的起始位置)
              如果无法提取有效文本，返回 ("", start)
    """
    # 参数校验
    if start < 0 or step <= 0 or start >= len(text):
        return ("", start)
    
    # 找到从start位置开始的下一个单词边界
    match = re.search(r'\b\w', text[start:])
    adjusted_start = start + match.start() if match else start
    
    # 计算理论结束位置
    end = adjusted_start + step
    
    # 确保结束位置不超过文本长度
    end = min(end, len(text))
    
    # 查找从adjusted_start到end之间第一个换行符的位置
    newline_pos = text.find('\n', adjusted_start, end)
    if newline_pos != -1:
        end = newline_pos + 1  # 包含换行符
    else:
        # 如果没有换行符，检查结束位置是否在单词中间
        if end < len(text) and re.match(r'\w', text[end]):
            # 从结束位置向前找第一个非单词字符
            boundary = text.rfind(' ', adjusted_start, end)
            if boundary != -1:
                end = boundary
    
    # 提取子字符串
    extracted = text[adjusted_start:end].rstrip()  # 只去除右侧空格
    
    # 计算下次读取位置
    next_position = end
    
    return (extracted, next_position)

# 示例用法：模拟连续读取含换行符的文本
# if __name__ == "__main__":
#     long_text = """This is the first line of text.
# This is the second line, which is longer than the first one.
# The third line contains some special cases like hyphenated-words.
# Finally, the last line."""
#     
#     
#     i=0
#     step = 20
#     for j in range(7):
#         txt,i = extract_text_with_position(long_text,i,step)
#         print(txt,i)
        
        
        
#     # 模拟分块读取过程
#     position = 0
#     chunk_size = 30
#     chunk_num = 1
#     
#     print("Original text:")
#     print("--------------")
#     print(long_text)
#     print("\nExtracted chunks:")
#     print("-----------------")
#     
#     while position < len(long_text):
#         chunk, position = extract_text_with_position(long_text, position, chunk_size)
#         if not chunk:
#             break
#         print(f"Chunk {chunk_num}: {repr(chunk)}")
#         print(f"Next position: {position}\n")
#         chunk_num += 1

