# Annex B

**ASR Demo program code (Stdemo Player 1.5)**

*Listing as printed in the 1995 thesis (extracted from the original Word 6.0 file).*

```
// ###########################################################
// PROGRAM NOTES
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Program Name: VOXRECFL.STD
//
// Called By: STDEMO.EXE
//
// Purpose: STDemo script language file to control execution of
//                Windows applications for speech recognition. This
//	    program performs FAST LEARNING (ie. no graphics are
//	    displayed)
//
//
// Author: Captain David Peter Young
//
// ############################################################
// PROGRAM STARTUP ROUTINE
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// DISABLE LOCKOUTS - show cursor permanently and enable windows
// input permanently, without these two line the cursor is locked
// within the demo window.
:C11
:I11
//
// SPEECH RECOGNITION INTRO - play intro welcome and display graphics
:pwelcome.wav
//
//
// INPUT PHRASE INFO
:%SCC
Type in the phrase using CAPITAL LETTERS ...
1
%
// ###########################################################
// VOICE SAMPLING ROUTINE
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Launch Gold Wave
:(goldwave.exe
//
// Remove help window with alt-f x
@fx
//
// ******* RECORD A SAMPLE OF THE BACKGROUND NOISE *****************
//
// Open a new file to record
@fn
// Select 16 bit MONO @ 22050 Hz for 1 sec
// Down arrow - Tab - Tab - Tab - Up Arrow - Up Arrow - Return
]|]~]~]~]^]^]!
//
// Ensure the "Device Controls" window window is active
:<Device Controls|0
//
// Notify user of noise sampling
// Hide STOP and CONTINUE buttons
:X0
:Y0
//
// Set I/O box timeout (time in seconds)
:+2
//
// Enlarge default font size to make message stand out
:d36
//
// Display Text
:#WCC
    SAMPLING BACKGROUND NOISE ...
#
//
// Return default setting
:X2
:Y2
:+0
:d12//
// Start recording
// two tabs are required for the first recording made after opening GoldWave
// Tab - Tab - Return
]~]~]!
//
// Save Noise Sample to NOISE.WAV
// Ensure the "GoldWave v2.11" window is active
:<GoldWave v2.11|0
//
// Save file in standard WAV format
// ALT-F S
@f
S
NOISE.WAV
]!
//
// If file already exists, confirm overwrite
// check for overwrite dialog window then answer yes
:?Save Sound File|AnswerYes
:GAnswerNA
:LAnswerYes
y
:LAnswerNA
//
// ****** RECORD VOICE SAMPLE **************
//
// Ensure focus on GoldWave window
:<GoldWave v2.11|0
//
// Open a new file to record
@f
n
// Select 16 bit MONO @ 22050 Hz for 5 sec
// Tab - Tab - Tab - Down Arrow - Return
]~]~]~]|]!
//
// Ensure the "Device Controls" window window is active
:<Device Controls|0
//
// Prompt speaker to give voice sample
:#WCC
After you press continue, recording will begin.
.N
You will have 5 seconds to state your phase.
#
//
// Start recording
// Tab - Tab - ShiftTab - Return
]~]~#]~]!
//
// Wait 5 seconds while recording is made
// required for synchronizing script to application
//
// Start playback - must alternate active hotspot with tab key
// to get return key to start player
// Tab - ShiftTab - Return
]~#]~]!
//
:LIsItGood
:*MRD
Is this the sample you want to submit for recognition?
1Resample|NO ...I want to make another recording.
2SaveSample|YES ..Recognize this voice sample.
*
// Resample voice
:LResample
// Prompt the speaker to give voice sample
:#WCC
RESAMPLING ...
.S
.N
You will have 5 seconds to state your phase.
#
//
// Ensure the "Device Controls" window is active
:<Device Controls|0
// Start recording - only one tab required to change hotspot
// on second and subsequent recordings
// Tab - Return
]~]!
//
// Wait 5 seconds will recording is made
//
// Start playback - must alternate active hotspot with tab key
// to get return key to start player
// Tab - ShiftTab - Return
]~#]~]!
//
// Prompt speaker to accept sample
:GIsItGood
//
// Save the current sample in the buffer to file
:LSaveSample
//
// Ensure the "GoldWave v2.11" window is active
:<GoldWave v2.11|0
//
// Save file in standard WAV format
// ALT-F S
@f
S
DEMOSAMP.WAV
]!
//
// If file already exists, confirm overwrite
// check for overwrite dialog window then answer yes
:?Save Sound File|OverWrite
:GNoConfirm
:LOverWrite
y
:LNoConfirm
//
// DEMO SAMPLE IS NOW SAVED FOR ANALYSIS
// Close GoldWave Application
// Alt-F - x
@fx
//
// remove application from STDemo stack
:)
// ###########################################################
// DEMO SAMPLE FEATURE EXTRACTION ROUTINE
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// LAUNCH MATLAB - version 4.0 for windows with Signal Processing,
// Neural Networks, and SPC Tools ToolBoxes
// Assume default MatLab directory
:(matlab.exe
//
// Start MatLab script file to extract features from
// speaker's voice sample (graphics off)
makespec('demosamp.wav',0); clear ]!
formant3('semosamp',0,1,'noise.wav'); clear ]!
//
// Wait 30 seconds for feature extraction
:W30
// Start MatLab script file to analyze features
fartmapb('femosamp',1, '$1' ,0); clear ]!
// Hold Prompt
:#WRD
Holding ... for results
#
//
// Close Matlab Window
:<MATLAB Command Window|0
@fx
//
// close MatLab on STDemo stack
:)
// ########################################################
//
// CLOSE PROGRAM ROUTINE
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Stop Label - this is jumped anytime STOP button is pushed
:L__STOP__
//
//
// GOODBYE MESSAGE - Display end of program message with
// short fuse timeout (ie. no button click required)
//
// Hide STOP and CONTINUE buttons
:X0
:Y0
//
// Set I/O box timeout (time in seconds)
:+5
//
// Enlarge default font size to make message stand out
:d36
//
// Play Good Bye Audio
:pGOODBYE.WAV
//
// Display Good Bye Text
:#WCC
END OF VOICE RECOGNITION
#
// Terminate script execution to invoke auto closure of open windows (if any)
:Z
// ==============
// END OF PROGRAM
// ==============
// ###########################################################
// PROGRAM NOTES
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Program Name: VOXRECFT.STD
//
// Called By: STDEMO.EXE
//
// Purpose: STDemo script language file to control execution of
//                Windows applications for speech recognition. This
//	    program performs FAST TESTING (ie. no graphics are
//	    displayed)
//
//
// Author: Captain David Peter Young
//
// ############################################################
// PROGRAM STARTUP ROUTINE
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// DISABLE LOCKOUTS - show cursor permanently and enable windows
// input permanently, without these two line the cursor is locked
// within the demo window.
:C11
:I11
//
// SPEECH RECOGNITION INTRO - play intro welcome and display graphics
:pwelcome.wav
//
// ###########################################################
// VOICE SAMPLING ROUTINE
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Launch Gold Wave
:(goldwave.exe
//
// Remove help window with alt-f x
@fx
//
// ******* RECORD A SAMPLE OF THE BACKGROUND NOISE *****************
//
// Open a new file to record
@fn
// Select 16 bit MONO @ 22050 Hz for 1 sec
// Down arrow - Tab - Tab - Tab - Up Arrow - Up Arrow - Return
]|]~]~]~]^]^]!
//
// Ensure the "Device Controls" window window is active
:<Device Controls|0
//
// Notify user of noise sampling
// Hide STOP and CONTINUE buttons
:X0
:Y0
//
// Set I/O box timeout (time in seconds)
:+2
//
// Enlarge default font size to make message stand out
:d36
//
// Display Text
:#WCC
    SAMPLING BACKGROUND NOISE ...
#
//
// Return default setting
:X2
:Y2
:+0
:d12//
// Start recording
// two tabs are required for the first recording made after opening GoldWave
// Tab - Tab - Return
]~]~]!
//
// Save Noise Sample to NOISE.WAV
// Ensure the "GoldWave v2.11" window is active
:<GoldWave v2.11|0
//
// Save file in standard WAV format
// ALT-F S
@f
S
NOISE.WAV
]!
//
// If file already exists, confirm overwrite
// check for overwrite dialog window then answer yes
:?Save Sound File|AnswerYes
:GAnswerNA
:LAnswerYes
y
:LAnswerNA
//
// ****** RECORD VOICE SAMPLE **************
//
// Ensure focus on GoldWave window
:<GoldWave v2.11|0
//
// Open a new file to record
@f
n
// Select 16 bit MONO @ 22050 Hz for 5 sec
// Tab - Tab - Tab - Down Arrow - Return
]~]~]~]|]!
//
// Ensure the "Device Controls" window window is active
:<Device Controls|0
//
// Prompt speaker to give voice sample
:#WCC
After you press continue, recording will begin.
.N
You will have 5 seconds to state your phase.
#
//
// Start recording
// Tab - Tab - ShiftTab - Return
]~]~#]~]!
//
// Wait 5 seconds while recording is made
// required for synchronizing script to application
:W5
//
// Start playback - must alternate active hotspot with tab key
// to get return key to start player
// Tab - ShiftTab - Return
]~#]~]!
//
// Prompt speaker to resample again or continue with recognition
:LIsItGood
:*MRD
Is this the sample you want to submit for recognition?
1Resample|NO ...I want to make another recording.
2SaveSample|YES ..Recognize this voice sample.
*
//
// Resample voice
:LResample
// Prompt the speaker to give voice sample
:#WCC
RESAMPLING ...
.S
After you press continue, recording will begin.
.N
You will have 5 seconds to state your phase.
#
//
// Ensure the "Device Controls" window is active
:<Device Controls|0
//
// Start recording - only one tab required to change hotspot
// on second and subsequent recordings
// Tab - Return
]~]!
//
// Wait 5 seconds will recording is made
:W5
//
// Start playback - must alternate active hotspot with tab key
// to get return key to start player
// Tab - ShiftTab - Return
]~#]~]!
//
// Prompt speaker to accept sample
:GIsItGood
//
// Save the current sample in the buffer to file
:LSaveSample
//
// Ensure the "GoldWave v2.11" window is active
:<GoldWave v2.11|0
//
// Save file in standard WAV format
// ALT-F S
@f
S
DEMOSAMP.WAV
]!
//
// If file already exists, confirm overwrite
// check for overwrite dialog window then answer yes
:?Save Sound File|OverWrite
:GNoConfirm
:LOverWrite
y
:LNoConfirm
//
// DEMO SAMPLE IS NOW SAVED FOR ANALYSIS
// Close GoldWave Application
// Alt-F - x
@fx
//
// remove application from STDemo stack
:)
// ###########################################################
// DEMO SAMPLE FEATURE EXTRACTION ROUTINE
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// LAUNCH MATLAB - version 4.0 for windows with Signal Processing,
// Neural Networks, and SPC Tools ToolBoxes
// Assume default MatLab directory
:(matlab.exe
//
// Start MatLab script file to extract features from
// speaker's voice sample (graphics off)
makespec('demosamp.wav',0); clear ]!
formant3('semosamp',0,1,'noise.wav'); clear ]!
//
// Wait 30 seconds for feature extraction
:W30
// Start MatLab script file to analyze features
fartmapb('femosamp',2,'test',0); clear ]!
// Hold Prompt
:#WRD
Holding ... for results
#
//
// Close Matlab Window
:<MATLAB Command Window|0
@fx
//
// close MatLab on STDemo stack
:)
// ############################################################
// CLOSE PROGRAM ROUTINE
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Stop Label - this is jumped anytime STOP button is pushed
:L__STOP__
//
//
// GOODBYE MESSAGE - Display end of program message with
// short fuse timeout (ie. no button click required)
//
// Hide STOP and CONTINUE buttons
:X0
:Y0
//
// Set I/O box timeout (time in seconds)
:+5
//
// Enlarge default font size to make message stand out
:d36
//
// Play Good Bye Audio
:pGOODBYE.WAV
//
// Display Good Bye Text
:#WCC
END OF VOICE RECOGNITION
#
// Terminate script execution to invoke auto closure of open windows (if any)
:Z
// ==============
// END OF PROGRAM
// ==============
```
