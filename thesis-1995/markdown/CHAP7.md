**CHAPTER SEVEN**

**CONCLUDING REMARKS**

**7.1 Thesis Summary**

An ASR (automatic speech recognition) system was developed which incorporated a Fuzzy ART (Adaptive Resonance Theory) Map ANN (artificial neural network) as the component that classifies and recognizes speech samples presented to the system. The process of converting the spoken acoustic signal into a representation suitable for input to the recognizer component was described in terms of a four stage ASR process which included sound recording, spectral analysis, feature extraction and representation, and utterance classification.

Both microphone and telephone were used in the sound recording stage in order to measure and compare the system’s performance on both transmission channels. The acoustic signals were digitized and converted into spectrogram form. Noise reduction, silence reduction and frequency amplitude normalization were carried out prior to tracking the first three speech formants. These formant were subsequently combined in a TFRV (tri formant ratio vector) representation that dramatically reduced the differences between the representation of the speech phrase due to speaker age and gender. The TFRV was then normalize to the range of fuzzy values (from zero to one) and LTW (linearly time warping) was performed to stretch or compress the TFRV to the size of the input layer of the Fuzzy ART Map ANN recognizer.

The combination of the TFRV speech signal representation and the Fuzzy ART Map ANN recognizer produced an ASR system capable of a speaker dependent recognition rate of 98.2% for microphone recorded speech and 91.5% for the same speech samples played over a noisy telephone line. The speaker independent rates were about 4% lower. Testing was performed using the RMC Speech Database, which contained eight test phrases chosen from the literature for their diverse phonetic representation. The voices of the ten males and one female used in the testing, were recorded in a relatively noisy computer room over a period of four months in order to capture the variability of human speech.

A multi-layer feedforward ANN trained with the backpropagation algorithm (aided by a momentum term and an adaptive learning rate) was used as a benchmark in side by side comparison tests with the Fuzzy ART Map ANN. Its performace was approximately 5% lower than that of the Fuzzy ART Map ANN while the time required to train it was considerably longer.

**7.2 Conclusion**

The goal of this research was to investigate the applicability of the Fuzzy ART Map ANN to the task of Automatic Speech Recognition. **The development of the ASR system described in Chapter Five <u>demonstrates</u> that the Fuzzy ART Map ANN can be used to perform speech recognition, while the** **testing documented in Chapter Six <u>establishes</u> that the Fuzzy ART Map ANN can perform ASR more effectively than the ANN used in the benchmark tests** in the following ways:

- Its rapid learning capability **significantly reduced system training time** and produced **more efficient speech recognition**;

- Its localized (vector) data storage s**upports modular packaging and reconfiguration of active vocabulary**;

- Its use of a unit (ones) matrix to initialize its network memory **eliminates the uncertainty associated with random selection of starting weights** required by the benchmark ANN; and

- Unlike the benchmark ANN, whose fixed network size limited its storage capacity, the Fuzzy ART Map ANN **network expands in response to the need to learn “new” data** (i.e., significantly different from that which it already has stored in its memory).

**7.3 Future Work**

Improvements to the ASR system developed in this thesis stem from the error analysis in section 6.4.5. The development of an frequency amplitude normalization technique that adapts to the spectral attenuation of a given telephone connection would greatly improve the system’s recognition performance in that area. Test scores may be improved by using on-line testing to take advantage of noise masks tailored to each speech sample. For telephone speech samples, temporal resolution could be improved to detect rapid changes in the speech signal through the use of a higher sampling rate, similar to that used for microphone recorded speech. Finally, the system could be made to execute faster if it was compiled as an executable program.

**REFERENCES**

\[Ain88\] W.A. Ainsworth, <u>Speech Recognition By Machine</u>, Peter Peregrinus Ltd, London, United Kingdom, 1988.

\[Alw85\] R.G. Alward, <u>A Speech Recognizer Based on Energy and Zero Crossing</u>, M.Eng. Thesis, Royal Military College of Canada, Jun 1985.

\[Bar57\] H.L. Barney and K.K. Dunn, “Speech Analysis”, pp 180-201 in <u>Manual Of Phonetics</u> , L. Kaiser (ed), North-Holland Publishing Co, Amsterdam, 1957.

\[Car87a\] Gail A. Carpenter and Stephen Grossberg, "A massively parallel architecture for a self-organizing neural pattern recognition machine”, Computer Vision Graphics and Image Processing, Vol.37, 1987, pp. 54-115.

