**CHAPTER FIVE**

**A FUZZY ART MAP ASR SYSTEM**

**5.1 Introduction**

This chapter marks the beginning of the core work of this thesis. The background information given in chapter two (Neural Networks), chapter three (Adaptive Resonance Theory and Fuzzy Logic), and chapter four (Automatic Speech Recognition and Formant Ratio Theory), has been presented in support of the discussion that follows.

This chapter investigates the applicability of a Fuzzy ART Map ANN to the ASR task through the implementation of an ASR system that incorporates a Fuzzy ART Map ANN as its recognition component. The system is capable of performing speaker and language independent discrete phrase recognition over public telephone lines, based on the time series of formant ratios. It is implemented on a 486DX33 desktop computer with sound card and microphone. The *GoldWave 2.11* application is used for on-line speech capture while the *Matlab 4.0* programming environment is used to accomplish the signal processing, feature extraction and ANN simulation. More specific details on the hardware and software used may be found in annex A. The source code for the programs written specifically for this thesis are contained in annexes B through G.

This ASR system is presented within the framework of the four stage ASR process presented earlier in chapter four. First, the **sound recording stage** describes the apparatus and method used to capture the speech signal as well as the creation and storage of the RMC Speech Database that was subsequently used to train and test the ASR system. Second, the **signal processing stage** deals with the spectral analysis of the recorded speech samples and the production of their spectrogram representations. Third, the **feature extraction stage** illustrates the steps required to identify the formants in the spectrogram representations produced in stage two. It also deals with the representation of speech features to the Fuzzy ART Map ANN for recognition. Finally, in the **utterance classification stage,** the Fuzzy ART Map ANN program is discussed regarding software simplifications, the tuning of the training parameters, and its information retrieval characteristics.

Both microphone and telephone recorded speech are illustrated throughout the chapter to compare the relative effectiveness of the ASR process in both transmission channels. Figure numbers carry the suffix “M” to denote microphone recorded signals while the suffix “T” is used to identify telephone recorded signals.

**5.2 Stage \#1 -- Speech Recording**

<u>The RMC Speech Database</u>

Realistic testing of any speech recognition system precludes the use of voice samples recorded within a narrow time-frame. A database of speech samples recorded over an extended period is needed to capture the daily variations in each of the speaker’s voices. Such a database was amassed from September 2 to December 22, 1994. Producing the RMC Speech database was not only more cost-effective than purchasing a commercially available speech corpus, but it had the added advantage that the subjects were locally available to perform live testing of the completed system. Off-line recording of speech samples allowed for the population of the database before the speech recognition system was completed, as well as providing speech samples for design testing. Once the ASR system was completed, on-line automated speech sampling was possible.

The RMC Speech Database is composed of voice samples from 14 volunteers from within the Department of Electrical and Computer Engineering at RMC. The particulars of each speaker are listed below to show the range of age, gender and language experience of the speaker set:

|                  |              |           |                         |
|:----------------:|:------------:|:---------:|:-----------------------:|
|  ***Speaker***   | ***Gender*** | ***Age*** | ***Languages Spoken***  |
|  Ann Hopkinson   |    Female    |    30+    |     English, French     |
| Bernard Tremblay |     Male     |    30     |     English, French     |
|  Collin Wortley  |     Male     |    49     |         English         |
| Danielle Bossart |    Female    |    54     | English, French, German |
|   David Gravel   |     Male     |    32     |     English, French     |
|   Don Hamilton   |     Male     |    31     |         English         |
|   David Young    |     Male     |    31     |         English         |
|    Ian Hawes     |     Male     |    26     |         English         |
|   Jean Dolbec    |     Male     |    26     |     French, English     |
|   Liam Porter    |     Male     |    30     |     English, French     |
|   Larry Reeves   |     Male     |    30     |         English         |
|  Murray Johnson  |     Male     |    36     |     English, French     |
|  Matthew Oliver  |     Male     |    29     |     English, German     |
|  Waldemar Borys  |     Male     |    31     |         English         |

