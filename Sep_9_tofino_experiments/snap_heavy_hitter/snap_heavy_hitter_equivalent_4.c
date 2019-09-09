struct Packet{
int srcip;
};
int heavy_hitter[1000000] = {0};
int hh_counter[1000000] = {0};
void func(struct Packet p){
p.srcip=p.srcip;
if (1==1&&heavy_hitter[p.srcip]==0&&1==1&&1==1) {hh_counter[p.srcip]=hh_counter[p.srcip]+1;
if (1==1&&hh_counter[p.srcip]==1000&&1==1&&1==1) {heavy_hitter[p.srcip]=1;

;}

;}
}