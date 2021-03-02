from gym.envs.registration import register

register(
    id='pibot-v0',
    entry_point='gym_pibot.envs:PiBotEnv',
)
register(
    id='pibot-v1',
    entry_point='gym_pibot.envs:PiBotEnv2',
)