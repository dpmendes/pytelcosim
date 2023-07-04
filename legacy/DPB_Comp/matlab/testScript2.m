clear all
clc
system = CoordinatedBeamformingCoMPSystem;
system.loadTestScenario3;

aggregateThroughput = system.calculateDownlinkDPBAggregateThroughputOverNumberOfSlots(20);
disp(aggregateThroughput);

d = Debugger;
d.system = system;
d.showAllBaseStationsUserEquipmentTimesScheduled;

d.showUserEquipmentReceivedBits;

system = CoordinatedBeamformingCoMPSystem;
system.loadTestScenario3;

aggregateThroughput = system.calculateDownlinkRoundRobinAggregateThroughputOverNumberOfSlots(20);
disp(aggregateThroughput);

d.system = system;
d.showAllBaseStationsUserEquipmentTimesScheduled;

d.showUserEquipmentReceivedBits;

%d.showAllBaseStationsNextSchedule;