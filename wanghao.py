# -*- coding:utf-8 -*-
import wx
import wx.lib.analogclock as ac
import wx.lib.agw.aquabutton as AB
import wx.gizmos as gizmos
import time
import random
import os
import sys
import binascii
import win32crypt,cmd


u_pwd = unicode('123456')
pwdHash = win32crypt.CryptProtectData(u_pwd,u'',None,None,None,0)
pwd = 'password 51:b:' + binascii.hexlify(pwdHash).upper()


uname = 'username:s:'
keys = ['IE6', 'IE7', 'IE8', 'IE9', 'IE10', 'win32IE11', 'win64IE11']

for mname in keys:
    if not os.path.exists('./rdp/'+mname+'.rdp'):
        model = open('./model/'+mname+'.txt')
        mdate = model.read()
        new = open('./rdp/'+mname+'.rdp', 'w')
        new.write(mdate)
        new.write(uname+"admin")
        new.write("\n")
        new.write(pwd)
        new.close()



class Mytime(wx.Panel):
    #时钟方法，然后添加到boxsizer中
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.SetBackgroundColour("blue")
        
        #时钟效果
        led = gizmos.LEDNumberCtrl(self,-1,(0,0),(300,50),gizmos.LED_ALIGN_CENTER)
        self.clock = led
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER,self.OnTimer)
        
    def OnTimer(self,evt):
        t = time.localtime(time.time())
        st = time.strftime("%I-%M-%S",t)
        self.clock.SetValue(st)

class MyButton(wx.Panel):
    #-------------远程链接按钮---------------------------------------------------------
    def __init__(self,parent):
        """"""
        wx.Panel.__init__(self,parent,-1)
        self.SetBackgroundColour(wx.Colour(0,255,255))

        box = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        #按钮数据
        self.date={"IE6":"./rdp/IE6.rdp",
                   "IE7":"./rdp/IE7.rdp",
                   "IE8":"./rdp/IE8.rdp",
                   "IE9":"./rdp/IE9.rdp",
                   "IE10":"./rdp/IE10.rdp",
                   "32IE11":"./rdp/win32IE11.rdp",
                   "64IE11":"./rdp/win64IE11.rdp"}
        #循环输出按钮
        self.buttonid={}
        for buttonname in self.date:
            
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255) 
            
            btn = AB.AquaButton(self,-1,None,buttonname)
            box.Add(btn,1,wx.EXPAND |wx.EAST| wx.WEST,5)
            btn.SetBackgroundColor(wx.Colour(r,g,b))
            btn.SetHoverColor(wx.Colour(g,r,b))
            btn.SetForegroundColour("black")
            btn.SetFont(font)
            self.Bind(wx.EVT_BUTTON, self.OnClick, btn)
            self.buttonid[btn.GetId()]= buttonname
        self.SetSizer(box)
        
    def OnClick(self,evt):
        ip = self.date[self.buttonid[evt.GetId()]]
        os.system("mstsc %s /console " % ip)
        
        
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,- 1, u"远程链接", size=(300,450),style=wx.DEFAULT_FRAME_STYLE)
        #self.SetBackgroundColour('black')
        #设置程序图标
        self.SetMaxSize((300,500))
        self.ICON = wx.Icon("2.ico",wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.ICON)
        
        mytime = Mytime(self)
        mybutton = MyButton(self)
        
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(mytime,-1,wx.EXPAND|wx.ALL)
        box.Add(mybutton,2,wx.EXPAND|wx.ALL)
        self.SetSizer(box)
        
        self.taskBarIcon = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.Bind(wx.EVT_ICONIZE,self.OnIconfiy)
        
        

    
    #点击最小化时，隐藏界面，到托盘    
    def OnIconfiy(self,event):
        self.Hide()
    
    #点击关闭时，隐藏界面，到托盘 
    def OnClose(self,event):
        self.Hide()
        
########################################################################
class TaskBarIcon(wx.TaskBarIcon):
    #最小化托盘

    #--------------ID----------------------------------------------
    ID_Abuout = wx.NewId()
    ID_MainFrame = wx.NewId()
    ID_Exit = wx.NewId()
    '''
    ID_IE6 = wx.NewId()
    ID_IE7 = wx.NewId()
    ID_IE8 = wx.NewId()
    ID_IE9 = wx.NewId()
    ID_IE10 = wx.NewId()
    ID_IE3211 = wx.NewId()
    ID_IE6411 = wx.NewId()
    '''
    
    #---------------不同机器对应的IP,和菜单栏的ID----------------------
    date={"IE6":6,
                       "IE7":7,
                       "IE8":8,
                       "IE9":9,
                       "IE10":10,
                       "32IE11":11,
                       "64IE11":12} 
    date1={6:"./rdp/IE6.rdp",
                   7:"./rdp/IE7.rdp",
                   8:"./rdp/IE8.rdp",
                   9:"./rdp/IE9.rdp",
                   10:"./rdp/IE10.rdp",
                   11:"./rdp/win32IE11.rdp",
                   12:"./rdp/win64IE11.rdp"}    
    
    def __init__(self,frame):
        wx.TaskBarIcon.__init__(self)
        
        self.SetMainFrame(frame)        
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK,self.OnTaskBarLeftDClick)
        self.Bind(wx.EVT_MENU, self.OnMainFrame, id=self.ID_MainFrame)
        self.Bind(wx.EVT_MENU, self.OnExit, id=self.ID_Exit)
        
        
    def SetMainFrame(self, frame):
        self.frame = frame
        self.SetIcon(wx.Icon("2.ico",type=wx.BITMAP_TYPE_ICO),u"远程链接")

    def OnTaskBarLeftDClick(self,event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()
        
    def OnMainFrame(self,event):    
        #显示主面板
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()
    
    #-------------------------------------   
    def OnExit(self,event):
        #关闭程序
        wx.Exit()
           
    def CreatePopupMenu(self):
        #添加最小化菜单
        self.menu = wx.Menu()
        
        self.menu.Append(self.ID_MainFrame, u"主面板")
        self.menu.AppendSeparator()
        self.Bind(wx.EVT_MENU,self.ConnectIE,id =self.ID_MainFrame)
        
        for key in self.date:
            if key:
                self.menu.Append(self.date[key],key)
                self.Bind(wx.EVT_MENU,self.ConnectIE, id=self.date[key])
                
        self.menu.AppendSeparator()
        self.menu.Append(self.ID_Exit, u"退出")
        return self.menu
    
    def ConnectIE(self, event):
        #托盘处链接远程机
        ip = self.date1[event.GetId()]
        os.system("mstsc %s /console" % ip)
        

       

        
     
        
if __name__ == '__main__':
    app = wx.App()
    fram = MyFrame()
    fram.Show()
    app.MainLoop()
        
