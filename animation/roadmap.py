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
def blend(a,b,p):
    return tuple(int(a[i]*(1-p)+b[i]*p) for i in range(3))
def text_center(d, xy, value, size, color, anchor="mm"):
    d.text(xy,value,font=font(max(10,int(size))),fill=color,anchor=anchor)
def line_glow(d, pts, color, width=3):
    d.line(pts,fill=(*color,30),width=width*5,joint="curve")
    d.line(pts,fill=(*color,170),width=width,joint="curve")
def frame(t,w,h,duration):
    # All compositions are authored on a fixed 1920x1080 stage and scaled once.
    W,H=1920,1080
    im=Image.new("RGB",(W,H),(5,9,23))
    d=ImageDraw.Draw(im,"RGBA")
    phase=min(0.999,t/duration)
    for j in range(95):
        x=(j*541+83+int(11*t*math.sin(j)))%W
        y=(j*317+119+int(8*t*math.cos(j)))%H
        r=1+(j%3==0)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(150,194,255,30+j%4*15))
    # Soft moving grid, same visual language as the interactive science map.
    for x in range(-80,2000,80):
        xx=x+int(18*math.sin(t*.18))
        d.line((xx,0,xx,H),fill=(70,115,170,13))
    for y in range(0,1100,80):
        d.line((0,y,W,y),fill=(70,115,170,13))
    d.text((92,55),"ROADMAPSCIENCE  /  MATHEMATICS",font=font(25),fill=(110,186,244,255))
    # Four chapters: introduction, sequential stages, prerequisites, full overview.
    if phase<.12:
        p=ease(phase/.12)
        text_center(d,(960,365-int((1-p)*65)),"МАТЕМАТИКА",94,(245,250,255,255))
        text_center(d,(960,465),"От логики до исследовательских задач",36,(166,195,225,int(255*p)))
        for j,c in enumerate(COLORS):
            a=(j+1)*math.pi/2+t*.65
            x=960+int(245*math.cos(a));y=695+int(95*math.sin(a))
            d.ellipse((x-13,y-13,x+13,y+13),fill=(*c,220))
            if j:
                line_glow(d,(960,695,x,y),c,2)
        text_center(d,(960,935),"15 ЭТАПОВ     •     4 ПАРАЛЛЕЛЬНЫХ НАПРАВЛЕНИЯ",23,(155,181,212,255))
    elif phase<.76:
        p=(phase-.12)/.64
        f=min(14,int(p*15))
        local=ease(p*15-f)
        # Camera follows the selected stage; neighbors retain spatial context.
        center=960
        centers=[center+(i-f)*315-int(local*315) for i in range(15)]
        tracks=["АНАЛИЗ","АЛГЕБРА","ГЕОМЕТРИЯ","ДИСКРЕТНАЯ / ПРИКЛАДНАЯ"]
        d.text((92,115),"ПОСЛЕДОВАТЕЛЬНОЕ И ПАРАЛЛЕЛЬНОЕ ИЗУЧЕНИЕ",font=font(28),fill="white")
        d.text((92,169),f"ЭТАП {f+1:02d} / 15   ·   {STAGES[f][0]}",font=font(31),fill=(193,213,242,255))
        for j,(c,label) in enumerate(zip(COLORS,tracks)):
            y=315+j*168
            d.text((92,y-65),label,font=font(20),fill=(*c,255))
            for i,x in enumerate(centers):
                if x<30 or x>2050: continue
                if i>0:
                    xp=centers[i-1]
                    if xp<2050:
                        line_glow(d,(xp+18,y,x-18,y),c,3)
                radius=18 if i==f else 11
                a=230 if i<=f else 80
                if i==f:
                    ring=31+int(5*math.sin(t*4)**2)
                    d.ellipse((x-ring,y-ring,x+ring,y+ring),outline=(*c,105),width=3)
                d.ellipse((x-radius,y-radius,x+radius,y+radius),fill=(*c,a))
                if abs(x-960)<530:
                    name=STAGES[i][1][j]
                    # Wrap rather than truncate labels.
                    words=name.split(); lines=[]; cur=""
                    for word in words:
                        if len(cur+" "+word)>23 and cur:lines.append(cur);cur=word
                        else:cur=(cur+" "+word).strip()
                    if cur:lines.append(cur)
                    for n,ln in enumerate(lines[:3]):
                        text_center(d,(x,y+40+n*26),ln,18,(220,231,249,255 if i<=f else 110))
        d.text((92,986),"НАПРАВЛЕНИЯ ИДУТ ПАРАЛЛЕЛЬНО; СВЯЗИ ПОКАЗЫВАЮТ ПРЕЕМСТВЕННОСТЬ",
               font=font(19),fill=(157,181,210,255))
    elif phase<.90:
        p=ease((phase-.76)/.14)
        text_center(d,(960,185),"ЗАВИСИМОСТИ МЕЖДУ РАЗДЕЛАМИ",48,"white")
        chains=[
            ["Функции","Пределы","Производные","Интегралы","Теория меры"],
            ["Множества","Матрицы","Пространства","Операторы","Абстрактная алгебра"],
            ["Геометрия","Векторы","Топология","Многообразия","Дифф. геометрия"]]
        for j,chain in enumerate(chains):
            y=355+j*218;c=COLORS[j]
            for k,name in enumerate(chain):
                x=215+k*375
                if k:
                    line_glow(d,(x-300,y,x-95,y),c,3)
                    head=x-94
                    d.polygon([(head,y),(head-12,y-7),(head-12,y+7)],fill=(*c,190))
                d.rounded_rectangle((x-90,y-37,x+90,y+37),radius=18,
                                    fill=(*blend((9,19,37),c,.17),255),outline=(*c,180),width=2)
                text_center(d,(x,y),name,16,"white")
        text_center(d,(960,1010),"НЕ ВСЁ НУЖНО ИЗУЧАТЬ СТРОГО ПО ОДНОЙ ЛИНИИ",24,(169,200,235,255))
    else:
        text_center(d,(960,145),"ЕДИНАЯ КАРТА МАТЕМАТИКИ",52,"white")
        for i,(name,topics) in enumerate(STAGES):
            x=150+(i%5)*405;y=285+(i//5)*230
            d.rounded_rectangle((x-125,y-60,x+230,y+126),radius=17,
                                fill=(13,25,47,245),outline=(65,96,140,160),width=2)
            d.text((x-105,y-43),f"{i+1:02d}  {name}",font=font(18),fill=(239,245,255,255))
            for j,topic in enumerate(topics):
                label=topic if len(topic)<32 else topic[:30]+"…"
                d.ellipse((x-104,y-5+j*27,x-96,y+3+j*27),fill=(*COLORS[j],255))
                d.text((x-84,y-12+j*27),label,font=font(14),fill=(183,206,234,255))
        text_center(d,(960,1018),"ROADMAPSCIENCE  ·  ИЗУЧАЙ СВЯЗИ, А НЕ ТОЛЬКО ТЕМЫ",22,(131,191,244,255))
    # Global progress indicator.
    d.rounded_rectangle((90,1040,1830,1046),radius=3,fill=(36,54,80,255))
    d.rounded_rectangle((90,1040,90+max(1,int(1740*phase)),1046),radius=3,fill=(75,205,250,255))
    if (w,h)!=(W,H):
        im=im.resize((w,h),Image.Resampling.LANCZOS)
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
