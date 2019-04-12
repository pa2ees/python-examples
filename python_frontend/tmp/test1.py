import subprocess as sub
import threading as thr
import Queue as qu
import time as ti
from signal import CTRL_C_EVENT

def get_output(prog_q, out_q, kill_prog_q):
    active_proc = None
    prog_dead = True
    thread_dead = False
    while thread_dead == False:
        if prog_dead == False:
            line = active_proc.readline().rstrip()
            #print "put line: %s" % (line)
            out_q.put(line)
        if prog_q.empty() == False and prog_dead == True:
            #print "should not get here much"
            active_proc = prog_q.get()
            if active_proc != None:
                prog_dead = False
        try: killit = kill_prog_q.get_nowait()
        except qu.Empty:
            pass
        else:
            if killit == 1:
                prog_dead = True
                #print "not done with thread\n"
                #ti.sleep(3)
                kill_prog_q.task_done()
            if killit == -1:
                thread_dead = True
                #print "Thread will die\n"
                kill_prog_q.task_done()
                

p = sub.Popen(['nios2-terminal', '--quiet'], shell=False, stdout=sub.PIPE)
#p = sub.Popen(('C:/Altera/11.0/qprogrammer/bin/quartus_pgm -c \"USB-Blaster [USB-0]\" --mode=JTAG -o p;\"D:/Altera Projects/Enterprise/adc_x/trx.sof\"'), shell=True, stdout=sub.PIPE, stderr=sub.STDOUT)

out_q = qu.Queue()
prog_q = qu.Queue()
kill_prog_q = qu.Queue()
t = thr.Thread(target=get_output, args=(prog_q, out_q, kill_prog_q))
t.daemon = True
t.start()
prog_q.put(p.stdout)

count = 0

while count < 300:
    count = count + 1
    try: line = out_q.get(False)
    except qu.Empty:
        #if (count % 10 == 0):
        #    print("#")
        pass
    else:
        if line == 'done':
            count = 1000
            break
        print "barf: %s" % (line)
        
    ti.sleep(0.01)

    if(count % 100 == 0):
        pass

kill_prog_q.put(1)
kill_prog_q.join()
#print "Thread should be idle"
p.kill()

with out_q.mutex:
    out_q.queue.clear()

ti.sleep(3)

p = sub.Popen(['nios2-terminal', '--quiet'], shell=False, stdout=sub.PIPE)
prog_q.put(p.stdout)

count = 0
while(count < 300):
    #count = count + 1
    try: line = out_q.get(False)
    except qu.Empty:
        #if (count % 10 == 0):
        #    print("#")
        pass
    else:
        if line == 'done':
            count = 1000
            break
        print "barf: %s" % (line)
        
    ti.sleep(0.01)

    if(count % 100 == 0):
        pass

kill_prog_q.put(-1)
kill_prog_q.join()
#print "thread should be dead"

p.kill()

with out_q.mutex:
    out_q.queue.clear()

#ti.sleep(1)
