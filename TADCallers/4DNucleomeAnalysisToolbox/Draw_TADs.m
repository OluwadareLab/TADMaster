function  Draw_TADs(H,posn,color_range)
% Draw TADs region on the Hi-C matrix H
% H: Input HiC matrix
% posn: list of boundary locations of TADs
% color_range: range of display, vector of 2 values
%
% Implemented by
% Jie Chen
% University of Michigan, Ann Arbor
% dr.jie.chen@ieee.org

if nargin < 3
    color_range=[min(H(:)),max(H(:))];
end


figure,imagesc(H,color_range), colormap hot, colormap(flipud(colormap));
hold on
if posn(end) ~= size(H,1)
    posn(end+1) = size(H,1);
end

LT = '-';
LW = 3;
for i = 2 : length(posn)
    plot([posn(i-1),posn(i)]-0.5,[posn(i-1),posn(i-1)]-0.5,LT,'linewidth',LW,'Color','b')
    plot([posn(i-1),posn(i)]-0.5,[posn(i),posn(i)]-0.5,LT,'linewidth',LW,'Color','b')
    plot([posn(i-1),posn(i-1)]-0.5,[posn(i-1),posn(i)]-0.5,LT,'linewidth',LW,'Color','b')
    plot([posn(i),posn(i)]-0.5,[posn(i-1),posn(i)]-0.5,LT,'linewidth',LW,'Color','b')     

end
set(gcf,'color',[1,1,1])
set(gcf, 'Position', [40 400 500 480])
set(gcf, 'PaperUnits', 'centimeters');
set(gcf, 'PaperSize', [20 20]);
set(gcf, 'PaperPosition', [1 1 18 18]);

set(gca,'Xtick',[])
set(gca,'Ytick',[])
end