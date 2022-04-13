HiC_wCent = load(input);
[HiC,~,idx_cent] = HiC_remove_cent(HiC_wCent,0);
matname=strcat(name,'.matrix');
dlmwrite(matname,HiC);
indexname= strcat(name,'.index');
dlmwrite(indexname,idx_cent);