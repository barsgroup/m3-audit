#coding:utf-8
'''
Created on 06.01.2011

@author: akvarats
'''

from m3.ui.ext import windows
from m3.ui.ext import panels
from m3.ui.ext import containers
from m3.ui.ext import fields

class AuditListWindow(windows.ExtWindow):
    '''
    Окно со списком записей аудита
    '''
    def __init__(self, *args, **kwargs):
        super(AuditListWindow, self).__init__(*args, **kwargs)
        
        self.title = u'Аудит операций'
        
        self.width = 800
        self.height = 550
        self.layout = 'border'
        
        self.panel_center = containers.ExtContainer(region='center',
                                                    layout='fit')
        self.panel_east = containers.ExtContainer(region='east',
                                          layout='fit')
        
        self.grid_rows = panels.ExtObjectGrid()
        
        self.panel_center.items.append(self.grid_rows)
        
        self.items.extend([self.panel_center,
                           self.panel_east,])
        
        
class DefaultAuditEastPanel(panels.ExtPanel):
    '''
    Дефолтная правая панель для окна со списком записей аудита
    '''
    
    def __init__(self, *args, **kwargs):
        super(DefaultAuditEastPanel, self).__init__(*args, **kwargs)
        
        self.items.append(fields.ExtDisplayField(value=u'Чуваки, я здесь!'))
        
        self.init_component(*args, **kwargs)