# Did You Get That? Evaluating GPT-4’s Ability to Identify Additional Context

- domains: includes the 3 single domain values and slots as json files
- data: includes master templates for single domain and dual domain tasks, as well as scripts to fill the data using random values. To run:

  ```
  python3 generate-data.py single-domain-master.xlsx
  ```
  or
  ```
  python3 generate-data-dual.py dual-domain.master.xlsx
  ```
  
- results: aggregated results, images, and script for creating those images called visualizations.py. To run:

  ```
  python3 visualizations.py
  ```
  
- task1: includes filled data for single and dual domain tasks, as well the prompt creation script and a file for generating results with GPT-4. To run, first change FILE global variable to the data you would like to use and then run:

  ```
  python3 gpt.py 
  ```
  
- task2: includes 4 files that contain successful or unsuccessful task 1 results split by single/dual domain, the script for creating prompts, and two files for generating results with GPT-4. To run, first change FILE global variable to the data you would like to use and then run either:

  ```
  python3 gpt-follow-up.py
  ```
  or
  ```
  python3 gpt-follow-up-dual.py
  ```
