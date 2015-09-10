# Netlink-taskstats
This is a simple Python module to fetch the TASKSTATS info from the Linux kernel.

You can run it with the command line:

>proc_taststats.py [process-ID]

The output looks like:

process:  29284

{'read_syscalls': 124, 'ac_flag': 2, 'version': 7, 'cpu_run_real_total': 16997416, 'cpu_count': 56, 'stimescaled': 5000, 'write_syscalls': 43, 'ac_uid': 0, 'read_bytes': 0, 'utimescaled': 12000, 'hiwater_vm': 108472, 'cpu_scaled_run_real_total': 16997416, 'cancelled_write_bytes': 0, 'ac_comm': 'bash', 'write_char': 288, 'freepages_count': 0, 'blkio_count': 0, 'swapin_count': 0, 'ac_majflt': 0, 'freepages_delay_total': 0, 'ac_utime': 12000, 'ac_sched': 0, 'ac_ppid': 29279, 'read_char': 63905, 'cpu_delay_total': 4521, 'nvcsw': 55, 'ac_stime': 5000, 'coremem': 24175, 'virtmem': 1954777, 'ac_btime': 1441913015, 'ac_exitcode': 0, 'write_bytes': 0, 'ac_etime': 15252779, 'blkio_delay_total': 0, 'ac_pid': 29284, 'nivcsw': 1, 'swapin_delay_total': 0, 'cpu_run_virtual_total': 22327282, 'ac_gid': 0, 'ac_minflt': 1253, 'ac_nice': 0, 'hiwater_rss': 1892}
