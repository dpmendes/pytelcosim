classdef CoordinatedScheduler < Scheduler
    
    properties
        clusterBaseStationsList = []
        allLinksList = []
        timesABaseStationHasBeenThePivot = []
        currentPivotBaseStation
    end
    
    methods
        function receiveClusterBaseStationsList...
                (thisObject, clusterBaseStationsList)
            thisObject.clusterBaseStationsList = clusterBaseStationsList;
        end
        
        function receiveAllLinksList(thisObject, allLinksList)
            thisObject.allLinksList = allLinksList;
        end
        
        function initializePivotCounters(thisObject)
            numberOfBaseStationsInCluster = ...
                length(thisObject.clusterBaseStationsList);
            thisObject.timesABaseStationHasBeenThePivot = ...
                zeros(1, numberOfBaseStationsInCluster);
        end
        
        function slotSchedule = scheduleNextSlot(thisObject)
            pivotBaseStation = thisObject.selectPivotBaseStation;
            thisObject.currentPivotBaseStation = pivotBaseStation;
            slotSchedule = thisObject.pivotRoundRobinSchedule;
            slotSchedule = [slotSchedule; ...
                thisObject.scheduleUsersFromNonPivotBaseStations];
        end
        
        function pivotBaseStation = selectPivotBaseStation(thisObject)
            minimumUserEquipmentNumberOfTimesServed = 0;
            numberOfBaseStationsInCluster = ...
                length(thisObject.clusterBaseStationsList);
            for i = 1:numberOfBaseStationsInCluster
                baseStation = thisObject.clusterBaseStationsList(i);
                minimumUserEquipmentNumberOfTimesServedForBaseStation = ...
                    baseStation.findMinimumUserEquipmentNumberOfTimesServed;
                if minimumUserEquipmentNumberOfTimesServedForBaseStation < ...
                        minimumUserEquipmentNumberOfTimesServed
                    minimumUserEquipmentNumberOfTimesServed = ...
                        minimumUserEquipmentNumberOfTimesServedForBaseStation;
                    pivotBaseStation = baseStation;
                end
            end
            thisObject.currentPivotBaseStation = pivotBaseStation;
            thisObject.updateTimesABaseStationHasBeenThePivot(pivotBaseStation);
        end
        
        function updateTimesABaseStationHasBeenThePivot...
                (thisObject, pivotBaseStation)
            [~, pivotBaseStationIndex] = ismember...
                (pivotBaseStation, thisObject.clusterBaseStationsList);
            thisObject.timesABaseStationHasBeenThePivot(pivotBaseStationIndex) = ...
                thisObject.timesABaseStationHasBeenThePivot(pivotBaseStationIndex)...
                +1;
        end
        
        function slotSchedule = pivotRoundRobinSchedule(thisObject)
            pivotBaseStation = thisObject.currentPivotBaseStation;
            slotSchedule = pivotBaseStation.requestNextScheduleToScheduler();
        end
        
        function slotSchedule = ...
                scheduleUsersFromNonPivotBaseStations(thisObject)
            slotSchedule = [];
            for i = 1:length(thisObject.clusterBaseStationsList)
                baseStation = thisObject.clusterBaseStationsList(i);
                if baseStation ~= thisObject.currentPivotBaseStation
                    newSlotSchedule = thisObject.findLessInterferingUserEquipmentPermutationWithRepetition...
                        (baseStation);
                    slotSchedule = [slotSchedule newSlotSchedule]; 
                end
            end
        end
        
        function slotScheduleForBaseStation = ...
                findLessInterferingUserEquipmentPermutationWithRepetition...
                (thisObject, baseStation)
            userEquipmentList = baseStation.getAssociatedUserEquipmentList;
            numberOfUserEquipment = length(userEquipmentList);
            numberOfResourceBlocks = thisObject.numberOfResourceBlocksPerSlot;
            numberOfPermutationsWithRepetition = numberOfUserEquipment.^...
                numberOfResourceBlocks;
        end   
    end  
end

