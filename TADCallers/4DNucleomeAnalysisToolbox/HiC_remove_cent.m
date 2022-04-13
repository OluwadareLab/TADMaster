function [HiCm, chrm, index_all] = HiC_remove_cent(HiC, chr, thr)
% Remove columns and rows with column sums less than thr
% Input: 
%    HiC    -   HiC matrix. Three deminsional matrices can be used.
%    chr    -   Starting points of the chromosomes. set to 0 to not calculate
%    thr    -   the minimum total number of reads needed for a column to be
%               included.
% Output:
%    HiCm   -   HiC matrix with removed columns and rows.
%    chrm   -   New starting points of the chormosomes.
%    index_all  -  Indices of the removed columns and rows.
%
% all columns with a 0 diagonal are removed, the minimum is used along
% the third dimension to make sure all necessary rows are removed when
% multiple samples are included.
% 
% Jie Chen, July 2014
% Contact: Dr.Jie.Chen@ieee.org
% Updated: Laura Seaman, January 2017
% Contact: laseaman@umich.edu


if nargin < 3
    %Only remove centromere
    thr = 3;
    if nargin < 2
        chr = 0;
    end
end


HiCm = HiC;

% If there are multiple layers, use the minimum value
HiCmean = min(HiC,[],3);

% Chromosome number
Num_chr = length(chr);

% Remove columns and rows
sumHiC = sum(HiCmean);
index_all = (sumHiC<thr);
index_all(diag(HiCmean)==0) = 1;

HiCm(index_all,:,:)=[];
HiCm(:,index_all,:)=[];

% Generate new chromosome indices
if length(chr) > 1
    chrm = chr;
    for n = 1 : Num_chr
        %Data reads and low sum columns/rows removal for computing chrm
        Z = sumHiC(chr(n):chr(n+1)-1);
        index = find(Z<=thr);
        chrm(n+1:end)=chrm(n+1:end)-length(index);
    end
else
    chrm = chr;
end
     
end

%cm(1)=[];