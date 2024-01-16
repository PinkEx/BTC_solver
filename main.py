import constraint
from typing import Any, List


class ProblemSolver2p:
    problem_solver: constraint.Problem
    def __init__(self) -> None:
        self.problem_solver = constraint.Problem()
        for i in range(5):
            P = chr(ord("A") + i)
            self.problem_solver.addVariable(
                f"N({P})", list(range(10))
            )
            self.problem_solver.addVariable(
                f"C({P})", ["b", "w", "g"]
            )
            self.problem_solver.addConstraint(
                lambda num, col: (num == 5 and col == "g") or (num != 5 and col != "g"),
                [f"N({P})", f"C({P})"]
            )

        for i in range(4):
            P, Q = chr(ord("A") + i), chr(ord("A") + i + 1)
            self.problem_solver.addConstraint(
                lambda num1, num2, col1, col2:
                    (num1 < num2) or (num1 == 5 and num2 == 5) or (num1 == num2 and col1 == "b" and col2 == "w"),
                [f"N({P})", f"N({Q})", f"C({P})", f"C({Q})"]
            )

    @property
    def possibilities(self):
        solutions, possibilities = self.problem_solver.getSolutions(), []
        for solution in solutions:
            possibility = []
            for i in range(5):
                P = chr(ord("A") + i)
                num, col = solution[f"N({P})"], solution[f"C({P})"]
                possibility.append(f"{num}_{col}")
            possibilities.append(possibility)
        return possibilities
    
    def set_self_code(self, code: List[str]):
        max_5g = 2 - code.count("5_g")
        self.problem_solver.addConstraint(
            lambda num1, num2, num3, num4, num5:
                (num1 == 5) + (num2 == 5) + (num3 == 5) + (num4 == 5) + (num5 == 5) <= max_5g,
            ["N(A)", "N(B)", "N(C)", "N(D)", "N(E)"]
        )
        for i in range(5):
            P = chr(ord("A") + i)
            for tile in code:
                if tile != "5_g":
                    self.problem_solver.addConstraint(
                        lambda num, col: (num != int(tile[0])) or (col != tile[-1]),
                        [f"N({P})", f"C({P})"]
                    )

    def get_question_answer(self, index: int, second_choice: int = -1, answer = None):
        if index == 0:
            self.problem_solver.addConstraint(
                lambda num1, num2, num3, num4, num5, col1, col2, col3, col4, col5:
                    (col1 == "w") * num1 + (col2 == "w") * num2 + (col3 == "w") * num3 + (col4 == "w") * num4 + (col5 == "w") * num5 == answer,
                ["N(A)", "N(B)", "N(C)", "N(D)", "N(E)", "C(A)", "C(B)", "C(C)", "C(D)", "C(E)"]
            )
        elif index == 1:
            self.problem_solver.addConstraint(
                lambda num1, num2, num3, num4, num5, col1, col2, col3, col4, col5:
                    (col1 == "b") * num1 + (col2 == "b") * num2 + (col3 == "b") * num3 + (col4 == "b") * num4 + (col5 == "b") * num5 == answer,
                ["N(A)", "N(B)", "N(C)", "N(D)", "N(E)", "C(A)", "C(B)", "C(C)", "C(D)", "C(E)"]
            )
        elif index == 2:
            for i in range(4):
                P, Q = chr(ord("A") + i), chr(ord("A") + i + 1)
                if (P, Q) in answer:
                    self.problem_solver.addConstraint(
                        lambda col1, col2: col1 == col2,
                        [f"C({P})", f"C({Q})"]
                    )
                else:
                    self.problem_solver.addConstraint(
                        lambda col1, col2: col1 != col2,
                        [f"C({P})", f"C({Q})"]
                    )
        elif index == 3:
            self.problem_solver.addConstraint(
                lambda num1, num2, num3, num4, num5:
                    num1 + num2 + num3 + num4 + num5 == answer,
                ["N(A)", "N(B)", "N(C)", "N(D)", "N(E)"]
            )
        elif index == 4:
            self.problem_solver.addConstraint(
                lambda num1, num2, num3:
                    num1 + num2 + num3 == answer,
                ["N(A)", "N(B)", "N(C)"]
            )
        elif index == 5:
            self.problem_solver.addConstraint(
                lambda num1, num2, num3:
                    num1 + num2 + num3 == answer,
                ["N(C)", "N(D)", "N(E)"]
            )
        elif index == 6:
            self.problem_solver.addConstraint(
                lambda num1, num2, num3:
                    num1 + num2 + num3 == answer,
                ["N(B)", "N(C)", "N(D)"]
            )
        elif index == 7:
            for i in range(4):
                P, Q = chr(ord("A") + i), chr(ord("A") + i + 1)
                if (P, Q) in answer:
                    self.problem_solver.addConstraint(
                        lambda num1, num2: num1 + 1 == num2,
                        [f"N({P})", f"N({Q})"]
                    )
                else:
                    self.problem_solver.addConstraint(
                        lambda num1, num2: num1 + 1 != num2,
                        [f"N({P})", f"N({Q})"]
                    )
        elif index == 8:
            self.problem_solver.addConstraint(
                lambda num1, num2:
                    num2 - num1 == answer,
                ["N(A)", "N(E)"]
            )
        elif index == 9:
            for i in range(5):
                P = chr(ord("A") + i)
                if P in answer:
                    self.problem_solver.addConstraint(
                        lambda num: num == 0,
                        [f"N({P})"]
                    )
                else:
                    self.problem_solver.addConstraint(
                        lambda num: num != 0,
                        [f"N({P})"]
                    )
        elif index == 10:
            for i in range(5):
                P = chr(ord("A") + i)
                if P in answer:
                    self.problem_solver.addConstraint(
                        lambda num: num == 5,
                        [f"N({P})"]
                    )
                else:
                    self.problem_solver.addConstraint(
                        lambda num: num != 5,
                        [f"N({P})"]
                    )
        elif index >= 11 and index <= 14:
            for i in range(5):
                P = chr(ord("A") + i)
                if P in answer:
                    self.problem_solver.addConstraint(
                        lambda num: num == second_choice,
                        [f"N({P})"]
                    )
                else:
                    self.problem_solver.addConstraint(
                        lambda num: num != second_choice,
                        [f"N({P})"]
                    )
        elif index == 15:
            self.problem_solver.addConstraint(
                lambda col1, col2, col3, col4, col5:
                    (col1 == "w") + (col2 == "w") + (col3 == "w") + (col4 == "w") + (col5 == "w") == answer,
                ["C(A)", "C(B)", "C(C)", "C(D)", "C(E)"]
            )
        elif index == 16:
            self.problem_solver.addConstraint(
                lambda col1, col2, col3, col4, col5:
                    (col1 == "b") + (col2 == "b") + (col3 == "b") + (col4 == "b") + (col5 == "b") == answer,
                ["C(A)", "C(B)", "C(C)", "C(D)", "C(E)"]
            )
        elif index == 17:
            self.problem_solver.addConstraint(
                lambda num1, num2, num3, num4, num5:
                    (num1 & 1) + (num2 & 1) + (num3 & 1) + (num4 & 1) + (num5 & 1) == answer,
                ["N(A)", "N(B)", "N(C)", "N(D)", "N(E)"]
            )
        elif index == 18:
            self.problem_solver.addConstraint(
                lambda num1, num2, num3, num4, num5:
                    (~num1 & 1) + (~num2 & 1) + (~num3 & 1) + (~num4 & 1) + (~num5 & 1) == answer,
                ["N(A)", "N(B)", "N(C)", "N(D)", "N(E)"]
            )
        elif index == 19:
            self.problem_solver.addConstraint(
                lambda num1, num2, num3, num4, num5:
                    (num1 == num2) + (num1 == num3) + (num1 == num4) + (num1 == num5) +
                    (num2 == num3) + (num2 == num4) + (num2 == num5) +
                    (num3 == num4) + (num3 == num5) +
                    (num4 == num5) == answer,
                ["N(A)", "N(B)", "N(C)", "N(D)", "N(E)"]
            )
        elif index == 20:
            if answer == "YES":
                self.problem_solver.addConstraint(
                    lambda num: num > 4,
                    ["N(C)"]
                )
            else:
                self.problem_solver.addConstraint(
                    lambda num: num <= 4,
                    ["N(C)"]
                )

