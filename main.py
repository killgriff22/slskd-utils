import slskd_api
from time import sleep
host = "http://192.168.1.191:5030"
api_key = "a86a43ce8ef4729047462c33bbc2849b"
slskd = slskd_api.SlskdClient(host, api_key )

app_status = slskd.application.state()
#print(slskd.files.get_downloads_dir())
def search(query):
    promise = slskd.searches.search_text(query)
    promise_id = promise['id']
    print(promise_id)
    sleep(5)
    results = slskd.searches.search_responses(promise_id)
    files_to_dl = []
    for result in results:
        for f in result['files']:
            if f['extension'] not in ['flac', 'lrc']:
                continue
            files_to_dl.append(f)
        if len(files_to_dl) > 0:
            slskd.transfers.enqueue(result['username'], files_to_dl)
            print(files_to_dl)
            files_to_dl = []
            break
search("discord the living tombstone")
#new branch

#available_rooms = slskd.searches.search_responses('80e802cc-ddf1-11f1-ad64-8cdcd43ff51a')

#print(available_rooms)