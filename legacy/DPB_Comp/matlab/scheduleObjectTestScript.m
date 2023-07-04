clear all
clc

ue1 = UserEquipment(1,1);
ue2 = UserEquipment(2,2);
ue3 = UserEquipment(3,3);
ue4 = UserEquipment(4,4);
ue5 = UserEquipment(5,5);
ue6 = UserEquipment(6,6);

s1 = Schedule(3);
s1.addUserToResourceBlock(ue1);
s1.addUserToResourceBlock(ue2);
s1.addUserToResourceBlock(ue3);

s2 = Schedule(3);
s2.addUserToResourceBlock(ue4);
s2.addUserToResourceBlock(ue5);
s2.addUserToResourceBlock(ue6);

slotsList = [s1 s2];

firstSlot = [];

for i = 1:length(slotsList)
    firstSlot = [firstSlot slotsList(i).getUserInResourceBlock(1)];
end
disp(firstSlot);

disp(firstSlot(1).getPosition);
disp(firstSlot(2).getPosition);