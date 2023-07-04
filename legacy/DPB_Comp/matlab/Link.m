classdef Link < handle

    properties
        baseStation
        userEquipment
        channel
        gain
        activeInTheCurrentSlot = true
    end
    
    methods
        function newObject = Link(channel)
            newObject.channel = channel;
        end
        
        function calculateLinkGain(thisObject)
            distance = thisObject.calculateDistance();
            linkChannel = thisObject.channel;
            thisObject.gain = linkChannel.calculateGain(distance);
        end
        
        function deactivateLink(thisObject)
            thisObject.activeInTheCurrentSlot = false;
        end
        
        function activateLink(thisObject)
            thisObject.activeInTheCurrentSlot = true;
        end
        
        function distance = calculateDistance(thisObject)
            [originX originY] = thisObject.baseStation.getPosition();
            [destinationX destinationY] = ...
                thisObject.userEquipment.getPosition();
            
            horizontalDistance = destinationX - originX;
            verticalDistance = destinationY - originY;
            
            distance = sqrt((horizontalDistance.^2)+(verticalDistance.^2));
        end
    end
end
