#! /usr/bin/env python3
import os
import sys
import signal
import logging
import traceback
from time import sleep
from os.path import exists
from subprocess import Popen, PIPE, call
import re
import urllib.parse
flag_pattern = re.compile(r"OOO%7B[A-Za-z0-9_\-!@#$%^&*]{20,100}%7D")

"""
This just tests a valid CC that's stored in the CC processing DB
"""
def test_valid_cc():

    stdout = make_contact("6360337890123455", "21","12")
    try:
        assert stdout.find(b"/livevid.html?message=Viewing%20authorized") > -1

        flags = re.findall(flag_pattern, stdout.decode('latin-1'))
        if flags:
            print(urllib.parse.unquote(flags[0]))
        else:
            print(stdout)
    except AssertionError as ae:
        print(stdout)
        raise ae

#
def make_contact(ccnum, expMM, expYY, referer_val="https://goforit.com/purchase.html"):
    url = "http://{}:{}/cc/process.js?card-number={}&expiry-year={}&expiry-month={}".format(sys.argv[1], sys.argv[2], ccnum, expYY, expMM)

    cmd = ["wget", "-O", "-", "--header", "Referer: {}".format(referer_val), url]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)

    stdout, stderr = p.communicate()

    return stdout + stderr


def run_all():
    # cmd = [server_js]  # start server
    # server_stdout = open("/tmp/server_stdout.log", "w")
    #
    # pserver = Popen(cmd, stdout=server_stdout, stderr=server_stdout)
    # sleep(.2)
    current_fn = ""
    try:

        functions = globals()
        all_functions = dict(filter((lambda kv: kv[0].startswith('test_')), functions.items()))
        for f in sorted(all_functions.keys()):
            if hasattr(all_functions[f], '__call__'):
                current_fn = f
                all_functions[f]()

    except Exception as ex:
        print("Error while processing " + current_fn)
        print(ex)
        traceback.print_exc()
        print("Error while processing " + current_fn)
        exit(99)
    finally:
        pass
        # if exists("/tmp/server_stdout.log"):
        #     print("-"*50 + "SERVER OUTPUT" + "-"*50)
        #     print(open("/tmp/server_stdout.log","r").read())
        #     print("-"*100)
        #call(["pkill", "node"])

if __name__ == "__main__":
    logging.getLogger("CCtests").setLevel("DEBUG")

    run_all()







