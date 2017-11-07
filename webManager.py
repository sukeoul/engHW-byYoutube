import time, os

try:
    import gspread
except ImportError:
    import pip
    pip.main(['install', '--user', 'gspread'])
    import gspread
try:
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError:
    import pip
    pip.main(['install', '--user', 'oauth2client'])
    from oauth2client.service_account import ServiceAccountCredentials

class sheetManager():
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)

    def initSheet(self,url):
        dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        now = time.localtime()
        title = time.strftime("%Y%m%d", now)

        sub = []
        with open(dir_path+"/srt/" + title + "_subtitle.txt", 'r', encoding='UTF8') as myfile:
            data = myfile.read()
            for line in data.split("\n"):
                sub.append(line)

        word = []
        with open(dir_path+"/word/" + title + "_word.txt", 'r', encoding='UTF8') as myfile:
            data = myfile.read()
            for w in data.split("\n"):
                word.append(w)

        spreadsheet = self.client.open("Eng")
        sheet = spreadsheet.add_worksheet(title, max(len(sub)+5, 50), 10)

        #Update sheet frame
        sheet.update_cell(1,1, title+" HomeWork")
        sheet.update_cell(2,2,'Video URL')
        sheet.update_cell(2,3, url)
        sheet.update_cell(2,8, "Place Homework here in H2")


        #Update subtitle contents
        sheet.update_cell(4,5, title+"_subtitle.txt")
        j=2
        mrange = 'E6:E' + (str(5+len(sub)))
        cell_list = sheet.range(mrange)
        i=0
        for cell in cell_list:
            cell.value=sub[i]
            i+=1
        sheet.update_cells(cell_list)

        #Update new phrases
        sheet.update_cell(4,2,'New Phrases')
        wrange = 'B6:B' + (str(5 + len(sub)))
        wcell_list = sheet.range(wrange)
        i = 0
        for cell in wcell_list:
            cell.value = word[i]
            i += 1
            if i == len(word) : break
        sheet.update_cells(wcell_list)


    def manageHomework(self, date):
        '''Writed for Checking home work, but not used'''
        spreadsheet = self.client.open("Eng")
        sh = spreadsheet.worksheet(date)

        wordsList= list(set(sh.col_values(2)))

        wordsList.remove('New Phrases')
        wordsList.remove('Video URL')
        while '' in wordsList: wordsList.remove('')

        hw = sh.cell(2,8)
        text = hw.value
        written = text.split(" ")
        result = ""
        for word in written:
            if word in wordsList:
                word = '*' + word
            result = result + word + " "

        sh2 = spreadsheet.worksheet('Grade_Of_Homework')
        dates = sh2.col_values(2)
        while '' in dates: dates.remove('')
        linenum = len(dates)+1

        sh2.update_cell(linenum, 1, date)
        sh2.update_cell(linenum, 2, result)

        spreadsheet.del_worksheet(sh)


