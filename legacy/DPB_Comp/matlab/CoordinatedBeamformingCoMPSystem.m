classdef CoordinatedBeamformingCoMPSystem < handle

    properties
        transceiversList = []
        baseStationsList = []
        userEquipmentList = []
        baseStationToUserEquipmentLinksList = []
        userEquipmentToBaseStationLinksList = []
        clustersList = []
        channel
        slotDurationInSeconds = 0.5e-3
        resourceBlocksPerSlot = 3
        resultsFileHandle
    end

    methods
        function aggregateThroughput = ...
                calculateDownlinkDPBAggregateThroughputOverNumberOfSlots...
                (thisObject, numberOfSlots)
            currentSlot = 1;
            totalBitsTransmitted = 0;
            resultsFile = thisObject.openResultsFile('dynamic_point_blanking.dat');
            thisObject.logUserEquipment;
            thisObject.logAssociatedUserEquipment;
            thisObject.logAllDownlinkLinks;

            while currentSlot <= numberOfSlots
                bitsTransmittedThisSlot = ...
                    thisObject.calculateDownlinkDPBSlotTransmittedBits;
                totalBitsTransmitted = ...
                    totalBitsTransmitted + bitsTransmittedThisSlot;
                thisObject.logSlotsBitsTransmitted...
                    (currentSlot, bitsTransmittedThisSlot);
                currentSlot = currentSlot + 1;
                if ~mod(currentSlot, 10)
                    fprintf('Current Slot = %i\n', currentSlot);
                end
            end

            slotDuration = thisObject.slotDurationInSeconds;
            aggregateThroughput = ...
                totalBitsTransmitted./(numberOfSlots.*slotDuration);
            %logAggregateThroughput(aggregateThroughput);
            thisObject.closeResultsFile(resultsFile);
        end

        function aggregateThroughput = ...
                calculateUplinkDPBAggregateThroughputOverNumberOfSlots...
                (thisObject, numberOfSlots)
            currentSlot = 1;
            totalBitsTransmitted = 0;
            resultsFile = thisObject.openResultsFile...
                ('dynamic_point_blanking_uplink.dat');
            thisObject.logUserEquipment;
            thisObject.logAssociatedUserEquipment;
            thisObject.logAllDownlinkLinks;

            while currentSlot <= numberOfSlots
                bitsTransmittedThisSlot = ...
                    thisObject.calculateUplinkDPBSlotTransmittedBits;
                totalBitsTransmitted = ...
                    totalBitsTransmitted + bitsTransmittedThisSlot;
                thisObject.logSlotsBitsTransmitted...
                    (currentSlot, bitsTransmittedThisSlot);
                currentSlot = currentSlot + 1;
                if ~mod(currentSlot, 10)
                    fprintf('Current Slot = %i\n', currentSlot);
                end
            end

            slotDuration = thisObject.slotDurationInSeconds;
            aggregateThroughput = ...
                totalBitsTransmitted./(numberOfSlots.*slotDuration);
            %logAggregateThroughput(aggregateThroughput);
            thisObject.closeResultsFile(resultsFile);
        end

        function resultsFile = openResultsFile(thisObject, filename)
            resultsFile = fopen(filename, 'w');
            thisObject.resultsFileHandle = resultsFile;
        end

        function logUserEquipment(thisObject)
            logString = sprintf('\nUSER EQUIPMENT LIST\n');
            fwrite(thisObject.resultsFileHandle, logString);
            for i = 1:length(thisObject.userEquipmentList)
                userEquipment = thisObject.userEquipmentList(i);
                [x, y] = userEquipment.getPosition;
                logString = sprintf('UE at (%i,%i)\n', x, y);
                fwrite(thisObject.resultsFileHandle, logString);
            end
        end

        function logAssociatedUserEquipment(thisObject)
            logString = sprintf('\nBASE STATION AND ASSOCIATED USER EQUIPMENT LIST\n');
            fwrite(thisObject.resultsFileHandle, logString);
            for i = 1:length(thisObject.baseStationsList)
                baseStation = thisObject.baseStationsList(i);
                [x, y] = baseStation.getPosition;
                logString = sprintf('BS at (%i,%i)\n', x, y);
                fwrite(thisObject.resultsFileHandle, logString);
                for j = 1:length(baseStation.associatedUserEquipmentList)
                    userEquipment = baseStation.associatedUserEquipmentList(j);
                    [x, y] = userEquipment.getPosition;
                    logString = sprintf('UE at (%i,%i)\n', x, y);
                    fwrite(thisObject.resultsFileHandle, logString);
                end
                logString = sprintf('\n');
                fwrite(thisObject.resultsFileHandle, logString);
            end
        end

        function logAllDownlinkLinks(thisObject)
            logString = sprintf('\nLINKS\n');
            fwrite(thisObject.resultsFileHandle, logString);
            for i = 1:length(thisObject.baseStationToUserEquipmentLinksList)
                link = thisObject.baseStationToUserEquipmentLinksList(i);
                userEquipment = link.userEquipment;
                baseStation = link.baseStation;
                [xu, yu] = userEquipment.getPosition;
                [xb, yb] = baseStation.getPosition;
                gain = link.gain;
                logString = sprintf...
                    ('From BS (%i,%i) to UE (%i,%i)\nLink gain = %e\n',...
                    xb, yb, xu, yu, gain);
                fwrite(thisObject.resultsFileHandle, logString);
            end
        end

        function logAllUplinkLinks(thisObject)
            logString = sprintf('\nLINKS\n');
            fwrite(thisObject.resultsFileHandle, logString);
            for i = 1:length(thisObject.userEquipmentToBaseStationLinksList)
                link = thisObject.userEquipmentToBaseStationLinksList(i);
                userEquipment = link.userEquipment;
                baseStation = link.baseStation;
                [xu, yu] = userEquipment.getPosition;
                [xb, yb] = baseStation.getPosition;
                gain = link.gain;
                logString = sprintf...
                    ('From UE (%i,%i) to BS (%i,%i)\nLink gain = %e\n',...
                    xu, yu, xb, yb, gain);
                fwrite(thisObject.resultsFileHandle, logString);
            end
        end

        function logSlotsBitsTransmitted...
                (thisObject, currentSlot, bitsTransmittedThisSlot)
            logString = sprintf('\nEND OF SLOT %i\n', currentSlot);
            fwrite(thisObject.resultsFileHandle, logString);
            logString = sprintf('Bits transmitted this slot = %e\n', bitsTransmittedThisSlot);
            fwrite(thisObject.resultsFileHandle, logString);
        end

        function closeResultsFile(thisObject, resultsFile)
            fclose(resultsFile);
            thisObject.resultsFileHandle = [];
        end

        function aggregateThroughput = ...
                calculateCBAggregateThroughputOverNumberOfSlots...
                (thisObject, numberOfSlots)
            currentSlot = 1;
            totalBitsTransmitted = 0;
            while currentSlot <= numberOfSlots
                bitsTransmittedThisSlot = ...
                    thisObject.calculateCoordinatedBeamformingSlotTransmittedBits;
                totalBitsTransmitted = ...
                    totalBitsTransmitted + bitsTransmittedThisSlot;
                currentSlot = currentSlot + 1;
            end

            slotDuration = thisObject.slotDurationInSeconds;
            aggregateThroughput = ...
                totalBitsTransmitted./(numberOfSlots.*slotDuration);
        end

        function aggregateThroughput = ...
                calculateDownlinkRoundRobinAggregateThroughputOverNumberOfSlots...
                (thisObject, numberOfSlots)
            currentSlot = 1;
            totalBitsTransmitted = 0;
            resultsFile = thisObject.openResultsFile('round_robin_scheduling.dat');
            thisObject.logUserEquipment;
            thisObject.logAssociatedUserEquipment;
            thisObject.logAllDownlinkLinks;
            while currentSlot <= numberOfSlots
                bitsTransmittedThisSlot = ...
                    thisObject.calculateDownlinkRoundRobinSchedulingSlotTransmittedBits;
                totalBitsTransmitted = ...
                    totalBitsTransmitted + bitsTransmittedThisSlot;
                thisObject.logSlotsBitsTransmitted...
                    (currentSlot, bitsTransmittedThisSlot);
                currentSlot = currentSlot + 1;
                if ~mod(currentSlot, 10)
                    fprintf('Current Slot = %i\n', currentSlot);
                end
            end

            slotDuration = thisObject.slotDurationInSeconds;
            thisObject.closeResultsFile(resultsFile);
            aggregateThroughput = ...
                totalBitsTransmitted./(numberOfSlots.*slotDuration);
        end

        function aggregateThroughput = ...
                calculateUplinkRoundRobinAggregateThroughputOverNumberOfSlots...
                (thisObject, numberOfSlots)
            currentSlot = 1;
            totalBitsTransmitted = 0;
            resultsFile = thisObject.openResultsFile('round_robin_uplink.dat');
            thisObject.logUserEquipment;
            thisObject.logAssociatedUserEquipment;
            thisObject.logAllUplinkLinks;
            while currentSlot <= numberOfSlots
                bitsTransmittedThisSlot = ...
                    thisObject.calculateUplinkRoundRobinSchedulingSlotTransmittedBits;
                totalBitsTransmitted = ...
                    totalBitsTransmitted + bitsTransmittedThisSlot;
                thisObject.logSlotsBitsTransmitted...
                    (currentSlot, bitsTransmittedThisSlot);
                currentSlot = currentSlot + 1;
                if ~mod(currentSlot, 10)
                    fprintf('Current Slot = %i\n', currentSlot);
                end
            end

            slotDuration = thisObject.slotDurationInSeconds;
            thisObject.closeResultsFile(resultsFile);
            aggregateThroughput = ...
                totalBitsTransmitted./(numberOfSlots.*slotDuration);
        end

        function bitsTransmittedThisSlot = ...
                calculateCoordinatedBeamformingSlotTransmittedBits(thisObject)
            bitsTransmittedThisSlot = 0;
            allBaseStationsSchedule = ...
                thisObject.scheduleResourceBlocksForBaseStations;

            for resourceBlock = 1:thisObject.resourceBlocksPerSlot
                scheduledUsers = ...
                    thisObject.getScheduledUsersFromAllSchedules...
                    (allBaseStationsSchedule, resourceBlock);
                thisObject.activateAllDownlinkLinks;
                scheduledUsersLinks = ...
                    thisObject.findScheduledUsersLinks(scheduledUsers);
                thisObject.deactivateAllDownlinkLinks;
                thisObject.activateScheduledUsersLinks(scheduledUsersLinks);
                thisObject.updateAllUserEquipmentRxSignalToInterferencePlusNoiseRatio;
                thisObject.updateAllUserEquipmentReceptionCapacity;
                bitsTransmittedInResourceBlock = ...
                    thisObject.calculateBitsTransmittedInDownlinkResourceBlock...
                    (scheduledUsers);
                bitsTransmittedThisSlot = ...
                    bitsTransmittedThisSlot + bitsTransmittedInResourceBlock;
            end
        end

        function bitsTransmittedThisSlot = ...
                calculateDownlinkRoundRobinSchedulingSlotTransmittedBits...
                (thisObject)
            bitsTransmittedThisSlot = 0;
            allBaseStationsSchedule = ...
                thisObject.scheduleResourceBlocksForBaseStations;

            for resourceBlock = 1:thisObject.resourceBlocksPerSlot
                scheduledUsers = ...
                    thisObject.getScheduledUsersFromAllSchedules...
                    (allBaseStationsSchedule, resourceBlock);
                thisObject.updateAllUserEquipmentRxSignalToInterferencePlusNoiseRatio;
                thisObject.updateAllUserEquipmentReceptionCapacity;
                bitsTransmittedInResourceBlock = ...
                    thisObject.calculateBitsTransmittedInDownlinkResourceBlock...
                    (scheduledUsers);
                bitsTransmittedThisSlot = ...
                    bitsTransmittedThisSlot + bitsTransmittedInResourceBlock;
            end
        end

        function bitsTransmittedThisSlot = ...
                calculateUplinkRoundRobinSchedulingSlotTransmittedBits...
                (thisObject)
            bitsTransmittedThisSlot = 0;
            allBaseStationsSchedule = ...
                thisObject.scheduleResourceBlocksForBaseStations;

            for resourceBlock = 1:thisObject.resourceBlocksPerSlot
                scheduledUsers = ...
                    thisObject.getScheduledUsersFromAllSchedules...
                    (allBaseStationsSchedule, resourceBlock);
                thisObject.activateLinksWithScheduledUsers(scheduledUsers);
                thisObject.updateAllBaseStationsRxSignalToInterferencePlusNoiseRatio;
                thisObject.updateAllBaseStationsReceptionCapacity;
                bitsTransmittedInResourceBlock = ...
                    thisObject.calculateBitsTransmittedInUplinkResourceBlock...
                    (scheduledUsers);
                bitsTransmittedThisSlot = ...
                    bitsTransmittedThisSlot + bitsTransmittedInResourceBlock;
            end
        end

        function activateLinksWithScheduledUsers(thisObject, scheduledUsers)
            thisObject.deactivateAllUplinkLinks;
            thisObject.activateScheduledUserEquipmentUplinkLinks...
                (scheduledUsers);
        end

        function bitsTransmittedThisSlot = ...
                calculateDownlinkDPBSlotTransmittedBits(thisObject)
            bitsTransmittedThisSlot = 0;
            clustersSchedule = thisObject.requestScheduleToClusters;

            for resourceBlock = 1:thisObject.resourceBlocksPerSlot
                scheduledUsers = thisObject.getScheduledUsersFromAllSchedules...
                    (clustersSchedule, resourceBlock);
                thisObject.logScheduledUsersInResourceBlock...
                    (scheduledUsers, resourceBlock);
                activeBaseStations = thisObject.determineActiveBaseStations...
                    (scheduledUsers);
                thisObject.deactivateAllDownlinkLinks;
                thisObject.activateActiveBaseStationsDownlinkLinks(activeBaseStations);
                thisObject.updateAllUserEquipmentRxSignalToInterferencePlusNoiseRatio;
                thisObject.updateAllUserEquipmentReceptionCapacity;
                bitsTransmittedInResourceBlock = ...
                    thisObject.calculateBitsTransmittedInDownlinkResourceBlock...
                    (scheduledUsers);
                bitsTransmittedThisSlot = ...
                    bitsTransmittedThisSlot + bitsTransmittedInResourceBlock;
            end
        end

        function bitsTransmittedThisSlot = ...
                calculateUplinkDPBSlotTransmittedBits(thisObject)
            bitsTransmittedThisSlot = 0;
            clustersSchedule = thisObject.requestScheduleToClusters;

            for resourceBlock = 1:thisObject.resourceBlocksPerSlot
                scheduledUsers = thisObject.getScheduledUsersFromAllSchedules...
                    (clustersSchedule, resourceBlock);
                thisObject.logScheduledUsersInResourceBlock...
                    (scheduledUsers, resourceBlock);
                thisObject.activateLinksWithScheduledUsers(scheduledUsers);
                thisObject.updateAllBaseStationsRxSignalToInterferencePlusNoiseRatio;
                thisObject.updateAllBaseStationsReceptionCapacity;
                bitsTransmittedInResourceBlock = ...
                    thisObject.calculateBitsTransmittedInUplinkResourceBlock...
                    (scheduledUsers);
                bitsTransmittedThisSlot = ...
                    bitsTransmittedThisSlot + bitsTransmittedInResourceBlock;
            end
        end

        function logScheduledUsersInResourceBlock...
                (thisObject, scheduledUsers, resourceBlock)
            logString = sprintf('\nRESOURCE BLOCK %i\n', resourceBlock);
            fwrite(thisObject.resultsFileHandle, logString);
            for i = 1:length(scheduledUsers)
                userEquipment = scheduledUsers(i);
                [xu, yu] = userEquipment.getPosition;
                logString = sprintf('UE (%i,%i)\n', xu, yu);
                fwrite(thisObject.resultsFileHandle, logString);
            end
        end

        function activeBaseStations = ...
                determineActiveBaseStations(thisObject, scheduledUsers)
            numberOfBaseStations = length(thisObject.baseStationsList);
            activeBaseStations = [];
            for i = 1:numberOfBaseStations
                baseStation = thisObject.baseStationsList(i);
                associatedUserEquipment = ...
                    baseStation.getAssociatedUserEquipmentList;
                isBaseStationActive = ...
                    sum(ismember(scheduledUsers, associatedUserEquipment));
                if isBaseStationActive
                    activeBaseStations = [activeBaseStations baseStation]; %#ok<AGROW>
                end
            end
        end

        function activateActiveBaseStationsDownlinkLinks...
                (thisObject, activeBaseStations)
            for i = 1:length(thisObject.baseStationToUserEquipmentLinksList)
                link = thisObject.baseStationToUserEquipmentLinksList(i);
                linkBaseStation = link.baseStation;
                if ismember(linkBaseStation, activeBaseStations)
                    link.activateLink;
                end
            end
        end

        function activateScheduledUserEquipmentUplinkLinks...
                (thisObject, scheduledUsers)
            for i = 1:length(thisObject.userEquipmentToBaseStationLinksList)
                link = thisObject.userEquipmentToBaseStationLinksList(i);
                linkUserEquipment = link.userEquipment;
                if ismember(linkUserEquipment, scheduledUsers)
                    link.activateLink;
                end
            end
        end

        function clustersSchedule = requestScheduleToClusters(thisObject)
            clustersSchedule = [];
            for i = 1:length(thisObject.clustersList)
                cluster = thisObject.clustersList(i);
                clustersSchedule = [clustersSchedule ...
                    cluster.requestScheduleToCentralUnit]; %#ok<AGROW>
            end
        end

        function bitsTransmittedInResourceBlock = ...
                calculateBitsTransmittedInDownlinkResourceBlock...
                (thisObject, scheduledUsers)
            bitsTransmittedInResourceBlock = 0;
            for i = 1:length(scheduledUsers)
                userEquipment = scheduledUsers(i);
                userEquipment.receiveResourceBlock;
                bitsTransmittedPerUserEquipment = ...
                    userEquipment.currentCapacityInBitsPerSecond.*...
                    thisObject.slotDurationInSeconds;

                thisObject.logUserEquipmentCapacity(userEquipment);

                bitsTransmittedInResourceBlock = ...
                    bitsTransmittedInResourceBlock + ...
                    bitsTransmittedPerUserEquipment;
            end
        end

        function bitsTransmittedInResourceBlock = ...
                calculateBitsTransmittedInUplinkResourceBlock...
                (thisObject, scheduledUsers)
            bitsTransmittedInResourceBlock = 0;
            for i = 1:length(scheduledUsers)
                userEquipment = scheduledUsers(i);
                if userEquipment.isDummy
                    continue;
                end
                receivingBaseStation = userEquipment.getServingBaseStation;
                receivingBaseStation.receiveResourceBlock;
                capacity = ...
                    receivingBaseStation.getCurrentCapacityInBitsPerSecond;
                userEquipment.transmitResourceBlock(capacity);
                bitsTransmittedPerBaseStation = ...
                    receivingBaseStation.currentCapacityInBitsPerSecond.*...
                    thisObject.slotDurationInSeconds;

                thisObject.logBaseStationCapacity(receivingBaseStation);

                bitsTransmittedInResourceBlock = ...
                    bitsTransmittedInResourceBlock + ...
                    bitsTransmittedPerBaseStation;
            end
        end

        function logUserEquipmentCapacity(thisObject, userEquipment)
            [x, y] = userEquipment.getPosition;
            capacity = userEquipment.currentCapacityInBitsPerSecond;
            logString = sprintf('\nUE (%i,%i) capacity = %e', x, y, capacity);
            fwrite(thisObject.resultsFileHandle, logString);
        end

        function logBaseStationCapacity(thisObject, baseStation)
            [x, y] = baseStation.getPosition;
            capacity = baseStation.currentCapacityInBitsPerSecond;
            logString = sprintf('\nBS (%i,%i) capacity = %e', x, y, capacity);
            fwrite(thisObject.resultsFileHandle, logString);
        end

        function deactivateAllDownlinkLinks(thisObject)
            linksList = thisObject.baseStationToUserEquipmentLinksList;
            thisObject.deactivateLinksList(linksList);
        end

        function deactivateAllUplinkLinks(thisObject)
            linksList = thisObject.userEquipmentToBaseStationLinksList;
            thisObject.deactivateLinksList(linksList);
        end

        function activateAllDownlinkLinks(thisObject)
            linksList = thisObject.baseStationToUserEquipmentLinksList;
            thisObject.activateLinksList(linksList);
        end

        function activateAllUplinkLinks(thisObject)
            linksList = thisObject.userEquipmentToBaseStationLinksList;
            thisObject.activateLinksList(linksList);
        end

        function allBaseStationsSchedule = ...
                scheduleResourceBlocksForBaseStations(thisObject)
            allBaseStationsSchedule = [];
            for i = 1:length(thisObject.baseStationsList)
                baseStation = thisObject.baseStationsList(i);
                slotSchedule = baseStation.requestNextScheduleToScheduler;
                allBaseStationsSchedule = ...
                    [allBaseStationsSchedule; slotSchedule]; %#ok<AGROW>
            end
        end

        function linksToUserEquipment = ...
                findScheduledUsersLinks(thisObject, scheduledUsers)
            linksToUserEquipment = [];
            for i = 1:length(scheduledUsers)
                userEquipment = scheduledUsers(i);
                newLinksToUserEquipment = findLinksToUserEquipment...
                    (thisObject, userEquipment);
                linksToUserEquipment = ...
                    [linksToUserEquipment newLinksToUserEquipment]; %#ok<AGROW>
            end
        end

        function aggregateCapacity = calculateAggregateCapacity(thisObject)
            thisObject.updateAllUserEquipmentReceptionCapacity;
            aggregateCapacity = 0;
            for i = 1:length(thisObject.userEquipmentList)
                userEquipment = thisObject.userEquipmentList(i);
                aggregateCapacity = aggregateCapacity + ...
                    userEquipment.currentCapacityInBitsPerSecond;
            end
        end

        function updateAllUserEquipmentReceptionCapacity(thisObject)
            for i = 1:length(thisObject.userEquipmentList)
                userEquipment = thisObject.userEquipmentList(i);
                userEquipment.calculateReceptionCapacity;
            end
        end

        function updateAllBaseStationsReceptionCapacity(thisObject)
            for i = 1:length(thisObject.baseStationsList)
                baseStation = thisObject.baseStationsList(i);
                baseStation.calculateReceptionCapacity;
            end
        end

        function updateAllUserEquipmentRxSignalToInterferencePlusNoiseRatio...
                (thisObject)
            for i = 1:length(thisObject.userEquipmentList)
                userEquipment = thisObject.userEquipmentList(i);
                linksToUserEquipment = ...
                    thisObject.findLinksToUserEquipment(userEquipment);
                intendedSignal = ...
                    thisObject.calculateIntendedSignalToUserEquipment...
                    (userEquipment, linksToUserEquipment);
                interferingSignal = thisObject.calculateInterferingSignalAtUserEquipment...
                    (userEquipment, linksToUserEquipment);
                userEquipment.updateSignalToInterferencePlusNoiseRatio...
                    (intendedSignal, interferingSignal);
            end
        end

        function updateAllBaseStationsRxSignalToInterferencePlusNoiseRatio...
                (thisObject)
            for i = 1:length(thisObject.baseStationsList)
                baseStation = thisObject.baseStationsList(i);
                linksToBaseStation = ...
                    thisObject.findLinksToBaseStation(baseStation);
                intendedSignal = ...
                    thisObject.calculateIntendedSignalToBaseStation...
                    (baseStation, linksToBaseStation);
                interferingSignal = thisObject.calculateInterferingSignalAtBaseStation...
                    (baseStation, linksToBaseStation);
                baseStation.updateSignalToInterferencePlusNoiseRatio...
                    (intendedSignal, interferingSignal);
            end
        end

        function addBaseStation(thisObject, baseStation)
            indexOfBaseStationInList = ...
                thisObject.findBaseStation(baseStation);

            if ~indexOfBaseStationInList
                thisObject.baseStationsList = [thisObject.baseStationsList ...
                    baseStation];
            end
        end

        function removeBaseStation(thisObject, baseStation)
            indexOfBaseStationInList = ...
                thisObject.findBaseStation(baseStation);

            if indexOfBaseStationInList
                i = indexOfBaseStationInList;
                thisObject.baseStationsList(i) = [];
            end
        end

        function indexInList = findBaseStation(thisObject, baseStation)

            %[~, indexInList] = ismember(baseStation, thisObject.baseStationsList);

            indexInList = find(strcmp(baseStation,thisObject.baseStationsList))


        end

        function addUserEquipment(thisObject, userEquipment)
            indexOfUserEquipmentInList = ...
                thisObject.findUserEquipment(userEquipment);

            if ~indexOfUserEquipmentInList
                thisObject.userEquipmentList = ...
                    [thisObject.userEquipmentList userEquipment];
            end
        end

        function removeUserEquipment(thisObject, userEquipment)
            indexOfUserEquipmentInList = ...
                thisObject.findUserEquipment(userEquipment);

            if indexOfUserEquipmentInList
                i = indexOfUserEquipmentInList;
                thisObject.userEquipmentList(i) = [];
            end
        end

        function indexInList = findUserEquipment(thisObject, userEquipment)
            %[~, indexInList] = ismember(userEquipment, thisObject.userEquipmentList);
            indexInList = find(strcmp(userEquipment, thisObject.userEquipmentList))


        end

        function updateDownlinkLinksList(thisObject)
            thisObject.baseStationToUserEquipmentLinksList = [];
            numberOfBaseStations = length(thisObject.baseStationsList);
            numberOfUserEquipment = length(thisObject.userEquipmentList);

            for i = 1:numberOfBaseStations
                for j = 1:numberOfUserEquipment
                    linkChannel = thisObject.channel;
                    link = BaseStationToUserEquipmentLink(linkChannel);
                    link.baseStation = thisObject.baseStationsList(i);
                    link.userEquipment = thisObject.userEquipmentList(j);
                    link.calculateLinkGain;
                    thisObject.baseStationToUserEquipmentLinksList = ...
                        [thisObject.baseStationToUserEquipmentLinksList link];
                end
            end
        end

        function updateUplinkLinksList(thisObject)
            thisObject.userEquipmentToBaseStationLinksList = [];
            numberOfBaseStations = length(thisObject.baseStationsList);
            numberOfUserEquipment = length(thisObject.userEquipmentList);

            for i = 1:numberOfBaseStations
                for j = 1:numberOfUserEquipment
                    linkChannel = thisObject.channel;
                    link = UserEquipmentToBaseStationLink(linkChannel);
                    link.baseStation = thisObject.baseStationsList(i);
                    link.userEquipment = thisObject.userEquipmentList(j);
                    link.calculateLinkGain;
                    thisObject.userEquipmentToBaseStationLinksList = ...
                        [thisObject.userEquipmentToBaseStationLinksList link];
                end
            end
        end

        function associateAllUserEquipment(thisObject)
            for i = 1:length(thisObject.userEquipmentList)
                userEquipment = thisObject.userEquipmentList(i);
                linksToUserEquipment = ...
                    thisObject.findLinksToUserEquipment(userEquipment);
                greatestGainLink = thisObject.findGreatestGainLink...
                    (linksToUserEquipment);
                userEquipment.associateToBaseStation...
                    (greatestGainLink.baseStation);
                baseStation = greatestGainLink.baseStation;
                baseStation.associateUserEquipment(userEquipment);
            end
        end

        function initializeBaseStationAssociatedUserEquipmentScheduledCounters...
                (thisObject)
            for i = 1:length(thisObject.baseStationsList)
                baseStation = thisObject.baseStationsList(i);
                baseStation.initializeUserEquipmentTimesScheduledCounters;
            end
        end

        function linksToUserEquipment = findLinksToUserEquipment...
                (thisObject, userEquipment)
            linksToUserEquipment = [];
            for i = 1:length(thisObject.baseStationToUserEquipmentLinksList)
                link = thisObject.baseStationToUserEquipmentLinksList(i);
                if link.activeInTheCurrentSlot
                    if link.userEquipment == userEquipment
                        linksToUserEquipment = [linksToUserEquipment link]; %#ok<AGROW>
                    end
                end
            end
        end

        function linksToBaseStation = findLinksToBaseStation...
                (thisObject, baseStation)
            linksToBaseStation = [];
            for i = 1:length(thisObject.userEquipmentToBaseStationLinksList)
                link = thisObject.userEquipmentToBaseStationLinksList(i);
                if link.activeInTheCurrentSlot
                    if link.baseStation == baseStation
                        linksToBaseStation = [linksToBaseStation link]; %#ok<AGROW>
                    end
                end
            end
        end

        function loadTestScenario1(thisObject)
            thisObject.addBaseStation(BaseStation(10,20));
            thisObject.addBaseStation(BaseStation(50,20));
            thisObject.addUserEquipment(UserEquipment(0,0));
            thisObject.addUserEquipment(UserEquipment(20,0));
            thisObject.addUserEquipment(UserEquipment(40,0));
            thisObject.addUserEquipment(UserEquipment(60,0));

            thisObject.configureDownlinkTest;
        end

        function loadTestScenario2(thisObject)
            thisObject.addBaseStation(BaseStation(20,20));
            thisObject.addBaseStation(BaseStation(10,0));
            thisObject.addBaseStation(BaseStation(30,0));
            thisObject.addUserEquipment(UserEquipment(25,20));
            thisObject.addUserEquipment(UserEquipment(15,0));
            thisObject.addUserEquipment(UserEquipment(35,0));
            thisObject.addUserEquipment(UserEquipment(0,10));

            thisObject.configureDownlinkTest;
        end

        function loadTestScenario3(thisObject)
            thisObject.addBaseStation(BaseStation(10,10));
            thisObject.addBaseStation(BaseStation(30,35));
            thisObject.addBaseStation(BaseStation(50,10));
            thisObject.addUserEquipment(UserEquipment(0,0));
            thisObject.addUserEquipment(UserEquipment(20,0));
            thisObject.addUserEquipment(UserEquipment(20,20));
            thisObject.addUserEquipment(UserEquipment(0,20));
            thisObject.addUserEquipment(UserEquipment(20,25));
            thisObject.addUserEquipment(UserEquipment(40,25));
            thisObject.addUserEquipment(UserEquipment(20,45));
            thisObject.addUserEquipment(UserEquipment(40,45));
            thisObject.addUserEquipment(UserEquipment(40,20));
            thisObject.addUserEquipment(UserEquipment(40,0));
            thisObject.addUserEquipment(UserEquipment(60,0));
            thisObject.addUserEquipment(UserEquipment(60,20));

            thisObject.configureDownlinkTest;
        end

        function loadTestScenario3Uplink(thisObject)
            thisObject.addBaseStation(BaseStation(10,10));
            thisObject.addBaseStation(BaseStation(30,35));
            thisObject.addBaseStation(BaseStation(50,10));
            thisObject.addUserEquipment(UserEquipment(0,0));
            thisObject.addUserEquipment(UserEquipment(20,0));
            thisObject.addUserEquipment(UserEquipment(20,20));
            thisObject.addUserEquipment(UserEquipment(0,20));
            thisObject.addUserEquipment(UserEquipment(20,25));
            thisObject.addUserEquipment(UserEquipment(40,25));
            thisObject.addUserEquipment(UserEquipment(20,45));
            thisObject.addUserEquipment(UserEquipment(40,45));
            thisObject.addUserEquipment(UserEquipment(40,20));
            thisObject.addUserEquipment(UserEquipment(40,0));
            thisObject.addUserEquipment(UserEquipment(60,0));
            thisObject.addUserEquipment(UserEquipment(60,20));

            thisObject.configureUplinkTest;
        end

        function loadTestScenario4Uplink(thisObject)
            thisObject.addBaseStation(BaseStation(2.5,2.5));
            thisObject.addBaseStation(BaseStation(7.5,2.5));
            thisObject.addBaseStation(BaseStation(2.5,7.5));
            thisObject.addBaseStation(BaseStation(7.5,7.5));

            for i = 0:10
                for j = 0:10
                    thisObject.addUserEquipment(UserEquipment(j,i));
                end
            end

            thisObject.configureUplinkTest;
        end

        function loadTestScenario5Downlink(thisObject)
            thisObject.addBaseStation(BaseStation(5,5));
            thisObject.addBaseStation(BaseStation(25,5));
            thisObject.addUserEquipment(UserEquipment(0,0));
            thisObject.addUserEquipment(UserEquipment(10,0));
            thisObject.addUserEquipment(UserEquipment(0,10));
            thisObject.addUserEquipment(UserEquipment(10,10));
            thisObject.addUserEquipment(UserEquipment(20,0));
            thisObject.addUserEquipment(UserEquipment(30,0));
            thisObject.addUserEquipment(UserEquipment(20,10));
            thisObject.addUserEquipment(UserEquipment(30,10));

            thisObject.configureDownlinkTest;
        end

        function configureDownlinkTest(thisObject)
            thisObject.setAllBaseStationsTransmitPowerInWatts(50);
            thisObject.configureBasics;
        end

        function loadSuburbUplinkScenario(thisObject)
            baseStationsSeparationInMeters = 40;
            baseStationsOrigin = [20 0];
            thisObject.addTenBaseStationsInHorizontalLineMetersApartFromPoint...
                (baseStationsSeparationInMeters, baseStationsOrigin);
            baseStationsOrigin = [20 30];
            thisObject.addTenBaseStationsInHorizontalLineMetersApartFromPoint...
                (baseStationsSeparationInMeters, baseStationsOrigin);

            userEquipmentSeparationInMeters = 20;
            userEquipmentOrigin = [10 5];
            thisObject.addTwentyUserEquipmentInHorizontalLineMetersApartFromPoint...
                (userEquipmentSeparationInMeters, userEquipmentOrigin);
            userEquipmentOrigin = [10 25];
            thisObject.addTwentyUserEquipmentInHorizontalLineMetersApartFromPoint...
                (userEquipmentSeparationInMeters, userEquipmentOrigin);
            thisObject.configureUplinkTest;
        end

        function addTenBaseStationsInHorizontalLineMetersApartFromPoint...
                (thisObject, separationInMeters, originPoint)
            currentBaseStationPosition = originPoint;
            for i = 1:10
                x = currentBaseStationPosition(1);
                y = currentBaseStationPosition(2);
                baseStation = BaseStation(x, y);
                thisObject.addBaseStation(baseStation);
                currentBaseStationPosition(1) = ...
                    currentBaseStationPosition(1) + separationInMeters;
            end
        end

        function addTwentyUserEquipmentInHorizontalLineMetersApartFromPoint...
                (thisObject, separationInMeters, originPoint)
            currentUserEquipmentPosition = originPoint;
            for i = 1:20
                x = currentUserEquipmentPosition(1);
                y = currentUserEquipmentPosition(2);
                userEquipment = UserEquipment(x, y);
                thisObject.addUserEquipment(userEquipment);
                currentUserEquipmentPosition(1) = ...
                    currentUserEquipmentPosition(1) + separationInMeters;
            end
        end

        function loadDowntownResidentialUplinkScenario(thisObject)
            baseStationsSeparationInMeters = 20;
            baseStationsOrigin = [10 0];
            thisObject.addTenBaseStationsInHorizontalLineMetersApartFromPoint...
                (baseStationsSeparationInMeters, baseStationsOrigin);
            baseStationsOrigin = [10 17];
            thisObject.addTenBaseStationsInHorizontalLineMetersApartFromPoint...
                (baseStationsSeparationInMeters, baseStationsOrigin);

            userEquipmentSeparationInMeters = 10;
            userEquipmentOrigin = [5 3];
            thisObject.addTwentyUserEquipmentInHorizontalLineMetersApartFromPoint...
                (userEquipmentSeparationInMeters, userEquipmentOrigin);
            userEquipmentOrigin = [5 14];
            thisObject.addTwentyUserEquipmentInHorizontalLineMetersApartFromPoint...
                (userEquipmentSeparationInMeters, userEquipmentOrigin);
            thisObject.configureUplinkTest;
        end

        function loadBuildingUplinkScenario(thisObject)
            baseStationsSeparationInMeters = 3;
            baseStationsOrigin = [4 0];
            thisObject.addTenBaseStationsInVerticalLineMetersApartFromPoint...
                (baseStationsSeparationInMeters, baseStationsOrigin);
            baseStationsOrigin = [12 0];
            thisObject.addTenBaseStationsInVerticalLineMetersApartFromPoint...
                (baseStationsSeparationInMeters, baseStationsOrigin);
            userEquipmentSeparationInMeters = 3;
            userEquipmentOrigin = [2 0];
            thisObject.addTenUserEquipmentInVerticalLineMetersApartFromPoint...
                (userEquipmentSeparationInMeters, userEquipmentOrigin);
            userEquipmentOrigin = [6 0];
            thisObject.addTenUserEquipmentInVerticalLineMetersApartFromPoint...
                (userEquipmentSeparationInMeters, userEquipmentOrigin);
            userEquipmentOrigin = [10 0];
            thisObject.addTenUserEquipmentInVerticalLineMetersApartFromPoint...
                (userEquipmentSeparationInMeters, userEquipmentOrigin);
            userEquipmentOrigin = [14 0];
            thisObject.addTenUserEquipmentInVerticalLineMetersApartFromPoint...
                (userEquipmentSeparationInMeters, userEquipmentOrigin);
            thisObject.configureUplinkTest;
        end

        function addTenBaseStationsInVerticalLineMetersApartFromPoint...
                (thisObject, separationInMeters, originPoint)
            currentBaseStationPosition = originPoint;
            for i = 1:10
                x = currentBaseStationPosition(1);
                y = currentBaseStationPosition(2);
                baseStation = BaseStation(x, y);
                thisObject.addBaseStation(baseStation);
                currentBaseStationPosition(2) = ...
                    currentBaseStationPosition(2) + separationInMeters;
            end
        end

        function addTenUserEquipmentInVerticalLineMetersApartFromPoint...
                (thisObject, separationInMeters, originPoint)
            currentUserEquipmentPosition = originPoint;
            for i = 1:10
                x = currentUserEquipmentPosition(1);
                y = currentUserEquipmentPosition(2);
                userEquipment = UserEquipment(x, y);
                thisObject.addUserEquipment(userEquipment);
                currentUserEquipmentPosition(2) = ...
                    currentUserEquipmentPosition(2) + separationInMeters;
            end
        end

        function configureBasics(thisObject)
            thisObject.channel = FreeSpaceChannel(2600e6);
            thisObject.updateAllUserEquipmentSlotDuration;
            thisObject.updateDownlinkLinksList;
            thisObject.updateUplinkLinksList;
            thisObject.informBaseStationsLinks;
            thisObject.associateAllUserEquipment;
            thisObject.initializeBaseStationAssociatedUserEquipmentScheduledCounters;
            thisObject.initializeBaseStationRoundRobinSchedulers;
            thisObject.formClusters;
        end

        function setAllBaseStationsTransmitPowerInWatts...
                (thisObject, transmitPower)
            for i = 1:length(thisObject.baseStationsList)
                baseStation = thisObject.baseStationsList(i);
                baseStation.setTransmitPowerInWatts(transmitPower);
            end
        end

        function configureUplinkTest(thisObject)
            thisObject.setAllUserEquipmentTransmitPowerInWatts(0.5);
            thisObject.setAllBaseStationsTransmitPowerInWatts(50);
            thisObject.configureBasics;
        end

        function setAllUserEquipmentTransmitPowerInWatts...
                (thisObject, transmitPower)
            for i = 1:length(thisObject.userEquipmentList)
                userEquipment = thisObject.userEquipmentList(i);
                userEquipment.setTransmitPowerInWatts(transmitPower);
            end
        end

        function informBaseStationsLinks(thisObject)
            for i = 1:length(thisObject.baseStationsList)
                baseStation = thisObject.baseStationsList(i);
                thisObject.informDownlinkLinks(baseStation);
                thisObject.informUplinkLinks(baseStation);

            end
        end

        function informDownlinkLinks(thisObject, baseStation)
            linksFromBaseStationList = ...
                thisObject.findLinksFromBaseStation(baseStation);
            thisObject.addLinksFromBaseStationList...
                (baseStation, linksFromBaseStationList);
        end

        function informUplinkLinks(thisObject, baseStation)
            linksToBaseStationList = ...
                thisObject.findLinksToBaseStation(baseStation);
            thisObject.addLinksToBaseStationList...
                (baseStation, linksToBaseStationList);
        end

        function linksFromBaseStation = findLinksFromBaseStation...
                (thisObject, baseStation)
            linksFromBaseStation = [];
            for i = 1:length(thisObject.baseStationToUserEquipmentLinksList)
                link = thisObject.baseStationToUserEquipmentLinksList(i);
                if link.baseStation == baseStation
                    linksFromBaseStation = [linksFromBaseStation link];
                end
            end
        end

        function updateAllUserEquipmentSlotDuration(thisObject)
            for i = 1:length(thisObject.userEquipmentList)
                userEquipment = thisObject.userEquipmentList(i);
                userEquipment.slotDurationInSeconds = ...
                    thisObject.slotDurationInSeconds;
            end
        end

        function initializeBaseStationRoundRobinSchedulers(thisObject)
            for i = 1:length(thisObject.baseStationsList)
                baseStation = thisObject.baseStationsList(i);
                baseStation.setNumberOfResourceBlocksPerSlot...
                    (thisObject.resourceBlocksPerSlot);
                baseStation.initializeRoundRobinScheduler;
                baseStation.informAssociatedUserEquipmentListToScheduler;
            end
        end

        function formClusters(thisObject)
            cluster = Cluster;
            for i = 1:length(thisObject.baseStationsList)
                baseStation = thisObject.baseStationsList(i);
                cluster.addBaseStationToCluster(baseStation);
            end
            cluster.setResourceBlocksPerSlot(thisObject.resourceBlocksPerSlot);
            cluster.createCentralUnitCoordinatingAddedBaseStations;
            linksList = thisObject.baseStationToUserEquipmentLinksList;
            % cluster.passAllLinksListToCentralUnit(linksList);

            thisObject.clustersList = [thisObject.clustersList cluster];
        end
    end

    methods(Static)
        function scheduledUsers = getScheduledUsersFromAllSchedules...
                    (allBaseStationsSchedule, resourceBlock)
                scheduledUsers = [];
                for i = 1:length(allBaseStationsSchedule)
                    baseStationSchedule = allBaseStationsSchedule(i);
                    userEquipment = ...
                        baseStationSchedule.getUserInResourceBlock(resourceBlock);
                    scheduledUsers = [scheduledUsers userEquipment]; %#ok<AGROW>
                end
        end

        function greatestGainLink = findGreatestGainLink(linksList)
            greatestGainLink = [];
            previousGreatestGain = 0;
            for i = 1:length(linksList)
                currentLink = linksList(i);
                currentLinkGain = currentLink.gain;
                if currentLinkGain > previousGreatestGain
                    previousGreatestGain = currentLinkGain;
                    greatestGainLink = currentLink;
                end
            end
        end

        function intendedSignal = calculateIntendedSignalToUserEquipment...
                (userEquipment, linksToUserEquipment)
            intendedSignal = 0;
            for i = 1:length(linksToUserEquipment)
                currentLink = linksToUserEquipment(i);
                if currentLink.baseStation == userEquipment.servingBaseStation
                    baseStation = currentLink.baseStation;
                    intendedSignal = intendedSignal + ...
                        baseStation.getTransmitPowerInWatts.*currentLink.gain;
                end
            end
        end

        function intendedSignal = calculateIntendedSignalToBaseStation...
                (baseStation, linksToBaseStation)
            intendedSignal = 0;
            for i = 1:length(linksToBaseStation)
                currentLink = linksToBaseStation(i);
                userEquipment = currentLink.userEquipment;
                if userEquipment.servingBaseStation == baseStation
                    intendedSignal = intendedSignal + ...
                        userEquipment.getTransmitPowerInWatts.*currentLink.gain;
                end
            end
        end

        function interferingSignal = calculateInterferingSignalAtUserEquipment...
                (userEquipment, linksToUserEquipment)
            interferingSignal = 0;
            for i = 1:length(linksToUserEquipment)
                currentLink = linksToUserEquipment(i);
                if currentLink.baseStation ~= userEquipment.servingBaseStation
                    baseStation = currentLink.baseStation;
                    interferingSignal = interferingSignal + ...
                        baseStation.getTransmitPowerInWatts.*currentLink.gain;
                end
            end
        end

        function interferingSignal = calculateInterferingSignalAtBaseStation...
                (baseStation, linksToBaseStation)
            interferingSignal = 0;
            for i = 1:length(linksToBaseStation)
                currentLink = linksToBaseStation(i);
                userEquipment = currentLink.userEquipment;
                if userEquipment.servingBaseStation ~= baseStation
                    interferingSignal = interferingSignal + ...
                        userEquipment.getTransmitPowerInWatts.*currentLink.gain;
                end
            end
        end

        function activateScheduledUsersLinks(scheduledUsersLinks)
            for i = 1:length(scheduledUsersLinks)
                link = scheduledUsersLinks(i);
                link.activateLink;
            end
        end

        function addLinksFromBaseStationList...
                (baseStation, linksFromBaseStationList)
            for i = 1:length(linksFromBaseStationList)
                link = linksFromBaseStationList(i);
                baseStation.addLinkFromBaseStationToList(link);
            end
        end

        function addLinksToBaseStationList...
                (baseStation, linksToBaseStationList)
            for i = 1:length(linksToBaseStationList)
                link = linksToBaseStationList(i);
                baseStation.addLinkToBaseStationToList(link);
            end
        end

        function deactivateLinksList(linksList)
            for i = 1:length(linksList)
                link = linksList(i);
                link.deactivateLink;
            end
        end

        function activateLinksList(linksList)
            for i = 1:length(linksList)
                link = linksList(i);
                link.activateLink;
            end
        end
    end
end
