# Netlink-taskstats
This is a simplified Python module to fetch the TASKSTATS info from the Linux kernel.

You can run it with the command line:

>proc_taststats.py [process-ID]

The output looks like:

process:  28663
{'read_syscalls': 251, 'ac_flag': 2, 'version': 7, 'cpu_run_real_total': 23996352, 'cpu_count': 16, 'stimescaled': 8000, 'write_syscalls': 16, 'ac_uid': 1008, 'read_bytes': 0, 'utimescaled': 16000, 'hiwater_vm': 201976, 'cpu_scaled_run_real_total': 23996352, 'cancelled_write_bytes': 0, 'ac_comm': 'su', 'write_char': 1822, 'freepages_count': 0, 'blkio_count': 0, 'swapin_count': 0, 'ac_majflt': 0, 'freepages_delay_total': 0, 'ac_utime': 16000, 'ac_sched': 0, 'ac_ppid': 28549, 'read_char': 575242, 'cpu_delay_total': 506701, 'nvcsw': 13, 'ac_stime': 8000, 'coremem': 33899, 'virtmem': 1953220, 'ac_btime': 1441902417, 'ac_exitcode': 0, 'write_bytes': 0, 'ac_etime': 18984951, 'blkio_delay_total': 0, 'ac_pid': 28663, 'nivcsw': 3, 'swapin_delay_total': 0, 'cpu_run_virtual_total': 24332020, 'ac_gid': 1008, 'ac_minflt': 1109, 'ac_nice': 0, 'hiwater_rss': 3568}
