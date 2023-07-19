import m5

# import all of the SimObjects
from m5.objects import *
from gem5.runtime import get_runtime_isa

# Add the common scripts to our path
m5.util.addToPath("../")

# import the caches which we made
from caches import *

# import the SimpleOpts module
from common import SimpleOpts

# Default to running 'hello', use the compiled ISA to find the binary
# grab the specific path to the binary
thispath = os.path.dirname(os.path.realpath(__file__))
default_binary = os.path.join(
    "/home/shishunchen/hdd0/gem5/",
    "tests/test-progs/hello/bin/x86/linux/hello",
)

# Binary to execute
SimpleOpts.add_option("binary", nargs="?", default=default_binary)

# Finalize the arguments and grab the args so we can pass it on to our objects
options = SimpleOpts.parse_args()

# create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MB")]  # Create an address range

# Create a simple CPU
system.cpu = X86TimingSimpleCPU()

system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

# Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)

system.membus = SystemXBar()

system.l2cache.connectMemSideBus(system.membus)


system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports


system.workload = SEWorkload.init_compatible(options.binary)

process = Process()
process.cmd = [options.binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print("Begining simulation!")
exit_event = m5.simulate()
print(
    "Exiting @ tick {} because {}".format(m5.curTick(), exit_event.getCause())
)
