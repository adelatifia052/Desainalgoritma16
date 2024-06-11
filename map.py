from PIL import Image, ImageDraw, ImageTk
import random
from numpy import sort
import tkinter as tk
from tkinter import ttk

width = 1500
height = 1500
max_width = 400
road_width = 20
canvas = Image.new("RGBA",(width , height ), "green")
draw = ImageDraw.Draw(canvas)
batas = [(0,0)]
space = 20
building = [
    Image.open("bangunan/small.jpg").resize((20,20)), 
    Image.open("bangunan/small2.jpg").resize((20,20)), 
    Image.open("bangunan/large-x.jpg").resize((100,50)),
    Image.open("bangunan/large2x.jpg").resize((100,50)), 
    Image.open("bangunan/large3x.jpg").resize((100,50)), 
    Image.open("bangunan/medium-x.jpg").resize((50,30)),
    Image.open("bangunan/medium2-x.jpg").resize((50,30))
    ]

environment = [
    Image.open("environment/batu1.png").convert("RGBA").resize((20,20)),
    Image.open("environment/rumput1.png").convert("RGBA").resize((20,20)),
    Image.open("environment/rumput2.jpg").convert("RGBA").resize((40,20)),
    Image.open("environment/pohon1.jpg").convert("RGBA").resize((20,20)),
    Image.open("environment/pohon2.png").convert("RGBA").resize((20,20)),
    Image.open("environment/pohon3.png").convert("RGBA").resize((20,20))
]

#Fungsi untuk menggambar area kecil di map
def drawArea(pos1, pos2, batAs, sisa):
    global building
    print(sisa , ": ", pos1, pos2)
    pos1 = (pos1[0], max(pos1[1], batAs))
    #sort atau balikkan posisi antara sumbu 1 dan 2 agar sumbu1 < sumbu 2
    xsort = sort([pos1[0],pos2[0]])
    ysort = sort([pos1[1],pos2[1]])
    if pos1[0] < pos2[0] and pos1[1] < pos2[1]: draw.rectangle(((pos1[0]+1, pos1[1]+1), (pos2[0]-1 , pos2[1]-1)), "gray")
    pos1 = (pos1[0] + 20 , pos1[1]+20)
    pos2 = (pos2[0] - 20 , pos2[1]-20)
    x = xsort[0] + 20
    y = ysort[0] + 20
    if pos1[0] < pos2[0] and pos1[1] < pos2[1]: draw.rectangle((pos1,pos2), "green")
    #Lakukan perulangan dari atas sampai bawah area
    while y <= ysort[1] - 60:
        #Lakukan perulangan dari kiri ke kanan area
        while x <= xsort[1] : 
            #Ambil asset yang sekiranya muat di area yang sekarang
            gedung = [gedung for gedung in building if gedung.size[0] + x < xsort[1] - 20]
            #JIka tidak ada asset yang muat hentikan perulangan
            if not gedung : break
            #Ambil salah satu asset 
            bangunan = random.choice(environment if y > ysort[0] + 20 and y <= ysort[1]-150 else gedung)
            #Lakukan validasi apakah posisi sekarang dekat dengan jalan atau tidak
            if x + bangunan.size[0] >= xsort[1] -20 : break
            if y > ysort[0] + 20 and y < ysort[1]-150  : canvas.paste(bangunan, (x,(y + random.randint(0, 60-bangunan.size[1]))))
            else : canvas.paste(bangunan, (x,y if y <= ysort[1]-150 else ysort[1]-bangunan.size[1]-20))
            x += bangunan.size[0] + space
        y += 70
        x = xsort[0] + 20
        #JIka suah mencapai batas kanan area , ulangi perulangan dari kiri lagi , dengan nilai y bertambah ke bawh
    # if len(sisa) and pos1[1] < batAs :
    #     print("aha")
    #     drawArea(pos1, (sisa[0][0] , ysort[0]), pos1[1], [])
    # if len(sisa) and pos1[1] > batAs :
    #     print("aha")
    #     drawArea(sisa[0], (xsort[1] , ysort[0]), pos1[1], [])

