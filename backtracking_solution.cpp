#include <bits/stdc++.h>
#include "utils.cpp"

using namespace std;

class QueensSolver {
private:
    int n;
    bool all_solutions, show_solutions;
    vector<int> curr_solution;
    int solution_count;

    void print_solution() {
        // Don't use endl because it flushes the output (inefficient)
        cout << "Solution " << solution_count << '\n';

        for (int r = 0; r < n; r++) {
            int col = curr_solution[r];
            for (int c = 0; c < col; c++) cout << ".";
            cout << "Q";
            for (int c = col + 1; c < n; c++) cout << ".";
            cout << '\n';
        }
        cout << '\n';
    }

    // The only thing that matters in these two functions is
    // that a specific diagonal is always mapped to the same index
    // and that this index fits within the vector size given
    int get_maj_diag(int r, int c) {
        return c - r + (n - 1);     // + (n - 1) ensures that the diagonal has a valid index (>= 0)
    }
    int get_min_diag(int r, int c) {
        return r + c;   // the same min diagonals have the same coordinate sum
    }

    void place_queen(int r, vector<bool> &filled_cols, vector<bool> filled_maj_diags, vector<bool> filled_min_diags) {
        // if we've found a solution but don't want to get all of them
        // just finish
        if (solution_count > 0 && !all_solutions) return;

        if (r == n) {    // row outside board
            // means that every queen is placed so we just found a solution
            solution_count++;
            if (show_solutions) {
                print_solution();
            }

            return;     // backtrack
        }
        for (int c = 0; c < n; c++) {   // go through all possible columns
            // check if column c is valid -> need to check diagonals and columns
            int maj_diag = get_maj_diag(r, c);
            int min_diag = get_min_diag(r, c);

            if (!filled_cols[c] && !filled_maj_diags[maj_diag] && !filled_min_diags[min_diag]) {
                curr_solution.push_back(c);
                filled_cols[c] = true;
                filled_maj_diags[maj_diag] = true;
                filled_min_diags[min_diag] = true;

                place_queen(r + 1, filled_cols, filled_maj_diags, filled_min_diags);

                curr_solution.pop_back();   // reset updates from this column and try another one
                filled_cols[c] = false;
                filled_maj_diags[maj_diag] = false;
                filled_min_diags[min_diag] = false;
            }
        }
    }

public:
    QueensSolver(int _n, bool _all_solutions, bool _show_solutions):
        n(_n), all_solutions(_all_solutions), show_solutions(_show_solutions) {
        solution_count = 0;
    }

    double solve() {
        int nr_of_diagonals = n * 2 - 1;    // total number of diagonals to one side
        vector<bool> filled_cols(n, false), filled_maj_diags(nr_of_diagonals, false), filled_min_diags(nr_of_diagonals, false);

        place_queen(0, filled_cols, filled_maj_diags, filled_min_diags);
        cout << "Found " << solution_count << " solution(s)" << '\n';
        return 0;   // TODO: time spent
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
        int MAX_BOARD_SIZE = 15, NR_TESTS_PER_BOARD_SIZE = 5;

        vector<vector<double>> results;
        if (args.run_tests == "all-solutions") {
            results = run_timing_tests(MAX_BOARD_SIZE, NR_TESTS_PER_BOARD_SIZE, true);
        }
        else if (args.run_tests == "one-solution") { 
            results = run_timing_tests(MAX_BOARD_SIZE, NR_TESTS_PER_BOARD_SIZE, false);
        }
        save_results(results, "results_bitwise_" + args.run_tests + ".csv");
    }
    else {
        QueensSolver qs(args.board_size, args.all_solutions, args.print_solutions);
        qs.solve();
    }
    return 0;
}
