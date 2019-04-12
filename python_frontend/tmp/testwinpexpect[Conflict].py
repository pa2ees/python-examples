import winpexpect as wpx
import subprocess as sub
import time as ti

#child = wpx.winspawn('nios2-terminal --flush')
#ti.sleep(2)

#child.sendline('python test2.py')

p = sub.Popen('nios2-terminal --quiet', shell=False)
ti.sleep(1.5)
p.kill()


#while (count < 10):
#    barf = child.readline().rstrip()
#    print "barf: %s" % (barf)