#Fungsi untuk memecah area menjadi lebih kecil lagi
def makeArea(startPoint):
    global width, height, road_width, batas
    print(startPoint)
    y = startPoint[1]  + 200
    x = startPoint[0] 
    tempX = 0
    tempY = 0
    limit_reached = 0
    tempAtas = []
    #Lakukan perulangan dari atas sampai bawah 
    while y <= height and  not limit_reached:
        tempX = 0
        if y >= height : limit_reached += 1
        #Lakukan perulangan dari kiri ke kanann
        while x <= width + 200 :
            batAs,batEs = batas[len(batas)-1][1],batas[len(batas)-1][1]
            yey = random.choice([0,100])
            tempAtas.append((x,y-yey))
            list_atas = []
            #Cari batas atas tiap area agar tidak tumpang tindih
            for atas in reversed(batas):
                batAs = atas[1] if atas[0] > x else batAs
                batEs = atas[1] if atas[0] > tempX else batEs
                if tempX < atas[0] < x : list_atas.append(atas)
            # if tempX < x :  draw.rectangle(((x,y), (x+road_width, y+road_width)), "black")
            if batEs < y-yey : 
                if tempX < x and y <= height: draw.rectangle(((tempX,y-yey), (x+20, y-yey+20)), "black")
                if tempX < x and y <= height: draw.line(((tempX+20,y-yey+10), (x, y-yey+10)), "white", 1)
                if tempX < x and y <= height: draw.rectangle(((x,batAs), (x+20, y-yey)), "black")
                if tempX < x and y <= height: draw.line(((x+10,batAs+20), (x+10, y-yey)), "white", 1)
                if tempX < x and y <= height and tempX >= 20: draw.rectangle(((tempX,batEs+10), (tempX+20, y-yey)), "black")
                if tempX < x and y <= height and tempX >= 20: draw.line(((tempX+10,batEs+20), (tempX+10, y-yey)), "white",1)
                drawArea((tempX+20 , batEs+20 ), (x  , y-yey), batAs+20, list_atas)
            tempX = x
            tempY = batAs
            x += random.randint(2,4) * 100
        y += 300
        #Jika sudah sampai batas kanan ulangi lagi perulangan dari kiri dengan y bertambah ke bawah

        tempAtas.append((tempX,tempY))
        if y > height : 
            y = height
        batas = tempAtas
        tempAtas = []
        x = startPoint[0]

#Inisialisasi variabel yang dibutuhkan utuk membuat UI
zoom_factor = 1.0
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 600
viewport_x = INITIAL_WIDTH//2 - 50
viewport_y = INITIAL_HEIGHT//2 - 50
viewport_width = 800
viewport_height = 600
new_map = None

#Fungsi untuk mengambil gambar map terbaru / generate map
def update_map():
    global draw, canvas, batas
    batas = [(0,0)]
    canvas = Image.new("RGBA",(width , height ), "green")
    draw = ImageDraw.Draw(canvas)
    makeArea((0,0))
    canvas.save("map.png")
    new_map  = canvas
    cropped_map = new_map.crop((viewport_x, viewport_y, viewport_x + viewport_width, viewport_y + viewport_height))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    update()
    
#Update properti seperti skala zoom atau viewpoint 
def update():
    global canvas
    cropped_map = canvas.crop((viewport_x * zoom_factor, viewport_y * zoom_factor, viewport_x* zoom_factor + viewport_width* zoom_factor, viewport_y* zoom_factor + viewport_height* zoom_factor))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    
def zoom_out():
    global zoom_factor
    if  zoom_factor < 3.5:
        zoom_factor += 0.1
        update()

def zoom_in():
    global zoom_factor
    if zoom_factor > 0.5:
        zoom_factor -= 0.1
        update()
        
def scroll(event):
    global viewport_x, viewport_y
    print(viewport_y)
    if event.delta > 0:
        viewport_y -= 20 if viewport_y > 0 else 0
    else:
        viewport_y += 20 if viewport_y < 1000 / zoom_factor else 0
    update()

#Fungsi untuk menghandle event ketika keyword asdw ditekan  
def on_key_press(event):
    global viewport_x, viewport_y
    key = event.keysym
    if key == 'a':
        viewport_x -= 20 if viewport_x > 0 else 0
    elif key == 's':
        viewport_y += 20 if viewport_y < 1000 / zoom_factor else 0
    elif key == 'd':
        viewport_x += 20 if viewport_x < 1000 / zoom_factor else 0
    elif key == 'w':
        viewport_y -= 20 if viewport_y > 0 else 0
    update()


#Inisialisasi Desain Windowns Form / GUI
root = tk.Tk()
root.title("Desain IKN City ")
root.geometry("800x600")  
root.minsize(600, 400)  
root.bind("<MouseWheel>", scroll)
root.bind("<KeyPress-a>", on_key_press)
root.bind("<KeyPress-s>", on_key_press)
root.bind("<KeyPress-d>", on_key_press)
root.bind("<KeyPress-w>", on_key_press)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

canvass = tk.Canvas(frame, bg='white')
canvass.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

map_label = ttk.Label(canvass)
canvass.create_window((0, 0), window=map_label, anchor='nw')

button_frame = ttk.Frame(root, padding=10)
button_frame.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=10, pady=10)

generate_button = ttk.Button(button_frame, text="Generate Map", command=update_map)
generate_button.grid(row=0, column=0, pady=5)

zoom_in_button = ttk.Button(button_frame, text="Zoom In", command=zoom_in)
zoom_in_button.grid(row=1, column=0, pady=5)

zoom_out_button = ttk.Button(button_frame, text="Zoom Out", command=zoom_out)
zoom_out_button.grid(row=2, column=0, pady=5)

def on_frame_configure(event):
    canvass.configure(scrollregion=canvass.bbox("all"))
    print(event)

frame.bind("<Configure>", on_frame_configure)
update_map()
root.mainloop()