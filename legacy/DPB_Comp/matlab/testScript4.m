tic

clear all
clc

system = CoordinatedBeamformingCoMPSystem;
system.loadTestScenario4Uplink;

aggregateThroughput = system.calculateUplinkDPBAggregateThroughputOverNumberOfSlots(1000);
str = sprintf('Aggregate throughput = %e bps', aggregateThroughput);
disp(str);

d = Debugger;
d.system = system;
d.showAllBaseStationsUserEquipmentTimesScheduled;

d.showBaseStationsReceivedBits;

system = CoordinatedBeamformingCoMPSystem;
system.loadTestScenario4Uplink;

aggregateThroughput = system.calculateUplinkRoundRobinAggregateThroughputOverNumberOfSlots(1000);
str = sprintf('Aggregate throughput = %e bps', aggregateThroughput);
disp(str);

d.system = system;
d.showAllBaseStationsUserEquipmentTimesScheduled;

d.showBaseStationsReceivedBits;

toc