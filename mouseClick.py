'''
Let the computer auto click!
Neal : njugui@gmail.com

'''
import win32gui
import win32api
import win32con
import time

pos_list = [(1306,662), 
            (550,500), 
            (550,550), 
            (500,550), 
            (500,500)]

def LeftClick(handle, pos):
    client_pos = win32gui.ScreenToClient(handle, pos)
    tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp) 
    win32api.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
   
def RightClick(handle, pos):
    client_pos = win32gui.ScreenToClient(handle, pos)
    tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32api.SendMessage(handle, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, tmp) 
    win32api.SendMessage(handle, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, tmp)

def MouseMove(handle, pos):
    client_pos = win32gui.ScreenToClient(handle, pos)
    tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp) 
    win32api.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
           
def get_curpos():
    return win32gui.GetCursorPos()

def get_win_handle(pos):
    return win32gui.WindowFromPoint(pos)
    
if __name__ == '__main__':
    time.sleep(10)
    pos1 = (1306, 662)
    pos2 = (1398, 658)
    handle = get_win_handle(pos1)
    LeftClick(handle, pos1)  
    handle = get_win_handle(pos2)
    LeftClick(handle, pos2)  
     
    '''
    for i in range(len(pos_list)):
        handle = get_win_handle(pos_list[i])
        LeftClick(handle, pos_list[i])
        time.sleep(2)'''
        
    
    