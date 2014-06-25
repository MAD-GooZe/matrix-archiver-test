#!/usr/bin/python

import os
import sys
import filecmp
import subprocess
import threading


TMP_FILE = "tmp.txt"
TMP_FILE_ARC = "tmp_arc.txt"
TIMEOUT = 10
FNULL = open(os.devnull, 'w')

print "Matrix archiver test script for AESC Summer School Contest"

class Command(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self, timeout):
		def target():
			self.process = subprocess.Popen(self.cmd, shell=True, stdout = FNULL, stderr = FNULL)
			self.process.communicate()

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			self.process.terminate()
			thread.join()
			return False
		else:
                        return True

test_size = 0
arc_size = 0
test_num = 0;
passed_tests = 0;

if len(sys.argv) < 3:
    sys.exit('Usage: %s pack.exe unpack.exe' % sys.argv[0])

pack = sys.argv[1]
unpack = sys.argv[2]
show_file_names = False
if len(sys.argv) > 3:
        show_file_names = sys.argv[3] == "-s"

for file in os.listdir("tests"):
	test_num += 1
	testfile = os.path.join("tests", file)
	if show_file_names:
                print "Testing file " + testfile + ".....",
        else:
                print "Testing file #" + str(test_num) + ".....",
	archive = Command(pack + " " + testfile + " " + TMP_FILE_ARC)
	dearchive = Command(unpack + " " + TMP_FILE_ARC + " " + TMP_FILE)
	if not archive.run(timeout = TIMEOUT):
                print "archiving time exceeded"
        elif not dearchive.run(timeout = TIMEOUT):
                print "dearchiving time exceeded"
        else:
                if not os.path.isfile(TMP_FILE_ARC):
                        print "archived file does not exist"
                elif not os.path.isfile(TMP_FILE):
                        print "dearchived file does not exist"
                elif not filecmp.cmp(testfile, TMP_FILE):
                        print "original and dearchived files do not match"
                else:
                        print "success,",
                        orginal_size = os.stat(testfile).st_size
                        archived_size = os.stat(TMP_FILE_ARC).st_size
                        compression = float(archived_size) / float(orginal_size) * 100
                        print "compression: " + str(round(compression, 3)) + "%"
                        test_size += orginal_size
                        arc_size += archived_size
                        passed_tests += 1

	if os.path.isfile(TMP_FILE_ARC):
		os.remove(TMP_FILE_ARC)
        if os.path.isfile(TMP_FILE):
		os.remove(TMP_FILE)
                
print "============================="
print "Passed tests: " + str(passed_tests) + "/" + str(test_num);
if passed_tests != 0:
	print "Original size: ", test_size 
	print "Archived size: ", arc_size
	compression = float(arc_size) / float(test_size) * 100
	print "Summary compression: " + str(round(compression, 3)) + "%"
