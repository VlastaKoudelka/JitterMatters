from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import numpy as np
import matplotlib.pyplot as plt
import time
from kivy.core.window import Window

tfrData = np.load('tfrData.npy')
plt.style.use('dark_background')
figLine, axLine = plt.subplots()
figIm, axIm = plt.subplots()

#initial jitter
jitter = 0
#a number of intervals measured to calculate jitter
winLength = 10
#a set of intervals lengths
elapsedVect = np.zeros((winLength,1))
#starting time in ms
currTimeMs = int(time.time()*1e3)
#same jitter instances index array
instIdx = np.array([0,1,2])

class setGameWidget(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        global tfrData, figLine, axLine, figIm, axIm
        #define a graph
        x = np.random.rand(20,1)
        y = np.random.rand(20,1)
        axLine.plot(x,y)
        axLine.axis('off')
               
        boxGame1 = self.ids.boxGame1
        boxGame1.add_widget(FigureCanvasKivyAgg(figLine))
        
        #define an image
        tfrData = np.flip(tfrData,2)
        tfrSample = tfrData[0,0,:,1:49]
        axIm.imshow(tfrSample,cmap='seismic',interpolation='bicubic')
        axIm.set_xticks([0, 12, 24, 36, 48])
        axIm.set_xticklabels(['-300','0','300','600','900'])
        axIm.set_xlabel('time [ms]')
        axIm.set_yticks([0, 10, 20, 30, 40, 50])
        axIm.set_yticklabels(['150','125','100','75','50','20'])
        axIm.set_ylabel('frequency [Hz]')
        axIm.set_title('ASSR 40Hz ERP spectogram')
        boxGame2 = self.ids.boxGame2
        boxGame2.add_widget(FigureCanvasKivyAgg(figIm))
        
#         pass
    def recallplot(self,*args):
        #both currTimesMs and elapsedVect must be global to be updated
        global currTimeMs, elapsedVect, figLine, axLine, figIm, axIm, instIdx
        #calculate time difference
        pastTimeMs = currTimeMs
        currTimeMs = int(time.time()*1e3)        
        diffTimeMs = currTimeMs - pastTimeMs
        #update the interval lengths vector        
        elapsedVect = np.roll(elapsedVect,1)
        elapsedVect[0] = diffTimeMs
        #calculate jitter based on interval lengths        
        jitter = int(np.std(elapsedVect)/np.sqrt(2))
        #scale jitter based on slider
        slide = self.ids.slide
        jitter = int(jitter*slide.value)
        #show the jitter through the label
        jitterLabel = self.ids.jitterLabel
        if jitter == 0:
            jitterLabel.text = 'Synchronized!'     
        else:
            jitterLabel.text = 'Jitter = ' + str(jitter) + ' ms'     
        
        #update the LinePlot
        boxGame1 = self.ids.boxGame1
        slide = self.ids.slide
        x = np.random.rand(int(jitter),1)
        y = np.random.rand(int(jitter),1)
        axLine.clear()
        boxGame1.clear_widgets()
        axLine.plot(x,y)
        axLine.axis('off')
        boxGame1.add_widget(FigureCanvasKivyAgg(figLine))
        
        #update the imshow
        if jitter > 10:
            jitter = 10
        instIdx = np.roll(instIdx,1)
        boxGame2 = self.ids.boxGame2
        axIm.clear()
        boxGame2.clear_widgets()
        tfrSample = tfrData[jitter,instIdx[0],:,1:49]
        axIm.imshow(tfrSample,cmap='seismic',interpolation='bicubic')
        axIm.set_xticks([0, 12, 24, 36, 48])
        axIm.set_xticklabels(['-300','0','300','600','900'])
        axIm.set_xlabel('time [ms]')
        axIm.set_yticks([0, 10, 20, 30, 40, 50])
        axIm.set_yticklabels(['150','125','100','75','50','20'])
        axIm.set_ylabel('frequency [Hz]')
        axIm.set_title('ASSR 40Hz ERP spectogram')
        boxGame2.add_widget(FigureCanvasKivyAgg(figIm))            

class JitterMattersApp(App):
    def build(self):
        return setGameWidget()
        

if __name__ == "__main__":
#     Window.size = (640,480)
#     Window.fullscreen = True
    JitterMattersApp().run()