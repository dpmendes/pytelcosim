classdef CentralUnit < handle
    properties
        scheduler
        resourceBlocksPerSlot = 0
        clusterBaseStationsList = []
    end
    
    methods
        function clusterSchedule = ...
                requestScheduleToDynamicPointBlankingScheduler(thisObject)
            scheduler = thisObject.scheduler; %#ok<PROP>
            clusterSchedule = scheduler.scheduleNextSlot; %#ok<PROP>
        end
        
        function initializeCoordinatedScheduler(thisObject)
            newScheduler = CoordinatedScheduler;
            thisObject.scheduler = newScheduler;
        end
        
        function initializeDynamicPointBlankingScheduler(thisObject)
            newScheduler = DynamicPointBlankingScheduler...
                (thisObject.resourceBlocksPerSlot);
            newScheduler.setNumberOfResourceBlocksPerSlot...
                (thisObject.resourceBlocksPerSlot);
            newScheduler.receiveClusterBaseStationsList...
                (thisObject.clusterBaseStationsList);
            newScheduler.initializePivotCounters;
            thisObject.scheduler = newScheduler;            
        end
        
        function receiveBaseStationsList(thisObject, baseStationsList)
            thisObject.clusterBaseStationsList = baseStationsList;
        end
        
        function passAllLinksListToScheduler(thisObject, allLinksList)
            scheduler = thisObject.scheduler; %#ok<PROP>
            scheduler.receiveAllLinksList(allLinksList); %#ok<PROP>
        end
        
        function setResourceBlocksPerSlot(thisObject, resourceBlocksPerSlot)
            thisObject.resourceBlocksPerSlot = resourceBlocksPerSlot;
        end
    end
    
end

