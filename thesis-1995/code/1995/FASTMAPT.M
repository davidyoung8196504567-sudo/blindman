function fastmapt(FormFile)

% FUZZY ADAPTIVE RESONANCE THEORY MAPPING NEURAL NETWORK
%
% This program uses the Formant vectors as a feature vector
% 
% By Capt D.P. Young, Bsc Physics & Computer Science RRMC, CD 
% Department of Electrical and Computer Engineering
% Royal Military College of Canada
% In partial fulfillment of the requirements for the degree MASTER of ENGINEERING
% May 1995
%
% Usage fastmapt(FormFile)
%
%    FormFile = string name of preprocessed speaker voice sample (mono PCM format)

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODE=1;
SIV=999;
PlotFlag=0;


vigilance=1.00; % This is the baseline training vigilance

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
	subplot(3,1,1);
	plot(LTW_NPA_TFRV,'k');
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
% FAST MAPPING - just stick all vectors into memory --- no matching search (saves time) 
%################################################################################################################

% Calculate complement coding input vector..Note that the dimension has doubled.
I = [LTW_NPA_TFRV,1-LTW_NPA_TFRV]; % it is assumed that the feature vector is a row vector


% LEARNING PHASE:     FAST LEARNING = NO RECODING OF CATEGORY WEIGHTS AFTER INITIAL FORMATION
% A new category is formed solely around a new input vector which did not fit in any other category

	max_cluster_number = max_cluster_number + 1;
	fprintf('\nNew Cluster Formed = %i \n',max_cluster_number);
        W(max_cluster_number,:) = I; % Because the learning rate is 1 all new clusters are centered on the founding vector
        SIM(max_cluster_number,:)=SIV;
 

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


% SAVE NETWORK WEIGHTS AND NUMBER OF LAST COMMITTED OUTPUT NODE
save fartmapt.mat W max_cluster_number SIM

% PRINT END OF PROGRAM
fprintf('=====================================================================================================\n');

