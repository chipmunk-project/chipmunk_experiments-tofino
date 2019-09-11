/* 
// Original program: 
struct Packet{
int meta_data_dst_tor;
int meta_data_nxt_hop;
int cur_time;
int flow_hash;
int new_flowlet;
int tmp;
};
int best_hop[1000] = {0};
int flowlet_time[1000] = {0};
int flowlet_hop[1000] = {0};
void func(struct Packet p){
if (1==1&&p.cur_time-flowlet_time[p.flow_hash]>1000&&1==1) {p.tmp=best_hop[p.meta_data_dst_tor];
flowlet_hop[p.flow_hash]=p.tmp;
;}
p.meta_data_nxt_hop=flowlet_hop[p.flow_hash];
flowlet_time[p.flow_hash]=p.cur_time;
} */

struct Packet{
    int meta_data_dst_tor;
    int pkt_2;
    int pkt_1;
    int flow_hash;
    int new_flowlet;
    int pkt_0;
};
int state_0 = {0};
int state_2 = {0};
int state_1 = {0};
void func(struct Packet p) {
if (1==1&&p.pkt_1-state_2>1000&&1==1) {p.pkt_0=state_0;
state_1=p.pkt_0;

;}
p.pkt_2=state_1;
state_2=p.pkt_1;

}