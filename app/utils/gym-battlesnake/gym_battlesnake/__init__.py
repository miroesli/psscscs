from gym.envs.registration import register

register(
    id='bs-amz-v0',
    entry_point='gym_battlesnake.envs:BattlesnakeGym',
)
register(
    id='bs-v0',
    entry_point='gym_battlesnake.envs:BsEnv',
)
register(
    id='bs-other-v0',
    entry_point='gym_battlesnake.envs:BsOtherEnv',
)

# from .snake_gym import BattlesnakeGym
