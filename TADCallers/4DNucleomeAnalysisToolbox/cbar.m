function cbar(x,y,s,labels)
%colorbar - inserts a colorbar into a figure. Makes it much smaller than
%the default matlab positioning.
%
% Inputs:
%   (x,y,s) - which subplot needs a colorbar (entries to subplot function),
%       make it 1,1,1 if not using subplots.
%    labels - what marks on the colorbar should be labeled. For example,
%       [-1,0,1] works well for many correlation matrices.
%
% Output: a colorbar on the current figure at the indicated subplot
%
% Positioning is included for 1x1, 1x2, 1x3, and 2x2 subplots. Additional
%   options can be added by adding to locations. The values in each vector
%   are: left, bottom, width, height in normalized units in which the lower
%   left corner of the figure is (0,0) and the top right is (1,1).
%
% Laura Seaman, November 2016
% University of Michigan, Ann Arbor
% laseaman@umich.edu


if nargin < 4
    labels = '';
end

locations = cell(3,3);
locations{1,1} = [0.860 0.755 0.016 0.17];
locations{1,2} = [0.470 0.725 0.008 0.20;...
        0.910 0.725 0.008 0.20];
locations{1,3} = [0.347 0.725 0.008 0.20;...
        0.627 0.725 0.008 0.20;...
        0.910 0.725 0.008 0.20];
locations{2,2} = [0.470 0.855 0.008 0.07;...
         0.910 0.855 0.008 0.07;...
         0.470 0.381 0.008 0.07;...
         0.910 0.381 0.008 0.07];

if ~strcmp(labels,'')
    colbar = colorbar('Ticks',labels);
end

ax = gca;
axpos = ax.Position;
colbar.Position = locations{x,y}(s,:);
ax.Position = axpos;

end

