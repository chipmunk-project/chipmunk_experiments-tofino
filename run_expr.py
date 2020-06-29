import subprocess
import sys
from build_map import generate_cmd_line
import time
import re

def run_simple(program_list, grid_size_list, group_size_list, alu_list, stateless_alu):
    for i in range(len(program_list) -1, -1, -1):
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
    
def run_complex(program_dict):
    for x, y  in program_dict.items():
            domino_file_name = '../domino-examples/domino_programs/' + x
            print(domino_file_name)
            filename = domino_file_name[domino_file_name.rfind('/') + 1 : domino_file_name.rfind('.')]
            stateful_alu_file = 'example_alus/stateful_alus/' + y[2]
            stateless_alu_file = 'example_alus/stateless_alus/stateless_alu.alu'
 
            group_size = y[1]

            (ret_code, output) = subprocess.getstatusoutput("mutator " + domino_file_name)
            assert ret_code == 0, "mutator failed"

            total_num_of_files = 10
            Sum = 0
            time_group = []
            depth_list = []
            width_list = []
            #add a for loop for all mutations
            for i in range(total_num_of_files):
                bit_size_for_constant_set = '2'
                program_file = "/tmp/" + filename + "_equivalent_" + str(i+1) + ".c"

                cmd_line_list, constant_set, total_num_of_grouped_files, _ = generate_cmd_line(program_file, group_size, bit_size_for_constant_set)
                # Output canonicalizer file to /tmp/file_name_canonicalizer.c
                canonicalizer_file ="/tmp/" + filename + "_equivalent_" + str(i+1) + "_canonicalizer.c"
     
                # Output restore the total number of group files
                # the name of group_files is /tmp/<file_name>_canonicalizer_equivalent_(/d).sk
                group_file = "/tmp/" + canonicalizer_file[canonicalizer_file.rfind('/') + 1:canonicalizer_file.rfind('.')] + "_equivalent_" + str(int(total_num_of_grouped_files) - 1) + ".c"
             
                # Run iterative solver for grouped files
                sketch_file_name = "/tmp/" + canonicalizer_file[canonicalizer_file.rfind('/') + 1:canonicalizer_file.rfind('.')] + "_equivalent_" + str(int(total_num_of_grouped_files) - 1) +".sk"
                constant_set = "'" + constant_set + "'"
                time_used_for_all_slice = []
                depth_list = []
                width_list = []
                input_bits = '10'
                for i in range(len(cmd_line_list)):
                    flag = 0
                    for g in y[0]:
                        depth = g.split(' ')[1]
                        width = g.split(' ')[2]
                        str_to_run_in_terminal = "iterative_solver " + sketch_file_name + " " + stateful_alu_file + " " + stateless_alu_file + " " + \
                                         g + \
                                         constant_set + " " + input_bits + " --parallel-sketch " + cmd_line_list[i]
                        time_start=time.time()
                        (ret_code, output) = subprocess.getstatusoutput(str_to_run_in_terminal)
                        iterative_solver_output_file_name = '/tmp/' + \
                                                    sketch_file_name[sketch_file_name.rfind('/') + 1:sketch_file_name.rfind('.')] + '_' + \
                                                    'with_stateful_alu' + '_' + \
                                                    stateful_alu_file[stateful_alu_file.rfind('/') + 1:stateful_alu_file.rfind('.')] + '_' + \
                                                    'with_stateless_alu' + '_' + \
                                                    stateless_alu_file[stateless_alu_file.rfind('/') + 1:stateless_alu_file.rfind('.')] + \
                                                    '_' + depth + "_" + width + '_slice_' + str(i + 1) + '.output'
                        with open(iterative_solver_output_file_name, 'w') as file:
                            file.write(output)
                        # It will return 0 if one of the grouped files get successful compilation
                        if (ret_code == 0):
                            dep_wid_info = re.findall("Synthesis succeeded with (\d+) stages and (\d+) ALUs per stage", output)
                            depth_list.append(int(dep_wid_info[0][0]))
                            width_list.append(int(dep_wid_info[0][1]))
                            print(str_to_run_in_terminal)
                            time_end=time.time()
                            print("Compilation succeeds for Program: " + program_file[program_file.rfind('/') + 1:] + ", with stateful alu: " + stateful_alu_file + " and stateless alu: " + stateless_alu_file + ", with grid size: " + str(dep_wid_info[0][0]) + " * " + str(dep_wid_info[0][1]) + " in slice " + str(i + 1))
                            print('time cost', round(time_end-time_start, 2),'s')
                            time_used_for_all_slice.append(time_end-time_start)
                            flag = 1
                            break
                    if flag == 0:
                        print("Compilation fails for Program: " + program_file[program_file.rfind('/') + 1:] + ", with alu: " + stateful_alu_file + " and stateless alu: " + stateless_alu_file + " in slice No." + str(i + 1))
                        sys.exit(1)
                print("The total time used if we use parallel computing resources is:", round(max(time_used_for_all_slice),2), 's')
                print("The resource usage is ", max(depth_list), " Stages with " , sum(width_list), " ALUs per stage")

def main(argv):
    """Main program."""
    if len(argv) != 2:
        print("Usage: python3 " + argv[0] + " <simple/simple_part/complex>")
        sys.exit(1)
    run_type = argv[1]
    assert run_type == "simple" or run_type == "simple_part" or run_type == "complex", "please provide the correct run_type"
    if run_type == "simple": 
        program_list = ['rcp.c', 'marple_new_flow.c', 'marple_tcp_nmo.c', 'sampling.c',
                         'stfq.c', 'conga.c', 'snap_heavy_hitter.c', 'spam_detection.c']
        grid_size_list = [' 2 2 ', ' 2 2 ', ' 3 2 ', ' 2 1 ', ' 3 3 ', ' 1 2 ', ' 1 1 ', ' 1 1 ']
        group_size_list = [' 1 ', ' 1 ', ' 1 ', ' 1 ', ' 1 ', ' 2 ', ' 2 ', ' 2 ']
        alu_list = ['pred_raw.alu', 'pred_raw.alu', 'pred_raw.alu', 'if_else_raw.alu', 'nested_ifs.alu', 'pair.alu', 'pair.alu', 'pair.alu']
        stateless_alu = 'example_alus/stateless_alus/stateless_alu.alu'
        run_simple(program_list, grid_size_list, group_size_list, alu_list, stateless_alu)
    elif run_type == "simple_part":
        program_list = ['sampling.c','snap_heavy_hitter.c', 'spam_detection.c']
        grid_size_list = [' 2 1 ', ' 1 1 ', ' 1 1 ']
        group_size_list = [' 1 ', ' 2 ', ' 2 ']
        stateless_alu = 'example_alus/stateless_alus/stateless_alu.alu'
        run_simple(program_list, grid_size_list, group_size_list, alu_list, stateless_alu)
    else:
        assert run_type == "complex"
        program_dict = {"dns_ttl_change.c" : [[' 1 1 ', ' 3 4 '], ' 1 ' ,'nested_ifs.alu'],
                        "stateful_fw.c" : [[' 1 1 ', ' 1 2 ', ' 4 3 '], ' 1 ', 'pred_raw.alu'],
                        "flowlets.c" : [[' 1 1 ', ' 3 3 '], ' 1 ', 'pred_raw.alu'],
                        "learn_filter.c" : [[' 1 1 ', ' 3 2 '], ' 1 ', 'raw.alu'],
                        "blue_decrease.c" : [[' 1 1 ', ' 4 2 '], ' 1 ', 'sub.alu'],
                       }
        run_complex(program_dict)

if __name__ == "__main__":
    main(sys.argv)
