classdef RoundRobinScheduler < Scheduler
    properties
    end
    
    methods
        function newObject = RoundRobinScheduler(numberOfResourceBlocksPerSlot)
            newObject = newObject@Scheduler(numberOfResourceBlocksPerSlot);
        end
        
        function slotSchedule = scheduleNextSlot(thisObject)
            userEquipmentList = thisObject.userEquipmentToBeScheduledList;
            timesServedList = ...
                thisObject.resourceBlocksServedPerUserEquipmentList;
            userEquipmentListSchedule = zeros(1, length(userEquipmentList));
            slotSchedule = Schedule(thisObject.numberOfResourceBlocksPerSlot);
            for i = 1:thisObject.numberOfResourceBlocksPerSlot
                [~, lessServedIndex] = min(timesServedList);
                timesServedList(lessServedIndex) = ...
                    timesServedList(lessServedIndex) + 1;
                userEquipmentListSchedule(lessServedIndex) = i;
                slotSchedule.addUserToResourceBlock...
                    (userEquipmentList(lessServedIndex));
            end
            thisObject.resourceBlocksServedPerUserEquipmentList = ...
                timesServedList;
        end
        
        function resetResourceBlocksServed(thisObject)
            numberOfUserEquipment = ...
                length(thisObject.userEquipmentToBeScheduledList);
            thisObject.resourceBlocksServedPerUserEquipmentList = ...
                zeros(1, numberOfUserEquipment);
        end
        
        function updateUserEquipmentToBeScheduledList...
                (thisObject, userEquipmentToBeScheduledList)
            thisObject.userEquipmentToBeScheduledList = ...
                userEquipmentToBeScheduledList;
        end
        
        function updateResourceBlocksServedPerUserEquipmentList...
                (thisObject, resourceBlocksServedPerUserEquipmentList)
            thisObject.resourceBlocksServedPerUserEquipmentList = ...
                resourceBlocksServedPerUserEquipmentList;
        end
        
        function resourceBlocksServedPerUserEquipmentList = ...
                getResourceBlocksServedPerUserEquipmentList(thisObject)
            resourceBlocksServedPerUserEquipmentList = ...
                thisObject.resourceBlocksServedPerUserEquipmentList;
        end
        
        function userEquipmentIndex = findUserEquipmentIndexInList...
                (thisObject, userEquipment)
            [~, userEquipmentIndex] = ismember...
                (userEquipment, thisObject.userEquipmentToBeScheduledList);
        end
        
        function removeUserEquipmentFromCurrentSchedule...
                (thisObject, userEquipment)
            
        end
       
    end
    
    methods(Static)

    end
end

