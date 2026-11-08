function fartmapt(FormFile,MODE,SIV,PlotFlag)

%            A FUZZY ART MAP NEURAL NETWORK
%               SPEECH RECOGNITION SYSTEM
%                      BASED ON 
%                   FORMANT RATIOS
%
%                         by 
%           Capt D.P. Young, CD, B.Sc., RRMC 
%                   Canadian Forces
%
% (c) Copyrigth by D.P. Young 1995
% This program may be used within the Department of National Defence
% but copyright for open use remains the property of the author.
%
%
% Usage fartmapt(FormFile,MODE,SIV,PlotFlag)
%
%   FormFile = string name of file containing extracted formant vectors produced by FORMANT3.M
%       MODE = 1 for training
%            = 2 for testing
%        SIV = Signal Identification Vector (used to map fuzzy ART categories to a given phrase)
%	     = 999 for autodetect from filename
%   PlotFlag = 0 for no graphics
%            = 1 for graphics

% TURN ON WHITE BACKGROUND FOR SCREEN SHOTS
% ensure all figures are closed first
close; close; close; close; close; close; close; close; close; close; close;
%whitebg;

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if MODE==1
   vigilance=1.00; % This is the baseline training vigilance
else
   vigilance=0.50; % This is the baseline testing vigilance
end;   

Choice_Parameter = 0.001; % The choice function uses this non-zero positive parameter in its denominator to
                          % break the tie between competitive nodes

NewClusterFlag = 0; % This flag is used to signal the creation of a new cluster

UNRECOGNIZED=999; % Code number used to label unrecognized input vectors. A positive number is used
		  % since it must serve later as an vector index (no negative indexes allowed)
		  % Warning: Ensure this number is not overrun by a real cluster number due to
		  % cluster expansion(explosion?).


StandardSIVLength=80; % Max length of SIV string, used to pad with blanks for if SIV=='string'
		      % to compare strings they must be the same length

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

% BATCH MODE SIV ASSIGNMENT BY FILE NAME
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% The SIV arguement is set to 999 when the program is to automatically construct a SIV code based
% on the file name of the YFR file. 

if SIV(1) == 999 
        BatchFlag=1;
	PHRASE=FormFile(8);
	if PHRASE=='0' SIV='DATE AND TIME';
	elseif PHRASE=='1' SIV='NAME';
	elseif PHRASE=='2' SIV='SHE HAD YOUR DARK SUIT IN GREASY WASH WATER ALL YEAR';
	elseif PHRASE=='3' SIV='DON^T MAKE ME CARRY AN OILY RAG LIKE THAT';
	elseif PHRASE=='4' SIV='MAY WE ALL LEARN A YELLOW LION ROAR';
	elseif PHRASE=='5' SIV='WE WERE AWAY A YEAR AGO';
	elseif PHRASE=='6' SIV='I KNOW WHEN MY LAWYER IS DUE';
	elseif PHRASE=='7' SIV='EVERY SALT BREEZE COMES FROM THE SEA';
	elseif PHRASE=='8' SIV='OUR YACHT SLID AROUND THE POINT INTO THE BAY';
	elseif PHRASE=='9' SIV='I WAS STUNNED BY THE BEAUTY OF THE VIEW';
	else SIV='BATCH FILE NAME ERROR';
	end; %if PHRASE
   else
        BatchFlag=0;
end; %if SIV

SIV=[SIV,blanks(StandardSIVLength-length(SIV))]; % pad SIV string to standard SIV length with blanks

FileNameSIV=SIV; % store phrase identifier from filename for automatic error detection using database files

%#########################################################################################################
% PERFORM FEATURE VECTOR REPRESENTATION PRIOR TO NETWORK INPUT
%#########################################################################################################

% Load formant vectors from FormFile

load(FormFile);


% Calculate the Tri Formant Ratio Vector (TFRV) representation

F3F2=(Formant(3,:)./Formant(2,:));
F2F1=(Formant(2,:)./Formant(1,:));
F3F1=(Formant(3,:)./Formant(1,:));
TFRV=[F3F2,F2F1,F3F1];


% Convert the TFRV to Normalized Polar Angle (NPA) form

NPA_TFRV=atan(TFRV)/(0.5*pi);


% Linear Time Warp (LTW) the Normalized TFRV to standard network input length 

StandardLength=500; 
LengthTFRV=length(TFRV);

