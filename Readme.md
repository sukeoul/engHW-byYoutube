# Giving english homework using youtube video

This script was written to give homework to my english student.

Script works following the steps below :

* Download .srt file from downsub.com
* Parse it and find the Phrases which is both in the srt file, and your wordlist(resource/wordlist.txt)
* Post the new phrases, and the texts in srt file to google drive worksheet
* You should list the url of the videos you will use in resource/url.txt
* That youtube video ***must have subtitles / close caption***

These are the pre-req for this script:

 * [gspread](https://github.com/burnash/gspread) - **client_secret.json file should be placed in /resource**
 * [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

You can run it by
```
python giveHW.py
```

It will work as the screenshot below<
![show.png](show.png)

Thanks.
