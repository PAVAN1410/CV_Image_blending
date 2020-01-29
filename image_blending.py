import cv2
import numpy as np
img=cv2.imread(r'c:\Users\apple.jpg')
img=cv2.resize(img,(512,512))
img1=cv2.imread(r'c:\Users\orange.jpg')
img1=cv2.resize(img1,(512,512))
#cv2.imshow('img',ap)
#cv2.imshow('im',ora)
ap_ora=np.hstack((img[:,:256],img1[:,256:]))
cv2.imshow('direct_addition',ap_ora)

#gaussian pyramid1

layer=img.copy()
gp=[layer]
for i in range(6):
    layer=cv2.pyrDown(layer)
    gp.append(layer)


#laplacian pyramid 1


layer=gp[5]
#cv2.imshow('upper level in gaussian pyramid',layer)
lap_pyr=[layer]
for i in range(5,0,-1):
    size=(gp[i-1].shape[1],gp[i-1].shape[0])
    gaussian_extend=cv2.pyrUp(gp[i],dstsize=size)
    laplacian=cv2.subtract(gp[i-1],gaussian_extend)
    lap_pyr.append(laplacian)
        
#gaussian pyramid2

layer=img1.copy()
gp1=[layer]
for i in range(6):
    layer=cv2.pyrDown(layer)
    gp1.append(layer)


#laplacian pyramid 1


layer=gp1[5]
#cv2.imshow('upper level in gaussian pyramid1',layer)
lap_pyr1=[layer]
for i in range(5,0,-1):
    
    size=(gp1[i-1].shape[1],gp1[i-1].shape[0])
    gaussian_extend=cv2.pyrUp(gp1[i],dstsize=size)
    laplacian=cv2.subtract(gp1[i-1],gaussian_extend)
    lap_pyr1.append(laplacian)


#laplacian pyramid of app_ora
lap_pyr12=[]  
n=0
for img_lap,img_lap1 in zip(lap_pyr,lap_pyr1):
    cols,rows,ch=img_lap.shape    
    laplacian=np.hstack((img_lap[:,0:int(cols/2)],img_lap1[:,int(cols/2):]))
    n+=1
    #cv2.imshow(str(n),laplacian)
    lap_pyr12.append(laplacian)



reconstruct_image=lap_pyr12[0]


for i in range(1,6):
    size=(lap_pyr12[i].shape[1],lap_pyr12[i].shape[0])
    reconstruct_image=cv2.pyrUp(reconstruct_image,dstsize=size)
    reconstruct_image=cv2.add(reconstruct_image,lap_pyr12[i])
cv2.imshow('after blending',reconstruct_image)
    
cv2.waitKey(0)
cv2.destroyAllWindows()
