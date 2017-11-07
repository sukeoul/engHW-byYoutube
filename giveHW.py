import work, os, time, webManager
try:
    import glob
except ImportError:
    import pip
    pip.main(['install', '--user', 'glob'])
    import glob

#This diretory path works for windows
dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

wb = webManager.sheetManager()
url = work.urlmanage()
work.getSrtFile(work.getVideoID(url))
os.chdir("./srt")
filedir = glob.glob("*.srt")
work.makeSrtPretty(dir_path+"/srt/"+filedir[0])
now = time.localtime()
newname = time.strftime("%Y%m%d", now)
work.findwords(dir_path+"/srt/"+newname+"_subtitle.txt", dir_path+'/wordlist.txt', 20) # Last parameter is the number of words

wb.initSheet(url)