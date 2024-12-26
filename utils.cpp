#include <bits/stdc++.h>
using namespace std;

vector<vector<double>> run_timing_tests_helper(function<double(int)> solve, int max_board_size, int number_of_times) {
    vector<vector<double>> ans;
    for (int board_size = 1; board_size <= max_board_size; board_size++) {
        vector<double> board_size_times;
        for (int i = 0; i < number_of_times; i++) {
            double time_taken = solve(board_size);
            board_size_times.push_back(time_taken);
        }
        ans.push_back(board_size_times);
    }
    return ans;
}

void save_results(const vector<vector<double>> &results, const string &filename) {
    ofstream file(filename);
    
    if (!file.is_open()) {
        throw runtime_error("Could not open file: " + filename);
    }

    // Write the header
    for (size_t i = 0; i < results.size(); ++i) {
        file << "size_" << (i + 1);
        if (i != results.size() - 1) {
            file << ",";
        }
    }
    file << "\n";

    // Find the maximum number of test results across all board sizes
    size_t max_tests = 0;
    for (const auto& board_size_results : results) {
        max_tests = max(max_tests, board_size_results.size());
    }

    // Write the results row by row
    for (size_t test = 0; test < max_tests; ++test) {
        for (size_t board_size = 0; board_size < results.size(); board_size++) {
            if (test < results[board_size].size()) {
                file << fixed << setprecision(6) << results[board_size][test];
            }
            if (board_size != results.size() - 1) {
                file << ",";
            }
        }
        file << "\n";
    }

    file.close();
}

struct CommandLineArgs {
    int board_size = 8;
    bool all_solutions = false;
    string run_tests = "false";
    bool print_solutions = false;
};

CommandLineArgs parse_arguments(int argc, char* argv[]) {
    CommandLineArgs args;

    for (int i = 1; i < argc; ++i) {
        string arg = argv[i];

        if (arg == "--board_size") {
            if (i + 1 < argc) {
                args.board_size = stoi(argv[++i]);
            } else {
                throw invalid_argument("Missing value for --board_size");
            }
        } else if (arg == "--all_solutions") {
            args.all_solutions = true;
        } else if (arg == "--run_tests") {
            if (i + 1 < argc) {
                string value = argv[++i];
                if (value == "false" || value == "all-solutions" || value == "one-solution") {
                    args.run_tests = value;
                } else {
                    throw invalid_argument("Invalid value for --run_tests. Allowed values are: false, all-solutions, one-solution");
                }
            } else {
                throw invalid_argument("Missing value for --run_tests");
            }
        } else if (arg == "--print_solutions") {
            args.print_solutions = true;
        } else {
            throw invalid_argument("Unknown argument: " + arg);
        }
    }

    return args;
}
