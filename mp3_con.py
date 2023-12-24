import os
from tkinter import *
import customtkinter
from PIL import Image, ImageTk
from pytube import YouTube
import requests


# Functions: 

# Βασικό να πάρουμε το όνομα φακέλου του χρήστη για να συμπληρώσουμε την διαδρομή για τη Mουσική
def find_user_name():
    current_path = str(os.getcwd())
    current_path = current_path.split('\\')
    return current_path[2]  

# For getting the thumbnail
def get_thumbnail(url):
    try:
        yt = YouTube(url)
        thumbnail_url = yt.thumbnail_url
        thumbnail_image = Image.open(requests.get(thumbnail_url, stream=True).raw)
        return thumbnail_image
    except Exception as e:
        print(f"Error getting thumbnail: {e}")
        return None

def display_thumbnail(url):
    thumbnail_image = get_thumbnail(url)
    if thumbnail_image:
        thumbnail_image.thumbnail((400, 400))
        thumbnail_photo = ImageTk.PhotoImage(thumbnail_image)
        thumbnail_label.configure(image=thumbnail_photo)
        thumbnail_label.image = thumbnail_photo
    else:
        thumbnail_label.configure(image=None)

# for submiting the URL for convertion
def on_Submit():
    try:

        link_input_URL = link_input.get()
        
        # Παίρνω το Video από YouTube
        link_video = YouTube(link_input_URL) #θέλω το on_progress για το ποσοστό ολοκλήρωσης
        
        # Διόρθωση Γραφικών και update του window για να φανούν
        link_label.configure(text=f'"{link_video.title}" is now being downloaded', text_color="#ffffff")
        display_thumbnail(link_input_URL)
        result_label_text = 'Please wait while the audio is downloading...'
        result_label.configure(text=result_label_text, text_color='#ffffff')
        window.update()     # ΣΟΣ: Αλλιώς οι αλλαγές συμβαίνουν μετά την ολοκλήρωση της on_Submit
        
        # Αλλαγή φακέλου για κατέβασμα
        os.chdir(f"C:\\Users\\{USER_NAME}\\Music")


        # Μετατροπή σε mp3 και κατέβασμα
        mp3_file = link_video.streams.get_audio_only()
        mp3_file.download()

        # Επιστροφή στον αρχικό φάκελο της εφαρμογής για να συνεχίσουμε
        os.chdir(PATH_OF_THIS_PROGRAM)

        result_label_text = f'"{link_video.title}"\nDownloaded Successfully'
        foreground_color = '#02b028'

    except:
        result_label_text = 'Invalid URL'
        foreground_color = '#db0404'
        thumbnail_label.configure(image=None)

    # Ανεξαρτήτως έκβασης του try με τα δεδομένα που συγκέντρωσα προχωράω στην
    # προβολή αποτελέσματος του convert και επαναφορά του label σε 'Place URL here:'    
    link_label.configure(text=link_label_text, text_color="#ffffff")  
    result_label.configure(text=result_label_text, text_color=foreground_color)
    link_input.delete(0, END)  # Καθαρίζει το περιεχόμενο του Entry

    


# CONSTANTS
BACKGROUND_COLOR = '#2f3030'
USER_NAME = find_user_name()
PATH_OF_THIS_PROGRAM = str(os.getcwd()) #to kratame gia na mporoume na epistrepsoyme sto programma


# window Specifics
window = Tk()
window.geometry('700x550')
window.title("YouTube to Mp3 Converter")
# icon = PhotoImage(file='C:\\Users\\gprel\\Documents\\Mp3_converter\\mp3ConvIcon2.png')
# window.iconphoto(True, icon)
window.config(background=BACKGROUND_COLOR)

# Window components

# link label
link_label_text = 'Place URL here:'
link_label = customtkinter.CTkLabel(window, 
                                    text=link_label_text,
                                    pady=20,
                                    font=('Ubuntu', 16))
link_label.pack()


link_input = customtkinter.CTkEntry(window,
                                    font=('Ubuntu', 14),
                                    width=400)
link_input.pack()



# Button for Submit
submit_button= customtkinter.CTkButton( window,
                                        text="Convert and Download",
                                        font=('Ubuntu',16),
                                        command=on_Submit)
submit_button.pack(pady=20)


# Result label (success/failed download)
result_label = customtkinter.CTkLabel(window, 
                                      text='', 
                                      font=('Ubuntu', 18))
result_label.pack()

# thumbnail of video to display if downloaded successfully
thumbnail_label = customtkinter.CTkLabel(window, 
                                         text='')
thumbnail_label.pack(pady=20)



window.mainloop()
