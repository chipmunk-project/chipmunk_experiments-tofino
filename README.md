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
1.1 part of simple example
```
python3 run_expr.py simple_part
```
1.2 all of simple examples
```
python3 run_expr.py simple
```

1.3 all of complex examples
```
python3 run_expr.py complex
```

2. If you only want to run one benchmark (Take learn_filter.c as an example)
```
python3 run_iterative_solver_automatically.py ../domino-examples/domino_programs/learn_filter.c 1 example_alus/stateful_alus/raw.alu example_alus/stateless_alus/stateless_alu.alu 5 3 10 2
```

3. If you want to run Chipmunk on one particular Domino program with slicing (Take learn_filter.c as an example)
```
python3 compile_with_chipmunk.py ../domino-examples/domino_programs/learn_filter.c 1 example_alus/stateful_alus/raw.alu example_alus/stateless_alus/stateless_alu.alu 5 3 10 2
```
5. If you want to run Chipmunk with Tofino ALU (Take conga.c as an example)
```
python3 compile_with_tofino.py ../domino-examples/domino_programs/sampling.c 1 3 3 10 2
python3 compile_with_tofino.py ../domino-examples/domino_programs/rcp.c 1 1 6 10 2
python3 compile_with_tofino.py ../domino-examples/domino_programs/marple_new_flow.c 1 2 3 10 2
python3 compile_with_tofino.py ../domino-examples/domino_programs/marple_tcp_nmo.c 1 3 2 10 2
python3 compile_with_tofino.py ../domino-examples/domino_programs/conga.c 2 1 3 10 2
python3 compile_with_tofino.py ../domino-examples/domino_programs/snap_heavy_hitter.c 2 1 2 10 2
python3 compile_with_tofino.py ../domino-examples/domino_programs/blue_increase.c 1 4 2 10 2
python3 compile_with_tofino.py ../domino-examples/domino_programs/blue_decrease.c 1 4 2 10 2
python3 compile_with_tofino.py ../domino-examples/domino_programs/dns_ttl_change.c 1 3 6 10 2
python3 compile_with_tofino.py ../domino-examples/domino_programs/flowlets.c 1 3 5 10 2
```
The following steps are used to run p4 in tofino
Step1: scp <generated p4 program> root@tofino1.cs.nyu.edu:/tmp/autogen.p4
Step2: ssh root@tofino1.cs.nyu.edu
Step3: cd ~/bf-sde-8.2.0
Step4: ./p4_build.sh /tmp/autogen.p4    NOTE:may need some manual semantically equivalent fix to change 0- to -
Step5: cd ~/tofino-boilerplate/CP
Step6: ./run.sh + feeding the initial value
