import winpexpect as wpx
import subprocess as sub
import time as ti

#child = wpx.winspawn('nios2-terminal 1>&2')
#ti.sleep(2)

#child.sendline('python test2.py')

p = sub.Popen('nios2-terminal 1>&2', shell=False, stderr=sub.PIPE)
#ti.sleep(1.5)

#count = 0
#while (count < 10):
#    barf = child.readline().rstrip()
#    print "barf: %s" % (barf)
#    count = count + 1

#p.kill()
