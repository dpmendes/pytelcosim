classdef Cluster < handle

    properties
        clusterBaseStationsList = []
        resourceBlocksPerSlot = 0
        centralUnit
    end
    
    methods
        function clusterSchedule = requestScheduleToCentralUnit(thisObject)
            centralUnit = thisObject.centralUnit; %#ok<PROP>
            clusterSchedule = ...
                centralUnit.requestScheduleToDynamicPointBlankingScheduler; %#ok<PROP>
        end
        
        function createCentralUnitCoordinatingAddedBaseStations...
            (thisObject)
            newCentralUnit = CentralUnit;
            newCentralUnit.setResourceBlocksPerSlot...
                (thisObject.resourceBlocksPerSlot);
            newCentralUnit.receiveBaseStationsList...
                (thisObject.clusterBaseStationsList);
            newCentralUnit.initializeDynamicPointBlankingScheduler;
            thisObject.centralUnit = newCentralUnit;
        end
        
        function setResourceBlocksPerSlot(thisObject, resourceBlocksPerSlot)
            thisObject.resourceBlocksPerSlot = resourceBlocksPerSlot;
        end
        
        function passAllLinksListToCentralUnit(thisObject, allLinksList)
            centralUnit = thisObject.centralUnit; %#ok<PROP>
            centralUnit.passAllLinksListToScheduler(allLinksList); %#ok<PROP>
        end
        
        function addBaseStationToCluster(thisObject, baseStation)
            indexOfBaseStation = thisObject.findBaseStationInList(baseStation);
            if ~indexOfBaseStation
                thisObject.clusterBaseStationsList = ...
                    [thisObject.clusterBaseStationsList baseStation];
            end
        end
        
        function removeBaseStationFromCluster(thisObject, baseStation)
            indexOfBaseStation = thisObject.findBaseStationInList(baseStation);
            if indexOfBaseStation
                thisObject.clusterBaseStationsList = ...
                    [thisObject.clusterBaseStationsList(1:indexOfBaseStation-1) ...
                    thisObject.clusterBaseStationsList(indexOfBaseStation+1:end)];
            end
        end
        
        function indexInList = findBaseStationInList(thisObject, baseStation)
            [~, indexInList] = ismember(baseStation, ...
                thisObject.clusterBaseStationsList);
        end
        
    end
    
end