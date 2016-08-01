from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive




class DriveSaver:
    def __init__(self):
        self.drive = None
        try:
            gauth = GoogleAuth()
            # Try to load saved client credentials
            gauth.LoadCredentialsFile("mycreds.txt")
            if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                # Refresh them if expired
                gauth.Refresh()
            else:
                # Initialize the saved creds
                gauth.Authorize()
            # Save the current credentials to a file
            gauth.SaveCredentialsFile("mycreds.txt")
            self.drive = GoogleDrive(gauth)
        except:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(gauth)


    def save(self, filename):
        try:
            file5 = self.drive.CreateFile()
            file5.SetContentFile(filename) # Read file and set it as a content of this instance.
            file5.Upload() # Upload it
        except:
            print "we could not save"

    def listFiles(self):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print 'title: %s, id: %s' % (file1['title'], file1['id'])

def main():
    d = DriveSaver()
    d.listFiles()

if __name__ == "__main__": main()
