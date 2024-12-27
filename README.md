# N-Queens
Several solutions were implemented for this problem, using OR-Tools, a SAT solver (from PySat), and manually implemented backtracking solutions in C++.

The library solutions require less information and background, so they are presented here first. Actually, the order presented here is in descending order of abstraction (or ascending order of complexity of implementation). This means that the first solution will be the most abstracted, and likely have the least complex code.

## Measuring Times
To measure and compare the times taken for each board size, we ran the algorithms several times (5 times) for each board size up to 15. This allows us to later plot the results and compare techniques.

## OR-Tools Solution
The implementation was based on https://developers.google.com/optimization/cp/queens.

This solution uses the OR-Tools library, which uses a Sat solver internally to find a valid solution.


## Sat Solver Solution (PySat)
In this solution, the implementation is focused on transforming the problem into a SAT problem. Basically, we setup the variables and their relations and pass them to the SAT solver.

## C++ Solutions
These are the solutions that we manually implemented. These require a special attention to efficiency.

Additionally, in order to understand these solutions, the reader should have at least a basic understanding of Data Structures and Algorithms (DSA), specifically of backtracking algorithms.

These solutions were tested in an online judge that presents several classic programming problems, like this one. The problem presented there is slightly different and it required some small adjustments to save the obtained solutions: https://leetcode.com/problems/n-queens/description/. Both of the solutions presented here were able to pass the test cases from this online judge.


For these solutions, it is suggested that the commands to run the program are copied and only the parameters should be adjusted (e.g., specify a different board size).

There are 2 files to run corresponding to two different solutions, as we'll see below.


### Efficient Backtracking Solution
To run the normal backtracking solution, which includes efficient checking of valid columns (in constant time instead of the normal linear time), just do:
```bash
g++ backtracking_solution.cpp && ./a.out --board_size 8 --print_solutions true --all_solutions true && rm a.out
```

#### Measure times
Since this takes some time to run, it is advised to just look at the plots. Feel free to run the bitwise solution, though.

To run the timing tests (note [here](#measuring-times) for further clarification on what these are):
```
g++ backtracking_solution.cpp && ./a.out --run_tests all_solutions && rm a.out
```

To run just for one solution, replace `--run_tests all-solutions` with `--run_tests one-solution`.


### Bitwise Backtracking Solution (more efficient)
To run this solution, which includes only traversal through valid columns through bitwise manipulation, just do:
```bash
g++ backtracking_bitwise_solution.cpp && ./a.out --board_size 8 --print_solutions true --all_solutions true && rm a.out
```

This solution is adapted from https://bpochily.github.io/bitwise-optimization-of-n-queens/ and https://www.cl.cam.ac.uk/~mr10/backtrk.pdf.

#### Measure times
This is actually quite fast to run, so it should be fine to do it.

To run the timing tests (note [here](#measuring-times) for further clarification on what these are):
```
g++ backtracking_bitwise_solution.cpp && ./a.out --run_tests all_solutions && rm a.out
```

To run just for one solution, replace `--run_tests all-solutions` with `--run_tests one-solution`.
