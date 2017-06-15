from tkinter import *
import sys
import urllib.parse
import urllib.request
import json
from tkinter import ttk
from tkinter import messagebox
import datetime
class Weather:
     
     url="http://api.openweathermap.org/data/2.5/weather?"
     APPID="57f9b005d2fe962bde3741f75c813a93"
     def __init__(self):
         self.root=Tk()
         self.create_gui()
         self.root.mainloop()

     def create_gui(self):
         frame=Frame(self.root)
         frame.pack(side='top')
         Label(frame,text="Enter location").pack(side="left")
         self.location=StringVar()
         Entry(frame,textvariable=self.location).pack(side="left")
         Button(frame,text="Go",command=self.get_weather_data).pack(padx=5,pady=5)
         self.canvas=Canvas(self.root,height=425,width=340,background="black")
         self.canvas.create_rectangle(10,10,330,415,fill='#F6AF06')
         self.canvas.pack(side='bottom')
     
     def get_weather_data(self):
         if not self.location.get():
             return
         self.clear_canvas()
         self.json_parsing()
         self.format_data()
         self.display_data()
    
     def clear_canvas(self):
         self.canvas.delete(ALL)
         self.canvas.create_rectangle(10,10,330,415,fill='#F6AF06')

     def get_data(self):
         try:
             data={'q':self.location.get(),'APPID':self.APPID}
             url_data=urllib.parse.urlencode(data)
             self.url=self.url+url_data
             with urllib.request.urlopen(self.url) as data:
                 json_data=data.read()
             return json_data
         except IOError as e:
             messagebox.showerror(
                 'Unable to connect', 'Unable to connect ')
             sys.exit(1)

     def json_parsing(self):
         data=self.get_data()
         data=data.decode("utf-8")
         self.data=json.loads(data)
  
     def format_data(self):
         if not self.data:
             messagebox.showerror(
                 'Name not found', 'Unable to fetch record - Name not found')
             return
         self.name=self.data["name"]
         self.country=self.data["sys"]["country"]
         self.lat=str(self.data["coord"]["lat"])
         self.lon=str(self.data["coord"]["lon"])
         self.icon="weatherimages/{}.png".format(str(self.data["weather"][0]['icon']))
         self.dust=self.data["weather"][0]["main"]
         self.temp=str(self.data["main"]["temp"])
         self.temp_max=str(self.data["main"]["temp_max"]-273.15)+u' \u2103'
         self.temp_min=str(self.data["main"]["temp_min"]-273.15)+u' \u2103'
         self.humidity=str(self.data["main"]["humidity"])
         self.w_speed=str(self.data["wind"]["speed"])
         self.w_degree=str(self.data["wind"]["deg"])
         self.pressure=str(self.data["main"]["pressure"])
         self.cloud=str(self.data["clouds"]["all"])
         self.sunrise=(datetime.datetime.fromtimestamp(self.data["sys"]["sunrise"]).strftime('%H:%M:%S'))
         self.sunset=(datetime.datetime.fromtimestamp(self.data["sys"]["sunset"]).strftime('%H:%M:%S'))
         self.description=self.data["weather"][0]["description"]
 
     def display_data(self):
         opt={'fill':'white','font':'Helvetica 12'}
         self.canvas.create_text(52,30,text=self.name,**opt)
         self.canvas.create_text(245,35,text="Latitude   : "+self.lat,**opt)
         self.canvas.create_text(245,53,text="Longitude : "+self.lon,**opt)
         self.canvas.create_text(55,50,text="Country : "+self.country,**opt)
         self.canvas.create_text(85,105,text="NOW",**opt)
         self.img = PhotoImage(file=self.icon)
         self.canvas.create_image(140,105,image=self.img)  
         self.canvas.create_text(240,105,text=self.description,**opt)
         self.canvas.create_text(85,155,text="Temperature",**opt)
         self.canvas.create_text(87,175,text=self.temp_min+"~"+self.temp_max,**opt)  
         self.canvas.create_text(95,215,text="Relative Humidity",**opt)
         self.canvas.create_text(198,215,text=self.humidity+"%",**opt)
         self.canvas.create_text(77,235,text="Wind Speed",**opt)
         self.canvas.create_text(205,235,text=self.w_speed+"m/s",**opt)
         self.canvas.create_text(70,255,text="Degree",**opt)
         self.canvas.create_text(223,255,text=self.w_degree+"degree",**opt)
         self.canvas.create_text(70,275,text="Pressure",**opt)
         self.canvas.create_text(225,275,text=self.pressure+"millibar",**opt)
         self.canvas.create_text(58,310,text="Clouds",**opt)
         self.canvas.create_text(200,310,text=self.cloud,**opt)
         self.canvas.create_text(60,328,text="Sunrise",**opt)
         self.canvas.create_text(200,328,text=self.sunrise,**opt)
         self.canvas.create_text(59,343,text="Sunset",**opt)
         self.canvas.create_text(200,343,text=self.sunset,**opt)

if '__main__'==__name__:
    Weather()
