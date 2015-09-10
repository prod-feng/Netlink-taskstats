#!/usr/bin/python
#
###
#
import struct, socket
import errno
import os
import array


# Definde the constants for NetLink module
ACK_REQUEST = (4 | 1)

NETLINK_ROUTE = 0
NETLINK_GENERIC = 16


NLM_F_REQUEST = 1
NLMSG_MIN_TYPE  = 0x10

GENL_ID_CTRL            = NLMSG_MIN_TYPE


NLMSG_NOOP      =        0x1     #/* Nothing.             */
NLMSG_ERROR     =        0x2     #/* Error                */
NLMSG_DONE      =        0x3     #/* End of a dump        */
NLMSG_OVERRUN   =        0x4     #/* Data lost            */



CTRL_CMD_UNSPEC         = 0
CTRL_CMD_NEWFAMILY      = 1
CTRL_CMD_DELFAMILY      = 2
CTRL_CMD_GETFAMILY      = 3
CTRL_CMD_NEWOPS         = 4
CTRL_CMD_DELOPS         = 5
CTRL_CMD_GETOPS         = 6

CTRL_ATTR_UNSPEC        = 0
CTRL_ATTR_FAMILY_ID     = 1
CTRL_ATTR_FAMILY_NAME   = 2
CTRL_ATTR_VERSION       = 3
CTRL_ATTR_HDRSIZE       = 4
CTRL_ATTR_MAXATTR       = 5
CTRL_ATTR_OPS           = 6


GE_Attr_Fmt=[
9,#   0 CTRL_ATTR_UNSPEC
'''=H''',# 1 U16(skb, CTRL_ATTR_FAMILY_ID
0,#   2 STRING(skb, CTRL_ATTR_FAMILY_NAME
'''=I''',# 3 U32(skb, CTRL_ATTR_VERSION
'''=I''',# 4 U32(skb, CTRL_ATTR_HDRSIZE
'''=I''',# 5 U32(skb, CTRL_ATTR_MAXATTR
'''=I''',# 6 U32(skb, CTRL_ATTR_OP_ID
'''=I''',# 7 U32(skb, CTRL_ATTR_OP_FLAGS
'''=I''',# 8 U32(skb, CTRL_ATTR_MCAST_GRP_ID
9 #  9 STRING(skb, CTRL_ATTR_MCAST_GRP_NAME
]

GE_Attr=[
0,#0,
0,#1,
0,#2,
0,#3,
0,#4,
0,#5,
0,#6,
0,#7,
0,#8,
0#9
]

TASKSTATS_CMD_ATTR_PID = 1
TASKSTATS_CMD_ATTR_TGID =2


TASKSTATS_TYPE_PID = 1 #             /* Process id */
TASKSTATS_TYPE_TGID = 2 #            /* Thread group id */
TASKSTATS_TYPE_STATS = 3 #           /* taskstats structure */
TASKSTATS_TYPE_AGGR_PID = 4 #        /* contains pid + stats */
TASKSTATS_TYPE_AGGR_TGID =5 #       /* contains tgid + stats */

TASKSTATS_CMD_GET = 1 #             /* user->kernel request/get-response */
TASKSTATS_CMD_NEW = 2 #             /* kernel->user event */

TASKSTATS_fields = [
 'version', 'ac_exitcode',
 'ac_flag', 'ac_nice',
 'cpu_count', 'cpu_delay_total',
 'blkio_count', 'blkio_delay_total',
 'swapin_count', 'swapin_delay_total',
 'cpu_run_real_total', 'cpu_run_virtual_total',
 'ac_comm',
 'ac_sched',
 'ac_uid', 'ac_gid', 'ac_pid', 'ac_ppid',
 'ac_btime', 'ac_etime', 'ac_utime', 'ac_stime',
 'ac_minflt', 'ac_majflt',
 'coremem',
 'virtmem',
 'hiwater_rss', 'hiwater_vm',
 'read_char', 'write_char', 'read_syscalls', 'write_syscalls',
 'read_bytes', 'write_bytes', 'cancelled_write_bytes',
 'nvcsw', 'nivcsw',
 'utimescaled', 'stimescaled', 'cpu_scaled_run_real_total',
 'freepages_count', 'freepages_delay_total'
]

TASKSTATS_fmt = 'HIBBQQQQQQQQ32sIxxxIIIIIQQQQQQQQQQQQQQQQQQQQQQQ'


debug = 0

