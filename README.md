# DodgeGameGeneticAlgorithim
A simple game of dodge the enemy, with a bit of machine Learning Genetic Algorithm to make it better

UPDATE 1/21/2021:
-Fixed the crossover function, this previously had a 31.25% chance to get a parents connection and now 98.75% chance, this was a problem since it was deleting all valued connections

-Bigger fix is that after a few more projects (Car Driving and a Cell Evolution) one I figured out that due to the crossover function there was a point where I set the childs connections for a certain node equal to the parents and that was in memory not creating a copy, but linking them so if you mutated the child it mutated the parent. This is changed to make a copy and now gets 6-8 average score with no hidden layers in like 20-30 generations and could probably go higher with more time/layers. Saw it get to 80+ score and I have the game stop at 200, since if you get there you pretty much can't lose so it's getting pretty close

Will keep coming back and updating this more if I find more improvements in my algorithim

All algorithims are self wrote, but the mutation functions exact values was influenced by CodeBullet's dinoGame as a lot of my machine learning ideas stem from him and Carykh (plus, I have no idea good values for mutations, I originally wrote another function entirely and was never evolving basically).
