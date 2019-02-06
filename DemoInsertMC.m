close all;
clear all;
clc;

%% DemoInsertMC

% This code is a demo illustrating the usage of InsertMC

load('Patient.mat') %Loads the raw mammogram

load('res.mat')     %Loads the density and breast masks
% NOTE: The density and breast masks were used to facilitate the automated
% insertion of MCs. The masks were obtained using the open-souce algorithm
% LIBRA, available for download at: 
% https://www.med.upenn.edu/sbia/libra.html

load('MaskMC.mat')  %Loads the set of 11 segmented MC clusters

% Parameters
Contrast=0.12;  %Contrast of the MCs, e.g., 0.07 means 7% contrast
Angle=45;        %Angle in degrees
MCnum=5;        %Select one of the 11 segmented MC clusters

% Mask erosion to avoid regions too close to the skin, chest-wall and
% pectoral muscle
res.BreastMask(:,end)=0; res.BreastMask(:,1)=0;
ErodedMask=imerode(res.BreastMask, strel('disk',floor(size(MaskMC,1)/2)));

% Removes isolated pixels
CleanDensity=bwmorph(res.DenseMask,'clean');

% Map of possible positions
PossiblePoints=ErodedMask.*CleanDensity;

%Ramdomly selects one of the possible points
[I J]=find(PossiblePoints==1);
Poss=[I J];
Point = datasample(1:size(Poss,1),1,'Replace',false);
Coordinates=Poss(Point,:);

% Insert the MC Cluster
[Inserted]=InsertMC(Patient,MaskMC(:,:,MCnum),Coordinates(1),Coordinates(2),Contrast,Angle);

%% Plots
figure(), subplot(1,3,1),
imshow(1-mat2gray(Patient(Coordinates(1)-ceil(size(MaskMC,1)/2):Coordinates(1)+floor(size(MaskMC,1)/2)-1,Coordinates(2)-ceil(size(MaskMC,1)/2):Coordinates(2)+floor(size(MaskMC,1)/2)-1)),[-0.1 1.1]);
title('Raw Data');
subplot(1,3,2),
imshow(MaskMC(:,:,MCnum),[]);
title('MC Mask');
subplot(1,3,3),
imshow(1-mat2gray(Inserted(Coordinates(1)-ceil(size(MaskMC,1)/2):Coordinates(1)+floor(size(MaskMC,1)/2)-1,Coordinates(2)-ceil(size(MaskMC,1)/2):Coordinates(2)+floor(size(MaskMC,1)/2)-1)),[-0.1 1.1]);
title('Inserted');