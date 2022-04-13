
function [newhicData,totbias_final]=ICE(hicData,nDiag_remove,max_iter)
% normalization ICE: Dekker-Mirney method, originally described in: Iterative 
% Correction of Hi-C Data Reveals Hallmarks of Chromosome Organization by 
% Imakaev et al, Nat Methods Oct 2012
%
% The method assumes that the sum of all columns should be equal,
% iteratively corrects until the change in less than the threshold or the
% number of max iterations is reached.
%
% Inputs:
%   hicData - raw Hi-C matrix to be normalized.
%   nDIag_remove - the number of diagonals to be removed, default = 1
%   max_iter - the maximum number of iterations to be used, default = 100
% Outputs: 
%   newhicData - HiC matrix after normalized.
%   totbias_final - final bias vector. this is the vector used for
%   correction each iteration.
% 
if(nargin<2)
    nDiag_remove=1;
end
if(nargin<3)
    max_iter=100;
end

% preprocessing

newhicData=hicData;
n=size(newhicData,1);
% remove diagonal (or other, depending on nDiag input)
for i=-(nDiag_remove-1):(nDiag_remove-1)
    d=diag(diag(hicData,i),i);
    hicData=hicData-d;
end

% apply ICE
flag=true;
count=0;
totbias=ones(1,length(hicData));

while flag
    bias=sum(hicData)/mean(sum(hicData));   
    hicData=diag(1./bias)*hicData*diag(1./bias);
    
    oldtot=totbias;
    totbias=totbias.*bias;
    
    count=count+1;
    if(count>max_iter || var(bias)<10^-10)
        flag=false;
    end
end

totbias_final=totbias;
newhicData=diag(1./totbias_final)*newhicData*diag(1./totbias_final);

end 



