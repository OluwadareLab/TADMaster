function wCent = AddCent(vect,idx)
%Add centromeres back to a vector
%   vect is a vector of chromosome positions
%   idx is a binary vector with ones in the positions of rows removed as
%   centromeric.

wCent = NaN(size(vect));
for t = 1:length(vect)
    zers = find(idx==0,vect(t));
    wCent(t) = zers(end);
end


end

