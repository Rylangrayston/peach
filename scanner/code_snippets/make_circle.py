'''
This script will create make_circle.obj  file 
the .obj will contain an object named circle_-_  and 
that object will contain a 600 vertecies in a circle.

understanding this code snippit will help you understand how 
we spin the data colected durng a scan using the spin method.

'''



import math
print ('math.pi: ', math.pi, '  1 rad: ', math.pi * 2)




z = 0
frames = 600
step = math.pi * 2 / frames
angle = 0

file = open('make_circle.obj', 'w')  
file.write('o circle_-_ \n')
for frame in range(0,frames):
	print ('frame:', frame)
	angle += step
	# .obj vetrex format = 'v' x z y 
	vert_string = 'v ' + str( 1 * math.sin(angle)) + ' ' + str(z) + ' ' + str(1 * math.cos(angle)) + '\n'
 	print(vert_string)
	file.write(vert_string)
file.close()



