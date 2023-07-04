classdef BaseStationToUserEquipmentLink < Link
    methods
        function newObject = BaseStationToUserEquipmentLink(channel)
            newObject = newObject@Link(channel);
        end
    end
end
