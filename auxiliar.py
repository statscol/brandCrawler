
import pandas as pd
import pytube as pyt
import os
import cv2
import shutil as sht
import datetime
import random

def yout_to_img(link_vid,path_dest,file_desc):
    vid_name='video{}'.format(str(random.randint(0,1000000))) 
    yt = pyt.YouTube(link_vid)
    print(vid_name)
    ##DOWNLOAD VIDEO AT 720p Res
    yt.streams.filter(res="720p").first().download(output_path=path_dest+file_desc+"/",filename=vid_name)
    
    files=os.listdir(path_dest+file_desc+'/')
    if len(files)==0:
        return("403: Link Not Valid or doesn't contain 720p version")
    else:  
        
#        os.rename(out_vid,vid_name)
        cam = cv2.VideoCapture(path_dest+file_desc+'/'+vid_name+'.mp4')
        currentframe = 0
    
        while(True):
            ret,frame = cam.read()
            if ret:
                name = path_dest+file_desc+'/frame' + str(currentframe) + '.jpg'
                
                if currentframe%5==0:
                    cv2.imwrite(name,frame)
                    
               
                if currentframe%1000==0:
                	print("Creating..."+name)

                
                currentframe += 1
            else:
                break
        cam.release()
        cv2.destroyAllWindows()
        os.remove(path_dest+file_desc+'/'+vid_name+'.mp4')


