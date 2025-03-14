# date-time

Accurately performing date and time calculations in software is non-trivial due to the inherent complexity and variability of temporal concepts such as time zones, daylight saving time (DST) adjustments, leap years and leap seconds, clock drifts, and different calendar systems. Although the challenges are frequently discussed in the grey literature, there has not been any systematic study of date/time issues that have manifested in real software systems. 

This repository focuses on the first of its kind study to systematically identify and analyze date and time related bugs in open-source python repositories. We qualitatively study bugs in temporal calculations and their associated fixes from open-source Python projects on GitHub to understand: (a) the conceptual categories of date/time computations in which bugs occur, (b) the programmatic operations involved in the buggy computations, and (c) the underlying root causes of these errors. We also analyze metrics such as bug severity and detectability as well as fix size and complexity.

## Repository Structure
- analysis: This directory contains the labeled analysis results and the insights derived from the study. 
- benchmarks: This directory contains the benchmark suite created modeling real-world code bugs and smells that were identified during our research. CodeQL queries can be tested on these programs.
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

## Acknowledgments
This work was supported in part by the National Science Foundation via grants OAC-2244348, CCF-2120955, and CCF-2429384.

Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