class Proc_TaskStats(object):
  """
  Module for processing CPU and disk IO information using TaskStats.
  """
  def __init__(self, process):
    self.name = "Proc_TaskStats"
    self.__pid__ = process

    self.socket = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_GENERIC)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)


    self.socket.bind((0,0))

    self.pid, self.groups = self.socket.getsockname()
    if debug > 0: print "self.pid:",self.pid


    self.type = GENL_ID_CTRL
    self.flags = NLM_F_REQUEST

    self.proc_gentlink()

    if debug > 0: print "Family ID: ", GE_Attr[CTRL_ATTR_FAMILY_ID]
    self.proc_taskstats()

    self.socket.close()

  def proc_taskstats(self):
    #get TASKSTATS info
    msg_ts=array.array(str('B'))
    msg_ts.fromstring(struct.pack("BBxx", TASKSTATS_CMD_GET, 0))

    #May need to validate the pid here
    if debug > 0: print "process id: ",self.__pid__
    cmd=struct.pack('=I', int(self.__pid__))
    mlen=len(cmd) + 4

    msg_ts.fromstring(struct.pack("HH", mlen, TASKSTATS_CMD_ATTR_PID))
    msg_ts.fromstring(cmd)
    msg_ts.fromstring('\0' * ((4 - (len(cmd) % 4)) & 0x3))

    nlmhdr_msg=array.array(str('B'),struct.pack(str('=IHHII'), len(msg_ts) + 16, GE_Attr[CTRL_ATTR_FAMILY_ID], ACK_REQUEST, 1, self.pid))
    nlmhdr_msg.extend(msg_ts)

    self.socket.send(nlmhdr_msg)

    data = self.socket.recv(65536)

    data=self.unpack_nlhdr(data)
    data=self.unpack_genlhdr(data)
    self.unpack_taskstats(data)


  def unpack_taskstats(self,data):
    #get TASKSTATS info
    # may need to check the lens and types above. Not now.
    attrs = dict(zip(TASKSTATS_fields, struct.unpack(TASKSTATS_fmt, data[16:])))
    attrs['ac_comm'] = attrs['ac_comm'].rstrip('\0')
    print attrs

  def proc_gentlink(self):
    #get GELINK Header info    
    cmd='TASKSTATS\0'
    mlen=len(cmd) + 4

    msg_ts=array.array(str('B'))
    msg_ts.fromstring(struct.pack("BBxx", CTRL_CMD_GETFAMILY, 0))
    msg_ts.fromstring(struct.pack("HH", mlen, CTRL_ATTR_FAMILY_NAME))
    msg_ts.fromstring(cmd)
    tmp=((4 - (len(msg_ts) % 4)) & 0x3)
    msg_ts.fromstring('\0' * ((4 - (len(cmd) % 4)) & 0x3))

    nlmhdr_msg=array.array(str('B'),struct.pack(str('=IHHII'), len(msg_ts) + 16, NETLINK_GENERIC, NLM_F_REQUEST, 0, 0))
    nlmhdr_msg.extend(msg_ts)

    self.socket.send(nlmhdr_msg)

    data = self.socket.recv(65536)#(16384)
    data=self.unpack_nlhdr(data)
    data=self.unpack_genlhdr(data)

    while len(data) > 0:
          data=self.unpack_attr_hdr(data)
    #
    if self.flags & 0x2 == 0:
          if debug>0: print "End of receiving message!"
          return

  def unpack_genlhdr(self,data):
        cmd, version = struct.unpack(str('=BBxx'), data[:4])
        if debug > 0: print "genlhdr: cmd:",cmd,"version: ",version
        return data[4:]

  def unpack_nlhdr(self,data):
        try:
            (size, type, flags, seq, pid) = struct.unpack(str('=IHHII'), data[:16])
            self.flags=flags
            if type == NLMSG_ERROR:
               error = -int(struct.unpack(str('=i'), data[16:20])[0])
               #print "Error: ", errno.errorcode[error]," : ", os.strerror(error)
               raise RuntimeError(errno.errorcode[error]+" : "+os.strerror(error))
            return data[16:size]
        except Exception as e:
            raise

  def unpack_attr_hdr(self,data):
            len, typ = struct.unpack(str('=HH'), data[:4])
            len = len & 0x7fff
            #
            if GE_Attr_Fmt[typ] ==0:
               if debug>0: print "name processing: "+data[4:len-1]
               GE_Attr[typ]=data[4:len-1]
            elif GE_Attr_Fmt[typ] ==9:
               pass
               #print "Not supported yet!"
            elif typ >5:
               pass
               #print "OPS attr, ignore..."
            else:
               GE_Attr[typ]=struct.unpack(GE_Attr_Fmt[typ], data[4:len])[0]
               #
            #
            return data[((((len +3 ))) & ~0x3):]

  def __del__(self):
    pass


if __name__ == '__main__':
   import sys
   process = -1
   if len(sys.argv) > 1 and sys.argv[1] > 0:
      process = sys.argv[1]
      print "process: ",process
      exp = Proc_TaskStats(process)
      
      