**Table 5.1 RMC Speech Database Speaker Profiles**

The speech samples consist of ten phrases recorded on a weekly basis over the four month collection period. These phrases are listed in table 5.2 in the order in which they were recorded within each session. They are numbered zero through nine to match the file naming convention (see figure 5.1) used to store the samples on computer. The first two phrases were included to aid in the registration of speech samples while the last eight phrases were chosen to represent a phonetically diverse range of speech sounds. The third and fourth phrases were taken from the TIMIT speech database, which has been used widely throughout the ASR literature. The remaining six phrases were taken from a published speaker recognition system where they were used to **“... *model the overall distribution of speech sounds that are likely to occur.*”** \[Sam76\]:

![Figure 5.1](figures/CHAP5/fig5-1.png)

*Figure 5.1 (vector drawing recovered from rendered page; the conversion damaged its layout, see the PDF or the printed original)*

|  |  |
|:--:|:--:|
| ***Phrase Identifier*** | ***Spoken Phrase*** |
| 0 | The date is ..... and the time is ...... |
| 1 | My name is ...... |
| 2 | She had your dark suit in greasy wash water all year. |
| 3 | Don’t make me carry an oily rag like that. |
| 4 | May we all learn a yellow lion roar. |
| 5 | We were away a year ago. |
| 6 | I know when my lawyer is due. |
| 7 | Every salt breeze comes from the sea. |
| 8 | Our yacht slid around the point into the bay. |
| 9 | I was stunned by the beauty of the view. |

**Table 5.2 RMC Speech Database Phrase List**

**5.3 Recording Method and Apparatus**

To create a robust system, factors concerning the acoustic environment, microphone system, transmission system, and variability of speech were considered in the recording method and apparatus used to capture and preserve the speech signal with a minimum of distortion.

<u>The Acoustic Environment</u>

The acoustic environment of the database recording sessions was chosen to be similar to that in which the finished ASR system was intended to operate, hence, the recording location was chosen in an openly accessible office area with background noise from computer equipment and personnel. The office space was located in room 5018 of the Sawyer Building at RMC. The reverberance in the room was increased by the sound reflecting quality of the painted cinder block walls.

<u>The Microphone System</u>

Since the microphone system is the point of entry for the speech signal to the ASR system, it is important to use a microphone that gives consistent performance over the range of frequencies that are to be recorded. The microphone system should also be able to focus on the speaker and ignore sounds emanating from other sources. The Realistic Super Cardiod microphone was used because it had these attributes. It has a flat frequency response curve over the desired frequency range and provides a 30 degree maximum pick-up cone about the microphone axis that can be used to focus on the speaker. Acoustic signals that have an angle of incidence to the microphone axis greater than 30 degrees are attenuated according to the polar pick-up pattern of the microphone. Generally, attenuation increases with the angle of incidence for a given frequency.

A sound treated microphone enclosure (mic box) was used to shield the microphone from sound sources not directly in front of the microphone and helped reduce the effects of reverberation. The enclosure consisted of a three cubic foot cardboard box lined with egg cartons. The speaker sat in front of the mic box and read the phrase script mounted inside the box. In this manner the speaker’s head was always directed towards the microphone during the recording. The microphone placement within the box was dead center of the back wall with the tail handle of the microphone extending through the back wall to support it without the need of a stand.

As an added noise reduction measure, the ambient room noise sampled on several occasions and was later used to construct an active noise mask in the feature extraction stage of the ASR process.

<u>The Transmission System</u>

The path that the speech signal travels from the microphone to the medium where it is digitally stored can be the source of spectral distortions and noise. The opportunity for signal distortion is much less during the on-line recording process compared to the off-line process. During the on-line recording of speech samples, the signal travels directly from the microphone to the computer sound card where it is digitized. During the off-line process the speech signal travels to the tape deck where it is stored in an analog format on magnetic tape. The signal is then played back from the magnetic tape to the computer sound card for digital storage. To minimize signal distortion during the off-line process, the microphone gain on the tape deck was taped over to prevent random adjustment between speaker sessions. As well, a metal bias cassette was used that provided good frequency response and minimized “tape hiss” noise during playback of the speech signal. No special shielding of the sound card or cables was employed.

