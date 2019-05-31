#!/usr/bin/python3

import sys
import getpass
import argparse
import psycopg2
import time
from timeit import default_timer as timer

def main():
  lcnt = 0
  cnt = 0
  ecnt = 0
  verbosity = 0
  emsg=""
  parser = argparse.ArgumentParser(
      add_help=False,
      description='''Test connection to database and simple fast select in loop,
      intended for connection pool testing.'''
    )
  parser.add_argument('-?','--help', help='show this help message and exit', action='help')
  parser.add_argument('-c','--loop-count', help='number of iterations', required=True, type=int)
  parser.add_argument('-s','--sleep', help='number of sleep seconds [float] in active database call', required=False, default=0, type=float)
  parser.add_argument('-S','--sleep-delay', help='number of sleep seconds [float] between two DB calls before disconnect', required=False, default=0, type=float)
  parser.add_argument('-a','--autocommit', help='set autocommit - for statement poolong', required=False, default=False, action='store_true')
  parser.add_argument('-e','--exit-on-error', help='exit on first error', required=False, default=False, action='store_true')
  parser.add_argument('-C','--connection-string', help='Connection string like: "dbname=test user=postgres host=some.host.com port=5432", libPQ environment variables and pgpass file works as expected', required=False)
  parser.add_argument('-v','--verbosity', help='number defining level of output messages verbosity', required=False, type=int, default=0)
  args = vars(parser.parse_args())
  lcnt = args['loop_count']
  verbosity = args['verbosity']
  lstart = timer()
   
  while cnt < lcnt:
    cnt += 1
    if cnt % 1000 == 0:
      print(".", end='', flush=True)
    connstr = "application_name='{}' {}".format(parser.prog, args["connection_string"])
    if verbosity > 2:
      print("Connection string: {}".format(connstr));
    try:
      connection = psycopg2.connect(connstr)
      connection.autocommit = args["autocommit"]
      cursor = connection.cursor()
      # Print PostgreSQL Connection properties
      if verbosity > 1:
        print ( connection.get_dsn_parameters(),"\n")
      # Print PostgreSQL version
      cursor.execute("select * from pg_settings;")
      #cursor.execute("SELECT 1; -- test_query const")
      records = cursor.fetchall()
      time.sleep(args["sleep_delay"])
      cursor.execute("select * from pg_sleep({});".format(args["sleep"]))
      if verbosity > 1:
        print("You are connected to - ", record, "\n")
    except (Exception, psycopg2.Error) as error :
      ecnt += 1
      emsg = error
      if verbosity > 0:
        print ("Error while connecting to PostgreSQL", error)
    finally:
      #closing database connection.
      if ('connection' in locals()) and (connection):
        if not args["autocommit"]:
          connection.commit()
        cursor.close()
        connection.close()
        if verbosity > 1:
          print("PostgreSQL connection is closed")
        if verbosity > 0:
          print("Iteration: {}, Errors: {}".format(cnt, ecnt))
    if (ecnt > 0 and args["exit_on_error"]):
      break
  print("\n")
  lend = timer()
  if ecnt > 0:
    print("Last error:", emsg)
    
  if cnt - ecnt > 0:
    lavgdur = ( lend - lstart )/( cnt - ecnt )
  else:
    lavgdur = "N/A"

  print("Loops: {} of {}, Errors: {}, Total duration: {}, Avg duration [success execution only]: {}".format(
    cnt, lcnt, ecnt, lend - lstart, lavgdur)
  )

if __name__ == "__main__":
   main()
