#include <bits/stdc++.h>
using namespace std;

#define LSB(i) ((i) & -(i))

class QueensSolver {
private:
    int n;
    vector<vector<int>> board;
    bool all_solutions, show_solutions;
    vector<int> curr_solution;
    int solution_count;

    void print_solution() {
        // I don't use endl because it flushes the output (inefficient)
        cout << "Solution " << ++solution_count << '\n';

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
        if (r == n) {    // row outside board
            // means that every queen is placed so we just found a solution
            print_solution();

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

    void solve() {
        int nr_of_diagonals = n * 2 - 1;    // total number of diagonals to one side
        vector<bool> filled_cols(n, false), filled_maj_diags(nr_of_diagonals, false), filled_min_diags(nr_of_diagonals, false);

        place_queen(0, filled_cols, filled_maj_diags, filled_min_diags);
    }
};

int main() {
    // Input and output efficiency
    cin.tie(0)->ios::sync_with_stdio(0);

    int n;
    cin >> n;
    QueensSolver qs(n, false, false);
    qs.solve();
    return 0;
}
