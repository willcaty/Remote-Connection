#coding:utf-8
import wx
import sys
import os


from wanghao import MyFrame

########################################################################
class RunFrame():
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.pwd = os.path.abspath(sys.path[0])
        self.user_home = os.path.expanduser("~")
        
    def run(self):
        app = wx.App(False)
        instance_name = "%s-%s" % (app.GetAppName(), wx.GetUserId())
        instance_chacker = wx.SingleInstanceChecker(instance_name,self.pwd)
        if instance_chacker.IsAnotherRunning():
            dlg = wx.MessageDialog(None,u"你已经打开了，是否再打开一个", u"浩哥提示！！！！",wx.YES_NO|wx.ICON_QUESTION)
            ret_code = dlg.ShowModal()
            if ret_code !=wx.ID_YES:
                dlg.Destroy()
                return 
            dlg.Destroy()
        
        frame = MyFrame()
        self.app = app
        self.frame = frame
        
        frame.Show()
        app.MainLoop()
        app.Destroy()
        
def main():
    sh = RunFrame()
    sh.run()
    
if __name__ == '__main__':
    main()
        
    
    