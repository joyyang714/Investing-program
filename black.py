import os
import requests, json, csv, datetime
import matplotlib; matplotlib.use('Agg');
import matplotlib.pyplot as py
import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk
from PIL import Image
import re
# import matplotlib.gridspec as gridspec

# global font
global f1, f2, f3, f4


# pop up window for stock gragh ------------------
def popup_bonus2():
    win = tk.Toplevel()
    win.geometry("2000x700")
    win.wm_title("Line Graph")

    l = tk.Label(win, text="MACD", font = f2)
    l.grid(row=0, column=0)

    kdImage2 = ImageTk.PhotoImage(file="C:\\Users\\joy\\AppData\\Local\\Programs\\Python\\Python36\\lib\site-packages\\matplotlib\\kdvalue2.png")
    bg_label2 = tk.Label(win, image=kdImage2)
    bg_label2.grid(row=1, column=0, sticky=tk.NW+tk.SE)
    bg_label2.image = kdImage2
    # os.remove("kdValue.png")

    b = tk.Button(win, text="Close", command=win.destroy)
    b.grid(row=2, column=0)


def popup_bonus():
    win = tk.Toplevel()
    win.geometry("2000x700")
    win.wm_title("Line Graph")

    l = tk.Label(win, text="Kd Line", font = f2)
    l.grid(row=0, column=0)

    kdImage = ImageTk.PhotoImage(file="C:\\Users\\joy\\AppData\\Local\\Programs\\Python\\Python36\\lib\site-packages\\matplotlib\\kdValue.png")
    bg_label = tk.Label(win, image=kdImage)
    bg_label.grid(row=1, column=0, sticky=tk.NW+tk.SE)
    bg_label.image = kdImage

    kdImage2 = ImageTk.PhotoImage(file="C:\\Users\\joy\\AppData\\Local\\Programs\\Python\\Python36\\lib\site-packages\\matplotlib\\kdvalue2.png")
    bg_label2 = tk.Label(win, image=kdImage2)
    bg_label2.grid(row=2, column=0, sticky=tk.S)
    bg_label2.image = kdImage2
    # os.remove("kdValue.png")

    b = tk.Button(win, text="Close", command=win.destroy)
    b.grid(row=2, column=0)


def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))