\[Car87b\] Gail A. Carpenter and Stephen Grossberg, "ART 2 : Self-organization of stable category recognition codes for analog input patterns",Applied Optics, Dec. 1, 1987,

pp. 4919-4930

\[Car88\] Gail A. Carpenter and Stephen Grossberg, "The ART of Adaptive Pattern Recognition by a Self-Organizing Neural Network", IEEE Computer, pp 77-88, Mar 1988.

\[Car90\] Gail A. Carpenter and Stephen Grossberg,”ART3: Hierarchical search using chemical transmitters in self-organizing pattern recognition architectures”, Neural Networks, vol. 3, pp. 129-152, 1990

\[Car91\] Gail A. Carpenter, Stephen Grossberg, D.B. Rosen, “Fuzzy ART: Fast stable learning and categorization of analog patterns by an adaptive resonance system”, Neural Networks, vol. 4, pp. 759-771, 1991.

\[Car92\] Gail A. Carpenter, Stephen Grossberg, John H. Reynolds, Natalya Markuzon and David B. Rosen, "Fuzzy ARTMAP: A Neural Network Architecture for Incremental Supervised Learning of Analog Multidimensional Maps", IEEE Trans. on Neural Networks, vol.3, pp 698-713, Sep 1992.

\[Col95\] Ron Cole et al.,”The Challenge of Spoken Language Systems: Research Directions for the Nineties”, IEEE Trans. on Speech and Audio Processing, vol 3, Jan 1995

\[CSN95\] Andrew Hunt, Barry Arons, Joe Campbell, Oliver Jakobs, Sonja Kowalewski, Tony Robinson, “Frequently Asked Questions”, Comp.Speech Newsgroup on Usenet, available on Internet via anonymous FTP from rtfm.mit.edu:/pub/usenet/news.answers/comp-speech-faq

\[Dix79\] N. Rex Dixon and Thomas B. Martin (eds), <u>Automatic Speech & Speaker Recognition</u>, IEEE Press, New York, New York, 1979.

\[Dod76\] George R. Doddington, “Personal Identity Verification Using Voice”, pp 398-402, in \[Dix79\]

\[Fur89\] Sadaoki Furui, <u>Digital Speech Processing, Synthesis, and Recognition</u>, Marcel Dekker, New York, New York, 1989.

\[Gro76\] Stephen Grossberg, “Adaptive pattern classification and universal recoding, II: Feedback, expectation, oflaction, and illusions”, Biological Cybernetics, No. 23, 1976, pp. 187-202

\[Gro82\] Stephen Grossberg, “Associative and Competitive Principles of Learning and Development - The Temporal Unfolding and Stability of STM and LTM Patterns”, in <u>Competition and Cooperation in Neural Nets</u>, Springer-Verlag, New York, 1982, pp295 - 341.

\[Har72\] R.R.K. Hartmann and F.C. Stork, <u>Dictionary Of Language And Linguistics</u>, Applied Science Publishers Ltd, London, England, 1972.

\[Lad75\] Peter Ladefoged, <u>A Course in Phonetics</u>, Harcourt Brace Jovanovich Inc., New York, New York, 1975.

\[Mar90\] Alianna Maren, Craig Harston, and Robert Pap, <u>Handbook of Neural Computing Applications</u>, Academic Press, San Diego, California, 1990.

\[Mil89\] James D. Miller,”Auditory-perceptual interpretation of the vowel”, J. Acoust. Soc. Am. 85(5), May 1989, pp 2114-2133

\[Mur73\] Gerald M. Murch, <u>Visual And Auditory Perception</u>, The Bobbs-Merrill Company, Indianapolis, Indiana, 1973, pp 105-110

\[Sam76\] Marvin R. Sambur, “Speaker Recognition Using Orthogonal Linear Prediction”, section IV, page 407 in \[Dix79\]

\[Whi76\] George M. White, “Speech Recognition: A Tutorial Overview”, pp 87-99 in \[Dix79\].

\[You85\] N.R. Young, <u>A Speech Recognizer Based on Energy Zero Crossing and Linear Prediction</u>, M.Eng. Thesis, Royal Military College of Canada, Dec 1985.

\[Zad88\] Lotfi A. Zadeh, “Fuzzy Logic”, IEEE Computer, pp 83-93, Apr 1988.

\[Zur92\] Jacek M. Zurada, <u>Introduction to Artificial Neural Systems</u>, West Publishing, St. Paul, MN, 1992.
