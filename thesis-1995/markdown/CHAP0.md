**A FUZZY ART MAP NEURAL NETWORK SPEECH RECOGNITION SYSTEM**

**BASED ON**

**FORMANT RATIOS**

**by**

**Captain D.P. Young, CD, B.Sc., rrmc**

**Canadian Forces**

**A Thesis**

**Presented to the School of Graduate Studies**

**in the**

**Department of Electrical and Computer Engineering**

**The Royal Military College of Canada**

**Kingston, Ontario**

**In partial fulfillment of the requirements for the degree**

**Master of Engineering**

**May 1995**

\(c\) Copyright by D.P. Young 1995

This thesis may be used within the Department of National Defense but copyright for open publication remains the property of the author.

**ABSTRACT**

This thesis investigates the applicability of a Fuzzy ART (Adaptive Resonance Theory) Map ANN (Artificial Neural Net) to the task of ASR (Automatic Speech Recognition). The motivation for this work stems from two observations. First, from an Internet discussion group survey, it is evident that the Fuzzy ART Map ANN is being applied to tasks in a variety of disciplines. These disciplines include Computer Science, Geology, and Medical Science, as well as Mechanical, Civil and Software Engineering. However, a survey of the literature has turned up no references to the application of the Fuzzy ART Map ANN to the ASR task. Secondly, ASR is a vital component of speech understanding systems that promise to improve the ease with which humans can interact with computers. Spoken communication with computers will allow users to remotely access computer based services through standard telephone links. This would make every telephone a potential computer terminal. As well, many of the world telephones use PC (Pulse Code) signaling and hence more sophisticated services that require DTMF (Dual Tone Multi-Frequency) signaling are not yet available. It is for these reasons that the development of ASR over telephone channels is imperative.

This thesis provides some basic background information about ANNs, ART, fuzzy logic, ASR, and formant ratio theory. It then describes how a Fuzzy ART Map ANN is implemented as the recognizer component of an ASR system to learn and identify formant ratio vectors extracted from spoken phrases. The audio frequency analysis is limited to a 300 to 3300 Hz bandwidth so that the system may operate on verbal commands over telephone channels. The recognition accuracy of this system is then tested using a database with eight phonetically rich phrases. The database was recorded by twelve males and two females over a four month period using a high quality microphone in a computer room environment. The tests are repeated using a multi-layer feedforward backpropagation ANN as the recognizer component to provide a relative performance benchmark. Finally, the performance of the Fuzzy ART Map ASR system is tested over the telephone channel.

**ACKNOWLEDGMENTS**

I wish to express sincere appreciation to my thesis advisor, Dr. Paul E. Allard, for his guidance and constructive criticism.

I would also like to thank the following people who volunteered their time and efforts to help build the RMC Speech Database that was used extensively throughout this thesis:

> Ann Hopkinson, Bernard Tremblay, Colin Wortley, Danielle Bossart, David Gravel, Don Hamilton, Ian Hawes, Jean Dolbec, Liam Porter, Larry Reeves, Murray Johnson, Matthew Oliver, and Waldemar Borys.

Finally, I would like to acknowledge the support of my family -- Donna, Cassandra, Kody and Keegan. They have made this effort possible.

**VITA**

**Name**:

> David Peter Young

**Born**:

> Sudbury, Ontario, 1963
>
> Son of Norman and Helen Young

**Education**:

> Primary and Secondary School in Sudbury, Ontario. Completed Grade 13 in 1982.
>
> Royal Roads Military College, Victoria, British Columbia, 1982-86. Awarded Bachelor of Science Degree in Computer Science and Physics in 1986.

**Experience**:

> Aerospace Engineering Officer, Canadian Forces from 1986 to date including:

- Programmer/Analyst, Aurora Software Development Unit (ASDU), CFB Greenwood, Nova Scotia, 1986.

- Staff Officer Automated Data for Aerospace Maintenance (ADAM), Air Command HQ, Winnipeg, Manitoba, 1987-88.

- Directing Staff Canadian Forces Officer Candidate School (CFOCS), CFB Chilliwack, British Columbia, 1988-90.

- Aircraft Maintenance Control and Records Officer (AMCRO), 419 Tac F(T) Sqn, CFB Cold Lake, Alberta, 1990-93.

