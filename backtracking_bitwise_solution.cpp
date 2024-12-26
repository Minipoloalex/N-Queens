#include <bits/stdc++.h>
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
        // cout << curr_solution.size() << " "  << col_bits << endl;
        // base case (finished)
        if (col_bits == mask) { // could also check: curr_solution.size() == n
            // all columns are filled -> found a solution
            solution_count++;
            if (show_solutions) {
                print_solution();
            }

            return;
        }

        // An int has 32 bits, so many will be set to 1 (after the bitwise NOT)
        // The mask ensures that bits outside the range are avoided, using only the n bits that represent valid columns
        int possible_bits = ~(col_bits | maj_diag_bits | min_diag_bits) & mask;
        for (int bit; possible_bits > 0; ) {
            bit = LSB(possible_bits);
            possible_bits ^= bit;   // trying this bit (should remove it from possible bits)
            curr_solution.push_back(bit);
            place_queen(col_bits | bit, (maj_diag_bits | bit) << 1, (min_diag_bits | bit) >> 1);
            curr_solution.pop_back();
        }
    }
public:
    QueensSolver(int _n, bool _all_solutions, bool _show_solutions):
        n(_n), all_solutions(_all_solutions), show_solutions(_show_solutions) {
        mask = (1 << n) - 1;
        solution_count = 0;
    }

    void solve() {
        place_queen(0, 0, 0);
        cout << "Found " << solution_count << " solution(s)" << '\n';
    }
};

void run_timing_tests(int max_board_size, int number_of_times) {
    for (int board_size = 1; board_size <= max_board_size; board_size++) {
        for (int i = 0; i < number_of_times; i++) {
            QueensSolver qs(board_size, false, false);
            qs.solve();
        }
    }
}

int main(int argc, char *argv[]) {
    // Default parameters
    int board_size = 8;
    bool print_solutions = false;
    bool run_tests = false;

    // Parse command-line arguments
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--board" || arg == "-b") {
            if (i + 1 < argc) {
                board_size = std::stoi(argv[++i]); // Convert the next argument to an integer
            } else {
                std::cerr << "Error: --board option requires a value.\n";
                return 1;
            }
        } else if (arg == "--print" || arg == "-p") {
            print_solutions = true;
        } else if (arg == "--run_tests" || arg == "-t") {
            run_tests = true;
        } else if (arg == "--help" || arg == "-h") {
            std::cout << "Usage: " << argv[0] << " [options]\n"
                      << "Options:\n"
                      << "  -b, --board SIZE    Set the board size (default: 8)\n"
                      << "  -p, --print         Print solutions\n"
                      << "  -t, --tests         Run tests\n"
                      << "  -h, --help          Show this help message\n";
            return 0;
        } else {
            std::cerr << "Unknown option: " << arg << "\n";
            return 1;
        }
    }

    if (run_tests) {
        int max_board_size = 15, number_of_times = 5;
        run_timing_tests(max_board_size, number_of_times);
    }
    else {
        QueensSolver qs(board_size, false, print_solutions);
        qs.solve();
    }
    return 0;
}
