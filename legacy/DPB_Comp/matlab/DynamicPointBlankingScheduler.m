classdef DynamicPointBlankingScheduler < Scheduler
 
    properties
        clusterBaseStationsList = []
        timesABaseStationHasBeenThePivot = []
        currentPivotBaseStation
    end
    
    methods
        function newObject = DynamicPointBlankingScheduler...
                (numberOfResourceBlocksPerSlot)
            newObject = newObject@Scheduler(numberOfResourceBlocksPerSlot);
        end
        
        function receiveClusterBaseStationsList...
                (thisObject, clusterBaseStationsList)
            thisObject.clusterBaseStationsList = clusterBaseStationsList;
        end
        
        function initializePivotCounters(thisObject)
            numberOfBaseStationsInCluster = ...
                length(thisObject.clusterBaseStationsList);
            thisObject.timesABaseStationHasBeenThePivot = ...
                zeros(1, numberOfBaseStationsInCluster);
        end
        
        function clusterSchedule = scheduleNextSlot(thisObject)
            thisObject.selectPivotBaseStation;
            clusterSchedule = thisObject.pivotRoundRobinSchedule;
            clusterSchedule = ...
                [clusterSchedule thisObject.scheduleNonPivotBaseStationUsers];
        end
        
        function pivotBaseStation = selectPivotBaseStation(thisObject)
            minimumUserEquipmentNumberOfTimesServed = 1e20;
            pivotBaseStation = [];
            numberOfBaseStationsInCluster = ...
                length(thisObject.clusterBaseStationsList);
            for i = 1:numberOfBaseStationsInCluster
                baseStation = thisObject.clusterBaseStationsList(i);
                minimumUserEquipmentNumberOfTimesServedForBaseStation = ...
                    baseStation.findMinimumUserEquipmentNumberOfTimesServed;
                if minimumUserEquipmentNumberOfTimesServedForBaseStation <= ...
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
            pivotBaseStation.setNumberOfResourceBlocksPerSlot...
                (thisObject.numberOfResourceBlocksPerSlot);
            slotSchedule = pivotBaseStation.requestNextScheduleToScheduler;
        end
        
        function nonPivotSchedule = scheduleNonPivotBaseStationUsers(thisObject)
            nonPivotSchedule = [];
            for i = 1:length(thisObject.clusterBaseStationsList)
                baseStation = thisObject.clusterBaseStationsList(i);
                if baseStation == thisObject.currentPivotBaseStation
                    continue
                end
                resourceBlocksConsideringOneFree = ...
                    thisObject.numberOfResourceBlocksPerSlot - 1;
                baseStation.setNumberOfResourceBlocksPerSlot...
                    (resourceBlocksConsideringOneFree);
                baseStationSchedule = ...
                    baseStation.requestNextScheduleToScheduler;
                baseStationSchedule.shiftUsersInResourceBlocksToTheRight();
                resourceBlocks = resourceBlocksConsideringOneFree + 1;
                thisObject.numberOfResourceBlocksPerSlot = resourceBlocks;
                baseStation.setNumberOfResourceBlocksPerSlot(resourceBlocks);
                nonPivotSchedule = [nonPivotSchedule baseStationSchedule];
            end
        end
    end
end