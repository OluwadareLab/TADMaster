function saveHiC(fname, mat, res, idx_cent1, idx_cent2)
%save a Hi-C matrix to a tab seperated
%   fname: a string of the text file name where the data will be saved
%   mat: the matrix with the Hi-C data inside
%   res: the resolution of the matrix in base pairs. Used for making the
%      row/column labels.
%   idx_cent1 - binary vector of centromere locations, used for making
%      row/column labels. The total number of non-0 elements should be the
%      number of columns in mat.
%   idx_cent2 - binary vector of centromere locations for rows of mat. Only
%      needed for inter-chromosomal matrices with different numbers of rows
%      and columns.

if nargin < 5
    idx_cent2 = idx_cent1;
end

% make header
bnds = [0:length(idx_cent1)-1; 1:length(idx_cent1)]*res;
bnds2 = bnds(:,~idx_cent1);
head1 = sprintf('%.0f-%.0f, ' , bnds2);

bnds = [0:length(idx_cent2)-1; 1:length(idx_cent2)]*res;
bnds2 = bnds(:,~idx_cent2);
bnds3 = num2cell(bnds2,1);
head2 = cellfun(@(x) [num2str(x(1)),'-',num2str(x(2))], bnds3,...
    'UniformOutput',false);

prntMat = cell(size(mat,1), size(mat,2)+1);
prntMat(:,1) = head2;
prntMat(:,2:end) = num2cell(mat);

f1 = fopen(fname,'w');
fprintf(f1,head1);

formatStr = repmat('%d, ',1,length(mat));
for r = 1:length(mat)
    fprintf(f1,['%s, ',formatStr,'\n'], prntMat{r,:});
end
fclose(f1);
end

