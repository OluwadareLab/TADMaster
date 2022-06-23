function saveTADs(fname,TADs,res,idx_cent)
%save tad boundaries to a comma seperated text file.
%   fname: a string of the csv file name where the data will be saved
%   TAD: the matrix with the TAD data inside, two columns with the start
%      and end of each TAD.
%   res: the resolution of the matrix in base pairs. Used for converting
%      TAD bounds to bp coordinates
%   idx_cent - binary vector of centromere locations. Used for converting
%      TAD bounds to bp coordinates

% column labels
columnLbls = {'start','end'};
% define TAD bounds
TADs_wCent = AddCent(TADs,idx_cent)*res;
TADs_prnt1 = [TADs_wCent(1:end-1), TADs_wCent(2:end)];
TADs_prnt2 = num2cell(TADs_prnt1 ,2);
TADs_prnt3 = cellfun(@(x) [num2str(x(1)),'-',num2str(x(2))], TADs_prnt2,...
    'UniformOutput',false);

f1 = fopen(fname,'w');
for r = 1:length(TADs_prnt3)
    fprintf(f1,'%s \n', TADs_prnt3{r,:});
end
fclose(f1);

end

