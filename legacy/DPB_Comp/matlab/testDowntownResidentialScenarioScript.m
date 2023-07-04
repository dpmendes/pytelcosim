tic

clear all
clc

system = CoordinatedBeamformingCoMPSystem;
system.loadDowntownResidentialUplinkScenario;

aggregateThroughput = system.calculateUplinkDPBAggregateThroughputOverNumberOfSlots(500);
str = sprintf('Aggregate throughput = %e bps', aggregateThroughput);
disp(str);

d = Debugger;
d.setDebuggerSystem(system);
d.showAllBaseStationsUserEquipmentTimesScheduled;

d.showBaseStationsReceivedBits;
d.showUserEquipmentTransmittedBits;

system = CoordinatedBeamformingCoMPSystem;
system.loadDowntownResidentialUplinkScenario;

aggregateThroughput = system.calculateUplinkRoundRobinAggregateThroughputOverNumberOfSlots(500);
str = sprintf('Aggregate throughput = %e bps', aggregateThroughput);
disp(str);

d.setDebuggerSystem(system);
d.showAllBaseStationsUserEquipmentTimesScheduled;

d.showBaseStationsReceivedBits;
d.showUserEquipmentTransmittedBits;

toc