import m5
from m5.objects import Cache

# Add the common scripts to our path
m5.util.addToPath("../../")

from common import SimpleOpts


class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 10

    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass

    def connectCPU(self, cpu):
        raise NotImplementError

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports


class L1ICache(L1Cache):
    size = "16kB"

    SimpleOpts.add_option(
        "--l1i_size", help=f"L1 instruction cache size. Default: {size}"
    )

    def __init__(self, options=None):
        super(L1ICache, self).__init__(options)
        if not options or not options.l1i_size:
            return
        self.size = options.l1i_size

    def connectCPU(self, CPU):
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    size = "64kB"

    SimpleOpts.add_option(
        "--l1i_size", help=f"L1 instruction cache size. Default: {size}"
    )

    def __init__(self, options=None):
        super(L1DCache, self).__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size

    def connectCPU(self, CPU):
        self.cpu_side = cpu.dcache_port


class L2Cache(Cache):
    size = "256kB"
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    SimpleOpts.add_option("--l2_size", help=f"L2 cache size. Default: {size}")

    def __init__(self, options=None):
        super(L2Cache, self).__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size

    def connectCPUSideBus(slef, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
