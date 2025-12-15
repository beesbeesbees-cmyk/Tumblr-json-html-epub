## STEP 0: Initialization.
import json
import re
import fnmatch
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
                frm, text="Where are your JSON files?", command=self.choose_json_directory).grid(column=0, row=0, columnspan=1, sticky="NW")
            self.jsonpath_display_text = tk.StringVar()
            self.jsonpath_display_text.set("Selected JSON Directory: ")
            self.jsonpath = ""
            self.json_directory_label = ttk.Label(frm, text="Selected JSON Directory: ", width=80)
            self.json_directory_label.grid(column=0, row=1, columnspan=3)
            self.json_directory_label['textvariable'] = self.jsonpath_display_text

            ttk.Button(
                frm, text="Where do you want your HTML files?", command=self.choose_html_directory).grid(column=1, row=0, columnspan=1)
            self.htmlpath_display_text = tk.StringVar()
            self.htmlpath_display_text.set("Selected HTML Directory: ")
            self.htmlpath = ""
            self.html_directory_label = ttk.Label(frm, text="Selected HTML Directory: ", width=80)
            self.html_directory_label.grid(column=0, row=2, columnspan=3)
            self.html_directory_label['textvariable'] = self.htmlpath_display_text
            
            self.target_post_type_display_text = tk.StringVar()
            self.target_post_type_display_text.set("Target Post Type: ")
            self.target_post_type_label = ttk.Label(frm,text="Target Post Type: ",width=80)
            self.target_post_type_label.grid(column=0, row=3, columnspan=3)
            self.target_post_type_label['textvariable'] = self.target_post_type_display_text

            options_list = ["", "regular", "answer", "text", "photo", "audio", "video", "link", "conversation", "quote"]
            self.target_post_type_input = tk.StringVar(frm)
            self.target_post_type = ttk.OptionMenu(frm, self.target_post_type_input, *options_list)
            self.target_post_type.grid(column=1, row=3, columnspan=3)
            self.target_post_type_input.set("Select an Option")

            self.tag_search_display_text = tk.StringVar()
            self.tag_search_display_text.set("Tag Search Term: ")
            self.tag_search_label = ttk.Label(frm,text="Tag Search Term: ",width=80)
            self.tag_search_label.grid(column=0, row=4, columnspan=3)
            self.tag_search_label['textvariable'] = self.tag_search_display_text

            self.tag_search_input = tk.StringVar()
            self.tag_search = ttk.Entry(frm, textvariable=self.tag_search_input)
            self.tag_search.grid(column=1, row=4, columnspan=3)
            self.tag_search['textvariable'] = self.tag_search_input

            self.search_display_text = tk.StringVar()
            self.search_display_text.set("Search Term: ")
            self.search_label = ttk.Label(frm,text="Search Term: ",width=80)
            self.search_label.grid(column=0, row=5, columnspan=3)
            self.search_label['textvariable'] = self.search_display_text

            self.search_input = tk.StringVar()
            self.search = ttk.Entry(frm, textvariable=self.search_input)
            self.search.grid(column=1, row=5, columnspan=3)
            self.search['textvariable'] = self.search_input

            self.status_display_text = tk.StringVar()
            self.status_label = ttk.Label(frm, text="", width=80)
            self.status_label.grid(column=0, row=6, columnspan=3)
            self.status_label['textvariable'] = self.status_display_text
            
            self.confirm_button = ttk.Button(frm, text="Confirm", command=self.execute) # Self passes itself as first param
            self.confirm_button.grid(column=1, row=7, columnspan=1, sticky="SE")
            self.confirm_button.state(['disabled'])
            self.exit_button = ttk.Button(frm, text="Exit", command=root.destroy)
            self.exit_button.grid(column=2, row=7, columnspan=1, sticky="SE")

    def choose_json_directory(self):
        jsonpath = filedialog.askdirectory(title="Where are your JSON files?")
        self.jsonpath = jsonpath
        self.jsonpath_display_text.set(f"JSONs are in: {jsonpath}") # Sets text of label to htmlpath)
        if os.path.exists(jsonpath): # If path exists, enable button
            self.confirm_button.state(['!disabled'])

    def choose_html_directory(self):
        htmlpath = filedialog.askdirectory(title="Where do you want your HTML files?")
        self.htmlpath = htmlpath
        self.htmlpath_display_text.set(f"HTMLs will go to: {htmlpath}") # Sets text of label to htmlpath)
        if os.path.exists(htmlpath): # If path exists, enable button
            self.confirm_button.state(['!disabled'])

    def execute(self):
        index = 0
        dup_index = 0
        parsed_ids = []

        jsonpath = self.jsonpath
        htmlpath = self.htmlpath 
        target_post_type = self.target_post_type_input.get() 
        tag_search = self.tag_search_input.get() 
        search_term = self.search_input.get() 

        ## STEP 2.0: Search jsonpath for .json files.
        for path, dirs, files in os.walk(jsonpath):
                print(f"{path}")
                for name in files:
                    if name.endswith((".json")):
                        f = open(str(path + "\\" + name), encoding="utf-8-sig")
                        data = json.load(f)

                        def categorizer(data):
                            ## STEP 2.4: Categorize the post.
                            if 'type' not in data.keys():
                                post_type = 'regular'
                            elif 'originalType' in data.keys():
                                post_type = data['originalType']
                            else:
                                post_type = data['type']
                            
                            return post_type
                        
                        post_type = categorizer(data)

                        if post_type == target_post_type:

                            def tag_reader(data):
                                if "tags" in data.keys():
                                    Tags = ", \r\n".join(data["tags"]) + f", {post_type}"
                                else:
                                    Tags = f"Untagged, {post_type}"
                                return Tags
                            
                            Tags = tag_reader(data)

                            if tag_search in Tags:

                                idnum = data['id']

                                def op_finder(data):
                                    if 'reblogged_root_name' in data.keys() and data['reblogged_root_name'] != '':
                                        op = data['reblogged_root_name']
                                    elif 'reblogged-root-name' in data.keys() and data['reblogged-root-name'] != '':
                                        op = data['reblogged-root-name']
                                    elif 'blog' in data.keys():
                                        op = data['blog']['name']
                                    else:
                                        op = data['tumblelog']['name']

                                    if 'blog' in data.keys():
                                        from_blog = data['blog']['name']
                                    else:
                                        from_blog = data['tumblelog']['name']

                                    return op, from_blog
                                
                                op, from_blog = op_finder(data)

                                def json_structureizer(data):
                                    ## STEP 2.7: Categorize the .json file structure.
                                    if 'trail' in data.keys():
                                        disp = 'CANNOT CURRENTLY DISPLAY'
                                        JSON_type = "SVC"
                                        date = data['date']
                                    elif "date-gmt" in data.keys():
                                        JSON_type = "API"
                                        date = data['date-gmt']
                                        if 'regular-body' in data.keys():
                                            disp = data['regular-body']
                                        elif 'post-text' in data.keys():
                                            disp = data['post-text']
                                    elif 'regular-title' in data.keys():
                                        JSON_type = "SVC"
                                        date = data['date']
                                        disp = '<h3>' + data['regular-title'] + '</h3>' + '<br>' + " \r\n" + data['regular-body']
                                    elif 'post_html' in data.keys():
                                        disp = data['post_html']
                                        JSON_type = "SVC"
                                        date = data['date']
                                    else:
                                        print(f"CANNOT PARSE: {name}")
                                        disp = ""
                                        JSON_type = "SVC"
                                        date = data['date']
                                    return disp, JSON_type, date

                                disp, JSON_type, date = json_structureizer(data)

                                def post_titler(data):
                                    if 'slug' in data.keys():
                                        post_title = data['slug']
                                    else:
                                        post_title = name
                                    
                                    return post_title
                                
                                post_title = post_titler(data)

                                html_base = "<!DOCTYPE html>" + "\r\n" + '<html lang="en">' + "\r\n" + '<meta charset="utf-8">' + '\r\n <head>' + f"<title>{post_title}</title>" + '\r\n' + '<link rel="stylesheet" type="text/css" href="nav.css"/> </head>' + "\r\n  <body><h6>"

                                def html_establisher(data, date, disp, Tags, from_blog, op, post_type, idnum):
                                    if post_type == 'answer':
                                        if 'asking_name' in data.keys() and data['asking_name'] != []:
                                            asker = data['asking_name']
                                        else:
                                            asker = 'Anon'
                                        disp = f"<blockquote><i>{asker} asked: \r\n\r\n <blockquote>{data['question']}</i></blockquote></blockquote>" + "\r\n\r\n" + " \r\n \r\n <hr>" + data['answer']
                                        html_out = html_base +  date + " \r\n" + disp
                                    elif post_type == 'text' or post_type == 'regular':
                                        html_out = html_base +  date + " \r\n <p>" + disp + "</p>"
                                    elif post_type == 'photo': 
                                        cap = ""
                                        if 'photoset_photos' in data.keys() and data['photoset_photos'] != []:
                                            b = []
                                            index_num = 0
                                            while index_num < len(data['photoset_photos']):
                                                Width = data['photoset_photos'][index_num]['width']
                                                Height = data['photoset_photos'][index_num]['height']
                                                hq = data['photoset_photos'][index_num]['high_res']
                                                b.append(f'<div class="indiv_pics"> <img width={Width}px height={Height}px src={hq}> </div>')
                                                index_num += 1
                                            disp = ' <br/>\r\n '.join(b)
                                        else:
                                            if 'photos' in data.keys() and data['photos'] != []:
                                                pics = data['photos']
                                                disp = []
                                                for dictionary in pics:
                                                    disp.append(f"<img src={dictionary['photo-url-1280']}>")
                                                disp = " \r\n".join(disp)
                                            elif "photo-url-1280" in data.keys() and data['photo-url-1280'] != "":
                                                disp = '<img src="' + data['photo-url-1280'] + '"/>'

                                        if 'photo-caption' in data.keys() and data['photo-caption'] != []:
                                            cap = data['photo-caption']
                                        elif 'caption' in data.keys() and data['caption'] != []:
                                            cap = data['caption'] 
                                            
                                        if "photo-url-1280" not in data.keys() and 'photoset_photos' not in data.keys() and 'post_html' in data.keys() and data['post_html'] != []:
                                            disp = data['post_html']  
                                            cap = ''
                                        elif cap == "": 
                                            cap = ''

                                        html_out = html_base + date + " \r\n <p>" + disp + "</p>" + cap
                                    elif post_type == 'audio':
                                        if 'id3-title' in data.keys() and data['id3-title'] != '':
                                            disp = f"{data['audio-embed']}" + " \r\n" + f"{data['id3-title']} by {data['id3-artist']}, on album {data['id3-album']}. \r\n \r\n {data['audio-caption']}"
                                        elif 'post_html' in data.keys():
                                            disp = f"{data['embed']}" + " \r\n" + f"{data['post_html']}" 
                                        elif 'audio-embed' in data.keys():
                                            disp = f"{data['audio-embed']}" + " \r\n" + f"{data['audio-caption']}"
                                        else:
                                            print(f"AUDIO ERRROR: {name}")
                                        
                                        html_out = html_base + date + " \r\n <p>" + disp + "</p>"
                                    elif post_type == 'video':
                                        if 'video-source' in data.keys() and data['video-source'] != '':
                                            disp = f"Original video url:\r\n{data['video-source']} \r\n \r\n {data['video-caption']}"
                                        elif 'post_html' in data.keys() and data['post_html'] != '':
                                            disp = f"{data['post_html']}"
                                        else:
                                            print(f"VIDEO ERROR: {name}")

                                        html_out = html_base + date + " \r\n <p>" + disp
                                    elif post_type == 'link':
                                        if 'link-url' in data.keys() and data['link-url'] != '':
                                            if 'link-text' in data.keys():
                                                disp = f"{data['link-text']}\r\n at {data['link-url']}\r\n \r\n {data['link-description']}"
                                            else:
                                                disp = f"{data['link-url']}\r\n \r\n {data['link-description']}"
                                        
                                        html_out = html_base + date + " \r\n <p>" + disp + "</p>"
                                    elif post_type == 'chat':
                                        if 'conversation-title' in data.keys():
                                            disp = f"<b>{data['conversation-title']}</b> \r\n \r\n {data['conversation-text']}"
                                        elif 'post_html' in data.keys():
                                            disp = f"{data['post_html']}"
                                        else:
                                            print(f"CHAT ERROR: {name}")

                                        html_out = html_base + date + " \r\n <p>" + disp + "</p>"
                                    elif post_type == 'conversation':
                                        if 'conversation-title' in data.keys():
                                            disp = f"<b>{data['conversation-title']}</b> \r\n \r\n {data['conversation-text']}"
                                        elif 'conversation' in data.keys():
                                            c = []
                                            cindex_num = 0
                                            while cindex_num < len(data['conversation']):
                                                label = data['conversation'][cindex_num]['label']
                                                phrase = data['conversation'][cindex_num]['phrase']
                                                c.append(f'<p><b>{label}</b> {phrase}</p> <br/> ')
                                                cindex_num += 1
                                            disp = ' \r\n '.join(c)
                                        else: 
                                            print(f"CONVERSATION ERROR: {name}")
                                        
                                        html_out = html_base + date + " \r\n <p>" + disp + "</p>"
                                    elif post_type == 'quote':
                                        if 'quote-source' in data.keys():
                                            disp = f"{data['quote-source']}     {data['quote-text']}"
                                        else:
                                            print(f"QUOTE ERROR: {name}")

                                        html_out = html_base + date + " \r\n <p>" + disp + "</p>"
                                    else:
                                        print(f"NO VALID POST TYPE: {name}")
                                        html_out = f"ERROR, SEE JSON {name}"
                                    
                                    return html_out
                    
                                html_out = html_establisher(data, date, disp, Tags, from_blog, op, post_type, idnum)
                                html_out = html_out + " \r\n <p>" + f"<sub>Tagged: \r\n <blockquote>{Tags}</blockquote></sub>" + f'<footer style="text-align:right"><sub>via {from_blog}. Originally posted by {op}, re/posted on {date}. {post_type} post. {idnum}</sub></footer>' + "</body>"
                                
                                def stuff_remover(html_out):

                                    ## STEP 3.2: Determine whether or not post contains a readmore.
                                    if "Keep reading" in html_out:
                                        print(f"READMORE: {name} contains a readmore.")

                                    if 'reblog-avatar' in html_out:
                                        html_out = re.sub('<a class="reblog-avatar.*?}" >', ' ', html_out)
                                        html_out = re.sub('<img class="reblog-avatar-image-thumb".*?" >', ' ', html_out)

                                    if 'https://www.youtube.com/' in html_out:
                                        html_out = re.sub('<figure.*?https://www.youtube.com/.*?/figure>', '[INSERT YOUTUBE VIDEO HERE]', html_out)
                                        html_out = re.sub('<figure class="tmblr-full tmblr-embed" data-provider="youtube.*?</figure>"','[INSERT YOUTUBE VIDEO HERE]',html_out)
                                    
                                    return html_out

                                html_out = stuff_remover(html_out)
                                
                                if search_term in html_out:

                                    def the_identify_spell(parsed_ids, dup_index, index):
                                        if idnum in parsed_ids:
                                            dup_index += 1
                                        else: 
                                            index += 1
                                            parsed_ids.append(idnum)
                                        return parsed_ids, dup_index, index
                                
                                    parsed_ids, dup_index, index = the_identify_spell(parsed_ids, dup_index, index)

                                    if 'CANNOT CURRENTLY DISPLAY' in html_out:
                                        print(f"COULD NOT WRITE: {name}")
                                    else:
                                        def html_writer(htmlpath, date, idnum, op, post_title):
                                            ## STEP 3.4: Name the html file. 
                                            htmlname = f"{htmlpath}\\{date[:10]}-{date[11:13]}-{date[14:16]}-{date[17:19]}_{idnum}-{op}_{post_title}.html"

                                            ## STEP 5.0: Write to html.
                                            html_file = open(htmlname, "w", encoding="utf8")
                                            html_file.write(html_out)
                                            html_file.close()

                                        html_writer(htmlpath, date, idnum, op, post_title)
        os.startfile(htmlpath)
        print(f"- {index} unique files processed. \n- {len(fnmatch.filter(os.listdir(jsonpath), '*.json'))} json files in the folder. \n- {dup_index} duplicates found.")

root = tk.Tk()
root.title("JSON to HTML")
myapp = App(root)

myapp.mainloop()