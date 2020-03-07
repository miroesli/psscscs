##    Project structure  
.  
├ main.py  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     :snake:    
├ api.py  
├ train.py  
├ simple_train.py  
├ algs/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - generic algorithms  
├ data/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - saved prediction models    
├ models/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - constructed models    
├ settings/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - JSON formatted model selection & input parameters  
└ utils/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - generic utilities  

  
## How to train models  
1. First get a model and create it, e.g. nn = AlphaNNet(config=config, in_shape=[15x15])  
2. Create an Agent for each snake, this allow for multi-agent tracking. snake = Agent(nn)    
3. Use the agent make_move function to predict the snake's next move, snake.make_move(state)  
4. For each agent add the agent.records attribute to X, X += agent.records. (these are the moves made in the game)  
5. Calculate Y for the winner with degrading reward, see `algs/alpha_snake_zero_trainer.py`  
6. Copy the nnet and pass this bad boys in, `from numpy import array; nnet.train(array(X), array(Y))`  
7. Make sure to save your model when done, simply call the AlphaNNet save function, `nnet.save('modelname')`  
8. Model should now be in the data/ folder, if name is defined in used config it will be reloaded on next deploy.  