for Index=1:StandardLength-1
    LTW_NPA_TFRV(Index)=NPA_TFRV(ceil(LengthTFRV/StandardLength*Index));
end;

LTW_NPA_TFRV(StandardLength)=NPA_TFRV(LengthTFRV); % this is a work around a bug in the ceil function


if PlotFlag > 0
	% Plot the feature vector
	figure(1);
	% In learning mode, just plot the feature vector
	% In test mode, leave room in the figure for the comparison sub-plots
	if MODE == 1
		plot(LTW_NPA_TFRV,'y');
	else
		subplot(3,1,1);
		plot(LTW_NPA_TFRV,'y');
	end;
	axis([0 StandardLength 0 1]); % a standard axis aids in visual comparison
	title(['Tri Formant Ratio Vector from ',WaveFile]);
	ylabel('NPA Ratio');
	grid on;
end;


% Initialize starting weights:
% Load Network Weight Matrix file if it exists or initialize from scratch
% NOTE: floppy drives can be used for removeable media

FID = fopen('fartmapt.mat'); % (FID = -1 if it doesn't exist)
if FID == -1
    fprintf(' \n INITIALIZING Fuzzy ART Map Network Memory Matrix ! \n');
    M=2*StandardLength;  % The input dimension of the network
	                 % It is TWICE THE SIZE OF THE FEATURE VECTOR due to complement coding
    N=10;          % N is the number of outputs from the network.
                   % It defines the number of classifications defineable - matrix is initialized with 10 outputs 
		   % MORE OUTPUTS ARE ADDED AS DEMANDED BY PROGRAM NEEDS
    W = ones(N,M); % W is the feedforward/feedback weight matrix between the input and output layers
    max_cluster_number = 0;  % keeps track of the highest committed cluster
    SIM=ones(N,length(SIV)); % Signal Identification Matrix with length(SIV) outputs and N category inputs
			     % NOTE** This convention is currently the reverse of that used in W weight matrix
			     % Recode the W matix to (input#,output#) standard at a later date (reduce code)
else
    fclose(FID);
    load('fartmapt.mat'); 
    [N,M]=size(W);
end;

%################################################################################################################
% FUZZY ART SELF ORGANIZATION 
%################################################################################################################

% Calculate complement coding input vector..Note that the dimension has doubled.
I = [LTW_NPA_TFRV,1-LTW_NPA_TFRV]; % it is assumed that the feature vector is a row vector

% Calculate choice function Tj(I) for each output node  
% To save time, PERFORM CHOICE FUNCTION ONLY FOR CATEGORY NODES AND ONE UNCOMMITTED NODE
for j = 1:(max_cluster_number+1) 
    T(j) =  sum( min(W(j,:),I) ) / ( Choice_Parameter + sum(W(j,:)) );
end; % for j

% Perform "Hypothesis" testing, in descending order of Choice Function output magnitude
% until a match is made that meets the required vigilance, and meets the Match Tracking requirements

active_nodes = (max_cluster_number+1); % identify number of nodes in competition (other outputs are spares)

MatchTracking=1; % set flag
while MatchTracking==1

  cluster_search = 1; % turn flag on
  while cluster_search == 1,  

    % find node with maximum output
    % IF TWO NODES BOTH HAVE MAX OUTPUTS THEN THE NODE WITH THE LOWEST INDEX GETS CHOSEN , max function does this automatically
    [maxnum,max_index] = max(T);

    % Vigilance (similarity) test 

    similarity = sum( min(W(max_index,:),I) ) / sum(I);

    if (similarity < vigilance) & (active_nodes > 1) 

        % RESET: Disable Node and look for next T(j)max 

        T(max_index) = 0; % deactivate winning node by setting its choice function to zero
        active_nodes = active_nodes - 1; % decrement active node counter

      else % RESONANCE: stop search and record cluster number

	cluster=max_index;
        cluster_search = 0; % set flag to end cluster search, exit from while loop
   
   end; % if similarity
 end; % while cluster_search

 if MODE==1
       % >>>>>>>>> LEARNING MODE - MATCH TRACKING PROCESS <<<<<<<<<<<<<<<
       % if the cluster output achieved by the resonance (above) is not mapped to the desired SIV code
       % in the Signal Identification Matrix (SIM) then the vigilance parameter is increase from the
       % baseline value to a value just above the similarity ratio (in order to induce reset) and the
       % "Hypothesis" testing is restarted from where it left off
 
       if SIM(cluster,:)==SIV	% Check for SIV match and break out of while loop
	  MatchTracking=0;                 
       elseif max_index > max_cluster_number  % Check for new cluster, and assign SIV to SIM
          SIM(cluster,:)=SIV;
          MatchTracking=0; % Break out of while loop
       else 					  % Boost vigilance just above similarity
	  vigilance = 1.00000000000001*similarity; % Matlab displays accuracy to 14 decimal places
       end; %if SIM
   else
       MatchTracking=0; % Only perform Match Tracking in learning mode
   end; % if MODE==1

end; % While MatchTracking==1


% LEARNING PHASE:     FAST LEARNING = NO RECODING OF CATEGORY WEIGHTS AFTER INITIAL FORMATION
% A new category is formed solely around a new input vector which did not fit in any other category

if max_index > max_cluster_number  % current max_index is a new cluster
    if MODE ==1 
	% Update flags, counters and weights
	NewClusterFlag = 1;
	max_cluster_number = max_index;
	fprintf('\nNew Cluster Formed = %i \n',max_cluster_number);
        W(max_index,:) = I; % Because the learning rate is 1 all new clusters are centered on the founding vector
     else
        % MODE 2 RECOGNITION ONLY - NO LEARNING ALLOWED
        fprintf('\n UNRECOGNIZED FEATURE !!! \n');
        cluster=UNRECOGNIZED; % assign the feature vector to the "UNRECOGNIZED" cluster instead of creating a new cluster
     end; % if MODE
end; % if max_index

% If in test mode, then Identify the voice sample
if max_index <= max_cluster_number
   if MODE==2
        SIV=SIM(cluster,:);

 	% AUTO ERROR DETECTION FOR DATBASE FILES - compare SIV of matching pattern to that of input file name
        if (BatchFlag == 1) & (strcmp(SIV,FileNameSIV)==0)
	      fprintf('WRONG PHRASE IDENTIFIED || ');
	end;

	% PRINT OUT MATCHING VECTOR INFO
        fprintf('%5.2f Percent || %s \n',100*similarity,SIV);

	% PLOT THE MATCHING MEMORY VECTOR FOR COMPARISON
	if PlotFlag > 0
		figure(1);
		subplot(3,1,2);
		plot(W(cluster,:),'y');
		axis([0 StandardLength 0 1]); % a standard axis aids in visual comparison
		title('Fuzzy ART Map Stimulus Response');
		ylabel('NPA Ratio');
		grid on;


		% OVERLAP THE TWO VECTORS
		subplot(3,1,3)
		plot(LTW_NPA_TFRV,'y')
		axis([0 StandardLength 0 1]); % a standard axis aids in visual comparison
		title([num2str(100*similarity),'% Match to ',deblank(SIV)]);
		xlabel('Linearly Warped Time Scale') 
		ylabel('NPA Ratio');
		hold on
		plot(W(cluster,:),'y');
		hold off
		grid on;
	end;

    end; % if MODE==2
end; % if max_index

%######################################################################################
% NEW IDEA - allow weight matrices to grow when it gets low on uncommitted output classes
% ADD WEIGHTS FOR TWENTY MORE CATEGORIES
  if (N - max_cluster_number) < 2
      N=N+20 ;
      fprintf('\n >>>>>>>>>>> Caution - Network Memory is GROWING!!! <<<<<<<<');
      W=[W;ones(20,M)];
      % Expand Signal Identification Matrix to accomodate 20 more input categories
      SIM=[SIM;ones(20,length(SIV))];
  end;
%   
%#######################################################################################
  
% PLOT FINAL WEIGHTS IF THEY HAVE CHANGED DUE TO NEW CLUSTER FORMATION
if NewClusterFlag == 1 & PlotFlag > 0
    figure(2);
    imagesc(W'); 
    axis('xy');
    title('Fuzzy ART Map Memory');
    xlabel('Long Term Memory (LTM) Patterns');
end;  

% SAVE NETWORK WEIGHTS AND NUMBER OF LAST COMMITTED OUTPUT NODE
if NewClusterFlag==1
	save fartmapt.mat W max_cluster_number SIM
end;

% PRINT END OF PROGRAM
fprintf('=====================================================================================================\n');
[y,fs]=loadwave('ringin.wav');
playwave(y,fs);
