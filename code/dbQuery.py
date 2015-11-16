import psycopg2 as psy
import os, sys
import csv
import codecs

def getExperimentIdsDB(con):
    
    cmd = "select distinct experiment_id from data order by experiment_id"
    cur = con.cursor()
    cur.execute(cmd)
    ids = cur.fetchall()
    ids = [i[0] for i in ids]
    return ids


def getBabiesCommonInExp(con, exp_id1, exp_id2):
    """
    WRITE WHAT THIS FUNCTION DOES
    """
    
    cmd = "select baby_id from data where experiment_id = %d intersect select baby_id from data where experiment_id =%d"
    cur = con.cursor()
    cur.execute(cmd%(exp_id1, exp_id2))
    babies = cur.fetchall()
    babies = [b[0] for b in babies]
    
    return babies