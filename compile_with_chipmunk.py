# domino.c --- (canonocalizer) ---> canonicalizer_file.c --- (grouper)
#  ---> a_group_of_domino_files.cc --- (domino_to_chipmunk) ---> .sk files
#  ---> run iterative_solver on each .sk file

from build_map import generate_cmd_line
import sys
import re
import subprocess
import time

def main(argv):
    """Main program."""
    if len(argv) != 9 :
        print("Usage: python3 " + argv[0] + " <domino program file> <group size> <stateful alu file> <stateless alu file> " +
              "<number of pipeline stages> " +
              "<number of stateless/stateful ALUs per stage> " +
              "<input bits> " +
               "bit_size_for_constant_set")
        exit(1)
    # program_file means the original domino program
    program_file = str(argv[1])
    group_size = str(argv[2])
    stateful_alu_file = str(argv[3])
    stateless_alu_file = str(argv[4])
    num_pipeline_stages = int(argv[5])
    num_alus_per_stage = int(argv[6])
    input_bits = str(argv[7])
    bit_size_for_constant_set = str(argv[8])

    cmd_line_list, constant_set, total_num_of_grouped_files = generate_cmd_line(program_file, group_size, bit_size_for_constant_set)

    # Output canonicalizer file to /tmp/file_name_canonicalizer.c
    canonicalizer_file ="/tmp/" + program_file[program_file.rfind('/') + 1 : program_file.rfind('.')] + "_canonicalizer.c"
    
    # Output restore the total number of group files
    # the name of group_files is /tmp/<file_name>_canonicalizer_equivalent_(/d).sk
    group_file = "/tmp/" + canonicalizer_file[canonicalizer_file.rfind('/') + 1:canonicalizer_file.rfind('.')] + "_equivalent_" + str(int(total_num_of_grouped_files) - 1) + ".c"


    # Run iterative solver for grouped files
    sketch_file_name = "/tmp/" + canonicalizer_file[canonicalizer_file.rfind('/') + 1:canonicalizer_file.rfind('.')] + "_equivalent_" + str(int(total_num_of_grouped_files) - 1) +".sk"
    constant_set = "'" + constant_set + "'"
    time_used_for_all_slice = []
    depth_list = []
    width_list = []
    for i in range(len(cmd_line_list)):
        flag = 0
        for depth in range(1, num_pipeline_stages + 1):
            if flag == 1:
                break
            for width in range(1, num_alus_per_stage + 1):
                str_to_run_in_terminal = "iterative_solver " + sketch_file_name + " " + stateful_alu_file + " " + stateless_alu_file + " " + \
                                 str(depth) + " " + str(width) + " " + \
                                 constant_set + " " + input_bits + " --parallel-sketch " + cmd_line_list[i]
                time_start=time.time()
                (ret_code, output) = subprocess.getstatusoutput(str_to_run_in_terminal)
                iterative_solver_output_file_name = '/tmp/' + \
                                            sketch_file_name[sketch_file_name.rfind('/') + 1:sketch_file_name.rfind('.')] + '_' + \
                                            'with_stateful_alu' + '_' + \
                                            stateful_alu_file[stateful_alu_file.rfind('/') + 1:stateful_alu_file.rfind('.')] + '_' + \
                                            'with_stateless_alu' + '_' + \
                                            stateless_alu_file[stateless_alu_file.rfind('/') + 1:stateless_alu_file.rfind('.')] + \
                                            '_' + str(depth) + "_" + str(width) + '_slice_' + str(i + 1) + '.output'
                with open(iterative_solver_output_file_name, 'w') as file:
                    file.write(output)
                # It will return 0 if one of the grouped files get successful compilation
                if (ret_code == 0):
                    dep_wid_info = re.findall("Synthesis succeeded with (\d+) stages and (\d+) ALUs per stage", output)
                    depth_list.append(dep_wid_info[0][0])
                    width_list.append(dep_wid_info[0][1])
                    print(str_to_run_in_terminal)
                    time_end=time.time()
                    print("Compilation succeeds for Program: " + program_file[program_file.rfind('/') + 1:] + ", with stateful alu: " + stateful_alu_file + " and stateless alu: " + stateless_alu_file + ", with grid size: " + str(dep_wid_info[0][0]) + " * " + str(dep_wid_info[0][1]) + " in slice " + str(i + 1))
                    print('time cost', round(time_end-time_start, 2),'s')
                    time_used_for_all_slice.append(time_end-time_start)
                    flag = 1
                    break
        if flag == 0:
            print("Compilation fails for Program: " + program_file[program_file.rfind('/') + 1:] + ", with alu: " + stateful_alu_file + " and stateless alu: " + stateless_alu_file + ", with grid size: " + str(num_pipeline_stages) + " * " + str(num_alus_per_stage) + " in slice No." + str(i + 1))
            sys.exit(1)
    print("The total time used if we use parallel computing resources is:", min(time_used_for_all_slice))
    print("The resource usage is ", max(depth_list), " Stages with ", sum(width_list), " ALUs per stage")
if __name__ == "__main__":
    main(sys.argv)
