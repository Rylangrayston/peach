#!/usr/bin/env python


'''
3d scanner 
writen by Rylan Grayston




call this program with :
python peach/scanner/scan.py 

it will ask you a few questions and then show you a video 
.. you must click down on the center of the spining object 
to select the center, then continue hloding down the mouse, drag
it over the laser beam and let go of the mouse while its on the 
color you wish to detect.


 

it will then go about trying to creat a 3d modle out of the image data 
and then save this in a wavefont / .obj file

you can import the the output.obj file using blender 3d
do file import wavefront
 ... be sure to chose the keep vertex order button located in the lower left of the screen right 
 after clicking import!



green dots represent a detected color 
red dots are the closest to the color that you chose to detect but not 
close enuf acroding to the thresholds 

there must be .jpg files in one of these directorys :
image_map_frames/
image_map_frames/proxy
laser_scan_frames/
laser_scan_frames/proxy 

the proxy directorys are intended for low res tests images 

the first image must have the name 1000.jpg and continu from there 
1001.jpg, 1002.jpg, 1003.jpg ... 9999.jpg  

the scanner can also get frames in real time from your webcam 
which is unsfull for coding and just seing how the program works.


if you choose to make and image map then 
simpley click the center of the image and watch the image map get created! 


'''

import cv
import cv2.cv as cv # what is the dif here?
import time
import random
import os
import math

import numpy as np

os.system('cls' if os.name=='nt' else 'clear')


# open cv or os ?.. returns numbers for differant mouse events lets give them names
MOUSE_MOVE  = 0;
MOUSE_DOWN  = 1;
MOUSE_UP    = 4;
TEMP_IMAGE = 'peach/scanner/temp.jpg'


answer = raw_input('live real time capture? y or n')
if answer == 'n':
    real_time = False
else:
    real_time = True

proxy = True
answer = raw_input('make image map or scan? i or s')
if answer == 'i':
    do_image_map = True
    path = 'peach/scanner/image_map_frames/'
    if proxy:
        path += 'proxy/'
else :
    do_image_map = False
    path = 'peach/scanner/laser_scan_frames/'
    if proxy:
        path += 'proxy/'


file_name = '1000.jpg'





