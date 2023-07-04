classdef FreeSpaceChannel < Channel

    properties
    end
    
    methods
        function newObject = FreeSpaceChannel(frequencyInHertz)
            newObject = newObject@Channel(frequencyInHertz);
        end
        
        function gainInDb = calculateGainInDb...
                (thisObject, distanceInMeters)
            
            gainInDb = 10.*log10(thisObject.calculateGain...
                (distanceInMeters));
        end
        
        function gain = calculateGain...
                (thisObject, distanceInMeters)

            lambda = thisObject.wavelengthInMeters;
            Gt = thisObject.transmitAntennaGain;
            Gr = thisObject.receiveAntennaGain;
            d = distanceInMeters;
            
            gain = (Gt.*Gr.*(lambda.^2))./(((4.*pi.*d).^2));
        end
            
    end
    
end