- Post Graduate Student, Royal Military College of Canada, Kingston, Ontario, 1993-95

**TABLE OF CONTENTS**

|  |  |
|----|----|
| Title Page .............................................................................................................. | i |
| Abstract ................................................................................................................. | ii |
| Acknowledgments .................................................................................................. | iii |
| Vita ....................................................................................................................... | iv |
| Table of Contents ................................................................................................... | v |
| List of Figures ........................................................................................................ | x |
| List of Tables ......................................................................................................... | xii |

**One Introduction**

|  |  |  |
|:---|----|----|
| 1.1 | Introductory Comments ............................................................................... | 1 |
| 1.2 | Thesis Outline ............................................................................................. | 3 |

**Two Neural Networks Overview**

|  |  |  |
|----|----|----|
| 2.1 | Introduction ................................................................................................ | 5 |
| 2.2 | ANN Programs ........................................................................................... | 7 |
| 2.3 | The Artificial Neuron Model ....................................................................... | 7 |
| 2.4 | Differentiating Between ANNs .................................................................... | 10 |
| 2.4.1 | ANN Architecture ....................................................................................... | 10 |
| 2.4.2 | ANN Learning Process ............................................................................... | 10 |
| 2.4.3 | ANN Recall Process ................................................................................... | 11 |
| 2.4.4 | Major ANN Architectures ........................................................................... | 13 |
| 2.5 | Backpropagation Learning in Multi-layer Feedforward ANNs ...................... | 14 |
| 2.6 | Chapter Summary ....................................................................................... | 15 |

**Three The Fuzzy Art Map ANN**

<table>
<colgroup>
<col style="width: 8%" />
<col style="width: 85%" />
<col style="width: 0%" />
<col style="width: 6%" />
</colgroup>
<tbody>
<tr>
<td>3.1</td>
<td colspan="2">Introduction to Adaptive Resonance Theory .................................................</td>
<td>16</td>
</tr>
<tr>
<td>3.2</td>
<td colspan="2">The Origin of ART Development ................................................................</td>
<td>17</td>
</tr>
<tr>
<td>3.3</td>
<td>Competitive Learning Models .....................................................................</td>
<td colspan="2">19</td>
</tr>
<tr>
<td>3.4</td>
<td>Stability Issues ............................................................................................</td>
<td colspan="2">21</td>
</tr>
<tr>
<td>3.5</td>
<td>The ART Cognitive Process ........................................................................</td>
<td colspan="2">21</td>
</tr>
<tr>
<td>3.6</td>
<td>When Does Adaptive Resonance Occur? .....................................................</td>
<td colspan="2">23</td>
</tr>
<tr>
<td>3.7</td>
<td>The ART Advantage ...................................................................................</td>
<td colspan="2">24</td>
</tr>
<tr>
<td>3.8</td>
<td>Fuzzy Logic ...............................................................................................</td>
<td colspan="2">25</td>
</tr>
<tr>
<td>3.8.1</td>
<td>Parallels in Fuzzy Logic and ANNs .............................................................</td>
<td colspan="2">25</td>
</tr>
<tr>
<td>3.8.2</td>
<td>The Proposition ..........................................................................................</td>
<td colspan="2">26</td>
</tr>
<tr>
<td>3.8.3</td>
<td>The Possibility Distribution Defined By Proposition .....................................</td>
<td colspan="2">27</td>
</tr>
<tr>
<td>3.8.4</td>
<td>The Quantified Proposition .........................................................................</td>
<td colspan="2">27</td>
</tr>
<tr>
<td>3.8.5</td>
<td>Fuzzy Logic Applied To Adaptive Resonance Theory .................................</td>
<td colspan="2">28</td>
</tr>
<tr>
<td>3.9</td>
<td>The Fuzzy ART ANN ................................................................................</td>
<td colspan="2">29</td>
</tr>
<tr>
<td>3.10</td>
<td>An Eight Stage Fuzzy ART Algorithm ........................................................</td>
<td colspan="2">30</td>
</tr>
<tr>
<td>3.11</td>
<td>The Fuzzy ART Map ANN ........................................................................</td>
<td colspan="2">35</td>
</tr>
<tr>
<td>3.12</td>
<td>Chapter Summary ......................................................................................</td>
<td colspan="2">38</td>
</tr>
</tbody>
</table>

