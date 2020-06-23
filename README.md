# chipmunk_experiment
Install necessary repos
NOTE1: Please put them into one folder
NOTE2: When installing SKETCH, please put add it into the PATH
1. install chipmunk_experiments-tofino and follow the README file inside
   git clone https://github.com/chipmunk-project/chipmunk_experiments-tofino
2. install domino-compiler and follow the README file inside
   git clone https://github.com/chipmunk-project/domino-compiler
3. install domino-examples and follow the README file inside
   git clone https://github.com/chipmunk-project/domino-examples
4. install chipmunk-tofino and follow the README file inside
   git clone https://github.com/chipmunk-project/chipmunk-tofino


test domino program with chipmunk

1. If you want to run all experiments together: 
```
python3 run_expr_simple.py
```

2. If you only want to run one benchmark (Take learn_filter.c as an example)
```
python3 run_iterative_solver_automatically.py ../domino-examples/domino_programs/learn_filter.c 1 example_alus/stateful_alus/raw.alu example_alus/stateless_alus/stateless_alu.alu 5 3 10 2
```

3. If you want to run Chipmunk on one particular Domino program with slicing
```
python3 compile_with_chipmunk.py ../domino-examples/domino_programs/learn_filter.c 1 example_alus/stateful_alus/raw.alu example_alus/stateless_alus/stateless_alu.alu 5 3 10 2
```
