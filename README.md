# chipmunk_experiment
test domino program with chipmunk

1. First install chipmunk (https://github.com/chipmunk-project/chipmunk).
2. Then install the master branch of the domino-compiler(https://github.com/chipmunk-project/domino-compiler)
3. Then run mutator on benchmarks to generate 10 semantically equivalent programs
   (e.g. mutator ~/chipmunk_experiments/domino_experiment_programs/rcp.c) 
4. Then run Chipmunk on all generated mutators
   (e.g. 
   ```
   time python3 run_iterative_solver_automatically.py rcp 10 1 example_alus/stateful_alus/pred_raw.alu example_alus/stateless_alus/stateless_alu.alu 4 4 10 2
   ```)

#TODO: add run_domino_automatically.py to domino-examples repo
5. Then run domino on all generated mutators in domino-examples folder
   (e.g. python3 run_domino_automatically.py rcp banzai_atoms/pred_raw.sk 10)

6. If you want to run Chipmunk on one particular Domino program with slicing
```
   python3 compile_with_chipmunk.py ~/domino_example_test/domino-examples/domino_programs/stfq.c 1 example_alus/stateful_alus/nested_ifs.alu example_alus/stateless_alus/stateless_alu.alu 3 3 10 2
```
Note: August 15, 2019: The python script has been changed. So the above command lines need to be updated accordingly.
