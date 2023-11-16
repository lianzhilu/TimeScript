from bcc import BPF
from bcc.utils import printb
import time

# define BPF program
prog = """
int hello(void *ctx) {
    bpf_trace_printk("Hello, World!\\n");
    return 0;
}
"""

# load BPF program
b = BPF(text=prog)
b.attach_kprobe(event=b.get_syscall_fnname("openat"), fn_name="hello")

# header
begin = -1
end = -1
timestr = str(time.time())[0:10]
dir = './record/'
f = open(dir+'record_'+timestr+'.txt', 'a')

# format output
while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        f.close()
        continue
    except KeyboardInterrupt:
        f.close()
        exit()
    taskstr = str(task)[2:-1]
    
    if taskstr == "python3" or taskstr == "gnome-shell" or taskstr == "gnome-terminal-" or taskstr == "sudo" or taskstr == "gdbus" or taskstr == "gedit" or taskstr == "gsd-media-keys" or taskstr == "pulseaudio" or taskstr == "ibus-daemon" or taskstr == "nautilus" or taskstr == "ibus-engine-sim" or taskstr == "ibus-extension-" or taskstr == "NetworkManager" or taskstr == "bash":
        continue

    # printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
    if "wasm" in taskstr or "bash" in taskstr:
        now  = time.time()
        
        if begin == -1:
            begin = now
            end = -1
        elif begin != -1 and now - begin > 5 and end == -1:
            end = now
            # print("begin: ", begin)
            # print("end: ", end)
            executime = end-begin-10
            print("execution time: ", executime)
            f.write(str(executime)+'\n')
            begin = end
            end = -1