import time
import os
import re
from urllib import parse as urlparse
from selenium import webdriver



def urlmanage():
    '''Return the first URL listed in you url.txt file and remove it'''
    urls = []
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/').replace('/src', "")
    with open(dir_path+"/resource/url.txt", 'r') as myfile:
        data=myfile.read()
        for u in data.split("\n"):
            urls.append(u)
    r = urls[0]
    with open(dir_path+"/resource/url.txt", 'w') as myfile:
        for i in range(1, len(urls)):
            myfile.write(urls[i]+"\n")

    return r

def getSrtFile(url):
    '''Download .srt file at /srt by using the service of downsub.com'''
    options = webdriver.ChromeOptions()
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/').replace('/src', "")
    options.add_experimental_option("prefs", {
        "download.default_directory": dir_path+"/srt",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(dir_path+'/resource/chromedriver', chrome_options=options)
    #driver.get('http://downsub.com/?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D'+id)
    #driver.find_element_by_xpath('//*[@id="show"]/b[1]/a').click()

    driver.get('http://downsub.com')
    driver.find_element_by_xpath('/html/body/div/div[3]/form/div/input').send_keys(url)
    driver.find_element_by_xpath('/html/body/div/div[3]/form/div/input').submit()
    driver.implicitly_wait(3);
    driver.find_element_by_xpath('//*[@id="show"]/b[1]/a').click()
    driver.implicitly_wait(3);
    time.sleep(10)
    driver.quit()

def getVideoID(url):
    '''Parse The youtube video ID from its url'''
    try:
        http = re.search("https?://", url).groups()
    except AttributeError:
        url = "http://"+url
    parsed = urlparse.urlparse(url)
    path = parsed.path
    query = parsed.query
    video_id = ""
    if path.upper() == "/WATCH":
        try:
            video_id = re.search("v=(.+)", query).group(1)
            if "&" in video_id:
                video_id = video_id[:video_id.index("&")]
        except AttributeError:
            pass
    elif "EMBED" in path.upper():
        try:
            video_id = re.search("/embed/(.+)", path).group(1)
        except AttributeError:
            pass

    if video_id:
        return video_id
    else:
        return None


def makeSrtPretty(file_name):
    '''
    Parse the Srt file to look pretty and save it as current_date_subtitle.txt file.
    Got help from https://github.com/jbaek7023/Youtube-Subtitle-Convertor-Make-it-Pretty-'''
    paragraph = []
    cleanr = re.compile('<.*?>')
    with open(file_name, 'rt', encoding="UTF8") as myfile:
        data = myfile.read()
        now = time.localtime()
        for line in data.splitlines():
            if len(line) > 4 and not line[0].isdigit():
                new_line = re.sub(cleanr, '', line)
                paragraph.append(new_line)
        output = ''
        for word in paragraph:
            output = output+ word+'\n'
    # write it
    print(output)
    now = time.localtime()
    newname = time.strftime("%Y%m%d", now)
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/').replace("/src","")

    with open(dir_path+"/srt/"+newname+"_subtitle.txt", 'w', encoding='utf8') as myfile:
        myfile.write(output)
        deleteFile(file_name)
    print("Subtitle saved")

def deleteFile(filename):
    if os.path.exists(filename) and not os.path.isdir(filename) and not os.path.islink(filename):
        os.remove(filename)

def findwords(subtitledir, wordlistdir, number_of_words):
    '''Find words both in wordlist.txt and the srt file currently working on and save it to new wordlist dir'''
    wordsinST = []
    wordsinL = []
    with open(subtitledir, 'rt', encoding='UTF8') as myfile:
        data = myfile.read()
        for word in data.split(" "):
            wordsinST.append(word.lower())
    with open(wordlistdir, 'r', encoding='UTF8') as myfile:
        data2 = myfile.read()
        for word in data2.split("\n"):
            wordsinL.append(word.lower())


    if len(worktodo) > number_of_words+1 :
        worktodo = worktodo[:number_of_words]

    now = time.localtime()
    newname = time.strftime("%Y%m%d", now)
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/').replace("/src","")

    with open(dir_path+"/word/" + newname + "_word.txt", 'w', encoding='UTF8') as myfile:
        for i in range(len(worktodo)):
            myfile.write(worktodo[i]+"\n")

    newwordlist = list(set(wordsinL)-set(worktodo))
    with open(wordlistdir, 'w', encoding='UTF8') as myfile:
        for word in newwordlist:
            myfile.write(word+"\n")

if(__name__=='__main__'):
    print(getVideoID("https://www.youtube.com/watch?v=JGEp4nWyHOs"))