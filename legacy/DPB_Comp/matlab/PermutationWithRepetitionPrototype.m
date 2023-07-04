a = [4 9 5];

numberOfPositions = 4;
numberOfChoices = length(a);
numberOfPermutationsWithRepetition = numberOfChoices.^numberOfPositions;

b = zeros(numberOfPermutationsWithRepetition, numberOfPositions);

n = numberOfPositions;
l = numberOfChoices;

for i=1:n 
   b(:,i)=reshape(reshape(repmat((1:l),1,l^(n-1)),l^i,l^(n-i))',l^n,1); 
end

for i = 1:length(b(:,1))
    for j = 1:length(b(1,:))
        b(i,j) = a(b(i,j));
    end
end

