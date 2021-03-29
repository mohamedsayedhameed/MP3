from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from ttkthemes import themed_tk as tk
import threading
from mutagen.mp3 import MP3
import os
import time
from tkinter import ttk

from pygame import mixer

root = Tk()
mixer.init()

## make a title
root.title('Melody')

## make icon
root.iconbitmap(r'image/music.ico')

## put a size
root.geometry('500x300')

## the menubar
menubar = Menu(root)
root.config(menu=menubar)

## the playlist list
playlist = []

## the submenu file
def open_file():
    global filename
    filename = filedialog.askopenfilename()
    add_to_playlist(filename)

## add to play list function
def add_to_playlist(f):
    f = os.path.basename(f)
    index = 0
    playlistbox.insert(index, f)
    playlistbox.pack()
    playlist.insert(index, filename)
    index += 1

submenu = Menu(menubar, tearoff =0)
menubar.add_cascade(label='file',menu=submenu)
submenu.add_command(label='open', command=open_file)
submenu.add_command(label='exit',command=root.destroy)

## del from playlistbox
def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
    
## the submenu help
def about_us():
    tkinter.messagebox.showinfo("about Melody", "music player build by python")

submenu = Menu(menubar, tearoff =0)
menubar.add_cascade(label='help',menu=submenu)
submenu.add_command(label='about Us', command=about_us)

## the left frame
left_frame = Frame(root)
left_frame.pack(side=LEFT)

## the right frame
right_frame = Frame()
right_frame.pack()

## the top frame
top_frame = Frame(right_frame)
top_frame.pack()

## make label name
filelabel = Label(top_frame, text="Let's make some noise")
filelabel.pack()

## make label length
labellength = Label(top_frame, text="total length:  --:--")
labellength.pack()

## make label currenttime
labelcurrenttime = Label(top_frame, text="Current Time : --:--")
labelcurrenttime.pack()

## make list box
playlistbox = Listbox(left_frame, height=15)
playlistbox.pack()

## add song button
addbutton = ttk.Button(left_frame, text="+ Add", command=open_file)
addbutton.pack(side=LEFT)

## del song button
delbutton = ttk.Button(left_frame, text="- Del", command=del_song)
delbutton.pack()

## show_details function
def show_details(play_song):
    filelabel['text'] = 'playing' + ' _ ' + os.path.basename(play_song)
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.sound(play_song)
        total_length = a.get_length()
        
    
    mins, secs = divmod(total_length, 60)
    mins , secs = round(mins), round(secs)
    formattext = '{:02d}:{:02d}'.format(mins, secs)
    labellength['text'] = 'total length:  '+formattext

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    
## start_count function
def start_count(t):
    global paused
    x = 0
    while x <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
             mins, secs = divmod(x, 60)
             mins, secs = round(mins), round(secs)
             timeformat = '{:02d}:{:02d}'.format(mins, secs)
             labelcurrenttime['text'] = 'total length' + '-' + timeformat
             time.sleep(1)
             x += 1

## make playButton
def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = 'music resumed'
        paused = False
    else:
            try:
                stop_music()
                time.sleep(1)
                selected_song = playlistbox.curselection()
                selected_song = int(selected_song[0])
                play_it = playlist[selected_song]
                print(play_it)
                mixer.music.load(play_it)
                mixer.music.play()
                statusbar['text']= 'playing music'+' '+os.path.basename(filename)
                show_details(play_it)
            except:
                tkinter.messagebox.showerror('file not found')
                
## the stop_music function
def stop_music():
    global paused
    paused = False
    mixer.music.stop()
    statusbar['text'] = 'music stop'

paused = False
## the pause_music function
def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = 'music paused'

## the rewind_music function
def rewind_music():
    play_music()
    statusbar['text']= 'music rewinded'

mute = False
_volume = 0
## the mute_music function
def mute_music():
    global mute
    global volume,  _volume
    if mute:
        mixer.music.set_volume(_volume)
        scale.set(_volume*100)
        statusbar['text'] = 'volume on'
        volume_btn.configure(image=volume_photo)
        mute = False
    else:
        _volume = volume
        mixer.music.set_volume(0)
        scale.set(0)
        statusbar['text'] = 'volume mute'
        volume_btn.configure(image=mute_photo)
        mute = True

## the set_vol function
def set_vol(val):
    global filename
    global volume
    volume = float(val)/100
    mixer.music.set_volume(volume)

#### close the window #### 
## the on_closing function
def on_closing():
    stop_music()
    root.destroy()

## the middle frame
middle_frame = Frame(root)
middle_frame.pack(pady=10)

## the play Button
play_photo = PhotoImage(file ='image/002-play.png')
play_btn = ttk.Button(middle_frame, image = play_photo, command = play_music)
play_btn.grid(row=0,column=0, padx=10)

## the Stop Button
stop_photo = PhotoImage(file ='image/stop.png')
stop_btn = Button(middle_frame, image = stop_photo, command = stop_music)
stop_btn.grid(row=0,column=1,padx=10)

## the Pause Button
pause_photo = PhotoImage(file ='image/001-pause.png')
pause_btn = Button(middle_frame, image = pause_photo, command = pause_music)
pause_btn.grid(row=0,column=2, padx=10)

## the foot frame
bottom_frame = Frame(root)
bottom_frame.pack(pady=10)

## the Rewind Button
rewind_photo = PhotoImage(file ='image/rewind.png')
rewind_btn = Button(bottom_frame, image = rewind_photo, command = rewind_music)
rewind_btn.grid(row=0, column=0)

## the volume button
volume_photo = PhotoImage(file = 'image/volume.png')
mute_photo  = PhotoImage(file = 'image/mute.png')
volume_btn = ttk.Button(bottom_frame, image= volume_photo, command=mute_music)
volume_btn.grid(row=0, column=1)

## the volume slider
scale = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(10)
mixer.music.set_volume(.1)
scale.grid(row=0, column=2)

## the statusbar
statusbar = Label(root, text='welcome to Melody',relief=GROOVE, anchor=W, borderwidth=5)
statusbar.pack(side=BOTTOM, fill=X)

## close the window
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()