<u>Speech Variability</u>

To test an ASR system realistically, it is necessary to record speech samples at various times of the day over an extended period, since the quality of a speaker’s voice varies over time. The RMC Speech Database was constructed with this goal in mind. Speakers were also asked to vary their rate of speech and intonation between sessions to provide a wider range of expression on which to test the robustness of the completed system.

**5.4 Storage Method**

All speech samples were digitized using the computer sound card and then compressed for bulk storage. The analog signals were digitized using a sampling rate of 22050 Hz with 16 bit amplitude resolution and stored in a monaural **PCM (Pulse Code Modulation)** *Windows* “WAV” file format. A filename convention was developed so that the speech sample files could be easily identified. The *MS DOS* operating system restricts the length of filenames to 8 letters, which lead to the adoption of the file naming convention shown in figure 5.1 :

**Figure 5.1 RMC Speech Database File Naming Convention**

The “WAV” files were subsequently compressed using the *WazWav 0.1* compression program, which achieves a lossy 4:1 compression ratio. Several before and after trials with this program revealed that the frequency loss of a **ComPanded** (compressed then expanded) speech sample occurred above the maximum frequency to be used in the feature extraction process. Thus the loss was an acceptable trade off for the 75% reduction in storage space. The compressed “WAV” files are given a “WAZ” extension on the sample file name.

The database was copied to 3.5 inch high density floppy disks as a backup measure to prevent data loss. A multi-volume archive or the database was created using the *ARJ* (lossless) compression program, which enabled an additional 10% reduction in storage space. To reduce the number of disks required to hold the entire database, the *FORM1968* program was used to reformat the disks from the standard 1.44 MB capacity to a 1.92 MB (1968 KB) capacity.

The gains of compressed data storage are evident when one considers that the RMC Speech Database in uncompressed form consists of 2002 files requiring 218.4 MB of uncompressed disk space. After compression using *WazWav* and *ARJ* and disk reformatting using *FORM1968* , the database occupies only 49.3 MB stored on 26 standard 3.5 inch floppy disks!

<u>ASR System Hardware Components</u>

Figure 5.2 summarizes the communication paths between the various hardware components of the ASR system. The circular shapes denote entities that are external to the ASR system, such as the human speaker and the telephone system. Three speech transmission routes are shown between the speaker and the computer sound card. The “on-line recording” route (directly from the microphone to the sound card) introduced the least amount of signal distortion. The “batch recording” route (used in the creation of the RMC Speech Database) introduced a small amount of spectral attenuation due to the interim analog storage of the speech signal. The “telephone recording” route provided the poorest recording quality of the three paths. The telephone filter effect combined with additive noise from the telephone pickup to produce a signal that represented a realistic challenge to the ASR system. The computer hard drive was used as the working storage area for the digitized signals and removable floppy disks were used to store the permanent copies. During on-line recording, computer speakers allowed people to audition their recordings before submitting them for classification.

![Figure 5.2](figures/CHAP5/fig5-2.png)

*Figure 5.2 (vector drawing recovered from rendered page)*

Figures 5.3-M and 5.3-T illustrate the time/amplitude representation of the phrase “***May we all learn a yellow lion roar*** ” batch recorded and stored in MDY12204.WAV, then replayed over a local telephone connection and on-line recorded to file TDY12204.WAV.

Speaker’s Initials

![image2](figures/CHAP5/image2.png)

**Figure 5.3-M Microphone Speech Signal MDY12204.WAV**

![image3](figures/CHAP5/image3.png)

**Figure 5.3-T Telephone Speech Signal TDY12204.WAV**

**5.5 Stage \#2 -- Signal Processing**

