function [NX,Tp] = ToepNorm(X,Mod)
% function: nomalize the matrix by dividing the diagonal and each paralell
%   of the diagonal by its mean
% Inpust:
%     X - matrix to be normalized, can be either square or not
%     mod - set to 1 to only average non-0 elements. default = 0 which
%        averages all elements.
%
% Jie Chen, June 2014
% http://www.jie-chen.com

if nargin < 2
    Mod = 0;
end

if isempty(X)
    NX = [];
    Tp = [];
    return;
end

% Get size informaiton
[m,n] = size(X);
ms = min(m,n);
mxs = max(m,n);

% Diagonal summation
ds = sumDiag(X);
% Number of elements
if Mod == 0
    Ne = [1:ms-1, ones(1,mxs-ms+1)*ms, ms-1:-1:1]';
elseif Mod == 1   % We only count non-zero elements
    Ne = sumDiag(X>0); 
    Ne = Ne(end:-1:1);
end
% Diagonal mean value
mds = ds(end:-1:1)./Ne;

% Normalization matrix
Tp = toeplitz(mds(m:-1:1),mds(m:end));
% Nomralization
NX = X./Tp;

NX(isinf(NX))=0;
NX(isnan(NX))=0;
end
