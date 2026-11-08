# Annex D

**FORMANT3.M Program Code (Matlab 4.0)**

*Listing as printed in the 1995 thesis (extracted from the original Word 6.0 file).*

```matlab
function formant3(SpecFile,PlotFlag,NRFlag,NoiseFile)

% YOUNG FORMANT EXTRACTOR
%
% PROGRAM OVERVIEW:
%
% USAGE: formant3(SpecFile,PlotFlag,NRFlag,NoiseFile)
%
% Plot Flag is used to control the level of screen "visualization"
% PlotFlag==2 will plot 9 figures
% PlotFlag==1 will plot 1 figure (the most important) of filtered speech formants
% PlotFlag==0 plots nothing (fastest execution)
%
% NRFlag==1 performs noise reduction of the spectrogram using the wav file "NoiseFile"
%        and is highly recommended for steady state background noise (ie. hard disk RPMs etc)

% TURN ON WHITE BACKGROUND FOR SCREEN SHOTS
% ensure all figures are closed first
close; close; close; close; close; close; close; close; close; close; close;
whitebg;

%#########################################################################
%	PART 1 - LOAD SPECTROGRAM
%#########################################################################

load(SpecFile);
[SpecRows,SpecCols]=size(Spec);

%~~~~~~~~~~~~~ GLOBAL CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NFFT=512;  		       	% Number of samples in FFT window frame
NOverLap=0.5*NFFT;
FreqRes=Fs/NFFT; 	% Bandwidth resolution of FFT frequency bands (specgram rows)
MinFreq=300;	    		% Ignore frequencies below this level
MaxFreq=3300;    		% Ignore frequencies above this level
		 		% Eg. Telephone bandwidth 300-3300 Hz
% The specgram row representing the miminum frequency
LowBand=ceil(MinFreq/FreqRes);
% The specgram row representing the maximum frequency HighBand=ceil(MaxFreq/FreqRes);
% The number of formants to be extracted from the signal
MaxFormants=3;
% The Half Formant Bandwidth in frequency (Hz)
HFBFreq=150;
% The Half Formant Bandwidth in specgram rows
HFBRows=ceil(HFBFreq/FreqRes);

%~~~~~~~~~~~~~ GLOBAL CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

% PLOT THE SPECTROGRAM OF JUST LOADED
if PlotFlag > 1
	figure(1)
	clf reset
	[SpecRows,SpecCols]=size(Spec);
  	TimeIndex=(1:SpecCols)*NOverLap/Fs;
  	FreqIndex=(1:SpecRows)*Fs/NFFT;
  	imagesc(TimeIndex,FreqIndex,Spec); axis('xy')
	title(['Spectrogram of ',WaveFile]) ;
	xlabel('Time (sec)');
	ylabel('Frequency (Hz)');
	colormap(1-gray);
        pause(3);
end;


if NRFlag > 0
   % PRODUCE A NOISE REDUCTION MASK
   [NOISE]=loadwav(NoiseFile); % background noise recorded from live session
   MaxNoise=max(abs(specgram(NOISE*Boost_Ratio,NFFT))');
   % max of transpose specgram matrix gives freq row maximums
   MaxNoise=MaxNoise'; % convert to a column vector
   MaxNoise=MaxNoise(1:SpecRows,1); % crop to same number of rows as spectrogram
   if PlotFlag > 1
	% PLOT MAXNOISE
	figure(2)
	clf reset;
  	TimeIndex=[0 1];
  	FreqIndex=(1:SpecRows)*Fs/NFFT;
  	imagesc(TimeIndex,FreqIndex,MaxNoise); axis('xy')
	title(['Max Spectral Amplitudes of ',NoiseFile]);
	ylabel('Frequency (Hz)');
	colormap(1-gray);
	pause(3);
   end; % if PlotFlag

   for TimeIndex=1:SpecCols
	Spec(:,TimeIndex)=Spec(:,TimeIndex)-MaxNoise;
   end;
   % ELIMINATE NEGATIVE NUMBERS FROM SPECTROGRAM
   Spec=(Spec+abs(Spec))/2;

   if PlotFlag > 1
	figure(3)
	clf reset;
  	TimeIndex=(1:SpecCols)*NOverLap/Fs;
  	FreqIndex=(1:SpecRows)*Fs/NFFT;
  	imagesc(TimeIndex,FreqIndex,Spec); axis('xy')
	title(['Noise Masked Spectrogram of ',WaveFile]) ;
	xlabel('Time (sec)');
	ylabel('Frequency (Hz)');
	pause(3);
   end;
end; % if NoiseReduction

%#########################################################################
%
%
%#########################################################################

% DETERMINE SHORT TERM ENERGY OF SPEC COLUMNS WITHIN THE GIVEN % FREQUENCY RANGE
STEnergy=(sum(Spec(LowBand:HighBand,:)));

% FREQUENCY)
if PlotFlag > 1
	figure(4)
	clf reset;

	[SpecRows,SpecCols]=size(Spec);
  	FreqIndex=(1:SpecRows)*Fs/NFFT;
  	imagesc(TimeIndex,FreqIndex,Spec(1:HighBand,:)); axis('xy')
	title(['Relative STE Curve of ',WaveFile]) ;
	xlabel('Time (sec)');
	ylabel('Frequency (Hz)');
	colormap(1-gray);

	% Plot STE curve overlay
	hold on;
	plot(TimeIndex,max(FreqIndex)*STEnergy/max(STEnergy),'k')
	hold off

	% mark the minimum and maximum frequency band stops
	hold on;
	plot(TimeIndex,MinFreq*ones(1,SpecCols),'k');
	plot(TimeIndex,MaxFreq*ones(1,SpecCols),'k');
	hold off;
	pause(3);
end;

% REMOVE PORTIONS OF LOW ENERGY (SILENCE AND FRICATIVES)
% using 2nd frequency row as a reference
Index=find(HighBand*STEnergy/max(STEnergy) > 2);
% keep only the high energy portions
Spec=Spec(:,Index);
% determine new size of spectrogram
[SpecRows,SpecCols]=size(Spec);
% keep only the high energy portions
STEnergy=STEnergy(Index);
LengthSTE=length(STEnergy);

% PLOT SPECTROGRAM WITH LOW ENERGY SECTIONS REMOVED
if PlotFlag > 1
	figure(5)
	clf reset;
  	TimeIndex=(1:SpecCols)*NOverLap/Fs;
  	FreqIndex=(1:SpecRows)*Fs/NFFT;
  	imagesc(TimeIndex,FreqIndex,Spec(1:HighBand,:)); axis('xy')
	title(['Silence Reduced Spectrogram of ',WaveFile]) ;
	xlabel('Time (sec)');
	ylabel('Frequency (Hz)');
	colormap(1-gray);

	% Plot STE curve overlay
	hold on;
	plot(TimeIndex,max(FreqIndex)*STEnergy/max(STEnergy),'k')
	hold off

	% mark the minimum and maximum frequency band stops
	hold on;
	plot(TimeIndex,MinFreq*ones(1,SpecCols),'k');
	plot(TimeIndex,MaxFreq*ones(1,SpecCols),'k');
	hold off;

	pause(3);
end;


% APPLY OCTAVE GAIN TO EMPHASIZE HIGHER FREQUENCY BANDS
for row=1:SpecRows
	Gain(row,1)=10^(log2(row)/5); %
end;
for TimeIndex=1:SpecCols
	Spec(:,TimeIndex)=Spec(:,TimeIndex).*Gain;
end;

if PlotFlag > 1
	% PLOT SPECTROGRAM TO SCREEN
	figure(6);
	clf reset;

	[SpecRows,SpecCols]=size(Spec);
  	TimeIndex=(1:SpecCols)*NOverLap/Fs;
  	FreqIndex=(1:SpecRows)*Fs/NFFT;
  	imagesc(TimeIndex,FreqIndex,Spec(1:HighBand,:)); axis('xy')
	title(['Octave Enhanced Spectrogram of ',WaveFile]) ;
	xlabel('Time (sec)');
	ylabel('Frequency (Hz)');
	colormap(1-gray);

	% mark the minimum and maximum frequency band stops
	hold on;
	plot(TimeIndex,MinFreq*ones(1,SpecCols),'k');
	plot(TimeIndex,MaxFreq*ones(1,SpecCols),'k');
	hold off;

	pause(3);
end;
%#########################################################################
%
%	PART 3 - EXTRACT FORMANTS
%
%#########################################################################

% PERFORM INITIALIZATIONS BASED ON SIZE OF SPECTROGRAM
Peak=zeros(SpecRows,SpecCols);
Formant=zeros(SpecRows,SpecCols);


% DETERMINE SPECTRAL PEAKS FOR EACH TIME SLICE

for TimeIndex=1:SpecCols

   PeakNumber=0;

   % SAVE FREQUENCY BIN NUMBER OF LOCAL PEAKS
   % (max values within Formant Bandwidth)
   for FreqBand=LowBand:HighBand;
      LowFB=FreqBand-HFBRows;
      if LowFB < 1
	LowFB=1;
      end;

      HighFB=FreqBand+HFBRows;
      if HighFB > SpecRows
	HighFB=SpecCols;
      end;

      FBMax=max(Spec(LowFB:HighFB,TimeIndex)); % the max value within the window

      if Spec(FreqBand,TimeIndex) == FBMax & FBMax ~= 0
	 PeakNumber=PeakNumber+1;
	% record the frequency band of the local peak	 	PeakFrequency(PeakNumber,TimeIndex)=FreqBand;
	% record its amplitude 	PeakAmplitude(PeakNumber,TimeIndex)=Spec(FreqBand,TimeIndex);
	% keep track of the total number of peaks in a given time slice 	NumberOfPeaks(TimeIndex)=PeakNumber;
      end;
   end; % for FreqBand

   % SINCE ARRAY WAS NOT INITIALIZED, TIME INDEX LENGTH IS VARIABLE
   % SINCE PEAKS MAY NOT BE PRESENT AT THE  END OF THE
  % SPECTROGRAM. IN THIS CASE, INSERT DUMMY VALUES AS PLACE
   % HOLDERS TO PROVIDE UNIFORM ARRAY LENGTHS
   if PeakNumber==0
	PeakFrequency(1,TimeIndex)=1;
	PeakAmplitude(1,TimeIndex)=1;
	NumberOfPeaks(TimeIndex)=0;
   end;
end; % for TimeIndex


% DEFINE FORMANTS AS PEAKS WITH GREATEST AMPLITUDE / NUMBERED
% FROM LOW TO HIGH FREQUENCY
for TimeIndex=1:SpecCols
	% SORT AMPLITUDES (ascending order)
	[SortedAmplitudes,PeakNumbers]=sort(PeakAmplitude(:,TimeIndex));
	% change the index to descending order
	PeakNumbers=flipud(PeakNumbers);

	% SELECT THE ONES WITH GREATEST AMPLITUDES
	if NumberOfPeaks(TimeIndex) < MaxFormants
		% pick only non-zero elements
		MaxPeaks=PeakNumbers(1:NumberOfPeaks(TimeIndex));
	else
		% pick the biggest ones in the index
		MaxPeaks=PeakNumbers(1:MaxFormants);
	end; % if

% LABEL THE FORMANTS IN ORDER OF PEAK NUMBER (LOWEST TO HIGEST
% FREQUENCY BAND)
	SortedMaxPeaks=sort(MaxPeaks);
	for FormantNumber=1:length(MaxPeaks)
	Formant(FormantNumber,TimeIndex)=
		PeakFrequency(SortedMaxPeaks(FormantNumber),TimeIndex);
	end;

end; % for TimeIndex

if PlotFlag > 1
	% PLOT SPECTROGRAM TO SCREEN
	figure(7);
	clf reset;

	[SpecRows,SpecCols]=size(Spec);
  	TimeIndex=(1:SpecCols)*NOverLap/Fs;
  	FreqIndex=(1:SpecRows)*Fs/NFFT;
  	imagesc(TimeIndex,FreqIndex,Spec(1:HighBand,:)); axis('xy')
	title(['Local Spectral Maxima of ',WaveFile]) ;
	xlabel('(Symbol Key)    . = PEAK    X = F1    O = F2    * = F3');
	ylabel('Frequency (Hz)');
	colormap(1-gray);

	% mark the minimum and maximum frequency band stops
	hold on;
	plot(TimeIndex,MinFreq*ones(1,SpecCols),'k');
	plot(TimeIndex,MaxFreq*ones(1,SpecCols),'k');

	% PLOT PEAKS AND ROUGH DRAFT OF FORMANTS ON SPECTROGAM
	plot(TimeIndex,PeakFrequency'*FreqRes-(FreqRes/2),'.k')
	plot(TimeIndex,Formant(1,:)'*FreqRes-(FreqRes/2),'xk')
	plot(TimeIndex,Formant(2,:)'*FreqRes-(FreqRes/2),'ok')
	plot(TimeIndex,Formant(3,:)'*FreqRes-(FreqRes/2),'*k')

	hold off;
	pause(3);
end;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   FILTER OUT SECTIONS WITH HIGH FIRST FORMANT
%   OR NO THIRD FORMANT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% FIND ALL ZERO VALUED THIRD FORMANTS AND SET ALL THE FORMANTS
% FOR THAT TIME SLICE TO ZERO
ZeroIndex=find(Formant(3,:) == 0);
for TimeIndex=1:length(ZeroIndex)
    for FormantNumber=1:MaxFormants
	Formant(FormantNumber,ZeroIndex(TimeIndex))=0;
    end;
end;

% FIND ALL FIRST FORMANTS GREATER THAN 1200 HZ AND ZERO OUT THE TIMESLICES
ZeroIndex=find(Formant(1,:) > ceil(1200/FreqRes));
for TimeIndex=1:length(ZeroIndex)
    for FormantNumber=1:MaxFormants
	Formant(FormantNumber,ZeroIndex(TimeIndex))=0;
    end;
end;


%%%%%%%%%%%%%%%%%% PLOT FILTERED FORMANTS
if PlotFlag > 1
	figure(8);
	clf reset;
	[SpecRows,SpecCols]=size(Spec);
  	TimeIndex=(1:SpecCols)*NOverLap/Fs;
  	FreqIndex=(1:SpecRows)*Fs/NFFT;
  	imagesc(TimeIndex,FreqIndex,Spec(1:HighBand,:)); axis('xy')
	title(['Probable Formants of ',WaveFile]) ;
	xlabel('(Symbol Key)    X = F1    O = F2    * = F3');
	ylabel('Frequency (Hz)');
	colormap(1-gray);
	% mark the minimum and maximum frequency band stops
	hold on;
	plot(TimeIndex,MinFreq*ones(1,SpecCols),'k');
	plot(TimeIndex,MaxFreq*ones(1,SpecCols),'k');

	% plot filtered formants
	plot(TimeIndex,Formant(1,:)'*FreqRes-(FreqRes/2),'xk')
	plot(TimeIndex,Formant(2,:)'*FreqRes-(FreqRes/2),'ok')
	plot(TimeIndex,Formant(3,:)'*FreqRes-(FreqRes/2),'*k')

	hold off;
	pause(3);
end;

%%%% KEEP ONLY THOSE FORMANT TIMESLICES WITH NON-ZERO VALUES
Formant=Formant(1:MaxFormants,find(Formant(3,:) > 0));
TimeIndex=(1:length(Formant))*NOverLap/Fs;


%%%%%%%%%%%%%%% CONVERT FORMANT VALUES TO FREQUENCY
Formant=Formant*FreqRes-(FreqRes/2);

if PlotFlag > 0
	% PLOT FORMANTS ON FREQUENCY SCALE FOR INSPECTION
	figure(9)
	clf reset;
	plot(TimeIndex,Formant(1,:)','k');
	title(['Formant Vectors from ',WaveFile]);
	xlabel('(Symbol Key)    X = F1    O = F2    * = F3');
	ylabel('Frequency (Hz)');
	hold on;
	plot(TimeIndex,Formant(2,:)','k');
	plot(TimeIndex,Formant(3,:)','k');
	plot(TimeIndex,Formant(1,:)','kx');
	plot(TimeIndex,Formant(2,:)','ko');
	plot(TimeIndex,Formant(3,:)','k*');
	hold off;
	grid on;

	pause(3);
end;

%#########################################################################
%
%	PART 5 - SAVE RESULTS TO FILE
%
%#########################################################################

% SAVE FEATURE VECTOR IN FORMANT "F" FILE

save tempfile Formant WaveFile
clear
load tempfile
save(['f',WaveFile(2:length(WaveFile)-4),'.mat'])
fprintf('Processing Completed !! \nResults stored in %s \n',['f',WaveFile(2:length(WaveFile)-4),'.mat']);
```
