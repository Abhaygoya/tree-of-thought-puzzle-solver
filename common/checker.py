import numpy as np
import copy
import common.consts as consts

class StateCheckerBase(object):

    def __init__(self, state_manager) -> None:
        self.state_manager = state_manager

    def check_current_state(self):
        return None


class SudokuStateCheckResults:

    def __init__(self) -> None:
        self.rows = []
        self.cols = []
        self.is_valid = True
        self.error_message = ""


class RuleBasedSudokuStateChecker(StateCheckerBase):

    def __init__(self, state_manager) -> None:
        super().__init__(state_manager)

    def check_current_state(self):
        init_board = self.state_manager.get_initial_state()
        current_board = self.state_manager.get_current_state()

        result = SudokuStateCheckResults()
        for row in current_board:
            result.rows.append(row)

        for col_idx in range(current_board.shape[1]):
            col = current_board[:, col_idx]
            result.cols.append(col)

        # Check constraint 1: the current board must have the same size as the initial board
        if (current_board.shape[0] != init_board.shape[0]) or (current_board.shape[1] != init_board.shape[1]):
            result.is_valid = False
            result.error_message = "The current Sudoku board has a size different than the original board."
            return result

        # Check constraint 2: the board must be filled with numbers from 1-n with no repeated numbers in each line, horizontally or vertically.
        for i in range(len(result.rows)):
            row = result.rows[i]
            has_duplicates, duplicated_elem = self._has_duplicates(row)
            if has_duplicates:
                result.is_valid = False
                err_msg_tmpl = "Row {} is invalid, it contains two {}s."
                result.error_message = err_msg_tmpl.format(row, duplicated_elem)
                return result
        
        for j in range(len(result.cols)):
            col = result.cols[j]
            has_duplicates, duplicated_elem = self._has_duplicates(col)
            if has_duplicates:
                result.is_valid = False
                err_msg_tmpl = "Column {} is invalid, it contains two {}s."
                result.error_message = err_msg_tmpl.format(col, duplicated_elem)
                return result
            
        # Check constraint 3: the current board should not overwrite the cells that are already filled before puzzle solving
        for i in range(init_board.shape[0]):
            for j in range(init_board.shape[1]):
                if (init_board[i][j] != consts.SUDOKU_UNFILLED_CELLS_PLACEHOLDER and init_board[i][j] != current_board[i][j]):
                    result.is_valid = False
                    err_msg_tmpl = "Cell [{}][{}] is invalid. The corresponding cell has been filled with {} initially. We cannot set it to a different number."
                    result.error_message = err_msg_tmpl.format(i, j, init_board[i][j])
                    return result
        
        return result

    def _has_duplicates(self, vec):
        if len(vec) <= 1:
            return False
        v = copy.deepcopy(vec)
        v = sorted(v)
        for i in range(len(v) - 1):
            if v[i] == v[i+1]:
                return True, v[i]
        return False, None
        
    
class LLMBasedSudokuStateChecker(StateCheckerBase):
    def __init__(self, state_manager) -> None:
        super().__init__(state_manager)

    def check_current_state(self):
        return None