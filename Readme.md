# Alphazero-on-Hex-game
A project implementing minimax as the baseline and reinforcement learning as the main method for 6*6 Hex game, receiving Best Honorable Mention Reward at the end of the course.    

## Create training model
```
python main.py
```
Poeple can modify code in main.py to change the previous model to load into.  
Run main.py then the training model will be store in Tables.  

## Baseline v.s. Hex game website
```
python test.py
```
We need to check whether our baseline are correct. As a result, we use the method of web crawling to send our action to the Hex game website and play the game online.  
We could modify how strong our baseline is by changing the settings in baseline.py.  

## Baseline v.s. models
```
python fight.py
```
Let our models play with our baseline to see if our models are strong enough.