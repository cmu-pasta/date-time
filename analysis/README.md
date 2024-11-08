# Results

This directory contains the results of our systematic study. Specifically, it includes:

- A manually analyzed and fully annotated dataset of 151 bugs.
- Data used to measure inter-rater agreement.
- Scripts used to visualize the data.

## Structure

Below is a description of the contents of this directory:

- [`sanity_checks.ipynb`](sanity_checks.ipynb): A Jupyter notebook containing scripts to perform sanity checks on the dataset of bugs. It validates data integrity and consistency.
- [`insights.ipynb`](insights.ipynb): A Jupyter notebook with code used to generate plots and visualizations for our study. It includes data analysis and visualization scripts to derive insights from the dataset.
- [`cohen_kappa.ipynb`](cohen_kappa.ipynb): A Jupyter notebook containing code to measure inter-rater agreement using Cohen's Kappa statistic.
- [`data/`](data): Directory containing all the data from the study:
  - [`bugs_analysis_base.tsv`](data/bugs_analysis_base.tsv): The base dataset containing the 151 bugs analyzed in the study.
  - [`bugs_analysis_rater_1.tsv`](data/bugs_analysis_rater_1.tsv): Annotations provided by rater 1.
  - [`bugs_analysis_rater_2.tsv`](data/bugs_analysis_rater_2.tsv): Annotations provided by rater 2.
- [`visualizations/`](visualizations): Directory containing all the generated visualizations in PDF format.
