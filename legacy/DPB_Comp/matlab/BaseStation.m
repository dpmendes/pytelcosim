classdef BaseStation < Transceiver

    properties
        numberOfResourceBlocksPerSlot
        scheduler
        associatedUserEquipmentList = []
        userEquipmentTimesScheduled = []
        linksFromBaseStationList = []
        linksToBaseStationList = []
    end

    methods
        function obj = BaseStation(x, y)
            obj = obj@Transceiver(x, y);
        end

        function addLinkFromBaseStationToList(thisObject, linkFromBaseStation)
            [~, indexOfBaseStationInList] = ismember...
                (linkFromBaseStation, thisObject.linksFromBaseStationList);
            if ~indexOfBaseStationInList
                thisObject.linksFromBaseStationList = ...
                    [thisObject.linksFromBaseStationList linkFromBaseStation];
            end
        end

        function addLinkToBaseStationToList(thisObject, linkToBaseStation)
            [~, indexOfBaseStationInList] = ismember...
                (linkToBaseStation, thisObject.linksToBaseStationList);
            if ~indexOfBaseStationInList
                thisObject.linksToBaseStationList = ...
                    [thisObject.linksToBaseStationList linkToBaseStation];
            end
        end

        function associatedUserEquipmentList = ...
                getAssociatedUserEquipmentList(thisObject)
            associatedUserEquipmentList = ...
                thisObject.associatedUserEquipmentList;
        end

        function removeLinkFromBaseStationFromList...
                (thisObject, linkFromBaseStation)
            [~, indexOfBaseStationInList] = ismember...
                (linkFromBaseStation, thisObject.linksFromBaseStationList);
            if indexOfBaseStationInList
                linksList = thisObject.linksFromBaseStationList;
                thisObject.linksFromBaseStationList...
                    (indexOfBaseStationInList) = [];
                thisObject.linksFromBaseStationList = linksList;
            end
        end

        function removeLinkToBaseStationFromList...
                (thisObject, linkToBaseStation)
            [~, indexOfBaseStationInList] = ismember...
                (linkToBaseStation, thisObject.linksToBaseStationList);
            if indexOfBaseStationInList
                linksList = thisObject.linksToBaseStationList;
                thisObject.linksToBaseStationList...
                    (indexOfBaseStationInList) = [];
                thisObject.linksToBaseStationList = linksList;
            end
        end

        function linksFromBaseStationList = ...
                getLinksFromBaseStationList(thisObject)
            linksFromBaseStationList = thisObject.linksFromBaseStationList;
        end

        function linksToBaseStationList = ...
                getLinksToBaseStationList(thisObject)
            linksToBaseStationList = thisObject.linksToBaseStationList;
        end
        function setNumberOfResourceBlocksPerSlot...
            (thisObject, numberOfResourceBlocksPerSlot)
        thisObject.numberOfResourceBlocksPerSlot = ...
            numberOfResourceBlocksPerSlot;
    end

    function initializeUserEquipmentTimesScheduledCounters(thisObject)
        numberOfAssociatedUserEquipment = ...
            length(thisObject.associatedUserEquipmentList);
        thisObject.userEquipmentTimesScheduled = ...
            zeros(1, numberOfAssociatedUserEquipment);
    end

    function numberOfResourceBlocksPerSlot = ...
            getNumberOfResourceBlocksPerSlot(thisObject)
        numberOfResourceBlocksPerSlot = ...
            thisObject.numberOfResourceBlocksPerSlot;
    end

    function associateUserEquipment(thisObject, userEquipment)
        indexOfUserEquipmentInList = ...
            thisObject.findUserEquipmentInList(userEquipment);
        if ~indexOfUserEquipmentInList
            thisObject.associatedUserEquipmentList = ...
                [thisObject.associatedUserEquipmentList userEquipment];
        end
    end

    function informAssociatedUserEquipmentListToScheduler(thisObject)
        baseStationScheduler = thisObject.scheduler;
        baseStationScheduler.updateUserEquipmentToBeScheduledList...
            (thisObject.associatedUserEquipmentList);
        baseStationScheduler.resetResourceBlocksServed();
    end

    function slotSchedule = requestNextScheduleToScheduler(thisObject)
        baseStationScheduler = thisObject.scheduler;
        numberOfResourceBlocks = thisObject.numberOfResourceBlocksPerSlot;
        baseStationScheduler.setNumberOfResourceBlocksPerSlot...
            (numberOfResourceBlocks);
        slotSchedule = baseStationScheduler.scheduleNextSlot();
        thisObject.updateUserEquipmentTimesServed();
    end

    function updateUserEquipmentTimesServed(thisObject)
        scheduler = thisObject.scheduler;
        thisObject.userEquipmentTimesScheduled = ...
            scheduler.getResourceBlocksServedPerUserEquipmentList;
    end

    function dissociateUserEquipment(thisObject, userEquipment)
        indexOfUserEquipmentInList = ...
            thisObject.findUserEquipmentInList(userEquipment);
        if indexOfUserEquipmentInList
            i = indexOfUserEquipmentInList;
            thisObject.associatedUserEquipmentList(i) = [];
        end
    end

    function initializeRoundRobinScheduler(thisObject)
        thisObject.scheduler = ...
                RoundRobinScheduler...
                (thisObject.numberOfResourceBlocksPerSlot);
    end

    function indexInList = findUserEquipmentInList...
            (thisObject, userEquipment)
        [~, indexInList] = ismember(userEquipment, ...
            thisObject.associatedUserEquipmentList);
    end

    function minimumUserEquipmentNumberOfTimesServed = ...
                findMinimumUserEquipmentNumberOfTimesServed(thisObject)
            minimumUserEquipmentNumberOfTimesServed = ...
                min(thisObject.userEquipmentTimesScheduled);
    end

    function numberOfAssociatedUserEquipment = ...
            countAssociatedUserEquipment(thisObject)
        numberOfAssociatedUserEquipment = ...
            length(thisObject.associatedUserEquipmentList);
    end
end