**Four Automatic Speech Recognition**

|  |  |  |
|----|----|----|
| 4.1 | Introduction ............................................................................................... | 39 |
| 4.2 | ASR System Classification ........................................................................ | 39 |
| 4.2.1 | Speaker Dependency ................................................................................. | 40 |
| 4.2.2 | Manner of Speech ..................................................................................... | 40 |
| 4.2.3 | Active Vocabulary Size ............................................................................ | 41 |
| 4.3 | A Four Stage ASR Process ........................................................................ | 42 |
| 4.4 | Applicable ASR Research Areas ................................................................ | 44 |
| 4.4.1 | Rapid Training .......................................................................................... | 44 |
| 4.4.2 | Robust Speech Recognition ....................................................................... | 44 |
| 4.4.2.1 | The Acoustic Environment ......................................................................... | 45 |
| 4.4.2.2 | The Microphone System ............................................................................ | 45 |
| 4.4.2.3 | The Transmission Channel ......................................................................... | 46 |
| 4.4.2.4 | The Variability of Speech .......................................................................... | 47 |
| 4.5 | Human Speech Communication ................................................................. | 49 |
| 4.5.1 | Speech Production ..................................................................................... | 49 |
| 4.5.2 | Speech Perception ..................................................................................... | 50 |
| 4.6 | Formant Ratio Theory ............................................................................... | 51 |
| 4.7 | Chapter Summary ...................................................................................... | 55 |

**Five A Fuzzy Art Map ASR System**

|  |  |  |
|----|----|----|
| 5.1 | Introduction ............................................................................................... | 57 |
| 5.2 | Stage \#1 -- Speech Recording .................................................................... | 58 |
| 5.3 | Recording Method and Apparatus .............................................................. | 60 |
| 5.4 | Storage Method ......................................................................................... | 62 |
| 5.5 | Stage \#2 -- Signal Processing ..................................................................... | 67 |
| 5.6 | Stage \#3 -- Feature Extraction .................................................................... | 70 |
| 5.6.1 | Noise Masking .......................................................................................... | 70 |
| 5.6.2 | Silence Reduction ...................................................................................... | 71 |
| 5.6.3 | Frequency Amplitude Normalization (Pre-emphasis) .................................. | 71 |
| 5.6.4 | Peak Picking ............................................................................................. | 73 |
| 5.6.5 | Formant Screening ..................................................................................... | 73 |
| 5.7 | Feature Representation .............................................................................. | 75 |
| 5.7.1 | Tri Formant Vector (TFV) Representation .................................................. | 75 |
| 5.7.2 | Bi Formant Ratio Vector (BFRV) Representation ....................................... | 77 |
| 5.7.3 | Normalized Polar Angle (NPA) Representation .......................................... | 77 |
| 5.7.4 | Tri Formant Ratio Vector (TFRV) Representation ...................................... | 79 |
| 5.8 | Stage \#4 -- Utterance Classification ............................................................ | 79 |
| 5.8.1 | Modifications to the Fuzzy ART Map ANN ............................................... | 83 |
| 5.8.2 | Network Training ...................................................................................... | 83 |
| 5.8.3 | Information Retrieval ................................................................................. | 85 |
| 5.9 | Chapter Summary ...................................................................................... | 86 |

**Six Experimental Results**

|  |  |  |
|----|----|----|
| 6.1 | Introduction ............................................................................................... | 87 |
| 6.2 | Testing Goals ............................................................................................ | 87 |
| 6.2.1 | Testing Control Measures .......................................................................... | 88 |
| 6.2.2 | Testing Methods ........................................................................................ | 88 |
| 6.3 | Test Results .............................................................................................. | 91 |
| 6.4 | Evaluation Of Results ................................................................................ | 97 |
| 6.4.1 | Benchmark ANN Performance Comparison ............................................... | 98 |
| 6.4.2 | Speaker Dependency Performance Comparison .......................................... | 98 |
| 6.4.3 | Transmission Channel Performance Comparison ........................................ | 98 |
| 6.4.4 | Feature Representation Performance Comparison ....................................... | 99 |
| 6.4.5 | Error Analysis ........................................................................................... | 99 |
| 6.5 | Chapter Summary ..................................................................................... | 102 |

