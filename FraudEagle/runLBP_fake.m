function [beliefs1, beliefs2, Hi] = runLBP_fake()

% Author : Leman Akoglu (Stony Brook University)
% Email: leman@cs.stonybrook.edu
% Copyright December 2, 2014
% Available for academic use only, not for commercial use

load ('toy/adj.mat');

[i j w] = find(adj2);
L = [i j w];

load('toy/edgep.mat')

[beliefs1, beliefs2, Hi] = LBP_lin_logsum( L, ones(size(adj2,1),2)*0.5, ones(size(adj2,2),2)*0.5, edgep, 100 );

end