# All functions for data
class Stock():
    
    def __init__(self):
        pass
    
    # 輸出各數據
    def Output(self, data):
        Main_Stat1.configure(text=Main_Stat1.cget("text") + data[0] + "\n")
        Main_Stat2.configure(text=Main_Stat2.cget("text") + data[1] + "\n")
        Main_Stat3.configure(text=Main_Stat3.cget("text") + data[2] + "\n")
        Main_Stat4.configure(text=Main_Stat4.cget("text") + data[3] + "\n")
        Main_Stat5.configure(text=Main_Stat5.cget("text") + data[4] + "\n")
        Main_Stat6.configure(text=Main_Stat6.cget("text") + data[5] + "\n")
        Main_Stat7.configure(text=Main_Stat7.cget("text") + data[6] + "\n")
        Main_Stat8.configure(text=Main_Stat8.cget("text") + data[7] + "\n")
        Main_Stat9.configure(text=Main_Stat9.cget("text") + data[8] + "\n")
    
    # 輸出股票名稱 + 代碼
    def Output2(self,title):
        Main_Stat0.configure(text = Main_Stat1.cget("text") + title)

    def Clean(self):
        Main_Stat0.configure(text="")
        Main_Stat1.configure(text="")
        Main_Stat2.configure(text="")
        Main_Stat3.configure(text="")
        Main_Stat4.configure(text="")
        Main_Stat5.configure(text="")
        Main_Stat6.configure(text="")
        Main_Stat7.configure(text="")
        Main_Stat8.configure(text="")
        Main_Stat9.configure(text="")

    def CrawlerBtn2(self):
        directory = "股票資料"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 當前路徑
        now_path = os.path.abspath('.')
        filepath = now_path + "/" + directory + "/" + self.stock_id + "_" + self.year + "." + self.month + ".csv"
        outputfile = open(filepath,'w', newline='', encoding='utf-8')
        outputwriter = csv.writer(outputfile)
        outputwriter.writerow(self.s['title'])
        outputwriter.writerow(self.s['fields'])

        for data in (self.s['data']):
            outputwriter.writerow(data)
        outputfile.close()

    # 按下「查詢」按鈕 -----------
    def CrawlerBtn(self):
        self.Clean()
        
        
        self.year = variable.get()
        self.month = variable2.get()
        self.stock_id = StockNum.get("1.0", "end-1c")
        self.year = str(int(re.search('\d+', self.year).group()) + 1911)
        self.month = re.search('\d+', self.month).group()
        
        if self.month == "01":
            self.month2 = "12"
            self.month3 = "11"
            self.year2 = str(int(self.year) - 1)
            self.year3 = str(int(self.year) - 1)
        elif self.month == "02":
            self.month2 = "01"
            self.month3 = "12"
            self.year2 = str(int(self.year))
            self.year3 = str(int(self.year) - 1)
        else:
            self.year2 = self.year
            self.year3 = self.year2
            if int(self.month) <= 10:
                self.month2 = "0" + str(int(self.month) - 1)
                self.month3 = "0" + str(int(self.month) - 2)
            if int(self.month) == 11:
                self.month2 = "10"
                self.month3 = "09"
            if int(self.month) > 11:
                self.month2 = str(int(self.month) - 1)
                self.month3 = str(int(self.month) - 2)
        
        url_twse = 'http://www.tse.com.tw/exchangeReport/STOCK_DAY?response=json&date=' + self.year + self.month + '01&stockNo=' + self.stock_id + '&_=1528365227229'
        res = requests.get(url_twse)
        self.s = json.loads(res.text)
        url_twse2 = 'http://www.tse.com.tw/exchangeReport/STOCK_DAY?response=json&date=' + self.year2 + self.month2 + '01&stockNo=' + self.stock_id + '&_=1528365227229'
        res2 = requests.get(url_twse2)
        self.s2 = json.loads(res2.text)
        url_twse3 = 'http://www.tse.com.tw/exchangeReport/STOCK_DAY?response=json&date=' + self.year3 + self.month3 + '01&stockNo=' + self.stock_id + '&_=1528365227229'
        res3 = requests.get(url_twse3)
        self.s3 = json.loads(res3.text)

        # print the column name
        if self.s['stat'] == "OK":

            # 查詢資料按鈕 --------------
            
            Main_Button2.grid(row=30, column=8, columnspan=3)
            button_bonus.grid(row=30, column=6)
            button_bonus2.grid(row=30, column=7)

            self.Output2(self.s['title'])
            self.Output(self.s['fields'])
            # print the data
            for data in (self.s['data']):
                self.Output(data)

            # K-D Line ---------------
            total_data_list = []  # 存放讀入的日期和每日九樣交易資料
            closing_price_list = []  # 每日收盤價，如果能用dict搭配日期、收盤價會更好
            date_list = []
            for data in (self.s3['data']):
                total_data_list.append(data)
                if "," in data[6]:
                    data[6] = data[6].replace(",", "")
                    closing_price_list.append(float(data[6]))
                else:
                    closing_price_list.append(float(data[6]))
                date_list.append(data[0])
            for data in (self.s2['data']):
                total_data_list.append(data)
                if "," in data[6]:
                    data[6] = data[6].replace(",", "")
                    closing_price_list.append(float(data[6]))
                else:
                    closing_price_list.append(float(data[6]))
                date_list.append(data[0])

            for data in (self.s['data']):
                total_data_list.append(data)
                if "," in data[6]:
                    data[6] = data[6].replace(",","")
                    closing_price_list.append(float(data[6]))
                else:
                    closing_price_list.append(float(data[6]))
                date_list.append(data[0])

            for d in range(9):
                date_list.remove(date_list[d])

            for i in range(len(date_list)):
                if date_list[i][7] == '0':
                    date_list[i] = date_list[i][:7] + date_list[i][-1]
                if date_list[i][4] == '0':
                    date_list[i] = date_list[i][5:]
                else:
                    date_list[i] = date_list[i][4:]

            k_value_list = []
            d_value_list = []
            k_value = 50
            d_value = 50
            
            for j in range(len(closing_price_list) - 9):
                current_9day_list = []
                maxin9 = 0  # 9日最高價
                maxin9_index = 0
                minin9 = 0  # 9日最低價
                minin9_index = 0
                for h in range(j, j + 9):  # 從closing price list中獲得前九天資料
                    current_9day_list.append(closing_price_list[len(closing_price_list) - 1 - h])
                
                maxin9_index = current_9day_list.index(max(current_9day_list))
                maxin9 = current_9day_list[maxin9_index]
                minin9_index = current_9day_list.index(min(current_9day_list))
                minin9 = current_9day_list[minin9_index]
                rsv = ((current_9day_list[-1] - minin9) / (maxin9 - minin9)) * 100
                k_value = (2 / 3) * k_value + (1 / 3) * rsv
                d_value = (2 / 3) * d_value + (1 / 3) * k_value
                k_value_list.append(k_value)
                d_value_list.append(d_value)
            
            # MACD line ----------------
            _a4 =1- 0.4
            _a7 = 1-2/8
            _a15 = 1-2/16
            ema_base4 = 0
            ema_molecule4 = 0
            ema_base7 = 0
            ema_molecule7 = 0
            ema_base15 = 0
            ema_molecule15 = 0
            dif_list = []
            macd_list = []
            macd_bar_list = []
            date_list2 = []
            for i in range(4):
                ema_base4 += _a4**i
            for i in range(0,7):
                ema_base7 += _a7**i
            for i in range(0,15):
                ema_base15 += _a15**i
            for j in range(len(closing_price_list)-16,-1,-1):
                current_15day_list = []
                current_7day_list = []
                for h in range(j,j+7): #從closing price list中獲得前12天資料
                    current_7day_list.append(closing_price_list[len(closing_price_list)-1-h])
                for h in range(j,j+15): #從closing price list中獲得前26天資料
                    current_15day_list.append(closing_price_list[len(closing_price_list)-1-h])
                for g in range(0,7):
                    ema_molecule7 += int(current_7day_list[g])*(_a7**g)
                for g in range(0,15):
                    ema_molecule15 += int(current_15day_list[g])*(_a15**g)
                ema15 = ema_molecule15/ema_base15
                ema7 = ema_molecule7/ema_base7
                dif = ema7 - ema15
                dif_list.append(dif)
            for g in range(len(dif_list)-5,-1,-1):
                current4dif_list = []
                for f in range(g,g+4):
                    current4dif_list.append(dif_list[f])
                for d in range(4):
                    ema_molecule4 += current4dif_list[d]*(_a4**d)
                ema4 = float(ema_molecule4/ema_base4)
                macd_list.append(ema4)
            for s in range(len(macd_list)):
                macd_bar = dif_list[s] - macd_list[s]
                macd_bar_list.append(macd_bar)
            for a in range(len(macd_bar_list)):
                date_list2.append(date_list[-len(macd_bar_list)+a])

            dif_list_match=dif_list[0:len(macd_list)]
            #date_list3=date_list[9:]#去掉ｋｄ線的九天
            name = self.stock_id
            # print the line chart
            self.makeLine(d_value_list, k_value_list,date_list,name)
            self.makeLine2(name,date_list2, macd_list,dif_list_match,macd_bar_list)
        else:
            Main_Stat4.configure(text="查無資料QQ")
            #隱藏按鈕
            Main_Button2.grid_forget()
            button_bonus.grid_forget()
            button_bonus2.grid_forget()
            os.remove("C:\\Users\\joy\\AppData\\Local\\Programs\\Python\\Python36\\lib\site-packages\\matplotlib\\kdValue.png")
            os.remove("C:\\Users\\joy\\AppData\\Local\\Programs\\Python\\Python36\\lib\site-packages\\matplotlib\\kdValue2.png")

    # 繪製折線圖
    def makeLine(self, d_value_list, k_value_list, date_list, name):
        py.style.use('dark_background')
        times = range(0, len(k_value_list), 1)
        fig = py.figure(figsize=(15, 6))
        my_xticks = date_list
        py.xticks(times, my_xticks, fontsize=5)
        py.plot(times, k_value_list, label="k value")
        py.plot(times, d_value_list, label="d value")
        py.legend(loc='upper left')
        py.xlabel('Date')
        py.ylabel('Value')
        py.title("k value and d value for stock code %s" % name)
        py.savefig('C:\\Users\\joy\\AppData\\Local\\Programs\\Python\\Python36\\lib\site-packages\\matplotlib\\kdValue.png')

    def makeLine2(self,name,date_list2, macd_list,dif_list_match,macd_bar_list): 
        py.style.use('dark_background')
        times = range(0, len(date_list2), 1)  
        py2 = py.subplots(figsize=(15, 6))
        my_xticks = date_list2
        py.xticks(times, my_xticks, fontsize=5.5)
        py.plot(times, macd_list, color = "coral", lw=1,label='MACD Line')
        py.plot(times, dif_list_match, color = "yellow", lw=1, label='Dif Line')
        py.bar(times, macd_bar_list, color='cyan', alpha=0.5, label='MACD Histogram')
        py.legend(loc='lower left')
        py.ylabel('Value')
        py.title("MACD value for stock code %s" % name)
        py.savefig('C:\\Users\\joy\\AppData\\Local\\Programs\\Python\\Python36\\lib\site-packages\\matplotlib\\kdValue2.png')