**Seven Concluding Remarks**

|  |  |  |
|----|----|----|
| 7.1 | Thesis Summary ........................................................................................ | 103 |
| 7.2 | Conclusions .............................................................................................. | 104 |
| 7.3 | Future Work ............................................................................................. | 105 |

|  |  |
|----|----|
| References ............................................................................................................... | 106 |

**Annexes**

|         |                                             |
|---------|---------------------------------------------|
| Annex A | ASR System Hardware and Software            |
| Annex B | ASR Demo Program Code (*Stdemo Player 1.5*) |
| Annex C | MAKESPEC.M Program Code (*Matlab 4.0*)      |
| Annex D | FORMANT3.M Program Code (*Matlab 4.0*)      |
| Annex E | FARTMAPT.M Program Code (*Matlab 4.0*)      |
| Annex F | BPMAPPER.M Program Code (*Matlab 4.0*)      |
| Annex G | BPTESTER.M Program Code (*Matlab 4.0*)      |

**LIST OF FIGURES**

|  |  |  |
|----|----|----|
| Figure 2.1 | Simplified Biological Neural Network .......................................... | 5 |
| Figure 2.2 | A Basic Artificial Neuron Model .................................................. | 9 |
| Figure 2.3 | Typical Neuron Activation Functions ............................................ | 9 |
| Figure 2.4 | ANN Architecture Nomenclature .................................................. | 12 |
| Figure 3.1.A | Serial List Learning Error -- Experimental Results ......................... | 18 |
| Figure 3.1.B | Serial List Learning Error -- Classical Theory Prediction ............... | 18 |
| Figure 3.2 | Competitive Learning Model ........................................................ | 20 |
| Figure 3.3 | The Fuzzy ART ANN Model ....................................................... | 34 |
| Figure 3.4 | Fuzzy ART Map Architecture ....................................................... | 37 |
| Figure 4.1 | A Four Stage ASR Process ........................................................... | 43 |
| Figure 4.2 | A Speech Variability Pyramid ....................................................... | 48 |
| Figure 4.3 | Vowel Formant Frequencies from Table 4.2 .................................. | 54 |
| Figure 4.4 | Vowel Formant Ratios from Table 4.2 .......................................... | 54 |
| Figure 4.5 | Normalized Polar Angle Formant Ratios of Table 4.2 Vowels ....... | 55 |
| Figure 5.1 | RMC Speech Database File Naming Convention ........................... | 63 |
| Figure 5.2 | ASR System Hardware Components ............................................. | 65 |
| Figure 5.3-M | Microphone Speech Signal MDY12204.WAV .............................. | 66 |
| Figure 5.3-T | Telephone Speech Signal TDY12204.WAV .................................. | 66 |
| Figure 5.4-M | Chunk \#1 of MDY12204.WAV .................................................... | 68 |
| Figure 5.4-T | Chunk \#1 of TDY12204.WAV ..................................................... | 68 |
| Figure 5.5-M | Chunk \#2 of MDY12204.WAV .................................................... | 68 |
| Figure 5.5-T | Chunk \#2 of TDY12204.WAV ..................................................... | 68 |
| Figure 5.6-M | Chunk \#3 of MDY12204.WAV .................................................... | 68 |
| Figure 5.6-T | Chunk \#3 of TDY12204.WAV ..................................................... | 68 |
| Figure 5.7-M | Spectrogram of MDY12204.WAV ............................................... | 69 |
| Figure 5.7-T | Spectrogram of TDY12204.WAV ................................................ | 69 |
| Figure 5.8-M | Microphone Noise Mask ............................................................... | 69 |
| Figure 5.8-T | Telephone Noise Mask ................................................................. | 69 |
| Figure 5.9-M | Noise Masking of MDY12204.WAV ............................................ | 69 |
| Figure 5.9-T | Noise Masking of TDY12204.WAV ............................................. | 69 |
| Figure 5.10-M | STE Curve for MDY12204.WAV ................................................ | 72 |
| Figure 5.10-T | STE Curve for TDY12204.WAV ................................................. | 72 |
| Figure 5.11-M | Silence Reduced MDY12204.WAV ............................................. | 72 |
| Figure 5.11-T | Silence Reduced TDY12204.WAV .............................................. | 72 |
| Figure 5.12-M | Octave Enhanced MDY12204.WAV ............................................ | 72 |
| Figure 5.12-T | Octave Enhanced TDY12204.WAV ............................................. | 72 |
| Figure 5-13-M | Local Maxima in MDY12204.WAV ............................................. | 74 |
| Figure 5-13-T | Local Maxima in TDY12204.WAV .............................................. | 74 |
| Figure 5.14-M | Formants in MDY12204.WAV ..................................................... | 74 |
| Figure 5.14-T | Formants in TDY12204.WAV ...................................................... | 74 |
| Figure 5.15-M | Formant Vectors in MDY12204.WAV .......................................... | 74 |
| Figure 5.15-T | Formant Vectors in TDY12204.WAV ........................................... | 74 |
| Figure 5.16-M | Tri Formant Vector Representation of MDY12204.WAV .............. | 76 |
| Figure 5.16-T | Tri Formant Vector Representation of TDY12204.WAV ............... | 76 |
| Figure 5.17-M | Bi Formant Ratio Vector Representation of MDY12204.WAV ...... | 78 |
| Figure 5.17-T | Bi Formant Ratio Vector Representation of TDY12204.WAV ....... | 78 |
| Figure 5.18-M | Tri Formant Ratio Vector Representation of MDY12204.WAV ..... | 80 |
| Figure 5.18-T | Tri Formant Ratio Vector Representation of TDY12204.WAV ...... | 80 |
| Figure 5.19-M | Fuzzy ART Map Recognition of MDY12204.WAV ...................... | 81 |
| Figure 5.19-T | Fuzzy ART Map Recognition of TDY12204.WAV ....................... | 81 |
| Figure 5.20 | ASR System Software Components .............................................. | 82 |
| Figure 5.21 | Modified Fuzzy ART Map ANN .................................................. | 84 |
| Figure 6.1 | Benchmark ANN -- Sample Training Progress Record .................. | 101 |
| Figure 6.2 | Benchmark ANN -- Sample Training Error Summary .................... | 101 |

