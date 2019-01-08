# Detective-Beethoven
Command line tool for analysing music. 

# Architecture
**Master** works as the bridge between every module. Every module reports his results to the master which then invokes the next element of the chain. This usually should start with interpreting the arguments, loading the data accordingly, running the analysis-function given the file type and reporting the results. 
- **Interpreter** deals with the parameter, returns the files to read in, the analysis-function to run and the report-fomrat
- **Loader** reads file, proclaims content and type (e.g. *singing noices*, mp3)
- **Analyser** chooses the analysing tool given the Input Format; Throws Exception if anylsis not defined for file (e.g. Genre Detection for text-based)
- **Reporter** outputs the results of the analyser in the specified format. Has to be choosed based on analyser functions (e.g. plain text, html)
 
# TODO
## Feature Ideas
- BPM Detection
  - Normal (easy)
  - Tempo changes (harder)
  - Tempo Features like Double and Half Time, maybe even tripple it ;)
  - Detect Time Signatur
- Genre Detection
- Chords, Melody etc. are way harder tasks

## Infrastructure
- Add audio import for common formats
- Add MIDI import
- Add Text-Based Notation import
