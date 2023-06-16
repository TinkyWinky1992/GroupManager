import utils
from event import Bot

if __name__ == "__main__":
   config = utils.get_config() 
   bot = Bot(config)
   bot.run()
   
   