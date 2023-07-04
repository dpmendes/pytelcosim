clear all
clc

tic

system = CoordinatedBeamformingCoMPSystem;
system.loadTestScenario3Uplink;

aggregateThroughput = system.calculateUplinkDPBAggregateThroughputOverNumberOfSlots(20);
str = sprintf('Aggregate throughput = %e bps', aggregateThroughput);
disp(str);

d = Monitor;
d.system = system;
d.showAllBaseStationsUserEquipmentTimesScheduled;

d.showBaseStationsReceivedBits;

system = CoordinatedBeamformingCoMPSystem;
system.loadTestScenario3Uplink;

aggregateThroughput = system.calculateUplinkRoundRobinAggregateThroughputOverNumberOfSlots(20);
str = sprintf('Aggregate throughput = %e bps', aggregateThroughput);
disp(str);

d.system = system;
d.showAllBaseStationsUserEquipmentTimesScheduled;

d.showBaseStationsReceivedBits;

toc