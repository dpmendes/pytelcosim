classdef Schedule < handle
    
    properties
        baseStation
        usersInResourceBlocks = []
        numberOfResourceBlocks
    end
    
    methods
        function newObject = Schedule(numberOfResourceBlocks)
            newObject.numberOfResourceBlocks = numberOfResourceBlocks;
        end        
        
        function addUserToResourceBlock(thisObject, userEquipment)
            if length(thisObject.usersInResourceBlocks) < ...
                    thisObject.numberOfResourceBlocks
                thisObject.usersInResourceBlocks = ...
                    [thisObject.usersInResourceBlocks userEquipment];
            end
        end
        
        function shiftUsersInResourceBlocksToTheRight(thisObject)
            dummyUser = UserEquipment(-1,-1);
            thisObject.usersInResourceBlocks = ...
                [dummyUser thisObject.usersInResourceBlocks];
        end
        
        function userEquipment = ...
                getUserInResourceBlock(thisObject, resourceBlock)
            userEquipment = thisObject.usersInResourceBlocks(resourceBlock);
        end
        
        function setBaseStation(thisObject, baseStation)
            thisObject.baseStation = baseStation;
        end
        
        function baseStation = getBaseStation(thisObject)
            baseStation = thisObject.baseStation;
        end
    end
    
end