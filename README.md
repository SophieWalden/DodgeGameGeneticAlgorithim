# DodgeGameGeneticAlgorithim
A simple game of dodge the enemy, with a bit of machine Learning Genetic Algorithm to make it better

The reason this doesn't get past average 4 with 1 hidden layer and 6 with 3 is that this game is too luck-based to perform a good genetic algorithim, atleast for my level, and thus my next few projects with this will probablybe a more set in stone concrete game where it doens't change game to game

Of course, you can crank up the hidden layers if you want, but at a certain level it become's too many nodes since theres a population of 100 all running games per population. I did train another machine Learning algorithim orginally on this game, and I got it to effectively never lose at this game, but it uses 2000 nodes, is trained without having to run through this evolution stuff, and only has to run itself, not 100 copies of itself.

All algorithims are self wrote, but the mutation functions exact values was influenced by CodeBullet's dinoGame as a lot of my machine learning ideas stem from him and Carykh (plus, I have no idea good values for mutations, I originally wrote another function entirely and was never evolving basically).
