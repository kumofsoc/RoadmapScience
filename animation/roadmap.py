"""RoadmapScience: animated mathematics roadmap video."""
import argparse
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip

STAGES = [
("Логика и основания", ["Логика", "Множества", "Алгебра", "Доказательства"]),
("Предуниверситетская база", ["Функции", "Комплексные числа", "Геометрия", "Комбинаторика"]),
("Начало высшей математики", ["Пределы", "Матрицы и СЛАУ", "Векторы", "Графы"]),
("Основные методы", ["Производные и интегралы", "Линейные операторы", "Квадрики", "Вероятность"]),
("Многомерная математика", ["Многомерный анализ", "Спектральная теория", "Векторный анализ", "Статистика"]),
("Уравнения и структуры", ["ОДУ", "Группы и кольца", "Топология", "Численные методы"]),
("Строгий анализ", ["Действительный анализ", "Поля и модули", "Метрические пространства", "Случайные процессы"]),
("Продвинутые структуры", ["Комплексный анализ", "Теория Галуа", "Общая топология", "Теория информации"]),
("Анализ и геометрия", ["Теория меры", "Алгебраическая топология", "Многообразия", "Уравнения в частных производных"]),
("Глубокая теория", ["Функциональный анализ", "Теория чисел", "Дифференциальная геометрия", "Оптимизация"]),
("Высшие разделы", ["Операторная теория", "Коммутативная алгебра", "Риманова геометрия", "Стохастический анализ"]),
("Специализированные теории", ["Спектральный анализ", "Алгебраическая геометрия", "Геометрический анализ", "Теория категорий"]),
("Исследовательская база", ["Современный анализ", "Гомологическая алгебра", "Топология многообразий", "Теория моделей"]),
("Современные направления", ["Нелинейные PDE", "Арифметическая геометрия", "Геометрические потоки", "Теория типов"]),
("Научная работа", ["Статьи и семинары", "Открытые задачи", "Новые методы", "Исследовательская программа"])
]
COLORS = [(67,215,255),(173,122,255),(75,239,179),(255,184,103)]
def font(size):
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "C:/Windows/Fonts/arial.ttf",
                 "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]:
        if Path(path).exists(): return ImageFont.truetype(path,size)
    return ImageFont.load_default()
def ease(x):
    x=max(0,min(1,x))
    return x*x*(3-2*x)
def frame(t, w, h, duration):
    scale=w/1920
    im=Image.new("RGB",(w,h),(5,9,23))
    d=ImageDraw.Draw(im,"RGBA")
    for j in range(75):
        x=int((j*541+83)%w); y=int((j*317+119)%h)
        r=max(1,int((1+0.8*math.sin(t*.5+j))*scale))
        d.ellipse((x-r,y-r,x+r,y+r),fill=(160,194,255,60))
    d.text((int(90*scale),int(52*scale)),"ROADMAP / MATHEMATICS",font=font(int(26*scale)),fill=(109,168,230,255))
    d.text((int(90*scale),int(104*scale)),"Полная карта высшей математики",font=font(int(52*scale)),fill="white")
    d.text((int(90*scale),int(178*scale)),"15 этапов  ·  4 параллельных направления  ·  от основ до исследований",
           font=font(int(24*scale)),fill=(171,191,218,255))
    active=min(14,int(t/duration*15))
    progress=ease((t/duration*15)-active)
    start=max(0,active-3)
    end=min(15,start+6)
    if end-start<6: start=max(0,end-6)
    xs=[int((175+i*320)*scale) for i in range(6)]
    ys=[int((350+j*155)*scale) for j in range(4)]
    for j,(color,label) in enumerate(zip(COLORS,["АНАЛИЗ","АЛГЕБРА","ГЕОМЕТРИЯ","ДИСКРЕТНОЕ / ПРИКЛАДНОЕ"])):
        y=ys[j]
        d.text((int(90*scale),y-int(62*scale)),label,font=font(int(17*scale)),fill=(*color,255))
        for i in range(end-start):
            k=start+i
            x=xs[i]
            if i:
                d.line((xs[i-1]+int(110*scale),y,x-int(110*scale),y),
                       fill=(*color,150 if k<=active else 35),width=max(2,int(3*scale)))
            alpha=255 if k<active else int(80+175*progress) if k==active else 55
            r=int((12+(5*math.sin(t*3)**2 if k==active else 0))*scale)
            d.ellipse((x-r,y-r,x+r,y+r),fill=(*color,alpha))
            if k==active:
                d.ellipse((x-2*r,y-2*r,x+2*r,y+2*r),outline=(*color,100),width=max(1,int(2*scale)))
            name=STAGES[k][1][j]
            if len(name)>25: name=name[:23]+"…"
            d.text((x-int(105*scale),y+int(28*scale)),name,font=font(int(17*scale)),
                   fill=(225,236,255,alpha))
    d.text((int(90*scale),int(940*scale)),f"ЭТАП {active+1:02d} / 15    {STAGES[active][0]}",
           font=font(int(30*scale)),fill="white")
    x0=int(90*scale); x1=w-int(90*scale); y=int(1000*scale)
    d.rounded_rectangle((x0,y,x1,y+int(7*scale)),radius=4,fill=(35,49,74,255))
    d.rounded_rectangle((x0,y,x0+int((x1-x0)*min(1,t/duration)),y+int(7*scale)),radius=4,fill=(69,204,255,255))
    return np.asarray(im)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="roadmap_math.mp4")
    p.add_argument("--duration",type=float,default=90)
    p.add_argument("--width",type=int,default=1920)
    p.add_argument("--height",type=int,default=1080)
    p.add_argument("--fps",type=int,default=30)
    a=p.parse_args()
    if a.duration<=0 or min(a.width,a.height,a.fps)<=0: p.error("Positive values required")
    clip=VideoClip(lambda t:frame(t,a.width,a.height,a.duration),duration=a.duration)
    clip.write_videofile(a.output,fps=a.fps,codec="libx264",audio=False,preset="medium",ffmpeg_params=["-pix_fmt","yuv420p"])
    clip.close()
if __name__=="__main__": main()
