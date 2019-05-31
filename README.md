# pgbTest
Scripts to test pgBouncer

pgbTest.py is single theraded
pgbTestT.py is multi theraded

Testing might require set ``net.ipv4.tcp_tw_reuse = 1`` to reuse TCP ports on testing host otherwise, based on TIME_WAIT and amount
of sessons used, available ports can be quickly exhausted.
