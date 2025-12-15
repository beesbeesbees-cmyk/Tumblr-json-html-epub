from ebooklib import epub
from bs4 import BeautifulSoup
import html
import re
import pathlib
import os
import os.path

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


class App(tk.Frame):
    def __init__(self, master): # Runs as soon as program starts
        super().__init__(master)
        
        frm = ttk.Frame(root, padding='0.1i')
        frm.grid()
        frm.rowconfigure(1, weight=3, minsize='0.5i')
        frm.rowconfigure(2, weight=3, minsize='0.5i')
        frm.columnconfigure(0, weight=3, minsize='0.5i')
        
        ttk.Button(
            frm, text="Where are your HTML files?", command=self.choose_directory).grid(column=0, row=0, columnspan=3, sticky="NW")
        self.path_display_text = tk.StringVar()
        self.path_display_text.set("Selected Directory: ")
        self.htmlpath = ""
        self.directory_label = ttk.Label(frm, text="Selected Directory: ", width=80)
        self.directory_label.grid(column=0, row=1, columnspan=3)
        self.directory_label['textvariable'] = self.path_display_text
        
        self.status_display_text = tk.StringVar()
        self.status_label = ttk.Label(frm, text="", width=80)
        self.status_label.grid(column=0, row=2, columnspan=3)
        self.status_label['textvariable'] = self.status_display_text
        
        self.confirm_button = ttk.Button(frm, text="Confirm", command=self.execute) # Self passes itself as first param
        self.confirm_button.grid(column=1, row=3, columnspan=1, sticky="SE")
        self.confirm_button.state(['disabled'])
        self.exit_button = ttk.Button(frm, text="Exit", command=root.destroy)
        self.exit_button.grid(column=2, row=3, columnspan=1, sticky="SE")
        
        
    def choose_directory(self):
        htmlpath = filedialog.askdirectory(title="Where are your HTML files?")
        self.htmlpath = htmlpath
        self.path_display_text.set(f"Selected Directory: {htmlpath}") # Sets text of label to htmlpath)
        if os.path.exists(htmlpath): # If path exists, enable button
            self.confirm_button.state(['!disabled'])

    def execute(self):
        
        htmlpath = self.htmlpath
        chapters = {}
        chapter_links = []
        imgs = []
        index = 0

        book = epub.EpubBook()
        book.add_item(epub.EpubNav(uid = 'nav', file_name = 'nav.xhtml'))
        book.spine = ['nav']
        style = '''
            @namespace epub "http://www.idpf.org/2007/ops";
            body {
                font-family: OpenDyslexic;
            }
            h6 {
                text-align: left;
                font-size: 10pt;
                font-weight: 200;     
            }
            ol {
                    list-style-type: none;
            }
            ol > li:first-child {
                    margin-top: 0.3em;
            }
            nav[epub|type~='toc'] > ol > li > ol  {
                list-style-type:square;
            }
            nav[epub|type~='toc'] > ol > li > ol > li {
                    margin-top: 0.3em;
            }
            indiv_pics {
                text-align: center;
                page-break-inside: avoid;
                object-align: center;
            }
            img {
                max-width: 100%;
                object-fit: contain;
                width: auto;
                object-align: center;
            }
            
            blockquote {
                font-size: 12pt;    
            }
            '''
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style,
            manifest=True,
        )
        book.add_item(nav_css)

        intit = os.path.basename(os.path.normpath(htmlpath))
        book.set_title(intit)
        book.set_language("en")

        for file in os.listdir(htmlpath):
            if file.endswith('.html'):
                fname = os.path.join(htmlpath,file)
                with open(fname, 'r', encoding="utf8") as f:
                    index = index + 1
                    soup = BeautifulSoup(f.read(),'html.parser')
                    # print(soup)
                    title = file
                    title = title.replace('.html','')
                    print(title)
                    # title = re.search('(?<=<h6>).*?(?=GMT)', str(soup))
                    # title = title.group(0)
                    filename = fname.replace(f"{htmlpath}\\", "")
                    
                    chapter = epub.EpubHtml(title = title, file_name = filename, media_type = 'application/xhtml+xml', content = str(soup), uid = str(index))
                    chapter.add_item(nav_css)
                    book.add_item(chapter)
                    book.spine.append(chapter)
                    chapter_links.append(epub.Link(href = filename, title = title, uid = str(index)))

        book.toc = tuple(chapter_links)  
        book.add_item(epub.EpubNcx(uid='ncx', file_name = 'toc.ncx'))
        book.spine.append('ncx')

        epub.write_epub(f"{htmlpath}\\{intit}.epub", book)
        print("epub written successfully! Check it out!")

root = tk.Tk()
root.title("JSON to HTML")
myapp = App(root)

myapp.mainloop()