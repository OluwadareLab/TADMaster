function [mat,chr] = HiC_load_mat(fname, nChr,chrFormat)
%load Hi-C data from txt file
%
% Input:
%   fname: path/filename for Hi-C matrix file. first row and column are
%      chrN-START, where N in the chromosome number, and START is the integer
%      start location for the bin.
%   nChr:  set to 1 if you don't want the chr vector
%   chrFormat: 0 (default) the locations are listed like: chr2-1000000,
%   when 1 the chr is not included like: 2-1000000
% Output:
%   chr - start bin for each chromosome 
%   mat - data matrix of counts
%
% Laura Seaman, May 2015
% Contact: laseaman@umich.edu

if nargin < 3
    if nargin < 2
        nChr = 0;
    end
    chrFormat = 0;
end

mat = importdata(fname);

% if nChr ~= 1
%     chr_bin = T * textdata(1,3:length(T.textdata)-1)';
%     chr = ones(1,23); chr(23) = length(mat) + 1;
%     c = 1;
%     for t = 1:length(chr_bin)
%         %t, chr_bin{t,:}
%         splt1 = strsplit(strtrim(chr_bin{t,:}),'-');
%         if chrFormat == 0
%             splt2 = strsplit(strtrim(splt1{1}),'chr');
%             chrl = str2double(splt2{2});
%         elseif chrFormat == 1
%             chrl = str2double(splt1{1});
%         end
%         if chrl > c
%             chr(c+1) = t; c = c+1;
%         end
%     end
% else
%     chr = [];
% end

end

