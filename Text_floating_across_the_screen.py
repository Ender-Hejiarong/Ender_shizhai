import tkinter as tk
import random
import threading
import time
def show_warm_tip():
    window = tk.Tk()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = 250
    window_height = 60
    x = random.randrange(0,screen_width-window_width)
    y = random.randrange(0,screen_height-window_height)

    window.title('温馨提示')
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    tips = ['多喝水哦!','保持微笑~','每天都要元气满满!','保持好心情!','早点睡!','梦想成真!'
            ,'期待下次见面哦!','金榜题名!','诸事顺利!',"别熬夜!"
            ,'愿所有烦恼消失!','今天过的开心嘛~',"天冷多加衣!"]
    tip = random.choice(tips)

    bg_colors = ['lightpink','skyblue','lightgreen','lavender','lightyellow','plum','coral','bisque','aquamarine','mistyrose','honeydew','lavenderblush','oldlace']
    bg = random.choice(bg_colors)
    tk.Label(window,
             text=tip,
             bg=bg,
             font=('微软雅黑',16),
             width=30,
             heigh=3
             ).pack()
    window.attributes('-topmost',True)
    window.mainloop()
threads = []
for i in range(300):
    t = threading.Thread(target=show_warm_tip)
    threads.append(t)
    time.sleep(0.005)
    threads[i].start()
