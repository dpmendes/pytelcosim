classdef Transceiver < handle
    properties(Constant)
        BOLTZMANN_CONSTANT = 1.38064852e-23;
    end
    
    properties% (Access = private)
        x = 0
        y = 0
        numberOfResourceBlocksReceived = 0
        transmitPowerInWatts = 0
        currentSignalToInterferencePlusNoiseRatio = 0
        currentCapacityInBitsPerSecond = 0
        bandwidthInHertz = 180e3
        receiverTemperatureInKelvins = 290
        totalBitsReceived = 0
        totalBitsTransmitted = 0
        slotDurationInSeconds = 0.5e-3
    end
    
    methods
        
        function newObject = Transceiver(x, y)
            newObject.setPosition(x, y);
        end
        
        function setPosition(thisObject, x, y)
            thisObject.x = x;
            thisObject.y = y;
        end
        
        function [x, y] = getPosition(thisObject)
            x = thisObject.x;
            y = thisObject.y;
        end
        
        function transmitPower = getTransmitPowerInWatts(thisObject)
            transmitPower = thisObject.transmitPowerInWatts;
        end
        
        function setTransmitPowerInWatts(thisObject, transmitPower)
            thisObject.transmitPowerInWatts = transmitPower;
        end
        
        function receiveResourceBlock(thisObject)
            C = thisObject.currentCapacityInBitsPerSecond;
            Tslot = thisObject.slotDurationInSeconds;
            thisObject.totalBitsReceived = thisObject.totalBitsReceived + ...
                C.*Tslot;
            thisObject.numberOfResourceBlocksReceived = ...
                thisObject.numberOfResourceBlocksReceived + 1;
        end
        
        function transmitResourceBlock(thisObject, capacity)
            thisObject.totalBitsTransmitted = ...
                thisObject.totalBitsTransmitted + ...
                capacity.*thisObject.slotDurationInSeconds;
        end
        
        function updateSignalToInterferencePlusNoiseRatio...
                (thisObject, intendedSignalPower, interferingSignalPower)
            noisePower = thisObject.calculateNoisePower();
            
            SINR = intendedSignalPower./(interferingSignalPower+noisePower);

            thisObject.currentSignalToInterferencePlusNoiseRatio = SINR;
        end
        
        function calculateReceptionCapacity(thisObject)
            SINR = thisObject.currentSignalToInterferencePlusNoiseRatio;
            BW = thisObject.bandwidthInHertz;
            capacity = BW.*log2(1+SINR);
            thisObject.currentCapacityInBitsPerSecond = capacity;
        end
        
        function currentCapacity = ...
                getCurrentCapacityInBitsPerSecond(thisObject)
            currentCapacity = thisObject.currentCapacityInBitsPerSecond;
        end
    end
    
    methods(Access=private)
        function noisePower = calculateNoisePower(thisObject)
            k = thisObject.BOLTZMANN_CONSTANT;
            T = thisObject.receiverTemperatureInKelvins;
            BW = thisObject.bandwidthInHertz;
            
            noisePower = k.*T.*BW;
        end
    end
end