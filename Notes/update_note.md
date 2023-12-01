# Update note 28-11-23
I have experimented and worked on the new michel_model branch.
I have seperated the acting and learning/replay parts. This allows us to play a full turn, before we go through the replay.

```python
    def act(self, state:torch.Tensor, player_idx: int) -> int:
        """ This function only takes decisions. It is supposed to be called 
        seperately from the .learn() method, when a decision has to be taken.
        This seperation has been done,
        as the full state (incl. done) is only known after all actors 
        finish their turn.
        """
        self.player_game_state[player_idx] = state
        self.model.eval()

        choice = random.random()
        if choice > self.epsilon:
            with torch.no_grad():
                return self.policy_model(state).max(1).indices
        return random.randint(0, 1) 
```


```python
   def replay(self, player_idx: int, state: torch.Tensor, action: int, done: bool) -> None:
        """ This function takes care of learning after action was taken. It is 
        supposed to be called at the end of a full round.
        """
        reward = self.__eval_reward(state)
        self.__store_experience(player_idx, state, action, reward, done)

        self.__update_epsilon()
        self.steps += 1
```

The way this works, is that we take all action of a turn. Then we iterate through all the states, and actions taken. If that is the final turn, we mark the final action as done=True.

```python
train_model(visualise: bool=False, sleep_ms: float=0):
    dqn = DQNAgent()

    for epoch in range(1, epochs):
        game = Game(humans=0, cpu=2, rnd_cpu=0, dqn_model_instance=dqn)
        for idx, _ in enumerate(game.players):

            game.players[idx].game = game
            while not game.finished:
                if sleep_ms:
                    time.sleep(0.001 * sleep_ms)
                if visualise:
                    game.visualise()

                game.play_turn()
                game.turns_played += 1

                done = game.finished
                for idx, _ in enumerate(game.players):
                    state_action_list = state_action_dict[idx]
                    while state_action_list:
                        state, action = state_action_list.pop(0)
                        final_move = (len(state_action_list) == 0) and done
                        dqn.replay(idx, state, action, final_move)
                        dqn.clear_state_action_dict()
```

This required passing a lot of reference back and foirth, and the current version is largely exploratory and messy. As it is going to be real hard to debug, I'll do a rewrite of this change from the current state of the model branch.

