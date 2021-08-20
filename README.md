# Coloring-Puzzle
## Introduction

The CNF Satisfiability Problem (CNF-SAT) is a rendition of the Satisfiability Problem, where the Boolean equation is indicated in the Conjunctive Normal Form (CNF), that implies that it is a combination of statements, where a provision is a disjunction of literals, and an exacting is a variable or its invalidation.

This product of an AND of Ors helps us solve the problems once those have been encoded into Boolean logic. The solutions can be found impulsively by various algorithms and automatic solvers such as SAT solvers. These problems can be the n-queens problem, Sudoku puzzles, Einstein riddle, n-puzzles, Graeco-Latin squares...

Especially, the Coloring Puzzle belongs to that group of problems mentioned above. The puzzle needs filling with either green or red color and the number inside the cell corresponds to the number of green squares adjacent to that cell.

Given a matrix of size m×n, this problem will be solved by pySAT library, A* algorithm, brute-force algorithm and backtracking algorithm, all of these use the logical principles of generated CNFs.

The plan that we apply for this project about the Coloring Puzzle problem is first producing the CNFs by generating many cases on the paper. Subsequently, the team members start discussing and find how to sow the seeds of those CNFs as a premise for the algorithms behind.

Searching on google shows us the solution to this problem is similar to the game fill-a-pix. This helps us process those CNFs faster and ready to deal with the pySAT library (it is almost the same as solving the n-queens problem we used in the previous exercise).

From there, we extend the application of those CNFs to solve the Coloring Puzzle by other algorithms according to the requirements of the problem.
