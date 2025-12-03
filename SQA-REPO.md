# SQA Project Report – MLForensics  
COMP 5710/6710 – Fall 2025  
Team: **RiteshPiyush-FALL2025-SQA**

## Team Members
- Ritesh Kolli  
- Piyush Salve  

**Repository:** https://github.com/Salmonella12/RiteshPiyush-FALL2025-SQA

---

# 1. Introduction
The purpose of this project was to integrate Software Quality Assurance activities into the MLForensics codebase. We applied three major SQA techniques:

- **Fuzz Testing**  
- **Forensics Logging / Instrumentation**  
- **Continuous Integration (CI) with GitHub Actions**

This report explains our implementation, the functions tested, bugs discovered, and lessons learned.

---

# 2. Fuzz Testing

We created `fuzz.py` inside the `MLForensics-farzana/` directory. The script automatically generates random test inputs and executes functions multiple times to test their robustness.

## 2.1 Functions Selected for Fuzzing
We fuzz-tested the following five functions from `mining/mining.py`:

1. `giveTimeStamp()`  
2. `dumpContentIntoFile(strP, fileP)`  
3. `deleteRepo(dirName, type_)`  
4. `makeChunks(the_list, size_)`  
5. `days_between(d1_, d2_)`

These functions cover a wide range of behaviors (dates, file I/O, directories, list operations, and date arithmetic).

---

## 2.2 Fuzzing Methodology
Our fuzzing engine generated various forms of random input:

- Random strings (ASCII, Unicode, control characters)  
- Random integers (large, small, negative)  
- Random `datetime` objects  
- Lists with randomized lengths  
- Directory names that may or may not exist  
- Invalid values (`None`, mixes of types, corrupted input)

Each function was fuzzed for **50 random iterations**, with inputs logged for reproducibility.

All results were captured in:

- `forensics.log`  
- `fuzz_results.log`

---

## 2.3 Fuzzing Results and Bugs Found

### ✔ Stable Functions (No Crashes)
The following functions handled fuzzing safely:

- **giveTimeStamp()**  
  Returned valid timestamps every time.

- **dumpContentIntoFile(strP, fileP)**  
  Correctly wrote bytes and returned proper output lengths.

- **deleteRepo(dirName, type_)**  
  Handled missing directories and invalid names safely.

- **makeChunks(the_list, size_)**  
  Did not crash even with unusual list sizes or chunk values.

### ❗ Crashing Function: `days_between(d1_, d2_)`
This function does not validate input types before subtracting:

```python
return abs((d2_ - d1_).days)
Fuzzing uncovered several exceptions, including:

TypeError: unsupported operand type(s) for -: 'NoneType' and 'str'

TypeError: unsupported operand type(s) for -: 'int' and 'str'

TypeError: unsupported operand type(s) for -: 'NoneType' and 'datetime'

Cause: The function assumes both arguments are valid datetime objects.
Recommendation: Add type checks or convert strings to datetime safely.

This was the primary robustness issue discovered.

3. Forensics Logging / Instrumentation

We added detailed forensic logging to the same five functions. The logs capture:

Function entry

Input parameters

Key operations

Return values

Exceptions during fuzzing

Logs are written to:
MLForensics-farzana/forensics.log
This helps with debugging and provides traceability, which is essential for QA and security analysis.
4. Continuous Integration (CI)

We implemented Continuous Integration using GitHub Actions. The workflow file is located at:
.github/workflows/ci.yml
4.1 CI Pipeline Steps

The workflow performs:

Checkout repository

Install Python 3.11

Install dependencies (gitpython, numpy, pandas)

Move into MLForensics-farzana/

Execute:python fuzz.py
Display log files for review

The CI runs on:

Every push to main

Every pull request to main

4.2 CI Results

The Actions tab shows successful (green ✔) workflow executions. This means:

CI is functioning correctly

Fuzz tests run automatically

The project stays consistent across updates
5. Lessons Learned
✔ Fuzz Testing Reveals Hidden Issues

Fuzzing automatically generated invalid inputs that exposed failures in days_between(). This reinforced how powerful fuzz testing is for finding edge-case bugs.

✔ Logging Improves Visibility

Instrumentation allowed us to trace crashes and understand exactly which iteration caused problems. This made debugging significantly easier.

✔ CI Ensures Reliability

Continuous Integration guarantees that every update triggers fresh testing, making the codebase more robust and reducing the risk of unnoticed regressions.

✔ Real-World Project Skills

This project taught us how to manage:

File structures

Imports across modules

Logging design

GitHub Actions configuration

These are essential skills for real-world software engineering and QA.
6. Conclusion

We successfully integrated fuzz testing, forensic logging, and CI automation into the MLForensics project. Fuzzing uncovered meaningful issues, logging improved analysis, and CI ensured continuous verification. The repository now demonstrates strong Software Quality Assurance practices suitable for real-world Python projects.
