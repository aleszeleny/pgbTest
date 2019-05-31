# pgbTest
Scripts to test pgBouncer

pgbTest.py is single theraded
pgbTestT.py is multi theraded

Testing might require set ``net.ipv4.tcp_tw_reuse = 1`` to reuse TCP ports on testing host otherwise, based on TIME_WAIT and amount
of sessons used, available ports can be quickly exhausted.

Script connects to database defined by connection string or libPQ environment variables and for specified amount of loops it connect, and execute two simple statements to retrieve data from pg_settings and pg_sleep().
Default sleep is zero.
Options can be used to define sleep time, for pg_sleep() call and from ordinary sleep - this was intended to compare load impact for pool modes - statemet/transaction.
For Statement pools, autocommit option is necessary.

If ``.pgpass`` file or ``PGPASSWORD`` environment variable contains password, then it can be ommited. 

Following example did not use autocommit option (tehrefore connect to transactio pool mode) runs 60 test (connect, select..., disconnect) in 10 parallel jobs connection to "-C" option value with 1/2 second sleep by pg_sleep() and 1 second sleep without DB call (simulation some non db related work - session will be in ``idle in transaction`` state).

``./pgbTestT.py  -S 1 -s .5 -e -j 10 -c 60 -C "dbname=test_db host=192.168.1.23 port=6432 user=test_user password=secret"``


```
usage: pgbTest.py [-?] -c LOOP_COUNT [-s SLEEP] [-S SLEEP_DELAY] [-a] [-e]
                  [-C CONNECTION_STRING] [-v VERBOSITY]

Test connection to database and simple fast select in loop, intended for
connection pool testing.

optional arguments:
  -?, --help            show this help message and exit
  -c LOOP_COUNT, --loop-count LOOP_COUNT
                        number of iterations
  -s SLEEP, --sleep SLEEP
                        number of sleep seconds [float] in active database
                        call
  -S SLEEP_DELAY, --sleep-delay SLEEP_DELAY
                        number of sleep seconds [float] between two DB calls
                        before disconnect
  -a, --autocommit      set autocommit - for statement poolong
  -e, --exit-on-error   exit on first error
  -C CONNECTION_STRING, --connection-string CONNECTION_STRING
                        Connection string like: "dbname=test user=postgres
                        host=some.host.com port=5432", libPQ environment
                        variables and pgpass file works as expected
  -v VERBOSITY, --verbosity VERBOSITY
                        number defining level of output messages verbosity
```

```
usage: pgbTestT.py [-?] [-a] [-s SLEEP] [-S SLEEP_DELAY] -c LOOP_COUNT
                   [-C CONNECTION_STRING] [-e] [-j JOB_COUNT] [-v VERBOSITY]

Test connection to database and simple fast select in loop, intended for
connection pool testing.

optional arguments:
  -?, --help            show this help message and exit
  -a, --autocommit      set autocommit - for statement poolong
  -s SLEEP, --sleep SLEEP
                        number of sleep [float] seconds
  -S SLEEP_DELAY, --sleep-delay SLEEP_DELAY
                        number of sleep seconds [float] between two DB calls
                        before disconnect
  -c LOOP_COUNT, --loop-count LOOP_COUNT
                        number of iterations
  -C CONNECTION_STRING, --connection-string CONNECTION_STRING
                        Connection string like: "dbname=test user=postgres
                        host=some.host.com port=5432", libPQ environment
                        variables and pgpass file works as expected
  -e, --exit-on-error   exit on first error
  -j JOB_COUNT, --job-count JOB_COUNT
                        number of loops started in parallel threads
  -v VERBOSITY, --verbosity VERBOSITY
                        number defining level of output messages verbosity
```
