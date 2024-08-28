
import customtkinter
from tkinter import *
from tkintermapview import TkinterMapView
from PIL import Image
import threading
import requests
import time
customtkinter.set_default_color_theme("blue")
api_key = "YOUR_API_KEY"
cse_id = " Search Engine ID"
defaultimg = customtkinter.CTkImage(Image.open("IMG_9810.JPG"), size=(500, 300))


class App(customtkinter.CTk):
    APP_NAME = "KaaN - GPT"
    WIDTH = 320
    HEIGHT = 320
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.minsize(App.WIDTH, App.HEIGHT)

        self.marker_list = []
        # ============ create two CTkFrames ============


        self.frame_left = customtkinter.CTkFrame(self, corner_radius=0, fg_color=None)
        self.frame_left.pack(side=LEFT, fill=Y)
        
        self.frame_right_loc=customtkinter.CTkFrame(self,corner_radius=0)
        self.frame_right_loc.pack(side=BOTTOM,fill=X)
        
        self.frame_right = customtkinter.CTkFrame(self, corner_radius=0)
        self.frame_right.pack(side=BOTTOM, fill=BOTH, expand=True)

        
        # ============ frame_right ============ #
        self.frame_left.grid_rowconfigure(3, weight=1)
        self.p_label = customtkinter.CTkLabel(self.frame_right_loc, text="Title", justify='center', width=300)
        self.p_label.grid(row=0, column=0, columnspan=2, padx=(5, 5), pady=(10, 0), sticky="ew")
        self.i_label = customtkinter.CTkLabel(self.frame_right_loc, text="Snippet", justify='center', width=300)
        self.i_label.grid(row=0, column=2, columnspan=2, padx=(5, 5), pady=(10, 0), sticky="ew")
        self.d_label = customtkinter.CTkLabel(self.frame_right_loc, text="Link", justify='center', width=300)
        self.d_label.grid(row=0, column=4, columnspan=2, padx=(5, 5), pady=(10, 0), sticky="ew")
        

       
        
        #------------Left Frame-----------#
        self.l_frame = customtkinter.CTkFrame(self.frame_left)
        self.l_frame.pack(fill=X)


        self.v_lable = customtkinter.CTkLabel(self.l_frame, text="KAAN", image=defaultimg, width=500, height=300)
        self.v_lable.pack(padx=5, pady=5)


        self.textBox=customtkinter.CTkTextbox(self.l_frame, height=25, width=300,)
        self.textBox.pack(padx=5,pady=5)


        # Add placeholder text
        self.placeholder_text = "Enter a question"
        self.add_placeholder()
        #------------Button Frame-----------#
        self.buttons_frame = customtkinter.CTkFrame(self.frame_left)
        self.buttons_frame.pack(side=BOTTOM, fill=BOTH)

        self.buttons_frame.grid_columnconfigure(0, weight=1)
        #threading.Thread(target=self.google_search, args=[api_key,cse_id], daemon=True).start()
        self.v_btn = customtkinter.CTkButton(self.buttons_frame,
                                                text="Get An Answer", height=40,
                                                command=threading.Thread(target=self.google_search, args=[api_key,cse_id], daemon=True).start(), corner_radius=0)
        self.v_btn.grid(pady=(10, 0), padx=(5, 5), row=0, column=0, sticky="we")
        

        
        # ============ frame_left ============
        """
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)
        """
    def get_input(self):

        input = self.textBox.get("1.0",'end-1c')
        return input
        
    def start(self):
        self.mainloop()

    def add_placeholder(self):
        # Insert placeholder text
        self.textBox.insert("1.0", self.placeholder_text)
        self.textBox.configure(fg_color="red")  # Optional: Change text color for placeholder

        # Bind events to handle focus and blur
        self.textBox.bind("<FocusIn>", self.remove_placeholder)
        self.textBox.bind("<FocusOut>", self.add_placeholder_on_blur)

    def remove_placeholder(self, event):
        if self.textBox.get("1.0", "end-1c") == self.placeholder_text:
            self.textBox.delete("1.0", "end")
            self.textBox.configure(fg_color="white")  # Optional: Change text color for normal text

    def add_placeholder_on_blur(self, event):
        if not self.textBox.get("1.0", "end-1c"):
            self.textBox.insert("1.0", self.placeholder_text)
            self.textBox.configure(fg_color="lightgray")

    def clear_screen(self):
        # This function will be called after 5 seconds
        # You can clear the labels or other UI elements here
        self.i_label.destroy()  # Remove the snippet label

    def google_search(self ,api_key, cse_id):
        #get input from user
        query=self.get_input()
        if query is None:
            query=self.get_input()
        else:
            # Define the endpoint and parameters for the request
            url = "https://www.googleapis.com/customsearch/v1"
            """
            cse_id: Search Engine ID
            q: question of what you need
            """
            params = {
                "key": api_key,
                "cx": cse_id,
                "q": query
            }
            # Make the GET request to the API
            response = requests.get(url, params=params)
            
            # Check for a successful response
            if response.status_code == 200:
                search_results = response.json()
                # Print the search results
                count=0
                for item in search_results.get('items', []):    
                    #self.p_label = customtkinter.CTkLabel(self.frame_right_loc, text=item['title'], justify='center', width=300)
                    #self.p_label.grid(row=count, column=0, columnspan=2, padx=(5, 5), pady=(10, 0), sticky="ew")
                    
                    self.i_label = customtkinter.CTkLabel(self.frame_right_loc, text=item['snippet'], justify='center', width=300)
                    self.i_label.grid(row=count, column=0, columnspan=2, padx=(5, 5), pady=(10, 0), sticky="ew")

                    #self.d_label = customtkinter.CTkLabel(self.frame_right_loc, text=item['link'], justify='center', width=300)
                    #self.d_label.grid(row=count, column=0, columnspan=2, padx=(5, 5), pady=(10, 0), sticky="ew")
                    count+=1
                    self.update()
                    time.sleep(0.1)

                    print(f"Title: {item['title']}")
                    print(f"Snippet: {item['snippet']}")
                    print(f"Link: {item['link']}")
                    print("\n")    
            else:
                print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    app = App()
    app.start()
    print('Finished')
