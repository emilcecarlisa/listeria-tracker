# Our objective
Create an interactive dashboard that combines various data regarding dietary consumption habits, pathogen contamination, and Best Practice violations data.
This screenshot offers a high level idea of what the dashboard might contain: ![Screenshot 2026-03-14 at 6.22.39 PM.png](..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fzm%2Fxgmwv6ln7pn6rbjzqsdsplk80000gp%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_BAxCHW%2FScreenshot%202026-03-14%20at%206.22.39%E2%80%AFPM.png)

- Mapping: map the data sources with the analysis docs. Update the read me with this mapping in the form of a table
- Exploratory task: use the corresponding research doc in the /docs folder to understand descriptive statistics about the data source
- Further analysis:
  - For each file listed in the details section below, make sure we have the right data to support our conclusions. If data is missing that would make a stronger analysis, we can discover that but you must surface it to me. For example we do not have plant based pathogen lab samples like we do for meat.
  - The dashboard will reuse useful graphs and analysis (docs and visualizations folders) but must be extracted for use in a new visualization (ipynb) file
  - Ensure that dates and comparisons across products are clear when creating graphs and descriptions of the data. For example, it should be clear when we're looking at historical data vs. something from 2025.
  - If the data confirms this, it should tell a story about how factory produced meat is increasing in popularity and contamination rates. This may suggest that caring for our animals might lower pathogen contamination rates, putting humans in a better health position.
- Future work based on complete findings:
  - Help me create a plan to build a rating system of the companies/brands based on their contamination levels and commercial practices (animal handling) which will help customers understand who has consistently poor commercial practices leading to worse contamination rates.

 ## Details
Files corresponding to the boxes in screenshot:
  - Foods People Eat:
    - Data source: usFoodGroupIntakesBySource.csv
    - Additional analysis task: Sum plant-based groups (vegetables, fruits, whole grains, refined grains, legumes, nuts/seeds, soy products) vs animal-based groups (meat, poultry, eggs, seafood, dairy).
      Divide by total to get percentage of intake (by cup/oz equivalents) that's plant vs animal.
    - Analysis docs:
      - consumptionDataAnalysis.md

  - Foods Contaminated with Pathogens
    - Data source: joinedGcpLabPoultryData.csv, labSamplingRawPorkFy2025.json, labSamplingRawPoultryFy2025.json, labSamplingRteFy2025.json
    - Analysis docs:
      - dataComparisonAnalysis.md
      - porkSausageAnalysis.md
      - jupyterVisualizationPseudocode.md
      - porkVsChickenComparison.md

  - What Foods Are Recalled Most?
    - Data source: fsisRecallSummary2025.xlsx
    - Analysis docs: None
    - Additional analysis task: discover whether animal vs plant products are recalled more often. Ensure that comparisons across food types are consistent. For example, ready to eat foods should be compared to ready to eat while raw meats should be compared to raw. Use the dataAnalysisSkill.md to convert the xlsx file into a readable format. Modify the skill or scripts/analyzeGcpData.py to facilitate this

Before starting:
    - Explore the docs for research that has already been conducted and can be reused
    - Organize implementations as you go, keeping track of what subtasks remain
    - Rename all files under data, docs, scripts, skills, visualizations folders so they use camel case instead of numbers, and whatever underscore or dash case they use now. Safely refactor by cleaning up the file name wherever it is referenced.


# Your background
You are a senior data analyst helping me improve the rigorousness and comprehensibility of this project


# Steps to break into subtasks
    - Create new files in the camel case standard
    - All source data files should be explored thoroughly if they haven't already been analysed
    - Make a plan to research, organize the data, then combine it into one dashboard
    - Visualizations under the /visualization folders should eventually be condensed into the new dashboard layout

# When creating jupyter vizualizations
    - Critical implementation detail: create markers or human readable breaks which help me find where one graph starts and ends so if I want to modify a graph after inputing it to Jupyter Notebooks I can easily find which graph it is without recopying the whole ipynb notebook
