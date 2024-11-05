import json 
from rich import print

with open('stats.json', 'r') as f:
    data= json.load(f)


var= data

id_, data1= var.popitem()
vids= data1['video_data']
# itm= vids.items()
data= sorted(vids.items(), key= lambda item: int(item[1]['statistics']['viewCount']), reverse=True)
stat= []
for vid in data:
    vid_id= vid[0]
    title= vid[1]['snippet']['title']
    viewcount= vid[1]['statistics'].get('viewCount')

    print(viewcount)
# print(itm)




# countdown = 10
# while countdown > 0:
#     print(countdown)
#     countdown += 1


#     def get_channel_video_data(self):
#         # 1) get video ids
#         channel_videos= self._get_channel_videos_id_per_page(limit=50)
#         video_ids= list(channel_videos.keys())
    
#         # 2) get video stats(like count,view count etc.. )
#         # Split video_ids into chunks (e.g., 50 at a time, since maxResults is limited)
#         batch_size = 50
#         parts= 'snippet,statistics,contentDetails'

#         for videoid in tqdm(channel_videos):
#             for part in parts:
#                 request= self.req_portal.videos().list(
#                     part= part,
#                     id= videoid,
#                     fields=f'items({part})'
#                 )
#                 try:
#                     data= request.execute()
#                     stats_data= data['items'][0][part]
#                     # update channel_videos dict with their respective data
#                     channel_videos[videoid].update(stats_data)

#                 except Exception as e:
#                     print(f'Error getting stats_data: {e}')
#                     stats_data= dict()

#             self.video_data= channel_videos
#             return channel_videos
