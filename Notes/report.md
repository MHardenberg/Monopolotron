### Dataset

- Monopoly game
- own implementtation
- rule simplification
    - no chest and chance cards
        - not necessary, makes implementation harder, no decision making that could be handled by the agent
    - no trading
        - harder implementation, more complex decision making process, makes environment too complex for our case
        - potential for future work
    - 2 players instead of 4
        - higher chances of owning the whole neigbourhood
    - only deciding whether to buy street or not, or build a building or not (but building have also same hard-coded restrictions to prevent agent breaking game rules)

### Agent

- DQN
- plays against itself
- all decision (made by both players) added to replay memory and used to train model
    - disadvantage: agent learning to beat itself → possibility of not find optimal policy
- alternative: to implement opponent as “optimal-policy player”, “random player” or separate DQN