function [Inserted]=InsertMC(Original,MCMask,x,y,Contrast,Angle)

%% InsertMC 
% This is an agorithm to insert microcalcificaition clusters into Digital
% Mammograms. The details are described in the article:

%[1] 'A 2-AFC study to validate artificially inserted microcalcification 
% clusters in digital mammography'SPIE Medical Imaging, 2019.

% This package also includes a set of 11 MC clusters segmented from
% clinical cases acquired using a Hologic Selenia Dimensions system.

% Input:
%           Original - Raw digital mammogram
%           MCMask - Mask with the microcalcification clusters
%           x,y - Coordinates for the insertion (center of MCMask)
%           Contrast - [0,1] Contrast of the MC
%           Angle - [0,360] Changes the orientation of the cluster

MaskRot=mat2gray(imrotate(MCMask,Angle,'bicubic'));
MaskRot(MaskRot~=0)=MaskRot(MaskRot~=0)*(Contrast);
MaskRot=abs(MaskRot-1);
Inserted=Original;
Inserted(x-ceil(size(MaskRot,1)/2):x+floor(size(MaskRot,1)/2)-1,y-ceil(size(MaskRot,1)/2):y+floor(size(MaskRot,1)/2)-1)=Original(x-ceil(size(MaskRot,1)/2):x+floor(size(MaskRot,1)/2)-1,y-ceil(size(MaskRot,1)/2):y+floor(size(MaskRot,1)/2)-1).*MaskRot;
