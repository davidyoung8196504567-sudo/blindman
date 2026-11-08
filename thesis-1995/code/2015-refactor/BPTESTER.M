function BPTESTER(FormFile,WeightFile,PlotFlag)

% BPTester - Back Propogation Neural Network
%
% This program inputs a formant file created by FORMANT3.M and a weight file created by BPMapper.M 
% to attempt to recognize the phrase.


StandardBFLength=500; % The length the feature vector is time warped to fit for network input

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
end

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
end

% Assign feature vector to test vector P
P=LTW_NPA_TFRV;
P=P'; %convert to column vectors for compatibility with the BP algorithm below

% INITIALIZE NETWORK ARCHITECTURE
%================================
load(WeightFile);


% PRESENTATION PHASE
A1 = tansig(W1*P,B1);
A2 = purelin(W2*A1,B2);

% MAXNET - identify the node with maximum output
[MaxValue,MaxNode]=max(A2);

PHRASE=MaxNode+1; % an offset to make the node # coincide with the phrase number

if PHRASE==2 
    SIV='SHE HAD YOUR DARK SUIT IN GREASY WASH WATER ALL YEAR';
elseif PHRASE==3 
    SIV='DON^T MAKE ME CARRY AN OILY RAG LIKE THAT';
elseif PHRASE==4 
    SIV='MAY WE ALL LEARN A YELLOW LION ROAR';
elseif PHRASE==5 
    SIV='WE WERE AWAY A YEAR AGO';
elseif PHRASE==6 
    SIV='I KNOW WHEN MY LAWYER IS DUE';
elseif PHRASE==7 
    SIV='EVERY SALT BREEZE COMES FROM THE SEA';
elseif PHRASE==8 
    SIV='OUR YACHT SLID AROUND THE POINT INTO THE BAY';
elseif PHRASE==9 
    SIV='I WAS STUNNED BY THE BEAUTY OF THE VIEW';
end

if PHRASE==str2num(FormFile(8))
   fprintf('\n%s',SIV);
else
   fprintf('\n WRONG PHRASE = %s',SIV);
end
fprintf('\n############################################################################################\n');