global Main_Stat1,Main_Stat3,Main_Stat4,Main_Stat5,Main_Stat6,Main_Stat7,Main_Stat8,Main_Stat9,variable,variable2, StockNum, canvas, Main_Button2, button_bonus, button_bonus2

stock = Stock()
root = tk.Tk()

# --- create canvas with scrollbar ---

canvas = tk.Canvas(root, width=770, height=700)
canvas.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')

canvas.configure(yscrollcommand = scrollbar.set)

# update scrollregion after starting 'mainloop'
# when all widgets are in canvas
canvas.bind('<Configure>', on_configure)

# --- put frame in canvas ---

frame = tk.Frame(canvas)
canvas.create_window((0,0), window=frame, anchor='nw')

# --- add widgets in frame ---
f1 = tkFont.Font(size=76, family="娃娃體-繁")
f2 = tkFont.Font(size=20, family="手札體-繁")
f3 = tkFont.Font(size=16, family="手札體-繁")
f4 = tkFont.Font(size=14, family="宋體-繁")
f5 = tkFont.Font(size=24, family="手札體-繁")

Main_Text = tk.Label(frame, text="資料日期:")

Main_Text2 = tk.Label(frame, text="股票代碼:")


Main_Text.grid(row=3, column=0, sticky=tk.E)
Main_Text2.grid(row=3, column=4, sticky=tk.E)


