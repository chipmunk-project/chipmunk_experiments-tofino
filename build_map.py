import re
import subprocess

def print_dic(given_dic):
    for x, y in given_dic.items():
        print(x, "<-----------", y)

# if list_x is a subset of list_y return true
def contain(list_x, list_y):
    if len(list_x) > len(list_y):
        return False
    for i in range(len(list_x)):
        if list_x[i] not in list_y:
            return False
    return True

def generate_cmd_line(program_file, group_size, bit_size_for_constant_set):
    # Run domino
    (ret_code, output) = subprocess.getstatusoutput("domino " + program_file + " hh.sk 10 10")
    
    # Run canonicalizer
    print("canonicalizer " + program_file)
    (ret_code, output) = subprocess.getstatusoutput("canonicalizer " + program_file)
    assert ret_code == 0, "canonicalizer failed"
    
    canonicalizer_file ="/tmp/" + program_file[program_file.rfind('/') + 1 : program_file.rfind('.')] + "_canonicalizer.c"
    # grouper
    (ret_code, total_num_of_grouped_files) = subprocess.getstatusoutput("grouper " + canonicalizer_file + " " + group_size)
    assert ret_code == 0, "grouper failed"
    
    group_file = "/tmp/" + canonicalizer_file[canonicalizer_file.rfind('/') + 1:canonicalizer_file.rfind('.')] + "_equivalent_" + str(int(total_num_of_grouped_files) - 1) + ".c"

    (ret_code, constant_set) = subprocess.getstatusoutput(("constant_set " + group_file + " " + bit_size_for_constant_set))
    assert ret_code == 0, "constant_set failed"
    # domino_to_chipmunk
    (ret_code, output) = subprocess.getstatusoutput("domino_to_chipmunk " + group_file)
    assert ret_code == 0, "domino_to_chipmunk failed"
    
    # build dic for each file
    file_name_list = ["/tmp/canonicalizer_map.txt", "/tmp/grouper_map.txt", "/tmp/domino_to_chipmunk_map.txt"]
    dic_list = [{}, {}, {}]
    
    # read from each file from file_name_list and put them into the dict
    for i in range(len(file_name_list)):
        filename = file_name_list[i]
        f = open(filename, "r")
        for x in f:
            key = x.split(':')[0]
            val = x.split(':')[1].split(',')
            assert len(val) == 1, "wrong length of val"
            if val[-1][-1] == '\n':
                val[-1] = val[-1][:-1]
            dic_list[i][key] = val[0]
    
    # propagate dic_list
    for i in range(1, len(file_name_list)):
        for x in dic_list[0]:
            if dic_list[0][x] in dic_list[i]:
                 dic_list[0][x] = dic_list[i][dic_list[0][x]]
    
    # Build the influ_dic
    # i.e. last_update:last_update,p.now --> key: last_update; val: [p.now, last_update]
    influ_dic = {}
    influence_map_file = "/tmp/influence_map.txt"
    f = open(influence_map_file, "r")
    for x in f:
        key = x.split(':')[0]
        val = x.split(':')[1].split(',')
        # remove the '\n' char
        if val[-1][-1] == '\n':
            val[-1] = val[-1][:-1]
        for i in range(len(val)):
            val[i] = dic_list[0][val[i]]
        influ_dic[dic_list[0][key]] = val
    
    # record how many stateful groups and how many packet fields
    total_state_groups = []
    total_packet_fields = []
    for x in influ_dic:
        if x.find("state_group_") != -1:
            group_num = re.findall("state_and_packet.state_group_(\d+)", x)
            if group_num[0] not in total_state_groups:
                total_state_groups.append(group_num[0])
        else:
            assert x.find("pkt_") != -1
            pkt_field = re.findall("state_and_packet.pkt_(\d+)", x)
            total_packet_fields.append(pkt_field[0])
            
        
    # Keep ascending order
    total_state_groups.sort()
    total_packet_fields.sort()
    
    # build the cmd line str
    cmd_line_list = []
    # build cmd line str for packet fields
    for i in range(len(total_packet_fields)):
        state_groups = []
        input_packet = []
        key = "state_and_packet.pkt_" + str(total_packet_fields[i])
        for x in influ_dic[key]:
            if x.find("state_group_") != -1:
                group_num = re.findall("state_and_packet.state_group_(\d+)", x)[0]
                if group_num not in state_groups:
                    state_groups.append(group_num)
                if group_num in total_state_groups:
                    total_state_groups.remove(group_num)
            else:
                assert x.find("pkt_") != -1
                pkt_num = re.findall("state_and_packet.pkt_(\d+)", x)[0]
                if pkt_num not in input_packet:
                    input_packet.append(pkt_num)
        state_groups.sort()
        input_packet.sort()
        # build the cmd line
        cmd_str = " --pkt-fields " + str(total_packet_fields[i])
        if len(state_groups) != 0:
            cmd_str += " --state-groups "
            for index in state_groups:
                 cmd_str += str(index) + " "
        if len(input_packet) == 0:
            # only set the input packet to be 0
            cmd_str += " --input-packet 0"
        else:
            cmd_str += " --input-packet "
            for index in input_packet:
                cmd_str += str(index) + " "
        cmd_line_list.append(cmd_str)

    state_dic = {}
    # Find influencer
    for i in range(len(total_state_groups)):
        state_groups = []
        # only need to take care of the state_0 in each state group
        key = "state_and_packet.state_group_" + str(total_state_groups[i]) + "_state_0"
        for x in influ_dic[key]:
            if x.find("state_group_") != -1:
                group_num = re.findall("state_and_packet.state_group_(\d+)", x)[0]
                if group_num not in state_groups:
                    state_groups.append(group_num)
        state_dic[key] = state_groups
    remove_list_state = []
    for x in state_dic:
        for y in state_dic:
            if x != y:
                if (x not in remove_list_state) and contain(state_dic[x], state_dic[y]):
                    remove_list_state.append(x)
                elif (y not in remove_list_state) and contain(state_dic[y], state_dic[x]):
                    remove_list_state.append(y)
    
    # build cmd line str for stateful vars
    for i in range(len(total_state_groups)):
        state_groups = []
        input_packet = []
        key = "state_and_packet.state_group_" + str(total_state_groups[i]) + "_state_0"
        if key in remove_list_state:
            continue
        for x in influ_dic[key]:
            if x.find("state_group_") != -1:
                group_num = re.findall("state_and_packet.state_group_(\d+)", x)[0]
                if group_num not in state_groups:
                    state_groups.append(group_num)
            else:
                assert x.find("pkt_") != -1
                pkt_num = re.findall("state_and_packet.pkt_(\d+)", x)[0]
                if pkt_num not in input_packet:
                    input_packet.append(pkt_num) 
        state_groups.sort()
        input_packet.sort()
        # build the cmd line
        cmd_str = " --state-groups "
        if len(state_groups) != 0:
            for index in state_groups:
                 cmd_str += str(index) + " "
        if len(input_packet) == 0:
            # only set the input packet to be 0
            cmd_str += " --input-packet 0"
        else:
            cmd_str += " --input-packet "
            for index in input_packet:
                cmd_str += str(index) + " "
        cmd_line_list.append(cmd_str)
    return cmd_line_list, constant_set, total_num_of_grouped_files

def run_all_experiments():
    program_file_list = ['learn_filter.c', 'blue_increase.c', 'blue_decrease.c', 'stateful_fw.c', 'dns_ttl_change.c', 'flowlets.c', 'rcp.c',
                         'marple_new_flow.c', 'marple_tcp_nmo.c', 'sampling.c', 'stfq.c', 'conga.c', 'snap_heavy_hitter.c', 'spam_detection.c']
    group_size_list = ['1','1','1','1','1','1','1','1','1','1','1','2','2','2']

    for i in range(len(program_file_list)):
        program_file = "/Users/Xiangyu/domino_example_test/domino-examples/domino_programs/" + program_file_list[i]
        group_size = group_size_list[i] 
        generate_cmd_line(program_file, group_size, "2")