In the previous stage, the acoustic speech signals were captured and converted to a digital format. The microphone path speech recordings were sampled at a rate of 22050 Hz and a resolution of 16 bits per sample. Telephone path speech recordings were sampled at a rate of 8000 Hz and a resolution of 16 bits per sample. In this stage, spectral analysis was performed. To accomplish this task, the *Matlab* program “SPECGRAM.M” was invoked using a 512 sample point Hanning window. A 50% window overlap was used for both microphone and telephone recorded speech samples. The resulting temporal resolution of the spectrogram was 11.6 msec for microphone recordings and 32.0 msec for telephone recordings.

The amplitude of the time domain signal was normalized before calculating the spectrogram. All values in the speech sample were adjusted by the ratio of the maximum sample amplitude compared to the maximum amplitude possible in 16 bit representation (2<sup>15</sup>). Endpoint detection of the spoken phrase was not attempted in the time domain signal. The relative level of background noise varied between speech samples and made the use of a fixed noise threshold prone to error.

The program “MAKESPEC.M” was written to build the spectrogram in a piecemeal fashion in order to circumvent the memory limitations of the ASR system hardware. This was accomplished by segmenting the speech sample into chunks one second long, calculating the spectrogram for each chunk, and then concatenating the resulting spectrograms together. To reduce the storage requirements for each spectrogram matrix, only that portion of the spectrogram representing frequencies below 5000 Hz was stored in the output file. The output filename for each spectrogram file incorporated the name of the sound file used to create it. The first letter in the filename was changed to an “S” to indicate it was a spectrogram file. Examples of the spectrogram produced by the “MAKESPEC.M” program are illustrated in figures 5.4 through 5.7 for both the microphone and telephone recorded speech samples. These spectrograms are used in the next stage of the ASR process.

![image4](figures/CHAP5/image4.png) ![image5](figures/CHAP5/image5.png)

**Figure 5.4-M Figure 5.4-T**

**Chunk \#1 of MDY12204.WAV Chunk \#1 of TDY12204.WAV**

![image6](figures/CHAP5/image6.png) ![image7](figures/CHAP5/image7.png)

**Figure 5.5-M Figure 5.5-T**

**Chunk \#2 of MDY12204.WAV Chunk \#2 of TDY12204.WAV**

![image8](figures/CHAP5/image8.png) ![image9](figures/CHAP5/image9.png)

**Figure 5.6-M Figure 5.6-T**

**Chunk \#3 of MDY12204.WAV Chunk \#3 of TDY12204.WAV**

![image10](figures/CHAP5/image10.png) ![image11](figures/CHAP5/image11.png)

**Figure 5.7-M Figure 5.7-T**

**Spectrogram of MDY12204.WAV Spectrogram of TDY12204.WAV**

![image12](figures/CHAP5/image12.png) ![image13](figures/CHAP5/image13.png)

**Figure 5.8-M Figure 5.8-T**

**Microphone Noise Mask Telephone Noise Mask**

![image14](figures/CHAP5/image14.png) ![image15](figures/CHAP5/image15.png)

**Figure 5.9-M Figure 5.9-T**

**Noise Masking of MDY12204.WAV Noise Masking of TDY12204.WAV**

**5.6 Stage \#3 -- Feature Extraction**

This stage is concerned with the isolation of linguistic features within the spectrograms of the speech samples. Non-relevant data is discarded to reduce the load of subsequent calculations. The following text describes the formant extraction process carried out by the “FORMANT3.M” program written as part of this thesis work. The first three formants are used to represent the spoken phrase to the Fuzzy ART Map ANN for identification and classification. Section 5.7 will cover the specifics of the feature representation used to accomplish this task. In order for the reader to gain an appreciation of the inherent difficulty of the ASR task over telephone lines, figures illustrating the processing of both microphone and telephone recorded speech spectrograms are included. Only the portion of the spectrogram corresponding to the telephone bandwidth (300 Hz to 3300 Hz) was considered in the feature extraction process.

**5.6.1 Noise Masking**