variable = tk.StringVar(frame)
variable.set("民國107年")
optionList = ["民國107年", "民國106年", "民國105年", "民國104年", "民國103年", "民國102年", "民國101年", "民國100年", "民國99年", "民國98年",
                  "民國97年", "民國96年", "民國95年", "民國94年", "民國93年", "民國92年", "民國91年", "民國90年", "民國89年", "民國88年", "民國87年",
                  "民國86年", "民國85年", "民國84年", "民國83年", "民國82年", "民國81年"]
        
variable2 = tk.StringVar(frame)
variable2.set("01月")
optionList2 = ["01月", "02月", "03月", "04月", "05月", "06月", "07月", "08月", "09月", "10月", "11月", "12月"]
                  

Main_Title = tk.Label(frame, text="股票投資程式", font=f1)

Main_Text = tk.Label(frame, text="資料日期:", font=f2)
Main_Text2 = tk.Label(frame, text="股票代碼:", font=f2)

Main_Stat0 = tk.Label(frame, text = "", font = f5)
Main_Stat1 = tk.Label(frame, text="", font=f3)
Main_Stat2 = tk.Label(frame, text="", font=f3)
Main_Stat3 = tk.Label(frame, text="", font=f3)
Main_Stat4 = tk.Label(frame, text="", font=f3)
Main_Stat5 = tk.Label(frame, text="", font=f3)
Main_Stat6 = tk.Label(frame, text="", font=f3)
Main_Stat7 = tk.Label(frame, text="", font=f3)
Main_Stat8 = tk.Label(frame, text="", font=f3)
Main_Stat9 = tk.Label(frame, text="", font=f3)
                  
