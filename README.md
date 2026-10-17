\# RuleCat: Secure COBOL Rule Extraction



Turns legacy COBOL into a searchable, traceable business-rule catalog, running entirely on-premises.



Built by Team Aparajitas for IBM Z Datathon 2026.



\## Problem



Banks can't safely change or audit decades-old COBOL because few people can explain what it does, and proprietary code can't be sent to public AI tools.



\## What it does



\- Parses COBOL procedure logic (IF, EVALUATE, COMPUTE) by paragraph

\- Uses a local LLM (Ollama) to explain each rule in plain English

\- Links every rule to its exact source lines

\- Flags doubtful rules: missing ELSE, missing WHEN OTHER, GO TO, arithmetic without ROUNDED, or an unsure LLM

\- Saves a searchable catalog to `rules.json`



\## Requirements



\- Python 3.8+ (standard library only, nothing to pip install)

\- \[Ollama](https://ollama.com) with a local model



\## Run it



```bash

ollama pull llama3.2

python rulecat.py extract sample/acctcalc.cbl

python rulecat.py search interest fee

```



Use another model with `MODEL=<name>` (on Windows cmd: `set MODEL=<name>`).

If Ollama isn't running, the tool still works and shows the raw code as the explanation.



\## Project layout



```

rulecat.py            extractor, flagger and search

sample/acctcalc.cbl   synthetic banking COBOL program

```



\## Example output



```

\[R003] CALC-FEE lines 30-34

&#x20; The code checks if the current balance is less than 1000 and, if so,

&#x20; sets the fee to 12.50, otherwise sets it to 0.



\[R004] CHECK-LOAN lines 36-38  ! no ELSE branch

```



\## IBM Z / LinuxONE



LinuxONE is the intended deployment target: source code and the rule catalog stay inside the bank's infrastructure. The current prototype is portable Python and has \*\*not yet been tested on s390x\*\*. Testing on s390x-compatible runtimes (e.g. llama.cpp) is planned.



\## Limitations and roadmap



\- LLM explanations can contain small errors, which is why rules show exact source lines and flags for human review

\- Planned: accuracy benchmark against a hand-labeled set of 30-50 rules, behavior checks on synthetic transactions, copybook and CICS/DB2 support, web UI



\## Open-source resources



\- \[Ollama](https://github.com/ollama/ollama) and \[Llama 3.2](https://ollama.com/library/llama3.2)

\- Python standard library



\## Team



Team Aparajitas

