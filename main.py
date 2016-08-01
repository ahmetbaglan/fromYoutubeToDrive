from youtubeDownload import *
from DriveSave import *
nowDir = os.getcwd()
isMp3 = False

url = "https://www.youtube.com/watch?v=sNhhvQGsMEc&list=PLFs4vir_WsTzcfD7ZE8uO3yX-GCKUk9xZ"

saver = DriveSaver()
downloader = Downloader()
downloader.downloadList(url)

for i in os.listdir(os.getcwd()):
    print i
    saver.save(i)
os.chdir(nowDir)