Main_OptionMenu = tk.OptionMenu(frame, variable, *optionList)
Main_OptionMenu2 = tk.OptionMenu(frame, variable2, *optionList2)
                  
Main_Space = tk.Label(frame, text="")
Main_Space2 = tk.Label(frame, text="")
                  
StockNum = tk.Text(frame, height=1, width=7, font=f3,bg="#CCEEFF",)

                  
Main_Button = tk.Button(frame, text="查詢",  font=f3, command=stock.CrawlerBtn)
Main_Button2 = tk.Button(frame, text="下載資料", height = 1, width=7, command = stock.CrawlerBtn2, font = f3)


button_bonus = tk.Button(frame, text="KD圖", command=popup_bonus, font=f3)
button_bonus2 = tk.Button(frame, text="MACD圖", command=popup_bonus2, font=f3)

image = Image.open("C:\\Users\\joy\\Documents\\商管程設\\final project\\stock.jpg")
image = image.resize((770, 100), Image.ANTIALIAS)
imageStock = ImageTk.PhotoImage(image)
main_image = tk.Label(frame, image=imageStock)
main_image.grid(row=0, column=0, columnspan=10, sticky=tk.NW + tk.SE,)

# ----------------------------grid--------------------------------------------#

Main_Title.grid(row=1, column=0, columnspan=10)

    
# Main_Space.grid(row=1, column=0)
Main_Space2.grid(row=4, column=0)
        
Main_OptionMenu.grid(row=3, column=1, sticky=tk.E, columnspan=1)
Main_OptionMenu2.grid(row=3, column=2, sticky=tk.W, columnspan=1)

Main_Text.grid(row=3, column=0, sticky=tk.E)
Main_Text2.grid(row=3, column=4, sticky=tk.E)

Main_Stat0.grid(row=5, column=0, columnspan=10, sticky = tk.SE + tk.NW)
Main_Stat1.grid(row=6, column=0, rowspan=20, sticky=tk.SE + tk.NW)
Main_Stat2.grid(row=6, column=1, rowspan=20, sticky=tk.SE + tk.NW)
Main_Stat3.grid(row=6, column=2, rowspan=20, sticky=tk.SE + tk.NW)
Main_Stat4.grid(row=6, column=3, rowspan=20, sticky=tk.SE + tk.NW)
Main_Stat5.grid(row=6, column=4, rowspan=20, sticky=tk.SE + tk.NW)
Main_Stat6.grid(row=6, column=5, rowspan=20, sticky=tk.SE + tk.NW)
Main_Stat7.grid(row=6, column=6, rowspan=20, sticky=tk.SE + tk.NW)
Main_Stat8.grid(row=6, column=7, rowspan=20, sticky=tk.SE + tk.NW)
Main_Stat9.grid(row=6, column=8, rowspan=20, sticky=tk.SE + tk.NW)
        
StockNum.grid(row=3, column=5, columnspan=2, sticky=tk.W)
        
Main_Button.grid(row=3, column=7)

# create a canvas so the scrollbar appears from the beginning
cvsMain = tk.Canvas(frame, width=770, height=600)
cvsMain.grid(row=40, column=0, columnspan=10, rowspan=50, sticky=tk.SW)


# --- start program ---


root.mainloop()
