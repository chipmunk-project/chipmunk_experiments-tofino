import subprocess

program_list = ['rcp.c', 'marple_new_flow.c', 'marple_tcp_nmo.c', 'sampling.c',
                 'stfq.c', 'conga.c', 'snap_heavy_hitter.c', 'spam_detection.c']
grid_size_list = [' 2 2 ', ' 2 2 ', ' 3 2 ', ' 2 1 ', ' 3 3 ', ' 1 2 ', ' 1 1 ', ' 1 1 ']
group_size_list = [' 1 ', ' 1 ', ' 1 ', ' 1 ', ' 1 ', ' 2 ', ' 2 ', ' 2 ']
alu_list = ['pred_raw.alu', 'pred_raw.alu', 'pred_raw.alu', 'if_else_raw.alu', 'nested_ifs.alu', 'pair.alu', 'pair.alu', 'pair.alu']
stateless_alu = 'example_alus/stateless_alus/stateless_alu.alu'
for i in range(len(program_list)):
    domino_file_name = '../domino-examples/domino_programs/' + program_list[i]
    stateful_alu = 'example_alus/stateful_alus/' + alu_list[i]
    grid_size = grid_size_list[i]
    group = group_size_list[i]
    cmd_line_str = 'python3 run_iterative_solver_automatically.py ' + \
                   domino_file_name + group + stateful_alu + ' ' + stateless_alu +\
                   grid_size + '10 2'
    (ret_code, output) = subprocess.getstatusoutput(cmd_line_str)
    print(program_list[i], "output")
    print(output)