if __name__ == "__main__":
    ps = ProblemSolver2p()
    
    print("your private code:")
    self_code = eval(input())
    # e.g. ["0_w", "2_b", "6_b", "9_b", "9_w"]
    ps.set_self_code(self_code)

    # e.g.
    # ["0_b", "3_b", "7_b", "7_w", "8_w"]
    # ps.get_question_answer(index=0, answer=15)
    # ps.get_question_answer(index=1, answer=10)
    # ps.get_question_answer(index=2, answer=[("A", "B"), ("D", "E")])
    # ps.get_question_answer(index=3, answer=25)
    # ps.get_question_answer(index=4, answer=10)
    # ps.get_question_answer(index=5, answer=22)
    # ps.get_question_answer(index=6, answer=17)
    # ps.get_question_answer(index=7, answer=[("D", "E")])
    # ps.get_question_answer(index=8, answer=8)
    # ps.get_question_answer(index=9, answer=["A"])
    # ps.get_question_answer(index=10, answer=[])
    # ps.get_question_answer(index=11, second_choice=1, answer=[])
    # ps.get_question_answer(index=12, second_choice=3, answer=["B"])
    # ps.get_question_answer(index=13, second_choice=7, answer=["C", "D"])
    # ps.get_question_answer(index=14, second_choice=9, answer=[])
    # ps.get_question_answer(index=15, answer=2)
    # ps.get_question_answer(index=16, answer=3)
    # ps.get_question_answer(index=17, answer=3)
    # ps.get_question_answer(index=18, answer=2)
    # ps.get_question_answer(index=19, answer=1)
    # ps.get_question_answer(index=20, answer="YES")
    while True:
        print("problem index:")
        index = int(input())
        if index >= 11 and index <= 14:
            print("second choice:")
            second_choice = int(input())
        else:
            second_choice = -1
        print("answer:")
        answer = eval(input())
        ps.get_question_answer(index=index, second_choice=second_choice, answer=answer)

        sz = len(ps.possibilities)
        print("#possibilities:", sz)
        if sz < 10:
            print(ps.possibilities)