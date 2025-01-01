#include <bits/stdc++.h>
#include "utils.cpp"

using namespace std;

#define LSB(i) ((i) & -(i))

class QueensSolver {
private:
    int n, mask;
    bool all_solutions, show_solutions;
    vector<int> curr_solution;
    int solution_count;

    void print_solution() {
        // Don't use endl because it flushes the output (inefficient)
        cout << "Solution " << solution_count << '\n';

        for (int r = 0; r < n; r++) {
            int col_to_power_of_2 = curr_solution[r];

            // we could also use __builtin_ctz which returns the count of trailing zeros
            // that would be faster since it avoids floating point calculations but it is g++ specific (not c++ in general)
            int col = int(log2(col_to_power_of_2));

            for (int c = 0; c < col; c++) cout << ".";
            cout << "Q";
            for (int c = col + 1; c < n; c++) cout << ".";
            cout << '\n';
        }
        cout << '\n';
    }

    void place_queen(int col_bits, int maj_diag_bits, int min_diag_bits) {
        // if we've found a solution but don't want to get all of them
        // just finish
        if (solution_count > 0 && !all_solutions) return;

        // base case (finished)
        if (col_bits == mask) { // could also check: curr_solution.size() == n
            // all columns are filled -> found a solution
            solution_count++;
            if (show_solutions) {
                print_solution();
            }

            return;
        }

        // An int has 32 bits, so many will be set to 1 (because of the bitwise NOT)
        // The mask ensures that bits outside the range are avoided, using only the n bits that represent valid columns
        int possible_bits = ~(col_bits | maj_diag_bits | min_diag_bits) & mask;
        while (possible_bits > 0) {
            int bit = LSB(possible_bits);
            possible_bits ^= bit;   // trying this bit: remove it from possible bits
            curr_solution.push_back(bit);
            place_queen(col_bits | bit, (maj_diag_bits | bit) >> 1, (min_diag_bits | bit) << 1);
            curr_solution.pop_back();
        }
    }
public:
    QueensSolver(int _n, bool _all_solutions, bool _show_solutions):
        n(_n), all_solutions(_all_solutions), show_solutions(_show_solutions) {
        mask = (1 << n) - 1;
        solution_count = 0;
    }

    double solve() {
        auto start = chrono::high_resolution_clock::now();
        place_queen(0, 0, 0);
        auto end = chrono::high_resolution_clock::now();

        cout << "Found " << solution_count << " solution(s) for a board size of " << n << '\n';
        
        int64_t nanoseconds = (end - start).count();
        double seconds = double(nanoseconds) / 1e9;
        return seconds;
    }
};

vector<vector<double>> run_timing_tests(int max_board_size, int number_of_times, bool find_all_solutions) {
    function<double(int)> solve = [&] (int board_size) -> double {
        return QueensSolver(board_size, find_all_solutions, false).solve();
    };
    return run_timing_tests_helper(solve, max_board_size, number_of_times);
}

int main(int argc, char *argv[]) {
    CommandLineArgs args = parse_arguments(argc, argv);


    if (args.run_tests != "false") {
        int NR_TESTS_PER_BOARD_SIZE = 5;

        vector<vector<double>> results;
        if (args.run_tests == "all_solutions") {
            results = run_timing_tests(args.board_size, NR_TESTS_PER_BOARD_SIZE, true);
        }
        else if (args.run_tests == "one_solution") { 
            results = run_timing_tests(args.board_size, NR_TESTS_PER_BOARD_SIZE, false);
        }
        save_results(results, "results_bitwise_" + args.run_tests + ".csv");
    }
    else {
        QueensSolver qs(args.board_size, args.all_solutions, args.print_solutions);
        qs.solve();
    }
    return 0;
}