A noise mask was constructed using background noise samples as a means of filtering out the background noise evident in the spectrograms of the speech samples. To build the noise mask, a spectrogram of one second of recorded background noise is calculated. Next, the maximum amplitude of each frequency band in the noise spectrogram is identified and used to produce a masking vector. This spectra of maximum noise amplitudes is subtracted from each time-slice of the speech sample spectrogram calculated above, thus removing any possible contributions of background noise. Any negative values resulting from the previous calculations are reset to a zero value. The use of this noise masking technique improved the identification of the formant frequencies. The masking vectors are shown in figure 5.8-M and figure 5.8-T. The effectiveness of this masking technique can be seen in the noise reduced spectrograms shown in figure 5.9-M and figure 5.9-T.

**5.6.2 Silence Reduction**

Silence reduction from the speech sample is performed based on a relative **STE (short term energy)** curve derived from the sample’s spectrogram. Each point on the curve corresponds to the sum of the frequency amplitudes for a given time-slice of the spectrogram. Since formants appear only in voiced speech it is desirable to isolate only the voiced portions of the speech sample in order to improve formant tracking. Since voiced speech has higher relative energy compared to unvoiced speech, all time-slices of the spectrogram whose STE value falls below a relative threshold (set to a percentage of the maximum STE energy) are discarded. Figures 5.10-M, 5.10-T, 5.11-M and 5.11-T illustrate the spectrograms of a microphone and telephone speech sample before and after the application of this silence reduction technique.

**5.6.3 Frequency Amplitude Normalization (Pre-emphasis)**

When considering the human voice, there is a general drop in the average amplitude of a frequency as frequency increases. This effect precludes the technique of simply picking formant peaks based on absolute frequency amplitude. In order to counter this effect, the amplitudes of all frequencies are amplified by an amount proportional to their relative frequency octave according to equation 5.1. This formula was derived through experimentation with microphone recorded speech samples. Ideally an adaptive gain function should be used (particularly for use with telephone channel speech) but this item has been left for future work. Figures 5.12-M and 5.12-T illustrate the effect of the octave enhancement technique.

**Octave Gain (SFR) = 10 ^ ( log <sub>2</sub> (SFR) / 5) (5.1)**

where SFR = Spectrogram Frequency Row number

![image16](figures/CHAP5/image16.png) ![image17](figures/CHAP5/image17.png)

**Figure 5.10-M Figure 5.10-T**

**STE Curve for MDY12204.WAV STE Curve for TDY12204.WAV**

![image18](figures/CHAP5/image18.png) ![image19](figures/CHAP5/image19.png)

**Figure 5.11-M Figure 5.11-T**

**Silence Reduced MDY12204.WAV Silence Reduced TDY12204.WAV**

![image20](figures/CHAP5/image20.png) ![image21](figures/CHAP5/image21.png)

**Figure 5.12-M Figure 5.12-T**

**Octave Enhanced MDY12204.WAV Octave Enhanced TDY12204.WAV**

**5.6.4 Peak Picking**

For each time-slice within the octave enhanced spectrogram, the local frequency maxima are identified through a “peak picking” process. For each frequency band within a given spectrogram time-slice, the amplitude of the frequency is compared to those of its neighbours within a fixed viewing window, where the frequency band in question is located at the center of the window. If it is the maximum value in the window, then it is a local maximum. Once all the local maxima are identified, only the ones with the greatest amplitudes are retained as candidates for the location of the formant frequencies. The 3 peaks with the largest amplitudes within a given time-slice are used to estimate of the frequency locations of the first three formants. Figures 5.13-M and 5.13-T illustrate the peaks and initial formant estimates resulting from this technique.

**5.6.5 Formant Screening**

The screening process rejects time-slices from the spectrogram which have erroneous formant frequency estimates. If the first formant frequency is estimated above 1200 Hz or if there are not three formant estimates for a given time-slice, then the time-slice is ignored. What remains is a series of “legal” formant estimates, which are then stored as formant vectors. All formant files are given the initial letter “F” and reflect the name of the spectrogram file from which they were produced (e.g., spectrogram file sdy12204.mat is used to create formant file fdy122042.mat). Figures 5.14-M and 5.14-T illustrate the formants remaining after the screening process. Figures 5.15-M and 5.15-T show the final formant vectors that are saved to file.

