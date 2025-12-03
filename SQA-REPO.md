\# SQA Project Report – MLForensics  

COMP 5710/6710 – Fall 2025



\## Team

\- \*\*Team Name:\*\* RiteshPiyush-FALL2025-SQA  

\- \*\*Members:\*\*  

&nbsp; - Ritesh Kolli  

&nbsp; - Piyush Salve



\*\*Repository:\*\* https://github.com/Salmonella12/RiteshPiyush-FALL2025-SQA



---



\## 1. Fuzz Testing



We created `fuzz.py` inside `MLForensics-farzana/` and fuzzed the following \*\*five functions\*\* from `mining/mining.py`:



1\. `giveTimeStamp()`

2\. `dumpContentIntoFile(strP, fileP)`

3\. `deleteRepo(dirName, type\_)`

4\. `makeChunks(the\_list, size\_)`

5\. `days\_between(d1\_, d2\_)`



Random strings, numbers, datetimes, directories, and invalid inputs were generated automatically.  

Fuzzing results were logged in:



\- `fuzz\_results.log`

\- `forensics.log`



\### Bugs Found

`days\_between()` crashed multiple times with `TypeError` when inputs were not datetime objects (e.g., strings, integers, None).  

This shows missing input validation.  

The other four functions handled fuzzing without major failures.



---



\## 2. Forensics Logging



We added logging to the same five functions.  

Each logs function entry, inputs, outputs, and exceptions.



Logs stored in:  

\*\*`MLForensics-farzana/forensics.log`\*\*



This allowed us to trace behavior during fuzzing and confirm where failures occurred.



---



\## 3. Continuous Integration (CI)



We created GitHub Actions workflow:





The CI pipeline:



1\. Installs Python 3.11  

2\. Installs required dependencies  

3\. Moves into `MLForensics-farzana/`  

4\. Runs `python fuzz.py`  

5\. Displays log files  



CI automatically runs on every push.



\*\*Builds available under:\*\*  

GitHub → Actions tab  

https://github.com/Salmonella12/RiteshPiyush-FALL2025-SQA/actions



---



\## 4. Lessons Learned

\- Fuzzing exposed hidden robustness issues (especially in `days\_between`).  

\- Logging made failures reproducible and easy to analyze.  

\- CI ensured our fuzz tests ran automatically and consistently.  

\- Managing imports, directories, and Git/GitHub structure was an important part of real-world software QA.



---



End of Report