**LIST OF TABLES**

|  |  |  |
|----|----|----|
| Table 2.1 | Comparison of Conventional and Neural Network Computation ......... | 8 |
| Table 2.2 | Some Major ANNs Classified By Learning and Recall Modes ........... | 13 |
| Table 3.1 | ART Architecture Learning Properties ............................................... | 24 |
| Table 3.2 | Fuzzy Logic Compared To Binary Logic ........................................... | 25 |
| Table 3.3 | An Eight Stage Fuzzy ART Algorithm .............................................. | 33 |
| Table 4.1 | Performance Classification Of Some Commercial ASR Systems ........ | 41 |
| Table 4.2 | A Comparison of Vowels by Formant Frequencies and Formant Ratios................................................................................................ | 53 |
| Table 5.1 | RMC Speech Database Speaker Profiles ............................................ | 59 |
| Table 5.2 | RMC Speech Database Phrase List .................................................... | 60 |
| Table 6.1 | Benchmark ANN / BFRV / Microphone / Speaker Dependent ............ | 92 |
| Table 6.2 | Benchmark ANN / BFRV / Microphone / Speaker Independent .......... | 92 |
| Table 6.3-M | Fuzzy ART Map / BFRV / Speaker Dependent / Microphone ............ | 93 |
| Table 6.3-T | Fuzzy ART Map / BFRV / Speaker Dependent / Telephone ............... | 93 |
| Table 6.4-M | Fuzzy ART Map / BFRV / Speaker Independent / Microphone .......... | 94 |
| Table 6.4-T | Fuzzy ART Map / BFRV / Speaker Independent / Telephone ............. | 94 |
| Table 6.5-M | Fuzzy ART Map / TFRV / Speaker Dependent / Microphone ............. | 95 |
| Table 6.5-T | Fuzzy ART Map / TFRV / Speaker Dependent / Telephone ............... | 95 |
| Table 6.6-M | Fuzzy ART Map / TFRV / Speaker Independent / Microphone .......... | 96 |
| Table 6.6-T | Fuzzy ART Map / TFRV / Speaker Independent / Telephone ............. | 96 |
| Table 6.7 | ASR System Testing Summary ......................................................... | 97 |
