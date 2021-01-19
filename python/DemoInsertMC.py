#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 13:48:56 2020

@author: Lucas Borges, coded by Rodrigo
"""

#%%

import numpy as np
import cv2 
import matplotlib.pyplot as plt
from scipy.io import loadmat

#%%
def insertMC(dcmData, maskMC, coords, contrast, angle):
    
    # Copy to a new np array
    inserted = np.empty(dcmData.shape, dtype=dcmData.dtype)
    inserted[:] = dcmData
    
    # MC rotation
    image_center = tuple(np.array(maskMC.shape) // 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    maskRot = cv2.warpAffine(maskMC, rot_mat, maskMC.shape, flags=cv2.INTER_CUBIC)
    
    # Normalize and aply contrast  
    maskRot = cv2.normalize(maskRot, None, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
    maskRot[maskRot<0] = 0
    maskRot = 1 - (maskRot * contrast)
    
    # Image coords to insert the MC
    lowCoord = np.array(coords) - np.array(image_center)
    upCoord = np.array(coords) + np.array(image_center)
    
    # Insert MC
    inserted[lowCoord[0]:upCoord[0],lowCoord[1]:upCoord[1]] *= maskRot 
    
    return inserted



#%% This code is a demo illustrating the usage of InsertMC

#Loads the raw mammogram
dcmData = loadmat('Patient.mat')['Patient']

resLoad = loadmat('res.mat')['res']     # Loads the density and breast masks
res = dict()
for dtype, value in zip(resLoad[0][0].dtype.names, resLoad[0][0]):
    res[dtype] = value
del resLoad

# NOTE: The density and breast masks were used to facilitate the automated
# insertion of MCs. The masks were obtained using the open-souce algorithm
# LIBRA, available for download at: 
# https://www.med.upenn.edu/sbia/libra.html

# Loads the set of 11 segmented MC clusters
maskMC = loadmat('MaskMC.mat')['MaskMC'] 

# Parameters
contrast = 0.12                                 # Contrast of the MCs, e.g., 0.07 means 7# contrast
angle = 45                                      # Angle in degrees
mcNum = np.random.randint(0,maskMC.shape[2])    # Select one of the 11 segmented MC clusters

# Mask erosion to avoid regions too close to the skin, chest-wall and
# pectoral muscle
res['BreastMask'][:,-1] = 0
res['BreastMask'][:,0] = 0

element = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(maskMC.shape[0]//2,maskMC.shape[0]//2))
erodedMask = cv2.erode(res['BreastMask'], element)


# Removes isolated pixels
element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
mask = cv2.morphologyEx(res['DenseMask'], cv2.MORPH_CLOSE, element1)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, element2)

cleanDensity = res['DenseMask'] * mask


# Map of possible positions
possiblePoints = erodedMask * cleanDensity


# Ramdomly selects one of the possible points
i,j = np.where(possiblePoints==1)
randInt = np.random.randint(0,i.shape[0])
coords = (i[randInt],j[randInt])

# Insert the MC Cluster
inserted = insertMC(dcmData, maskMC[:,:,mcNum], coords, contrast, angle)




#%% Plots


image_center = tuple(np.array(maskMC[:,:,mcNum].shape) // 2)
# Image coords to insert the MC
lowCoord = np.array(coords) - np.array(image_center)
upCoord = np.array(coords) + np.array(image_center)


plt.figure()

plt.subplot(1,3,1) 
plt.imshow(65535 - dcmData[lowCoord[0]:upCoord[0],lowCoord[1]:upCoord[1]], 'gray')
plt.title('Raw Data')

plt.subplot(1,3,2) 
plt.imshow(maskMC[:,:,mcNum], 'gray')
plt.title('MC Mask')

plt.subplot(1,3,3) 
plt.imshow(65535 - inserted[lowCoord[0]:upCoord[0],lowCoord[1]:upCoord[1]], 'gray')
plt.title('Inserted')

