#!/usr/bin/env python

import cv
import cv2.cv as cv
import time
import random
import os
import math
os.system('cls' if os.name=='nt' else 'clear')

MOUSE_MOVE  = 0;
MOUSE_DOWN  = 1;
MOUSE_UP    = 4;

class ColorPicker:
    """ simple colorpicker to see HSV values from openCV """
    _imageRGB = None;
    _imageHSV = None;

    def __init__( self ):
        cv.NamedWindow( "camera", 1 );
        cv.SetMouseCallback( "camera", self.onMouse );
        self.mat = cv.LoadImage( "scanner/image_map_frames/1001.jpg" );
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
        if( event == MOUSE_DOWN ):
            pix = self.mat[mouseY, mouseX];#self._imageRGB
            self.choice = pix
            self.position = mouseX
            print "X, Y >> H, S, V:", [mouseX, mouseY], pix;
            if self.begin == False:
                print('Starting.... ')
                self.begin = True

#            print self._colorImage[100, 100]

    def run( self ):
        #


##########################################################33
        #cv.NamedWindow("camera", 1)
        capture = cv.CaptureFromCAM(0)
        i = 0
        pan = 0 
        #color to detect bgr
        R = 40
        G = 104
        B = 220
        #amout grid size of points checked in image
        skip_x = 4
        skip_y = 4
        real_time = True
        # factor scales the size of the object in output.obj
        factor_y = .1
        factor_x = .1
        factor_z = 1

        #string to hold all faces will be writen to obj file at the end of the scan
        faces = '' 

        # is this the first frame? will be set to False after the first frame 
        first_frame = True

        #how many rows were scanned in the first frame
        rows_scaned = 0

        # if the color of the detected pixle difrenter than detect threshold we will move it far away from the modle making it easy to delete
        detect_threshold = 60
        # if the pixle is with in stop_looking_threshold then stop lookin for another one... this stops the scanner from detectign more than 
        #one line.
        stop_looking_threshold = 60
        first_row = True

        current_row = 0

        vert_index = 0

        do_image_map = False  

        # how was the object scanned .. options may be 'dolly' 'spin' 'pan' 'laser_pan'
        scan_method = 'spin'

        # variable to spin data with
        frames_per_revolution = 100
        # 
        angle_step = math.pi * 2 / frames_per_revolution
        angle = 0



        #user questions 
        answer = raw_input('live real time capture? y or n')
        if answer == 'n':
            real_time = False


        answer = raw_input('make image map or scan? i or s')
        if answer == 'i':
            do_image_map = True
            path = 'scanner/image_map_frames/'
        else :
            path = 'scanner/frames/'



        file = open('scanner/output.obj', 'w')
        file.write('o PeachyScan\n')
        
        if not real_time:
            
            
            # getting the list of files
            files = os.listdir(path);
            print(len(files), 'files detected in ', path)


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
            


       









#######################################################################3

        self.choice = (45.0, 86.0, 19.0)  #45.0, 86.0, 19.0
        self.choice = (230, 230, 230)
        if self.choice != (0,0,0):
            self.begin = True
        while True:   #   0000000000000000000000000000000000000000000000000000000000000
            if do_image_map:
                break
            #


