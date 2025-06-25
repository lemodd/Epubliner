'''
readme中所有功能都实现了


'''



import tkinter as tk
import pygubu
import yaml
import time
import sys
import pyautogui
import tkinter.messagebox

from tkinter import *
from tkinter import filedialog
from pathlib import Path
from EpubLinerui import EpubLinerUI

from util import *

page_state = 0




class EpubLiner(EpubLinerUI):
    def __init__(self, master=None, on_first_object_cb=None):
        super().__init__(master, on_first_object_cb=None)
        
        self.my = self.builder.get_object('tk_1')
        self.label = self.builder.get_object('label_1')
        self.hidedtitle = 0
#         self.my.attributes("-toolwindow", 1)
        
        self.top = 1
        
        self.fonts = ['微软雅黑','宋体','仓耳今楷02 W03','仿宋','楷体']
        self.font_no = 0
   
        #阅读进度在self.chapter中位置
        self.counter = 0        
        self.text_width = 34
        self.tex = ''
        self.font_size = 12
         
        self.hidedtitle = False
        self.transparent = False
        
        self.appinfo={} 
        #当前章节
        self.chapterNo = 0
#         self.epub_file_path = 'E:/lemo/EpubLiner/4.0/c.epub'
        
        with open('re.yaml',encoding='utf-8') as f:
            self.appinfo = yaml.load(f,Loader=yaml.FullLoader)#读取yaml文件
            
        self.text_width = self.appinfo['options']['text_width']
        
        self.label.config(width = self.text_width)
        
        x = self.appinfo['options']['scrx']
        y = self.appinfo['options']['scry']
        self.my.geometry(f"+{x}+{y}")
        
        self.hidedtitle = self.appinfo['options']['hidedtitle']
        self.my.overrideredirect(self.hidedtitle)
#         self.my.attributes("-transparent", "#f0f0f0")
        self.transparent = self.appinfo['options']['transparent']
        self.set_transparent()
        
        self.font_no = self.appinfo['options']['font_no']
        self.font_size = self.appinfo['options']['font_size']
        
        if self.appinfo['options']['book_reading']:
            self.epub_file_path =self.appinfo['options']['book_reading']

            for item in self.appinfo['books']:

                if self.epub_file_path == item['bookname']:
#                     print(item)
                    self.chapterNo = item['chapterNo']
                    self.counter = item['counter']
                    self.lang = item['lang']
                    break
            
            self.openepub()
            self.pagedown()
        
        self.my.protocol("WM_DELETE_WINDOW", self.exitapp)  

    def openepub(self):
        self.book = EpubReader(self.epub_file_path)
        self.chapter = self.book.get_chapter(self.chapterNo) 
#         self.lang = detect_language(self.book.get_chapter(3))
        
        with open('re.yaml',encoding='utf-8') as f:
            self.appinfo = yaml.load(f,Loader=yaml.FullLoader)#读取yaml文件
            
            
        new = True    
        for item in self.appinfo['books']:
#             print('fffff',item)
            if 'bookname' in item and item['bookname'] == self.epub_file_path:

                self.chapterNo = item['chapterNo']
                self.counter = item['counter']
                self.lang = item['lang']
                print('存有记录，将继续阅读')
                new = False
                break   
        if new:
            #没有记录，新建一条
            print('new-------')
            newbook = {}
            newbook['bookname'] = self.epub_file_path
            newbook['chapterNo'] = 0
            newbook['counter'] = 0
            newbook['lang'] = self.lang
            
            self.appinfo['books'].append(newbook)
                      
        self.appinfo['options']['book_reading'] = self.epub_file_path
        
        self.save_appinfo() 
        
    def pagedown(self,event=None):
        
        if self.lang == "cn":
            text_length = int(self.text_width/2)-2
            self.tex = self.chapter[self.counter:self.counter + text_length]
            self.tex = self.tex.replace('\n',' ')
            self.counter += text_length
            
            progress = str(int(self.counter/len(self.chapter)*100))
            self.tex = f"[{progress}] {self.tex}"
            
            #仓耳今楷02 W03
            #
            self.label.config(text=self.tex,font=(self.fonts[self.font_no],self.font_size))

        else:
            text_length = self.text_width-2
            self.tex,self.counter = extract_text_with_position(self.chapter,self.counter,text_length)
            
            progress = str(int(self.counter/len(self.chapter)*100))
            self.tex = f"[{progress}] {self.tex}"
            
            self.label.config(text=self.tex,font=(self.fonts[self.font_no],self.font_size))
            
        #如果本章结束，翻到下一章
        if self.counter >= len(self.chapter):
            self.chapterNo += 1
            self.chapter = self.book.get_chapter(self.chapterNo) 
            self.counter = 0

        
        print(self.tex)
        
        for item in self.appinfo['books']:
            if self.epub_file_path == item['bookname']:
                item['chapterNo'] = self.chapterNo
                item['counter'] = self.counter - text_length
                break

        self.save_appinfo() 


    def pageup(self):
        if self.lang == "cn":
            text_length = int(self.text_width/2)
            self.tex = self.chapter[self.counter - text_length:self.counter]
            self.tex = self.tex.replace('\n',' ')
            self.counter -= text_length
            self.label.config(text=self.tex,font=(self.fonts[self.font_no],self.font_size))
            print(self.tex)
        else:
            if self.counter >= self.text_width:
                self.counter -= self.text_width
            else:
                return
            
            text_length = self.text_width
            self.tex,self.counter = extract_text_with_position(self.chapter,self.counter,text_length)
            self.label.config(text=self.tex,font=(self.fonts[self.font_no],self.font_size))
            
            if self.counter >= self.text_width:
                self.counter -= self.text_width
            else:
                return

        if self.counter >= len(self.chapter):
            self.chapterNo += 1
            self.openepub()
            self.counter = 0

        print(self.counter,len(self.chapter),self.tex)
        
        for item in self.appinfo['books']:
            if self.epub_file_path == item['bookname']:
                item['chapterNo'] = self.chapterNo
                item['counter'] = self.counter