![image22](figures/CHAP5/image22.png) ![image23](figures/CHAP5/image23.png)

**Figure 5-13-M Figure 5.13-T**

**Local Maxima in MDY12204.WAV Local Maxima in TDY12204.WAV**

![image24](figures/CHAP5/image24.png) ![image25](figures/CHAP5/image25.png)

**Figure 5.14-M Figure 5.14-T**

**Formants in MDY12204.WAV Formants in TDY12204.WAV**

![image26](figures/CHAP5/image26.png) ![image27](figures/CHAP5/image27.png)

**Figure 5.15-M Figure 5.15-T**

**Formant Vectors in MDY12204.WAV Formant Vectors in TDY12204.WAV**

**5.7 Feature Representation**

In order to input the extracted formant vectors to the Fuzzy ART Map neural network, they must be combined into a single vector of fixed length, and it must be normalized within the range of fuzzy values. Several representations of the formant vectors were tested, including:

- Tri Formant Vector (TFV),

- Bi Formant Ratio Vector (BFRV),

- Normalized Polar Angle (NPA), and

- Tri Formant Ratio Vector (TFRV).

Each of these feature vector representations is expanded upon in the following discussion. As before, both microphone and telephone speech samples are illustrated to compare the relative effectiveness of each representation technique.

**5.7.1 Tri Formant Vector (TFV) Representation**

A TFV representation, given by equation 5.2, was created by concatenating the three formant vectors together. The TFV was then normalized by dividing by 3300 Hz (the maximum possible frequency value in the formant extraction process). Finally, **LTW (linearly time warping)** was performed to stretch or compress the vector to a standard length of 500 units. The main disadvantage of this representation is that it is relatively speaker age and gender dependent due to the use of absolute frequency values to represent the phonemes spoken in the speech sample. Figures 5.16-M and 5.16-T illustrate the normalization and LTW of this representation.

**TFV = \[ *F*<sub>3</sub>, *F*<sub>2</sub>, *F*<sub>1</sub> \] (5.2)**

![image28](figures/CHAP5/image28.png)

**Figure 5.16-M Tri Formant Vector Representation of MDY12204.WAV**

![image29](figures/CHAP5/image29.png)

**Figure 5.16-T Tri Formant Vector Representation of TDY12204.WAV**

**5.7.2 Bi Formant Ratio Vector (BFRV) Representation**

The BFRV, given by equation 5.3, was constructed from the concatenation of two formant ratio vectors. The standard length used to perform LTW for the BFRV representation was only 300 elements, which substantial reduced memory storage needs compared to that of the TFV representation. As well, the use of formant ratios dramatically reduced speaker dependence. The technique used to normalize the BFRV is discussed in the next section.

