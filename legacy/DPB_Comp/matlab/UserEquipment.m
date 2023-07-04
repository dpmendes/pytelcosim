classdef UserEquipment < Transceiver
    
    properties
        servingBaseStation = []
    end
    
    methods
        function newObject = UserEquipment(x, y)
            newObject = newObject@Transceiver(x, y);
        end
        
        function associateToBaseStation(thisObject, baseStation)
            thisObject.servingBaseStation = baseStation;
        end
        
        function dissociateFromBaseStations(thisObject)
            thisObject.servingBaseStation = [];
        end
        
        function baseStation = getServingBaseStation(thisObject)
            baseStation = thisObject.servingBaseStation;
        end
        
        function isDummy = isDummy(thisObject)
            [x, y] = thisObject.getPosition;
            isDummy = (x < 0) & (y < 0);
        end
    end
   
end

