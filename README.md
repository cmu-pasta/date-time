# date-time

Software systems across various industries rely heavily on date and time computations for crucial tasks like scheduling, financial transactions, data logging, and validation. However, these calculations can be surprisingly complex and error-prone due to factors like:
1. Time Zones: Handling time across different regions and their varying time zones, including daylight saving time (DST), can lead to confusion and errors.
2. Leap Years: Accounting for leap years and their impact on calendar calculations is a frequent source of bugs.
3. Diverse Representations: Different programming languages and libraries use distinct date and time representations, introducing inconsistencies and potential for misuse.
4. API Nuances: Subtle differences in the APIs of date and time libraries can lead to incorrect assumptions and unexpected behavior.
These complexities often result in bugs that can be challenging to detect and fix.

## Proposed Approach

This repository focuses on the first research thrust, which seeks to systematically identify and mitigate date and time-related bugs in open-source repositories:

1. Empirical Study of Date/Time-Related Issues (DATE-SMELLS):
- We will perform a comprehensive analysis of open-source repositories on GitHub, particularly those using Python, JavaScript, and Java, to identify common date/time-related issues and bug patterns.
- This analysis will involve analyzing GitHub issues, code commits, and discussions to uncover how developers have encountered and addressed date/time-related problems.
- We will develop a taxonomy to classify these issues based on factors like affected functions, relevant logic, root cause, and impact.
- The results of this study will be documented and disseminated in the form of DATE-SMELLS, a catalog of common date/time-related bug patterns, to raise awareness among software engineers.

2. Automatic Bug-Finding Tool (DATE-COP):
- Based on the identified DATE-SMELLS, we will develop complementary static and dynamic analysis techniques to automatically discover and report date/time-related bugs in open-source projects.
- Static analysis: We will leverage tools like CodeQL to implement syntax-based static analysis rules that can detect specific bug patterns across vast amounts of code.
- Dynamic analysis: We will develop dynamic linting techniques that can identify problematic date/time operations by monitoring and analyzing program execution during testing.
- These analysis techniques will be integrated into a GitHub bot, DATE-COP, capable of automatically identifying and reporting bugs in repositories at scale.

## Repository Structure
This repository will be organized to facilitate the development and evaluation of the DATE-SMELLS and DATE-COP components:
- assignments: This folder contains the solutions from all REU students to assignments created on various important topics. 
- benchmarks: This directory contains the benchmark suite created modeling real-world code bugs and smells that were identified during our research. 
- scripts: This directory contains the helper scripts used for data mining, cleaning, visualization, and other computations.
- date-cop: This folder will contain the source code for the DATE-COP GitHub bot, including its static and dynamic analysis components.

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
- Report DATE-SMELLS: If you encounter a common date/time-related bug pattern in your own projects or in open-source repositories, please share your findings with us by creating an issue in this repository.
- Improve analysis techniques: Contribute to the development of static and dynamic analysis techniques by proposing new rules, improving existing ones, or enhancing the DATE-COP implementation.
- Evaluate DATE-COP: Help us evaluate the effectiveness of DATE-COP by running it on open-source projects and reporting your findings.

## License
This repository is licensed under the MIT License. Feel free to use, modify, and share the code and resources contained within it.
We believe that by collaborating and sharing knowledge, we can make a significant impact on the reliability and security of software systems by reducing the number of date and time-related errors.