function [NX,locs] = BlockToepNorm(X,thr,filtMax, plt, brek)
% normalizes Hi-C matrices, accounts for copy number changes by subdividing
% the matrix in regions of constant copy number as measured by the total
% number of reads in each bin.
%
% Inputs:
%   X       square matrix to be normalized
%   thr     threshold for sums to qualify as a big jump
%   filtMax maximum frequency in band pass filter. Generally 0.01 for 100kb
%           	and 0.1 for 1 Mb resolution Hi-C matrices
%   plt     1 to make a plot for help identifying appropriate value of thr.
%               0 (default) to not make the plot
%   brek    list of breakpoints to be used, for manual selection instead of
%               calculation from the Hi-C matrix using thr and filtMax.
%               default is to not use this, but instead use thr and filtMax
%               which become irrivelent if this is provided as anything
%               other than NaN.
% Outputs:
%   NX    the matrix after normalization
%   locs  the locations selected as changes in copy number and used as
%           boundaries for the submatrices for normalization.
% 
% Breakpoints are put at the largest change in the raw counts near points in
% which the filtered counts change by more than thr. Breakpoints cannot be
% within 1/8th of a chromsome from either end of the chromosome or 1/16th of 
% a chromosome of each other. 
% 
% Laura Seaman, July 2015
% University of Michigan, Ann Arbor
% laseaman@umich.edu

if nargin < 5
    brek = NaN;
end
if nargin < 4
    plt = 0;
end

if isnan(brek)
    bnd = round(length(X)/8);
    bnd2 = round(length(X)/16);
    
    %calculate and smooth sums
    sums = squeeze(sum(X,1));
    [b,a] = butter(2,[1e-6,filtMax],'bandpass');
    sums_bpf = filter(b,a,sums);
    dif_bpf = abs(diff(sums_bpf));
    dif_sums = abs(diff(smooth(sums,5)));
    valA = findpeaks(dif_bpf);
    val = valA(valA > thr);
    [~,idx_pk,~] = intersect(dif_bpf,val);
    idx_pk = sort(idx_pk);
    
    if plt == 1
        figure, subplot(121)
        plot(sums)
        hold on, plot(sums_bpf)
        plot(idx_pk,sums_bpf(idx_pk),'o')
        title('number of reads per bin')
        xlabel('bin'), ylabel('total number of reads')
        legend('# reads / bin','smoothed # reads / bin','loc of large change')
        
        subplot(122), hold on
        plot(dif_bpf)
        plot([0,length(X)],[thr,thr])
        title('smoothed change in number of reads')
        xlabel('bin'), ylabel('smoothed change')
        legend('\Delta smoothed # reads / bin','threhold for breakpoint')
    end
    
    locs = 1;
    for t = 1:length(idx_pk)
        l = idx_pk(t);
        if l <=bnd || l >= (length(X)-bnd)
            continue
        elseif l-locs(end) < bnd
            dif_max = max([dif_sums( max(1,l-bnd2): min(l+bnd2,length(X)) ); dif_sums(locs(end))] );
            t=find(dif_sums == dif_max);
            locs(end) = t(1);
            
            % check and see if min/max in dif_sums are necessary
        else
            dif_max = max(dif_sums( max(1,l-bnd2): min(l+bnd2,length(X)) ) );
            locs = [locs,find(dif_sums == dif_max,1)];
        end
    end
    locs = [locs,length(X)+1];
else
    locs = brek;
end

NX = NaN(size(X));
for sec = 1:length(locs)-1
    reg = locs(sec):locs(sec+1)-1	;
    sub = X(reg,reg);
    NX(reg,reg) = ToepNorm(sub);
    
    for sec2 = sec+1:length(locs)-1
        reg2 = locs(sec2):locs(sec2+1)-1;
        sub = X(reg,reg2);
        HiC_sub_norm = ToepNorm(sub);
        
        NX(reg,reg2) = HiC_sub_norm;
        NX(reg2,reg) = HiC_sub_norm';
    end
end

end
