separationInMeters = 40;
currentBaseStationPosition = [10 0];
for i = 1:10
    position = currentBaseStationPosition;
    disp(position);
    currentBaseStationPosition(1) = ...
        currentBaseStationPosition(1) + separationInMeters;
end