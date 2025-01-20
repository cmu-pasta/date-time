# date-time

Software systems across various industries rely heavily on date and time computations for crucial tasks like scheduling, financial transactions, data logging, and validation. However, these calculations can be surprisingly complex and error-prone due to factors like:
1. Time Zones: Handling time across different regions and their varying time zones, including daylight saving time (DST), can lead to confusion and errors.
2. Leap Years: Accounting for leap years and their impact on calendar calculations is a frequent source of bugs.
3. Diverse Representations: Different programming languages and libraries use distinct date and time representations, introducing inconsistencies and potential for misuse.
4. API Nuances: Subtle differences in the APIs of date and time libraries can lead to incorrect assumptions and unexpected behavior.

These complexities often result in bugs that can be challenging to detect and fix.

## About

This repository focuses on the first of its kind study to systematically identify and analyze date and time related bugs in open-source python repositories.


## Repository Structure
- analysis: This directory contains the labeled analysis results and the insights derived from the study. 
- benchmarks: This directory contains the benchmark suite created modeling real-world code bugs and smells that were identified during our research. 
- scripts: This directory contains the helper scripts used for data mining, cleaning, and other computations.
- codeql: This folder contains the source code for the CodeQL queries used to perform the static analysis.

## Prerequisites

- [Git][]
- [Python][]
- [Poetry][]

## Installing Dependencies

```sh
poetry install
```

## Development
We use [Black][] and [isort][] to format our Python code. You can manually run these formatting tools on the CLI by using the commands:

```sh
poetry run black .
poetry run isort .
```

To automate the formatting process, we have added a pre-commit hook to git. To enable this, you need to run the following commands:

```sh
pre-commit install
```

[black]: https://black.readthedocs.io/en/stable/
[git]: https://git-scm.com/downloads
[isort]: https://pycqa.github.io/isort/
[poetry]: https://python-poetry.org/docs/
[python]: https://www.python.org/downloads/

## Contributions
We welcome contributions from the community to help us achieve our goal of strengthening date and time logic correctness in software systems. Here are some ways you can contribute:
- Report bug patterns: If you encounter a common date/time-related bug pattern in your own projects or in open-source repositories, please share your findings with us by creating an issue in this repository.
- Improve analysis techniques: Contribute to the development of static analysis techniques by proposing new rules or improving existing ones.
- Evaluation: Help us evaluate the effectiveness of our CodeQL queries by running it on open-source projects and reporting your findings.

## License
This repository is licensed under the MIT License. Feel free to use, modify, and share the code and resources contained within it.
We believe that by collaborating and sharing knowledge, we can make a significant impact on the reliability and security of software systems by reducing the number of date and time-related errors.