#                 print(item)

        self.save_appinfo()
        
        
    def exitapp(self,event=None):
        self.appinfo['options']['scrx'] = self.my.winfo_x()
        self.appinfo['options']['scry'] = self.my.winfo_y()
        
#         with open('re.yaml','w',encoding='utf-8') as f:
#             yaml.dump(self.appinfo,f,allow_unicode=True)
        self.save_appinfo()
        sys.exit(0)
        self.my.destroy()
        
    def save_appinfo(self):
        with open('re.yaml','w',encoding='utf-8') as f:
            yaml.dump(self.appinfo,f,allow_unicode=True)
            
    def m(self,event=None):
        if self.font_size >= 20:
            return 
        self.font_size += 1
        print(self.font_size)
        
        self.appinfo['options']['font_size'] = self.font_size
        
        self.label.config(text=self.tex,font=(self.fonts[self.font_no],self.font_size))
        
    
    def f(self,event=None):
        if self.font_no < 4:
            self.font_no += 1
        else:
            self.font_no = 0
        self.appinfo['options']['font_no'] = self.font_no   
        self.label.config(text=self.tex,font=(self.fonts[self.font_no],self.font_size))

    
    def n(self,event=None):
        if self.font_size <= 5:
            return 
        self.font_size -= 1
        self.appinfo['options']['font_size'] = self.font_size
        print(self.font_size)            
        self.label.config(text=self.tex,font=(self.fonts[self.font_no],self.font_size))    
            
    def o(self,event=None):
        self.epub_file_path = filedialog.askopenfilename(title = "test",filetypes=[("电子书",".epub")])
        print(self.epub_file_path)

        self.openepub()           
        
        
    def x(self, event=None):
        if page_state == 1:
            self.pagedown()
        self.pagedown()
        

    def z(self, event=None):
        if page_state == 0:
            self.pageup()
        self.pageup()
        
    def t(self, event=None):
        self.my.attributes("-topmost", self.top)
        self.top = not self.top
        
        self.appinfo['options']['ontop'] = self.top
        
        self.save_appinfo()
        
    def r(self, event=None):
        self.transparent = not self.transparent
        self.set_transparent()
        self.appinfo['options']['transparent'] = self.transparent        
        self.save_appinfo() 

    #设置透明
    def set_transparent(self):
        if self.transparent:
            self.my.attributes("-transparent", "#f0f0f0")
        else:
            self.my.attributes("-transparent", "")
        



        
    def h(self, event=None):
        
        self.hidedtitle = not self.hidedtitle
        self.my.overrideredirect(self.hidedtitle)
        
        self.appinfo['options']['hidedtitle'] = self.hidedtitle
        
        self.save_appinfo() 
    
    
    def move_scr(self, event=None):
        if event.keysym == 'w':
            self.w(event.keysym == 'w')
        if event.keysym == 'a':
            self.a(event.keysym == 'a')
        if event.keysym == 's':
            self.s(event.keysym == 's')
        if event.keysym == 'd':
            self.d(event.keysym == 'd')
        
        x = self.my.winfo_x()
        y = self.my.winfo_y()
                
        self.appinfo['options']['scrx'] = x
        self.appinfo['options']['scry'] = y
        

        
#         color = pyautogui.pixel(x,y)
#         color_hex = rgb_to_hex(color)
#         
# #         self.my.configure(bg=color_hex)
#         self.label.configure(background=color_hex)
        
# 
#         print(color_hex)
        self.save_appinfo()     




#移动窗口====
    def w(self, event=None):
        x = self.my.winfo_x()
        y = self.my.winfo_y()-1
        self.my.geometry(f"+{x}+{y}")

    def a(self, event=None):
        x = self.my.winfo_x()-1
        y = self.my.winfo_y()
        self.my.geometry(f"+{x}+{y}")        

    def s(self, event=None):
        x = self.my.winfo_x()
        y = self.my.winfo_y()+1
        self.my.geometry(f"+{x}+{y}")

    def d(self, event=None):
        x = self.my.winfo_x()+1
        y = self.my.winfo_y()
        self.my.geometry(f"+{x}+{y}")

        
        
#移动窗口====
    
#设置窗口长度，“,”减小；“.” 增加       
    def on_longer_press(self, event=None):
        self.text_width += 1
        self.label.config(width=self.text_width)
        
#         with open('re.yaml',encoding='utf-8') as f:
#             self.appinfo = yaml.load(f,Loader=yaml.FullLoader)#读取yaml文件
        
        self.appinfo['options']['text_width'] = self.text_width
        
        self.save_appinfo() 
        
    def on_shorter_press(self,event=None):
        self.text_width -= 1
        self.label.config(width=self.text_width)
        
#         with open('re.yaml',encoding='utf-8') as f:
#             self.appinfo = yaml.load(f,Loader=yaml.FullLoader)#读取yaml文件
        
        self.appinfo['options']['text_width'] = self.text_width
        
        self.save_appinfo() 
    
#设置窗口长度，“,”减小；“.” 增加           


if __name__ == "__main__":
    app = EpubLiner()
    app.run()
