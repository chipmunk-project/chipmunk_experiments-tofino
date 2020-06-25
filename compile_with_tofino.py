# domino.c --- (canonocalizer) ---> canonicalizer_file.c --- (grouper)
#  ---> a_group_of_domino_files.cc --- (domino_to_chipmunk) ---> .sk files
#  ---> run iterative_solver on each .sk file

from build_map import generate_cmd_line
import sys
import re
import subprocess
import time

def print_dic(given_dic):
    for x, y in given_dic.items():
        print(x, "<-----------", y)

# output the input matching
# which pkt fields is feeded into which phv container
def input_order(var_dic, given_list):
    print()
    print("For input matching:")
    for i in range(len(given_list)):
        item = given_list[i]
        val = "state_and_packet.pkt_" + item
        for x, y in var_dic.items():
            if y == val:
                print(x, "is mapped to field" + str(i))

# output which value we should focus on
def output_order(var_dic, given_list_of_list):
    print("For this particular slice, we should look at the output of following stateful and stateless variables:")
    assert(len(given_list_of_list) == 2)
    for i in range(2):
        if i == 1:
            for x in given_list_of_list[i]:
                key_word = "state_and_packet.state_group_" + x
                for k, v in var_dic.items():
                    if v.find(key_word) != -1:
                        if v[-1] == '0':
                            # remove the array index part
                            if k.find('[') != -1:
                                k = k[:k.find('[')]
                            print(k, "is mapped to reg_" + x + " register_value_f1")
                        else:
                            assert v[-1] == '1'
                            # remove the array index part
                            if k.find('[') != -1:
                                k = k[:k.find('[')]
                            print(k, "is mapped to reg_" + x + " register_value_f0")
        if i == 0:
            for j in range(len(given_list_of_list[i])):
                val = "state_and_packet.pkt_" + given_list_of_list[i][j]
                for k, v in var_dic.items():
                    if v == val:
                        print(k, "is mapped to field"+ str(j))
    print()

def parse_cmd_line(cmd_str):
    cmd_arr = cmd_str.split(' ')
    # return list include pkt_fields, state_groups, input_pkt
    ret_list = [[], [], []]
    for x in cmd_arr:
        if x == '--pkt-fields':
            i = 0
        elif x == '--state-groups':
            i = 1
        elif x == '--input-packet':
            i = 2
        elif x.isdigit():
            ret_list[i].append(str(x))
    return ret_list

def main(argv):
    """Main program."""
    if len(argv) != 7 :
        print("Usage: python3 " + argv[0] + " <domino program file> <group size> " + "<number of pipeline stages> " +
              "<number of stateless/stateful ALUs per stage> " + "<input bits> " + "bit_size_for_constant_set")
        exit(1)
    # program_file means the original domino program
    program_file = str(argv[1])
    group_size = str(argv[2])
    stateful_alu_file = "example_alus/stateful_alus/tofino.alu"
    stateless_alu_file = "example_alus/stateless_alus/stateless_alu_for_tofino.alu"
    num_pipeline_stages = int(argv[3])
    num_alus_per_stage = int(argv[4])
    input_bits = str(argv[5])
    bit_size_for_constant_set = str(argv[6])

    cmd_line_list, constant_set, total_num_of_grouped_files, given_dic = generate_cmd_line(program_file, group_size, bit_size_for_constant_set)

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
                                 constant_set + " " + input_bits + " --parallel-sketch " + cmd_line_list[i] + " --target-tofino"
                print(str_to_run_in_terminal)
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
                    # TODO:get info from cmd_line_list[i]
                    cmd_info = parse_cmd_line(cmd_line_list[i]) 
                    input_order(given_dic, cmd_info[2])
                    output_order(given_dic, cmd_info[:2])
                    print("Start tofino verification by doing the following steps:")
                    tofino_file_name = sketch_file_name[sketch_file_name.rfind('/') + 1:sketch_file_name.rfind('.')] + \
                                        '_tofino_stateless_alu_for_tofino_' + str(depth) + "_" + str(width) + ".p4"
                    print("Step1: scp " + tofino_file_name + " root@tofino1.cs.nyu.edu:/tmp/autogen.p4")
                    print("Step2: ssh root@tofino1.cs.nyu.edu")
                    print("Step3: cd ~/bf-sde-8.2.0")
                    print("Step4: ./p4_build.sh /tmp/autogen.p4" + "    NOTE:may need some manual semantically equivalent fix to change 0- to -")
                    print("Step5: cd ~/tofino-boilerplate/CP")
                    print("Step6: ./run.sh + feeding the initial value")
                    res_str = input("If pass tofino verification, enter yes, otherwise no: ")
                    if res_str == 'yes':
                        print("verification passed for slice No." + str(i + 1))
                    else:
                        print("verification failed")
                        sys.exit(1)
                    dep_wid_info = re.findall("Synthesis succeeded with (\d+) stages and (\d+) ALUs per stage", output)
                    depth_list.append(int(dep_wid_info[0][0]))
                    width_list.append(int(dep_wid_info[0][1]))
                    time_end=time.time()
                    print("Compilation succeeds for Program: " + program_file[program_file.rfind('/') + 1:] + ", with stateful alu: " + stateful_alu_file + " and stateless alu: " + stateless_alu_file + ", with grid size: " + str(dep_wid_info[0][0]) + " * " + str(dep_wid_info[0][1]) + " in slice " + str(i + 1))
                    print('time cost', round(time_end-time_start, 2),'s')
                    time_used_for_all_slice.append(time_end-time_start)
                    flag = 1
                    break
        if flag == 0:
            print("Compilation fails for Program: " + program_file[program_file.rfind('/') + 1:] + ", with alu: " + stateful_alu_file + " and stateless alu: " + stateless_alu_file + ", with grid size: " + str(num_pipeline_stages) + " * " + str(num_alus_per_stage) + " in slice No." + str(i + 1))
            sys.exit(1)
    print("The total time used if we use parallel computing resources is:", round(max(time_used_for_all_slice),2), 's')
    print("The resource usage is ", max(depth_list), " Stages with " , sum(width_list), " ALUs per stage")
if __name__ == "__main__":
    main(sys.argv)
