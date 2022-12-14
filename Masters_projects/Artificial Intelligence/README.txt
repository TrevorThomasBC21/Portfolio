# Artificial Intelligence, MSDS 688
## Readme

This directory contains several labs completed for the Artificial Intelligence course as part of my Masters degree in Data Science.  The labs vary significantly in content, so each lab directory includes an additional readme that was provided to students as an outline of the assignment.  They contain a brief reintroduction to the topic to be covered in the lab, followed by descriptions of the functions we had to build.

### Summary of Course

This course, a part of the "Machine Learning and Artificial Intelligence" track within the Master of Science Data Science (MSDS) program at Regis University, was primarily focused on the coding of functions that would be used in applications utilizing traditional artificial intelligence concepts.  These concepts include graph data structure search algorithms (BFS, DFS, heuristic search, branch and bound search, A* search), constraint satisfaction algorithms (forward checking, domain reduction, generic propogation), game play algorithms (minimax, alpha-beta pruning, progressive deepening), and Bayesian Network development and navigation.

### Original Work vs Provided Materials

Each directory includes several files provided to students to facilitate the lab.  All of my original work is contained in a single python file in each repective lab directory.  This file uses the naming convention lab{#}.py, where # is replaced by the actual number of the lab.  All other files in each directory, including readmes, test files, and some python classes to be used in the assignments, were provided by the professor and are not original.  I've included them because they are necessary for the functionality of the original files I made, particularly the tester.py file that confirms all my functions worked properly and were written as efficiently as possible.  More information can be found in each lab's readme file.

### Important information

All original functions had to be built "from scratch," meaning we were instructed not to use available Python packages or modules that could complete the assignment easily.  The only imports allowed were from the provided class files - for example, in the Bayesian Network lab, a BayesNet class was provided in the bayes_api.py file that included several basic methods to be used to construct the Bayesian network and obtain attributes (such as a method that returned all ancestors for a given node).  Once completed, we ran the tester.py file in each respective directory that ensured each function worked properly, was robust to various inputs, and operated in as few steps as possible.  The tests being run are contained in the provided tests.py files for each lab.  So long as it is located in the same directory as the other files for a given lab, the tester.py file can be run from the command line to verify the assignment was successfully completed.