**BFRV = \[ (*F*<sub>3</sub>/*F*<sub>2</sub>) , (*F*<sub>2</sub>/*F*<sub>1</sub>) \] (5.3)**

**5.7.3 Normalized Polar Angle (NPA) Representation**

The formant ratios shown above represent the slope of a line between the origin and the intersection point of the numerator and denominator in Cartesian coordinates. Experimentation revealed a non-uniform distribution of the formant ratios slopes numbers for English phonemes. As well, the normalization of such slope numbers to fuzzy range values was difficult (an arbitrarily high value had to be chosen). These problems were not evident when the formant ratios were expressed with polar coordinates. Separation between the formant ratios of different phonemes was improved and the maximum polar angle (90 degrees or 0.5π radians) made normalization easier. The conversion of the BFRV from Cartesian to NPA form is given by equation 5.4. The effect this conversion has on the BFRV representation can be seen in figures 15.17-M and 5.17-T.

**NPA(BFRV) = arctan(BFRV) / 0.5π (5.4)**

![image30](figures/CHAP5/image30.png)

**Figure 5.17-M Bi Formant Ratio Vector Representation of MDY12204.WAV**

![image31](figures/CHAP5/image31.png)

**Figure 5.17-T Bi Formant Ratio Vector Representation of TDY12204.WAV**

**5.7.4 Tri Formant Ratio Vector (TFRV) Representation**

The addition of a third formant ratio \[***F*<sub>3 </sub>**/***F*<sub>1</sub>**\] vector to the BFRV (equation 5.3) produces the TFRV representation given by equation 5.5. This extension to the BFRV improves the distinction between feature vectors representing similar sounding vowels. An example given in \[Mil89\] is the vowel pair AA (hot) and AO (caught). Another example is UH (full) and UW (good). Figure 4.2 illustrates how the **F<sub>3</sub>/F<sub>1</sub>** ratio helps discriminate these vowels compared to the use of only the **F<sub>3</sub>/F<sub>2</sub>** and **F<sub>2</sub>/F<sub>1</sub>** ratios (as in the BFRV). The TFRV and its NPA representation are shown in figures 5.18-M and 5.18-T.

**TFRV = \[ (*F*<sub>3</sub>/*F*<sub>2</sub>), (*F*<sub>2</sub>/*F*<sub>1</sub>), (*F*<sub>3</sub>/*F*<sub>1</sub>) \] (5.5)**

**5.8 Stage \#4 -- Utterance Classification**

In this stage, a Fuzzy ART Map ANN is used to classify the vectors representing the speech samples that were produced in stage \#3. Figures 5.19-M and 5.19-T present the classification process in three plots. The first plot shows the TFRV representation of the speech sample that is presented to the network. The second plot shows the matching vector retrieved by the Fuzzy ART Map ANN in response to the network input. The last plot in each figure illustrates an overlay comparison of the two matching vectors for inspection.

Figure 5.20 summarizes the ASR system software components responsible for carrying out the four stages of the ASR process. The program code for the *Stdemo* script files is included in annex B. The program code for the *Matlab* script files can be found in annexes C, D, and E.

The remainder of this section describes the design of software that simulates the neural network and the settings of the network parameters used to achieve various results. Network modifications, training parameters, and information retrieval are discussed.

![image32](figures/CHAP5/image32.png)

**Figure 5.18-M Tri Formant Ratio Vector Representation of MDY12204.WAV**

![image33](figures/CHAP5/image33.png)

**Figure 5.18-T Tri Formant Ratio Vector Representation of TDY12204.WAV**

![image34](figures/CHAP5/image34.png)

**Figure 5.19-M Fuzzy ART Map Recognition of MDY12204.WAV**

![image35](figures/CHAP5/image35.png)

**Figure 5.19-T Fuzzy ART Map Recognition of TDY12204.WAV**

![image36](figures/CHAP5/image36.png)

**5.8.1 Modifications to the Fuzzy ART Map ANN**

The feature classifier is implemented in the program FARTMAPT.M. It is based on the description of the Fuzzy ART Map neural network in \[Car92\]. Since the architecture is being simulated in software, certain simplifications of the processing algorithm were possible. The first modification involves the “supervising” Fuzzy ART<sub>B</sub> module which produces the target output for the Fuzzy ART<sub>A</sub> module. It has been replaced by a mapping matrix which serves to label the output nodes of the Fuzzy ART<sub>A</sub> module with the corresponding desired target vector ***b*** . Figure 5.21 is a reproduction of figure 3.4 from \[Car92\] which has been modified to reflect this simplification.

![Figure 5.21](figures/CHAP5/fig5-21.png)

*Figure 5.21 (vector drawing recovered from rendered page; the conversion damaged its layout, see the PDF or the printed original)*

In figure 5.21, the vector ***a*** represents the speech feature vector being classified by the Fuzzy ART module while vector ***b*** represents the correct classification label of vector a . When vector ***a*** causes an output node to become committed, the corresponding row of the mapping matrix is initialized with the value of vector ***b***, thus effectively labeling the output node of the Fuzzy ART module.

A second modification addresses the problem of identifying adequate network memory capacity when initializing the size of the network weight matrix. Due to the local manner in which the LTM traces are stored in the network memory , the dynamic expansion of the network memory during training is possible. The ANN program was modified to append 10 new columns to the network weight matrix when it began to reach full capacity.

**5.8.2 Network Training**

The simplification described above is possible because of the Fuzzy ART modules parameters are set for fast learning and no recoding of output categories. This means that the centroids of new clusters are defined by the vector that caused its creation and that the LTM weight remain fixed thereafter. The stability that results enables the rapid single epoch learning of training sets, since there is no adaptation or “drift” of the cluster centroid with the exposure to subsequent input. In light of its fixed nature in this implementation, a more apt description for the cluster centroid would be a **classification landmark**, since it does not reflect the center of a cluster of points in feature space. The landmark vector defines the center of a classification zone whose radius is defined by the vigilance parameter distance measure.

![image37](figures/CHAP5/image37.png)

The network learns the mapping of the feature space by storing only those feature vectors that create new landmark points in feature space. There are two possible scenarios. First, a new feature vector defines a point outside of all existing classification zones as defined by the baseline vigilance parameter. In this case the vector is automatically considered a new landmark based solely on its distance from all other landmarks. In the second scenario, a new feature vector defines a point within a conflicting classification zone or several overlapping zones (where the zone size is defined by the baseline value of the vigilance parameter). In the second case, the network automatically begins incrementing the baseline vigilance parameter in a **match tracking** process that identifies and compares the classification of the closest landmark to that of the new feature vector. A classification mismatch results in the formation of a new landmark. This learning process is efficient in that it only stores those vectors required to define the boundary areas between the different classifications in feature space. The number of landmarks required to map out these boundaries is directly proportional to the similarity of the classifications to be learned.

**5.8.3 Information Retrieval**

The network recognizes feature vectors based on the nearest landmark defined in the networks memory. Since the network must compare the feature vector under consideration to all of the landmark vectors stored in its memory map, the speed of information retrieval is decreased as the size of the network memory grows. Due to the trade-off of speed and accuracy that comes with increased network training and increased memory size, it is important that the feature vectors be represented to the network in a manner that minimizes vector size and maximizes inter-classification distances. The aim is to require fewer vectors to define the landmarks of the classification boundaries in feature space, and to reduce the memory required to store each vector. The judicious selection of speech features that can efficiently represent the linguistic message is important here. The use of the TFRV to identify phoneme content is an example of such a representation.

**5.9 Chapter Summary**

This chapter investigates the applicability of a Fuzzy ART Map ANN to the ASR task through the implementation of an ASR system that incorporates a Fuzzy ART Map ANN as its recognition component. The system is capable of performing speaker and language independent discrete phrase recognition over public telephone lines, based on the time series of formant ratios. This ASR system is presented within the framework of the four stage ASR process presented earlier in chapter four:

- First, the **sound recording stage** describes the apparatus and method used to capture the speech signal as well as the creation and storage of the RMC Speech Database that was subsequently used to train and test the ASR system;

- Second, the **signal processing stage** deals with the spectral analysis of the recorded speech samples and the production of their spectrogram representations;

- Third, the **feature extraction stage** illustrates the steps required to identify the formants in the spectrogram representations produced in stage two and also deals with the representation of these features to the Fuzzy ART Map ANN for recognition. Both microphone and telephone recorded speech are shown to compare the effectiveness of the techniques used in both transmission channels; and

- Fourth, the **utterance classification stage** discusses the Fuzzy ART Map ANN program regarding software simplifications, the tuning of the training parameters, and its information retrieval characteristics.

This chapter represents the core work of this thesis. It explains the rationale for the design decisions incorporated in the Fuzzy ART Map ASR system (the source code for the software components is contained separately in the annexes). The effectiveness of this system is tested next in chapter six.
