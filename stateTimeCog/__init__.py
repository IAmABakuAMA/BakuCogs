import os

cog_dir = os.path.dirname(os.path.abspath(__file__))
cog_name = os.path.basename(cog_dir)

from .stateTimeCog import StateTimeCog

def setup(bot):
    bot.add_cog(StateTimeCog(bot))
