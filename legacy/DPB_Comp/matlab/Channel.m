classdef Channel < handle

    properties (Constant)
        speedOfLightInMetersPerSecond = 3e8
    end

    properties
        frequencyInHertz = -1
        transmitAntennaGain = 1
        receiveAntennaGain = 1
    end

    methods (Abstract)
        calculateGain(thisObject, distanceInMeters)
    end

    methods
        function newObject = Channel(frequencyInHertz)
            if frequencyInHertz <= 0
                error('Frequency must be positive');
            end
            newObject.frequencyInHertz = frequencyInHertz;
        end

        function wavelength = getWavelengthInMeters(thisObject)
            c = thisObject.speedOfLightInMetersPerSecond;
            f = thisObject.frequencyInHertz;
            wavelength = c./f;
        end
    end
end