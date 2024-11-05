from src.youtube import YTstats
from rich import print
from dotenv import load_dotenv
import os

load_dotenv()
Api_KEY= os.getenv("Api_KEY")
channel_name= 'johnwatsonrooney'
filename= 'stats.json'


yt= YTstats(Api_KEY) 

channel_id= yt.search_and_get_channel_id(channel_name)
if channel_id:
	print('channel_ID:', channel_id)
	print(yt.get_channel_statistics(channel_id))
	print(yt.get_channel_video_data())
	yt.dump_to_Json(filename)
	


