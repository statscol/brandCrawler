
import pandas as pd
import pytube as pyt
import os
import cv2
import shutil as sht
import datetime
import random
import json
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt



def yout_to_detections(link_vid,path_dest,file_desc,DARKNET_PATH):
    vid_name='video{}'.format(str(random.randint(0,1000000))) 
    yt = pyt.YouTube(link_vid)
    print(vid_name)
    ##DOWNLOAD VIDEO AT 720p Res
    yt.streams.filter(res="720p").first().download(output_path=path_dest+file_desc+"/",filename=vid_name)
    
    files=os.listdir(path_dest+file_desc+'/')
    if len(files)==0:
        return("203: Link Not Valid or doesn't contain 720p version")
    else:  
        
#        os.rename(out_vid,vid_name)
        cam = cv2.VideoCapture(path_dest+file_desc+'/'+vid_name+'.mp4')
        currentframe = 0
        names_img=[]
        while(True):
            ret,frame = cam.read()
            if ret:
                name = path_dest+file_desc+'/frame' + str(currentframe) + '.jpg'
                
                cv2.imwrite(name,frame)
                names_img.append(name)    
               
                if currentframe%1000==0:
                	print("Creating..."+name)

                
                currentframe += 1
            else:
                break
        cam.release()
        cv2.destroyAllWindows()
        os.remove(path_dest+file_desc+'/'+vid_name+'.mp4')
        ##ESCRIBIR ARCHIVO CON NOMBRES DE IMÁGENES PARA EL DETECTOR
        with open(path_dest+vid_name+".txt", "w") as outfile:
            outfile.write("\n".join(names_img))

        os.chdir(DARKNET_PATH)
        commands=["./darknet detector test data/obj.data cfg/yolov4-obj.cfg yolov4-obj_final.weights -ext_output -dont_show -out /home/jf/"+vid_name+".json < "+path_dest+vid_name+".txt"]
        os.system("".join(commands))
        for file in names_img:
            os.remove(file)
        print("Detections...completed")
        os.remove(path_dest+vid_name+".txt")
        return("/home/jf/"+vid_name+".json")

def get_brand_expo(JSON_FILE_AUX,IMG_WIDTH=1280,IMG_HEIGHT=720):
  """ JSON_FILE_AUX: Filename of .json to be analyzed
      IMG_WIDTH: IMAGE WIDTH (it assumes all images have the same width and height)
      JSON_PATH: PATH WHERE JSON_FILE_AUX is stored 
    """
    
  IMG_AREA=IMG_WIDTH*IMG_HEIGHT

  detections=[]
  width=[]
  height=[]
  area=[]
  frames=[]


  ##GET JSON FILE IN STRUCTURED FORM
  with open(JSON_FILE_AUX) as json_file:
      data = json.load(json_file)
      
      for record in data:
          
          
          for obj in record['objects']:
              detections.append(obj['name'])
              frames.append(record['frame_id'])
              aux_w=obj['relative_coordinates']['width']*IMG_WIDTH
              aux_h=obj['relative_coordinates']['height']*IMG_HEIGHT
              aux_a=aux_w*aux_h
              width.append(aux_w)
              height.append(aux_h)
              area.append(aux_a)
  
  ## GET AGGREGATIONS OUT OF .JSON
  data_res=pd.DataFrame({'frame':frames,'detections':detections,'width':width,'height':height,'area':area})

  avr_data=data_res.groupby('detections').agg({'width':'mean','height':'mean','area':'mean','detections':'count','frame':'nunique'})
  marcas=avr_data.index

  ##RELEVANT VARIABLE TRANSFORMATIONS

  avr_data['area_rel']=avr_data['area']/IMG_AREA
  avr_data['time_proxy']=avr_data['frame']/30
  avr_data['appearances_rel']=avr_data['detections']/len(frames)

  ## GET INDEX AND SCALING IT TO 0-100%
  indice=PCA().fit_transform(avr_data[['appearances_rel','area_rel','time_proxy']])
  scaler=MinMaxScaler()
  indice_std=scaler.fit_transform(indice[:,0].reshape((-1,1)))*100

  
  avr_data['exposicion']=indice_std
  avr_data['filename']=JSON_FILE_AUX.replace(".json","")
  avr_data=avr_data[avr_data['exposicion']>1]
 # os.remove("/home/jf/"+vid_name+".json")
  return(avr_data[['area_rel','appearances_rel','time_proxy','exposicion']].reset_index().sort_values(by="exposicion",ascending=True))

def gen_img(data_expo,path_app):
   
    f,ax=plt.subplots(figsize=(10,8),dpi=200)
    ax.barh(data_expo['detections'],data_expo['exposicion'],color="darkred")
    ax.set_ylabel("Marca",fontsize=15)
    ax.set_xlabel("Indice de Exposición (%)",fontsize=15)
    ax.set_title("Exposición de Marcas para el Video",fontsize=15)
    if os.path.isfile(path_app+"static/img/prueba.png"): ##probar si la imágen existe
       os.remove(path_app+"static/img/prueba.png") 
    f.savefig(path_app+"static/img/prueba.png")
#    f.savefig("/static/prueba.png")