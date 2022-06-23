function  h = HiC_plot(mat, t, OneAxis, nDiag, noFig, cmap, noLog)
% Plot HiC matrix
%
% Input:
%    mat     -   HiC matrix
%    t       -   graph title
%    OneAxis -   set to 1 for a standardized colorbar (not shown), 0 to show 
%                colorbar on plot, otherwise, individual colorbar not
%                shown (default=2).
%    nDiag   -   0 - dont remove diagonal, 1 - remove diagonal (default), 3 - remove
%                tridiagonal
%    noFig   -   0- no new figure (default), 1 - new figures
%    cmap    -   0 red/white color map (default), 1 - flipped hot
%    noLog   -   0 - do not put Hi-C matrix on log Scale, 1 (default) use
%                log transformation.
%
% all inputs are optional except mat. The default command is equivalent to:
% h = HiC_plot(mat,'', 2, 1, 0, 0)
%
% Laura Seaman, May 2015
% Contact: laseaman@umich.edu

if nargin < 7
    noLog = 1;
if nargin < 6
    cmap = 0;
    if nargin <5
        noFig = 0;
        h = 0;
        if nargin < 4
            nDiag = 1;
            if nargin < 3
                OneAxis = 2;
                if nargin < 2
                    t = '';
                end
            end
        end
    end
end
end

adj = .5;

if nDiag == 0
    matplot = mat;
elseif nDiag == 3
    triDiag = diag(diag(mat)) + diag(diag(mat,1),1) + diag(diag(mat,-1),-1);
    matplot = mat - triDiag;
else
    matplot = mat - diag(diag(mat));
end

if noLog == 1
    matplot = log2(matplot+adj);
end

if noFig == 1
    h = figure;
end
imagesc(matplot)
title(t); 
if cmap == 0
    cmap = [1,1,1; 1,.98,.98; 1,.96,.96; 1,.93,.93; 1,.9,.9; 1,.86,.86; 1,.8,.8;1,.6,.6; ...
    1,.4,.4; 1,.2,.2; 1,.1,.1; 1,.05,.05; 1,.02,.02; 1,0,0 ];
    colormap(cmap) 
elseif cmap == 1
    %colormap(flipud(hot))
    colormap(hot)
end
if OneAxis == 0
    colorbar
elseif OneAxis == 1
    caxis([0 9])
elseif length(OneAxis) ==2
    caxis(OneAxis)
end

end

