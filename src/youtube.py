# Register App and download channel statistics
# Get list of all videos with some basic infomation
# get in depth statistic for each videos
# head to jupter note book for to Analyze the data

from rich import print
import json
import googleapiclient.discovery
# from tqdm import tqdm #this is a progress bar package/library


# creat class obj for youtube stats
class YTstats:

	def __init__(self, api_key):
		self.api_key= api_key
		self.channel_id= None
		self.channel_statistics= None  #stores channel stats data
		self.video_data= None #stores channel_video data

		self.req_portal= self.create_api_client()


	# functon to get statistic channels
	def get_channel_statistics(self, channel_id):
		try:
			request= self.req_portal.channels().list(
				part= 'statistics',
				id= channel_id
			)
	
			data= request.execute()
			channel_stats= data['items'][0].get('statistics')
			self.channel_statistics= channel_stats

			return self.channel_statistics
			# print(channel_stats)

		except Exception as e:
			print(f'Error getting channel statistics: {e}')

	
	# method to pull video data/stats
	def get_channel_video_data(self):
		try:
			# 1) Get video IDs
			channel_videos = self._get_channel_videos_id_per_page(limit=50)
			video_ids = list(channel_videos.keys())

			# Split video_ids into chunks (e.g., 50 at a time, since maxResults is limited)
			batch_size = 50
			parts = 'snippet,statistics,contentDetails'

			for i in range(0, len(video_ids), batch_size):
				video_ids_batch = video_ids[i:i + batch_size]

				request = self.req_portal.videos().list(
					part=parts,
					id=','.join(video_ids_batch),
					fields='items(id,snippet,statistics,contentDetails)'

				)

				data = request.execute()

				for item in data['items']:
					video_id = item['id']
					channel_videos[video_id].update({
						'snippet': item.get('snippet', {}),
						'statistics': item.get('statistics', {}),
						'contentDetails': item.get('contentDetails', {})
					})

			self.video_data = channel_videos
			return channel_videos

		except Exception as e:
			print(f'Error getting channel video data: {e}')


	# method to get video ids of a given channel
	def _get_channel_videos_id_per_page(self, limit=None):
		channel_video_id= dict()
		try:
			max_results= limit if (limit is not None and isinstance(limit, int)) else 10
			request= self.req_portal.search().list(
				part= 'snippet',
				channelId= self.channel_id,
				order= 'date',
				maxResults= max_results,
				fields='items(id(videoId),id(kind)),nextPageToken'
			)


			while request:
				data= request.execute()
				for item in data['items']:
					if item['id']['kind'] == 'youtube#video':
						video_id= item['id'].get('videoId')
						if video_id:
							channel_video_id[video_id]= dict()


				# Use the nextPageToken for the next request
				request = (
					self.req_portal.search().list(
						part='snippet',
						channelId=self.channel_id,
						order='date',
						maxResults=max_results,
						pageToken=data.get('nextPageToken'),
						fields='items(id(videoId),id(kind)),nextPageToken'
					) if 'nextPageToken' in data else None
				)

			# print(len(video_ids))
			return channel_video_id

		
		except Exception as e:
			print(f'Error getting channel_videos!: {e}')

		# return channel_video_id


	# method to search and get a channels id
	def search_and_get_channel_id(self, channel_name:str=None):
		try:
			request= self.req_portal.search().list(
				part= 'snippet',
				q= channel_name,
				channelType= 'any'
			)
	
			data= request.execute()
			channel_id= data['items'][0].get('id').get('channelId')
			self.channel_id= channel_id

		except Exception as e:
			print(f'Error getting channel')

		return channel_id


	# method to connect YoutubeAPIclient 
	def create_api_client(self):
		try:
			api_service_name= 'youtube'
			api_version= 'v3'
			api_key= self.api_key
	
			# Build the API client
			youtube= googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
	
			return youtube
		except Exception as e:
			print(f'Error building channel portal')


	# method to sort data to json file
	def dump_to_Json(self, filename):

		try:
			if self.channel_statistics is None or self.video_data is None:
				print('Got no data...')
				return
				

			fused_data= {self.channel_id:{'channel_statistics': self.channel_statistics, 'video_data': self.video_data}}
	
			with open(filename, 'w') as f:
				json.dump(fused_data, f, indent=4)

			print('Json_file created!')

		except Exception as e:
			print(f'Error creating Json file: {e}')


	


