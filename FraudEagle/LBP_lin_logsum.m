function [beliefs1, beliefs2, Hi] = LBP_lin_logsum( adjlist, nodep1, nodep2, edgep, it )


% Author : Leman Akoglu (Stony Brook University)
% Email: leman@cs.stonybrook.edu
% Copyright December 2, 2014
% Available for academic use only, not for commercial use

% adjlist : (Ex3) adjacency list; 
%	First two columns for source (1...N) and dest (1...M), N: #users and M: #prod.s
%	3rd column either (1) 1 for + and 2 for - , or (2) 1-5: ratings
% nodep1: NxK1 matrix of initial prior potentials; N: #users, K1: classes/states
% nodep2: MxK2 matrix of initial prior potentials; M: #prod.s, K2: classes/states
% edgep: K1xK2x|domain3rdColumn|
% it: max #iter.s

edgep

[N K1] = size(nodep1);
[M K2] = size(nodep2);
E = size(adjlist,1);

% initializing all messages to 1
% holding ALL msgs in log's so init to 0
m_to = zeros(E,K2);
m_from = zeros(E,K1);

nodep1 = log(nodep1);
nodep2 = log(nodep2);
edgep = log(edgep);

epsilon = 10^-6;

% for each node 
repeat = true;
iter=0;
ts=tic;
while( repeat )    
    tic
    iter=iter+1
	maxdiff = -Inf;
	
	% compute product buffer for N
	prodN = zeros(N,K1);
	for i=1:E
		prodN(adjlist(i,1),:) = prodN(adjlist(i,1),:) + ( m_from(i,:) );
	end
	
	% compute messages to M nodes
alldiff=zeros(2*E,1);
	for i=1:E
		a = adjlist(i,1);
		b = adjlist(i,2);
		mn = ( prodN(a,:) - ( m_from(i,:) ) );
            
		part = nodep1(a,:) + mn;
		newmsg = zeros(1,K2);              
		for k=1:K2
			term = ( part + edgep( :,k,adjlist(i,3) )' ); 
			newmsg(k) = log(sum(exp(term-max(term)))) + max(term); 
		end
		%if(sum(newmsg)>0)
		%	newmsg = newmsg / sum(newmsg);
		%else
		%	newmsg = 10^-6*ones(1,K2);
		%end
		%newmsg(newmsg==0) = 10^-6;	
		
		% normalize: newmsg(i)/sum(newmsg)
		newmsg = newmsg-( log(sum(exp(newmsg-max(newmsg)))) + max(newmsg) );
		
		
		fark = exp(newmsg) - exp(m_to(i,:));
		diff = norm(fark);		
alldiff(i) = diff;		
		if( diff > maxdiff)
			maxdiff = diff;  
		end 

		m_to(i,:) = newmsg; 
		%neighs(n)
		%newmsg
		%pause
		
	end % iterating N nodes
	
		
	% compute product buffer for M
	prodM = zeros(M,K2);
	for i=1:E
		prodM(adjlist(i,2),:) = prodM(adjlist(i,2),:) + ( m_to(i,:) );
	end
	
	% compute messages to N nodes
	for i=1:E
		a = adjlist(i,2);
		b = adjlist(i,1);
		mn = ( prodM(a,:) - ( m_to(i,:) ) );
		
	            
		part = nodep2(a,:) + mn;
		newmsg = zeros(1,K1);              
		for k=1:K1
			term = ( part + edgep( k,:,adjlist(i,3) ) );  
			newmsg(k) = log(sum(exp(term-max(term)))) + max(term); 
		end
		
		%if(sum(newmsg)>0)
		%	newmsg = newmsg / sum(newmsg);
		%else
		%	newmsg = 10^-6*ones(1,K1);
		%end
		%newmsg(newmsg==0) = 10^-6;
		
		% normalize: newmsg(i)/sum(newmsg)
		newmsg = newmsg-( log(sum(exp(newmsg-max(newmsg)))) + max(newmsg) );
		
		
		fark = exp(newmsg) - exp(m_from(i,:));
		diff = norm(fark);
alldiff(i+E) = diff;	
		
		if( diff > maxdiff)
			maxdiff = diff;  
		end     
		
		m_from(i,:) = newmsg; 
		%neighs(n)
		%newmsg
		%pause
		
	end % iterating M nodes
	
	%salldiff = sort(alldiff);
	maxd = max(alldiff) 
	mind = min(alldiff) 
	meand = mean(alldiff)
	p90 = quantile(alldiff, 0.9)
	%pause
	
	if maxdiff < epsilon
        repeat = false;
    end
    
    if(iter==it)        
        break;
    end
	toc
	
end
toc(ts)
iter

%m1
%m2

%m_from(m_from==0) = 10^-6;
%m_to(m_to==0) = 10^-6;

% compute beliefs
beliefs1 = zeros(N,K1);
beliefs2 = zeros(M,K2);
% compute product buffer for N
for i=1:E
	a = adjlist(i,1);
	b = adjlist(i,2);
	beliefs1(a,:) = beliefs1(a,:) + ( m_from(i,:) );
	beliefs2(b,:) = beliefs2(b,:) + ( m_to(i,:) );	
end

for a=1:N
	beliefs1(a,:) = (nodep1(a,:)) + ( beliefs1(a,:) );
	
	nwm = beliefs1(a,:);
	for k=1:K1
		beliefs1(a,k) = 1 / ( sum(exp(nwm-nwm(k))) );
	end
	%beliefs1(a,:) = beliefs1(a,:) / sum(beliefs1(a,:)); 
end
for b=1:M
	beliefs2(b,:) = (nodep2(b,:)) + ( beliefs2(b,:) );
	
	nwm = beliefs2(b,:);
	for k=1:K2
		beliefs2(b,k) = 1 / ( sum(exp(nwm-nwm(k))) );
	end
	%beliefs2(b,:) = beliefs2(b,:) / sum(beliefs2(b,:)); 
end

% [MAP1 ind1] = max(beliefs1,[],2);
% [MAP2 ind2] = max(beliefs2,[],2);



Hi = exp(m_from(:,K1)); %edge-beliefs for fakeness of users


end