##########################################################33
            # i and pan grow each time we have scaned an entire frame

            #print(i)
            #time.sleep(1)
            # if we are doing a real time scan then capture frames from the web cam
            if real_time: 
                img = cv.QueryFrame(capture)
            

                cv.SaveImage('scanner/test2.jpg', img)
                self.mat = cv.LoadImageM('scanner/test2.jpg', cv.CV_LOAD_IMAGE_COLOR)
                #self.mat = mat
            #mat = cv.LoadImageM('scanner/edit.jpg', cv.CV_LOAD_IMAGE_COLOR)
            
            # load frames from disk:
            if not real_time:
                if i > len(files)-3 : 
                    i = 0
                    exit_scanner()
                    break
                file_name = '' + str(1001 + i ) + '.jpg'

                self.mat = cv.LoadImageM(path+file_name, cv.CV_LOAD_IMAGE_COLOR)
                #mat = cv.LoadImageM(path+files[i], cv.CV_LOAD_IMAGE_COLOR)

            
                

            #os.system('cls' if os.name=='nt' else 'clear')

            #print('y resolution of ', self.mat.rows/skip_y )
            #time.sleep(3)
            B,G,R = self.choice
            first_row = True
            current_row = 0
            if self.begin == True:
                i += 1 
                print('prosesing frame ', i )
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

                        if closest_yet < detect_threshold:
                            self.mat[row_number-skip_y, bright_position-skip_y] = (0,250,0)
                            if scan_method == 'dolly' or scan_method == 'pan' or scan_method == 'laser_pan':
                                file.write('v ' + str(row_number * factor_y) + ' ' + str(bright_position * factor_x * math.cos(angle)) + ' ' + str(pan + (random.random()*.1))  +  '\n')
                            if scan_method == 'spin':
                                file.write('v ' + str((bright_position * factor_x ) * math.cos(angle) )  + ' ' + str(row_number * factor_z)+ ' ' + str((bright_position * factor_y ) * math.sin(angle) )  +  '\n')
                                #print('spining')
                            do_face = True
                            
                        else:
                            self.mat[row_number-skip_y, bright_position-skip_y] = (0,0,250)
                            if scan_method == 'dolly' or scan_method == 'pan' or scan_method == 'laser_pan':
                                file.write('v ' + str(row_number * factor_y ) + ' ' + str(bright_position * factor_x + 20) + ' ' + str(pan + (random.random()*.1))  +  '\n')
                            if scan_method == 'spin':
                                file.write('v ' + str((bright_position * factor_x ) * math.cos(angle) )  + ' ' + str(row_number * factor_z + 20 )+ ' ' + str((bright_position * factor_y ) * math.sin(angle) )  +  '\n')
                            
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
            


#######################################################################3








            #print(self.choice)
            c = cv.WaitKey(10)
            if c == 27:
                exit_scanner()
                break


        if not real_time and do_image_map:
            self.begin = False
            print('making image map')
            time.sleep(2)
            i = 0
            # do every frame_skip frames 
            frame_skip = 1
            j = 0
            colum_capture = []
            
            capture_width = 1
            path = 'scanner/image_map_frames/'
            files = os.listdir(path);
            print(int(len(files)/frame_skip), 'files detected in ', path)
            while True:

                image_map = cv.LoadImageM(path+'image_map.jpg', cv.CV_LOAD_IMAGE_COLOR)
                cv.ShowImage("camera", image_map)
                c = cv.WaitKey(10)
                if c == 27 or self.begin:
                    capture_position = self.position
                    break

            while True:
                i += 1
                if i % 10 == 0:
                    cv.SaveImage('scanner/image_map.jpg', image_map)
                j += frame_skip
                if i > int((len(files)-5)/ frame_skip) : 
                    i = 0
                    #break
                file_name = '' + str(1000 + j ) + '.jpg'

                print(path+file_name)
                self.mat = cv.LoadImageM(path+file_name, cv.CV_LOAD_IMAGE_COLOR)

                # load a vertical line of pixles rgb color values into variable colum_capture the pix on ether side green 

                for x in range(capture_width):
                    colum_capture = []
                    for row in range(self.mat.rows):
                        colum_capture.append( self.mat[row, capture_position + x])
                        #self.mat[row, capture_position+x+int(capture_width/2)] = (0,200,0)
                        #self.mat[row, capture_position-x-int(capture_width/2)] = (0,200,0)

                    for row in range(image_map.rows):
                        image_map[row,i*capture_width + x] = colum_capture[row]







                cv.ShowImage("camera", image_map)
                time.sleep(.2)
                if i % 3 == 0:
                    for row in range(self.mat.rows):
                        self.mat[row, capture_position+x+int(capture_width/2)] = (0,200,0)
                        self.mat[row, capture_position-x-int(capture_width/2)] = (0,200,0)
                    cv.ShowImage("ColorPicker", self.mat)
                    time.sleep(.2)
                

                


                



                print(self.choice)
                c = cv.WaitKey(10)
                if c == 27:
                    exit_scanner()
                    cv.SaveImage('scanner/image_map.jpg', image_map)
                    break





#//colorPicker

if __name__=="__main__":
    demo = ColorPicker()
    demo.run()
