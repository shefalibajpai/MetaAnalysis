import psycopg2 as psy
import os, sys
import csv
import codecs

def getExperimentIdsDB(con):
    
    cmd = "select distinct d.experiment_id, e.name from data as d join experiment as e on (e.id = d.experiment_id) order by d.experiment_id"
    cur = con.cursor()
    cur.execute(cmd)
    out = cur.fetchall()
    ids = [i[0] for i in out]
    names = [i[1] for i in out]
    return ids, names


def getBabiesCommonInExp(con, exp_id1, exp_id2, language = None):
    """
    WRITE WHAT THIS FUNCTION DOES
    """
    cmd = "select baby_id from data where experiment_id = %d intersect select baby_id from data where experiment_id =%d"
        
    if language:
        language_filt = str(tuple(language))
        cmd = "select baby_id from data where experiment_id = %d and language in %s intersect select baby_id from data where experiment_id =%d and language in %s"
        if len(language) == 1:
            language_filt = language_filt.replace(',','')
            
    
    cur = con.cursor()
    if language:
        cur.execute(cmd%(exp_id1, language_filt, exp_id2, language_filt))
    else:
        cur.execute(cmd%(exp_id1, exp_id2))
    babies = cur.fetchall()
    babies = [b[0] for b in babies]
    
    return babies