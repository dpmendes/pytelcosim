clear all
clc

system = CoordinatedBeamformingCoMPSystem;
system.loadTestScenario1;

disp('');
disp('START');
disp('Base Stations');

for i = 1:length(system.baseStationsList)
    baseStation = system.baseStationsList(i);
    [x y] = baseStation.getPosition();
    str = sprintf('Base Station %i, (%i, %i)\n', i, x, y);
    disp(str);

    disp('Associated User Equipment');
    associatedUserEquipmentList = baseStation.associatedUserEquipmentList;
    for j = 1:length(associatedUserEquipmentList)
        userEquipment = associatedUserEquipmentList(j);
        [x y] = userEquipment.getPosition();
        str = sprintf('User Equipment at (%i, %i)\n', x, y);
        disp(str);
    end
end

disp('');
disp('User Equipment');

for i = 1:length(system.userEquipmentList)
    userEquipment = system.userEquipmentList(i);
    [x y] = userEquipment.getPosition();
    str = sprintf('User Equipment %i, (%i, %i); ', i, x, y);
    disp(str);

    servingBaseStation = userEquipment.servingBaseStation;
    [x y] = servingBaseStation.getPosition;
    str = sprintf('Serving Base Station at (%i, %i)\n\n', x, y);
    disp(str);
end

aggregateCapacity = system.calculateAggregateCapacity;

disp(aggregateCapacity);

disp('');
disp('END');