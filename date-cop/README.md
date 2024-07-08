1. Set CODEQL_PATH on your system
2. The qlpack.yml file needs to be defined
3. download the codeql pack zip from codeql and have codeql cli working on the system

- create database: ..\codeql\codeql database create .\date-cop\static-analysis\databases\testdb --language=python --source-root=.\benchmarks\
- run query: ..\codeql\codeql database analyze .\date-cop\static-analysis\databases\testdb\  .\date-cop\static-analysis\deprecated_method.ql --output=results.csv --format=csv --verbose --no-rerun=false


TODO:
- Update the README
- What are the possible values for:
/**
 * @name deprecated method
 * @description Deprecated methods are dangerous and can cause silent failures.
 * @kind problem
 * @tags 
 * @problem.severity recommendation
 * @sub-severity high
 * @precision high
 * @id py/deprecated-method
 */??

 - create a script to run the codeql analysis queries?