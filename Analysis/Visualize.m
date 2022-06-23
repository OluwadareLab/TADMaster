%function [ output_args ] = Visualize( Data, boundary, method, Resolution, colorvalue )
%==============================================================
% This function allows for the visualization of data in Heat Map
Data = log(load(Data)); % Perform a log to see data distribuiton
%disp(Data);
boundary = load(boundary)
%===============================================================
%Choose Color Map

if (colorvalue==1)
    color='hot';
elseif (colorvalue==2)
    color = 'hsv';
elseif (colorvalue==3)
    color = 'cool' ;
elseif (colorvalue==4)
    color = 'copper';
elseif (colorvalue==5)
    color = 'spring'; 
else
    color = 'jet';
end
%================================================================
colormap(color);
imagesc(Data);
colorbar;
xlabel_text = sprintf('Genomic bin (resolution: %s)',Resolution);
ylabel_text = sprintf('Genomic bin (resolution: %s)',Resolution);
xlabel(xlabel_text);
ylabel(ylabel_text);
printf("test")
for i = 1:length(boundary(:,1))
     hold on;
     Start = boundary(i,1);
     Last = boundary(i,2);
     for j = Start:Last
             plot(Start,j,'b.','MarkerSize',2);
             plot(j,Start,'b.','MarkerSize',2);
             plot(j,Last,'b.','MarkerSize',2);
             plot(Last,j,'b.','MarkerSize',2);
     end        
end
printf("test")
title_text = sprintf('TADs for %s Implementation',method);
title(title_text)

%================================================================
%Save plot to directory
plotname = strcat(output,method,'_plot.png');
saveas(gcf,plotname);
%================================================================

%end

