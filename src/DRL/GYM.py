class PiRoboEnv(gym.Env):
    """A stock trading environment for OpenAI gym"""
    # metadata = {'render.modes': ['human']}
    def __init__(self, df):
        super(PiRoboEnv, self).__init__()
        self.df = df
        self.reward_range = (0, MAX_REWARD)
        # Actions: [Forwards, Backwards, Left, Right, Turn Servo]
        self.action_space = spaces.Box(
          low=np.array([0, 0, 0, 0, 0]), high=np.array([10, 10, 10, 10, 10]), dtype=np.float16)
        # Initial observation will just be the ultrasound sensor
        self.observation_space = spaces.Box(
          low=0, high=1, shape=(1,), dtype=np.float16)

    def reset(self):
        self.score = INIT_SCORE
