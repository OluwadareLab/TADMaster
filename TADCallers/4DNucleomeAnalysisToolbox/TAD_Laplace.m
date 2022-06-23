function [TAD_boundaries,Hn,FV_raw] = TAD_Laplace(H0,sig0, ms0, MOD, MERG,Lg)
% TADs extraction via Laplacian segmentation
% --- inputs ---
% H:     Input HiC matrix
% sig0:  Algebraic connectivity threshold
% ms0:   Threshold of region size: we donot split a region smaller than ms0
% MOD:   Algorithm mode
%        1 - 1st step performed on Toeplitz normalized matrix
%        2 - 1st step performed on usual matrix
%        other: Block normalization (list of breakpoints)
% MERG:  Merge single bin domains into its neighbors
%        0 - Donot merge
%        1 - Merge
% Lg:    Use thresholded log scale or not
%        0 - not log scale
%        1 - ln scale, thresholded between -3 and 6
% --- output ---
% TAD_boundaries - vector of boundaries
%
% Reference:
% Hierachicial identification of topological domain via graph Laplacian
% J. Chen, A. O. Hero, I. Rajapakse
%
% Implemented by: Jie Chen
% dr.jie.chen@ieee.org
% Edited by: Laura Seaman
% laseaman@umich.edu

%% Default parameters
if nargin < 6
    Lg = 0;
if nargin < 5
    MERG = 0;
    if nargin < 4
        MOD = 1;
        if nargin < 3
            ms0 =3;
            if nargin < 2
                sig0 = 0.8;
            end
        end
    end
end
end


%% Remove unmappable region if they are included
idx0 = sum(H0)==0;
H0(:,idx0)=[];
H0(idx0,:)=[];

if Lg == 1
    H = min(max(log(H0),-3),6);
    H = H - min(H(:));
else
    H = max(H0,0.0001);
end

dH = diag(diag(H));
H = H - dH;       % Remove the diagonal  
%H = H+H' / 2;
L = size(H0,1);


%% Splitting on Toeplitz normalized matrix
if MOD == 1
    % First split is performed on Toeplitz normalized matrix
    Hn=ToepNorm(H0);                           % Toeplitz normalization
    [FV,~]=Fdvectors(Hn,0);                % Fiedler vector
    Pos = [1;find(sign(FV(2:end))-sign(FV(1:end-1))~=0)+1;L];    % Positions of starting domain
elseif MOD == 2
    % Splitting directly on the data matrix
    Pos = [1, L];
    Hn = H;
elseif length(MOD) > 1
    for b = 1:length(MOD), MOD(b) = MOD(b) - sum(idx0(1:MOD(b)-1)); end
    Hn = BlockToepNorm(H,0,1e5, 0, MOD);
    % for i = 1:length(Hn), for j = i+1:length(Hn), if Hn(i,j) ~= Hn(j,i), [i,j], end, end, end
    [FV,~]=Fdvectors(Hn,0);                % Fiedler vector
    Pos = [1;find(sign(FV(2:end))-sign(FV(1:end-1))~=0)+1;L];    % Positions of starting domain
elseif MOD >= 20
    Hn = BlockToepNorm(H,MOD,1e5, 0);
    [FV,~]=Fdvectors(Hn,0);                % Fiedler vector
    Pos = [1;find(sign(FV(2:end))-sign(FV(1:end-1))~=0)+1;L];    % Positions of starting domain
end
FV_raw = FV;

%% Recursive splitting
spa = zeros(L,1);
spa(Pos)=1;

for i = 1 : length(Pos)-1
    
    % Block range
    idx = Pos(i):Pos(i+1)-1;
    
    % If block size <= ms0, we will not split again
    if length(idx)>ms0
        % Sub-matrix
        SH = H(idx,idx);
        % Fiedler number and vector
        [FV,FN]=Fdvectors(SH);
        
        % If the Fiedler number of the block is small
        if FN <= sig0
            % Continue to split
            sp = SubSplit(SH,sig0,ms0);
            % Mark boundaries
            spa(Pos(i)+find(sp>0)-1)=1;
        end
        
    end
    
end


posn = find(spa>0);

%% Merge single-bin domain if MERG = 1
if MERG ~= 0
    posn=MergeSmall(posn,H);
 %   posn=MergeSmall(posn,H);
end

%% Output
TAD_boundaries = posn;


end


%% ============= Sub-functions =============

%% Sub-function 1: Recusive split
function sp = SubSplit(Ho,sig0, ms0)
% Recursively splitting a connection matrix via Fiedler value and vector

% Fiedler vector
[Fdv,Fdvl]=Fdvectors(Ho);
% Position of sign change (sub-block starting)
Pos = [1;find(sign(Fdv(2:end))-sign(Fdv(1:end-1))~=0)+1;size(Ho,1)];

sp = zeros(size(Ho,1),1);
sp(Pos) = 1;
% If Fiedler value is high enough
if  Fdvl > sig0+1e-5        %   +1e-5 for numerical stability
    sp = 1;
    return;
end

% For each sub-block
for i = 1 :  length(Pos)-1
    % Range
    idx = Pos(i):Pos(i+1)-1;
    
    % minimum sub-block size
    if length(idx)>ms0
        % Continue to split
        sp1 = SubSplit(Ho(idx,idx),sig0,ms0);
        % Mark bock boundary
        sp(Pos(i)+find(sp1>0)-1)=1;
    end
end


end

%% Fiedler vector calculation
function [Fdv,Fdvl] = Fdvectors(H,NN)

H = (H +H')/2;

if nargin < 2
    NN = 0;
end
dgr = sum(H);
dgr(dgr==0)=1;
DN = diag(1./sqrt(dgr));
L = DN*(diag(dgr)-H)*DN;

if NN == 1
    L = diag(dgr)-H;
end

L = (L+L')/2;
[V,D] = eigs(L,2,'SA');  % Or we can just use svd / eig
Fdv = V(:,end);
Fdvl =(D(end,end));
%


if NN == 1;
    Fdvl = Fdvl/size(L,1)^0.3;
end
end

%% Merging small regions
function Pos=MergeSmall(posn,H);
Pos = posn;
Posr= Pos;
% Find region only with 1 bin size
idx1 = find(Pos(2:end)-Pos(1:end-1)==1);
for i = 1 : length(idx1)
    cond1 = idx1(i)+1 <= length(Pos);
    cond2 = idx1(i)-1 >= 1;
    % Check this single bin this more similar to upstream or downstream bins.
    if idx1(i)+1 <= length(Pos)
        vrp = mean(H(Pos(idx1(i)),Pos(idx1(i))+1:Pos(idx1(i)+1)));
    end
    if idx1(i)-1 >= 1
        vrm = mean(H(Pos(idx1(i)),Pos(idx1(i)-1):Pos(idx1(i))-1));
    end
    if cond1&cond2  & vrm >= vrp
        Posr(idx1(i)) = -100;
    elseif  cond1&cond2  & vrm < vrp
        Posr(idx1(i)+1) = -100;
    end
    if idx1(i) == 1
        Posr(2) = -100;
    end
    if idx1(i) == Pos(end)-1
        Posr(end-1)=-100;
    end
end
Pos(Posr==-100)=[];
end


%% Toeplitz normalization
function NX= ToepNorm(X)


% Get size informaiton
L = size(X,1);

% Diagonal summation
ds = sumDiag(X);

% Diagonal mean value
mds = ds(L:end)./[L:-1:1]';

% Normalization matrix
Tp = toeplitz(mds);
% Nomralization
NX = X./Tp;

NX(isinf(NX))=0;
NX(isnan(NX))=0;
end