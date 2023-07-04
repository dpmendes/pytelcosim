classdef Scheduler < handle
    properties
        numberOfResourceBlocksPerSlot
        userEquipmentToBeScheduledList = []
        resourceBlocksServedPerUserEquipmentList = []
    end
    
    methods (Abstract)
        slotSchedule = scheduleNextSlot(thisObject)
    end
    
    methods
        function newObject = Scheduler(numberOfResourceBlocksPerSlot)
            newObject.numberOfResourceBlocksPerSlot = ...
                numberOfResourceBlocksPerSlot;
        end
        
        function setNumberOfResourceBlocksPerSlot...
                (thisObject, numberOfResourceBlocksPerSlot)
            thisObject.numberOfResourceBlocksPerSlot = ...
                numberOfResourceBlocksPerSlot;
        end
    end
end