class Scanner:
    """ program uses a cammera and line laser to make a 3d modle from a real object """
    _imageRGB = None;
    _imageHSV = None;

    def __init__( self , path, do_image_map, real_time):
        self.real_time = real_time
        self.do_image_map = do_image_map
        self.frame_advance = 1
        self.center = None
        self.frame = 0 
        self.path = path
        cv.NamedWindow( "camera", 1 );
        cv.SetMouseCallback( "camera", self.onMouse );
        self.mat = cv.LoadImage( (path + file_name) );
        #self._imageRGB = cv.LoadImage( "scanner/test2.jpg" ); # "scanner/frames/0557.jpg" "scanner/test2.jpg"
        self._imageHSV = cv.CreateImage( cv.GetSize( self.mat ), 8, 3 );
        #self.choice = choice
        #choice = (0,0,0)

        cv.CvtColor( self.mat, self._imageHSV, cv.CV_BGR2HSV );
        cv.ShowImage( "camera", self.mat );
        self.choice = (0,0,0)
        self.begin = False
        self.position = 20
        print( "Keys:\n"
            "    ESC - quit the program\n"
            "    b - switch to/from backprojection view\n"
            "To initialize tracking, drag across the object with the mouse\n" )

    def onMouse( self, event, mouseX, mouseY, flags, param):
        if( event == MOUSE_UP ):
            pix = self.mat[mouseY, mouseX];#self._imageRGB
            self.choice = pix
            self.position = mouseX
            print "X, Y >> H, S, V:", [mouseX, mouseY], pix;
            if self.begin == False:
                print('Starting.... ')
                self.begin = True
                self.frame_advance = 1
                self.frame = 0

        if(event == MOUSE_DOWN):
            self.center = mouseX
            self.frame_advance = 0


    



    def run( self ):
        


        #cv.NamedWindow("camera", 1)
        capture = cv.CaptureFromCAM(0)
        scan_method = 'spin'
        self.frame = 0
        pan = 0 
        #color to detect bgr
        R = 40
        G = 104
        B = 220
        #amout grid size of points checked in image
        skip_x = 2
        skip_y = 2
        skip_frame = 20
        
        # factor scales the size of the object in output.obj
        factor_y = .1
        factor_x = .1
        factor_z = .1

        #string to hold all faces will be writen to obj file at the end of the scan
        faces = '' 

        # is this the first frame? will be set to False after the first frame 
        first_frame = True

        #how many rows were scanned in the first frame
        rows_scaned = 0

        # if the color of the detected pixle difrenter than detect threshold we will move it far away from the modle making it easy to delete
        detect_threshold = 150
        # if the pixle is with in stop_looking_threshold then stop lookin for another one... this stops the scanner from detectign more than 
        #one line.
        stop_looking_threshold = 100
        first_row = True

        current_row = 0

        vert_index = 0

        do_image_map = False  

        # how was the object scanned .. options may be 'dolly' 'spin' 'pan' 'laser_pan'
        

        # variables to spin data with###

        frames_per_revolution = 2633
        
        angle_step = math.pi * 2 / (frames_per_revolution / skip_frame)
        angle = 0



        #user questions 




        file = open('peach/scanner/output.obj', 'w')
        # create an object in the .obj file
        file.write('o PeachyScan\n')
        
        if self.real_time == False:
            # getting the list of files
            files = os.listdir(self.path);
            print(len(files), ' files detected in ', self.path)


        def color_dif(r,g,b,R,G,B):
            r_dif = abs(r - R)
            g_dif = abs(g - G)
            b_dif = abs(b - B)
            return(r_dif + g_dif + b_dif)

        def add_key(img, r,g,b,size=20):
            for rows in range(size):
                for colums in range(size):
                    img[colums,rows] = (b,g,r)
            return(img)
        def exit_scanner():
            file.write(faces)
            file.close()

        def make_image(width,height):
            ''' 
             returns a 2d array of touples that hold the BGR values on an image.
            '''
            blank_image = np.zeros((height,width,3), np.uint8)
            return(cv.fromarray(blank_image))
            


       











        #self.choice = (45.0, 86.0, 19.0)  #45.0, 86.0, 19.0
        #self.choice = (230, 230, 230)
        if self.choice != (0,0,0):
            self.begin = True



        if self.do_image_map == False:    
            while True:   #   0000000000000000000000000000000000000000000000000000000000000
                
                    
                #


                ##########################################################33
                # self.frame and pan grow each time we have scaned an entire frame

                #print(self.frame)
                #time.sleep(1)
                # if we are doing a real time scan then capture frames from the web cam
                if self.real_time: 
                    img = cv.QueryFrame(capture)
                

                    cv.SaveImage(TEMP_IMAGE, img)
                    self.mat = cv.LoadImageM(TEMP_IMAGE, cv.CV_LOAD_IMAGE_COLOR)
                    #self.mat = mat
                #mat = cv.LoadImageM('scanner/edit.jpg', cv.CV_LOAD_IMAGE_COLOR)
                
                # load frames from disk:
                if not self.real_time:
                    self.frame += self.frame_advance
                    if self.frame > len(files)-2 : 
                        self.frame = 0
                        if self.begin:
                            exit_scanner()
                            break
                    file_name = '' + str(1000 + self.frame ) + '.jpg'

                    self.mat = cv.LoadImageM(self.path+file_name, cv.CV_LOAD_IMAGE_COLOR)
                    #mat = cv.LoadImageM(path+files[self.frame], cv.CV_LOAD_IMAGE_COLOR)

                
                    

                #os.system('cls' if os.name=='nt' else 'clear')

                #print('y resolution of ', self.mat.rows/skip_y )
                #time.sleep(3)
                B,G,R = self.choice
                first_row = True
                current_row = 0 
                if self.begin == True and self.frame % skip_frame == 0:
                     
                    print('prosesing frame ', self.frame )
                    if scan_method == 'dolly' or scan_method == 'pan' or scan_method == 'laser_pan': 
                        pan += .1
                    if scan_method == 'spin':
                        angle += angle_step
                    for row_number in range(self.mat.rows):
                        if row_number % skip_y == 0 : 
                            current_row += 1
                            if first_frame: 
                                rows_scaned += 1
                            pixle_row = []

                            for colum_number in range(self.mat.cols):
                                if colum_number % skip_x == 0:
                                    rgb = self.mat[row_number,colum_number]
                                    b, g, r = rgb
                                    color_dif(r,g,b,R,G,B)
                                    
                                    pixle_row.append(color_dif(r,g,b,R,G,B))
                            #print(max(pixle_row))
                            
                            closest_yet = 20000
                            position = 0
                            bright_position = 0
                            for pixle_value in pixle_row:
                                position += skip_x

                                if pixle_value < closest_yet:
                                    closest_yet = pixle_value
                                    bright_position = position
                                    if pixle_value < stop_looking_threshold:
                                        break
                            #print(bright_position, ('*' * int(bright_position/20)) )

                            if closest_yet < detect_threshold and bright_position > self.center:
                                self.mat[row_number-skip_y, bright_position-skip_y] = (0,250,0)
                                if scan_method == 'dolly' or scan_method == 'pan' or scan_method == 'laser_pan':
                                    file.write('v ' + str(row_number * factor_y) + ' ' + str(bright_position * factor_x * math.cos(angle)) + ' ' + str(pan + (random.random()*.1))  +  '\n')
                                if scan_method == 'spin':
                                    file.write('v ' + str(((bright_position - self.center) ) * math.cos(angle) )  + ' ' + str(row_number * factor_z)+ ' ' + str((bright_position -self.center ) * math.sin(angle) )  +  '\n')
                                    #print('spining')
                                do_face = True
                                
                            else:
                                self.mat[row_number-skip_y, bright_position-skip_y] = (0,0,250)
                                if scan_method == 'dolly' or scan_method == 'pan' or scan_method == 'laser_pan':
                                    file.write('v ' + str(row_number * factor_y ) + ' ' + str(bright_position * factor_x) + ' ' + str(pan + (random.random()*.1))  +  '\n')
                                if scan_method == 'spin':
                                    file.write('v ' + str(((bright_position - self.center) ) * math.cos(angle) )  + ' ' + str(row_number * factor_z + 20 )+ ' ' + str((bright_position - self.center) * math.sin(angle) )  +  '\n')
                                
                                do_face = False
                            
                            vert_index += 1
                            if not first_frame: 
                                if first_row and do_face:
                                    face = 'f ' + str(vert_index) + ' ' + str(vert_index - rows_scaned) + ' ' + str(vert_index - rows_scaned + 1) + '\n'
                                    faces = faces + face

                                if not first_row and current_row != rows_scaned and do_face:
                                    face = 'f ' + str(vert_index) + ' ' + str(vert_index - rows_scaned) + ' ' + str(vert_index - rows_scaned + 1) + '\n'
                                    faces = faces + face
                                    face = 'f ' + str(vert_index) + ' ' + str(vert_index - rows_scaned) + ' ' + str(vert_index - 1) + '\n'
                                    faces = faces + face
                                    #print(face,'..face')


                        first_row = False
                    first_frame = False

                self.mat = add_key(self.mat,R,G,B,20)
                cv.ShowImage("camera", self.mat)
                


                 








                #print(self.choice)
                c = cv.WaitKey(10)
                if c == 27:
                    exit_scanner()
                    break


        if not self.real_time and self.do_image_map:
            self.begin = False
            print('making image map')
            mat = cv.LoadImageM(self.path+'1000.jpg', cv.CV_LOAD_IMAGE_COLOR)
            print mat.rows , mat.cols
            time.sleep(2)
            image_map = make_image(mat.cols, mat.rows)
            cv.SaveImage('peach/scanner/image_map.jpg', image_map)
            #time.sleep(2)
            self.frame = 0
            # do every frame_skip frames 
            frame_skip = 40
            j = 0
            colum_capture = []
            
            capture_width = 1
            #path = 'scanner/image_map_frames/'
            files = os.listdir(self.path);
             
            print(int(len(files)/frame_skip), 'files detected in ', self.path)

            while True:
                #ggggggg
                image_map = cv.LoadImageM(self.path + '1000.jpg', cv.CV_LOAD_IMAGE_COLOR)
                cv.ShowImage("camera", image_map)
                c = cv.WaitKey(10)
                if c == 27 or self.begin:
                    capture_position = self.position
                    break

            while True:
                self.frame += 1
                if self.frame % 10 == 0:
                    cv.SaveImage('scanner/image_map.jpg', image_map)
                j += frame_skip
                if self.frame > int((len(files)-5)/ frame_skip) : 
                    self.frame = 0
                    #break
                file_name = '' + str(1000 + j ) + '.jpg'

                print(self.path+file_name)
                self.mat = cv.LoadImageM(path+file_name, cv.CV_LOAD_IMAGE_COLOR)

                # load a vertical line of pixles rgb color values into variable colum_capture the pix on ether side green 

                for x in range(capture_width):
                    colum_capture = []
                    for row in range(self.mat.rows):
                        colum_capture.append( self.mat[row, capture_position + x])
                        #self.mat[row, capture_position+x+int(capture_width/2)] = (0,200,0)
                        #self.mat[row, capture_position-x-int(capture_width/2)] = (0,200,0)

                    for row in range(image_map.rows):
                        image_map[row,self.frame*capture_width + x] = colum_capture[row]







                cv.ShowImage("camera", image_map)
                time.sleep(.2)
                if self.frame % 3 == 0:
                    for row in range(self.mat.rows):
                        self.mat[row, capture_position+x+int(capture_width/2)] = (0,200,0)
                        self.mat[row, capture_position-x-int(capture_width/2)] = (0,200,0)
                    cv.ShowImage("ColorPicker", self.mat)
                    time.sleep(.2)
                

                


                



                print(self.choice)
                c = cv.WaitKey(10)
                if c == 27:
                    exit_scanner()
                    cv.SaveImage('peach/scanner/image_map.jpg', image_map)
                    break


if __name__=="__main__":
    demo = Scanner(path = path, do_image_map = do_image_map, real_time = real_time)
    demo.run()
