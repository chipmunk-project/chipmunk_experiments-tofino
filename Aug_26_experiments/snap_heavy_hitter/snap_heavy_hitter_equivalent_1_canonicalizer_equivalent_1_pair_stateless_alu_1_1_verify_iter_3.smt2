(assert (forall ((pkt_0_4_6_0  Int  )(state_group_0_state_0_5_7_0  Int  )(state_group_0_state_1_6_8_0  Int  )) (let ((_n0 state_group_0_state_1_6_8_0 ))
(let ((_n1 state_group_0_state_0_5_7_0 ))
(let ((_n2 true ))
(let ((_n3 (+   _n1   (ite  _n2  1 0) ) ))
(let ((_n4 (ite (=  _n0  0)  _n3   _n1  ) ))
(let ((_n5 (<   _n0   (ite  _n2  1 0) ) ))
(let ((_n6 999 ))
(let ((_n7 false ))
(let ((_n8 (ite  _n5   _n1   (ite  _n7  1 0)  ) ))
(let ((_n9 (=   _n8   _n6 ) ))
(let ((_n10 (not  _n9 ) ))
(let ((_n11 (and   _n5   _n10 ) ))
(let ((_n12 (not  _n5 ) ))
(let ((_n13 (or   _n11   _n12 ) ))
(let ((_n14 (not  _n13 ) ))
(let ((_n15 (+   _n1   (ite  _n14  1 0) ) ))
(let ((_n16 (and   _n11   _n5 ) ))
(let ((_n17 (-  (ite  _n16  1 0) )))
(let ((_n18 2 ))
(let ((_n19 (ite  _n16   _n18   (ite  _n7  1 0)  ) ))
(let ((_n20 (+   _n19   _n17 ) ))
(let ((_n21 (ite  _n16   _n20   (ite  _n7  1 0)  ) ))
(let ((_n22 (+   _n1   _n21 ) ))
(let ((_n23 (ite (=  (ite  _n11  1 0)  1)  _n22   _n15  ) ))
(let ((_n24 (ite (=  (ite  _n5  1 0)  1)  _n23   _n1  ) ))
(let ((_n25 (=   _n24   _n4 ) ))
(let ((_n27 (ite (=  _n1  999)  (ite  _n2  1 0)   _n0  ) ))
(let ((_n28 (ite (=  _n0  0)  _n27   _n0  ) ))
(let ((_n29 (+   _n0   (ite  _n14  1 0) ) ))
(let ((_n30 (ite (=  (ite  _n11  1 0)  1)  _n0   _n29  ) ))
(let ((_n31 (ite (=  (ite  _n5  1 0)  1)  _n30   _n0  ) ))
(let ((_n32 (=   _n31   _n28 ) ))
(let ((_n34 pkt_0_4_6_0 ))
(implies  (and (and (>= state_group_0_state_1_6_8_0 0) (< state_group_0_state_1_6_8_0 1024 ))  (and (and (>= state_group_0_state_0_5_7_0 0) (< state_group_0_state_0_5_7_0 1024 ))  (and (>= pkt_0_4_6_0 0) (< pkt_0_4_6_0 1024 )) ) )   (and  _n25  _n32 )  ))))))))))))))))))))))))))))))))))))
(check-sat)
(get-model)
(exit)