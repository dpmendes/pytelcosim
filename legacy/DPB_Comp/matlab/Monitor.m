classdef Monitor < handle
    properties
        system = []
        ueList = []
        bsList = []
    end
    
    methods
        function showUserEquipmentReceivedBits(thisObject)
            for i = 1:length(thisObject.ueList)
                ue = thisObject.ueList(i);
                [x, y] = ue.getPosition;
                bits = ue.totalBitsReceived;

                fprintf('UE at (%i,%i) received %i bits.\n', x, y, bits);
            end
        end
        
        function showUserEquipmentTransmittedBits(thisObject)
            for i = 1:length(thisObject.ueList)
                ue = thisObject.ueList(i);
                [x, y] = ue.getPosition;
                bits = ue.totalBitsTransmitted;
                
                fprintf('UE at (%i,%i) transmitted %i bits.\n', x, y, bits);
            end
        end
        
        function showBaseStationsReceivedBits(thisObject)
            for i = 1:length(thisObject.bsList)
                bs = thisObject.bsList(i);
                [x, y] = bs.getPosition;
                bits = bs.totalBitsReceived;

                fprintf('BS at (%i,%i) received %i bits.\n', x, y, bits);
            end
        end
        
        function showAssociatedUserEquipment(thisObject)
            for i = 1:length(thisObject.bsList)
                bs = thisObject.bsList(i);
                [x, y] = bs.getPosition;
                associatedUeList = bs.associatedUserEquipmentList;
                fprintf('\nBS %i at (%i,%i).\n', i, x, y);

                for j = 1:length(associatedUeList)
                    ue = associatedUeList(j);
                    [x, y] = ue.getPosition;
                    fprintf('UE at (%i,%i) associated.\n', x, y);
                end
            end            
        end
        
        function showAllBaseStationsNextSchedule(thisObject)
            allBaseStationsSchedule = ...
                thisObject.system.scheduleResourceBlocksForBaseStations;

            for i = 1:length(thisObject.system.baseStationsList)
                for j = 1:thisObject.system.resourceBlocksPerSlot
                    ue = allBaseStationsSchedule(i,j);
                    [x, y] = ue.getPosition;
                    fprintf('UE at (%i,%i) scheduled in resource block %i.\n', x, y, j);
                end
            end
        end
        
        function showAllBaseStationsUserEquipmentTimesScheduled(thisObject)
            for i = 1:length(thisObject.bsList)
                bs = thisObject.bsList(i);
                fprintf('\nBS %i UE times served =', i);
                disp(bs.userEquipmentTimesScheduled);
            end                   
        end
        
        function setMonitorSystem(thisObject, system)
            thisObject.system = system;
            thisObject.initializeMonitorLists;
        end
        
        function initializeMonitorLists(thisObject)
            thisObject.ueList = thisObject.system.userEquipmentList;
            thisObject.bsList = thisObject.system.baseStationsList;
        end
    end
end

