
from game_engine import GameEngine
from hyper_param import HyperParam

hyper_param = HyperParam()
game_engine = GameEngine(hyper_param)
game_engine.run()