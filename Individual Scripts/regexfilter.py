# This script performs regex filtering

import pandas
import glob
import os
import re

# This does automated filtering
files = []
# THIS IS YOUR FOLDER OF COMMITS YOU EXTRACTED FROM GITHUB - CHANGE THIS 
path = r"C:\Users\User\Desktop\Work\SMU\Capstone\Datasets\commits\extra\*.csv"
for fname in glob.glob(path):
    files.append(fname)
print(files)
for i in files:
    print(i)
    dataframe = pandas.read_csv(i, usecols=[1, 2, 3, 4, 5
                                              ])  # skip first col cause it's just index and dataframe tracks index anyway so it's redundant
    pattern = '(?i)(seg( ?)fault(s?)|segmentation fault|crash|\\bDOS\\b|denial.of.service|null pointer deref(erence)?|null( )?ptr deref(erence)?|\\bOOB\\b|out-of-bounds|out(side)? of bounds|out of bound|overflow|underflow|integer (?:underflow|overflow)|corruption|invalid memory access|data loss|validation|validate|check(?: |-)fail|failing check|check issue|invalid address|undefined behavio(u?)r|div(ision)?(s)? by (?:0|zero)|divide by (?:0|zero)|uninitiali[z|s]ed memory|\\bFPE\\b|floating point exception|exploit(s)?|\\bXXE\\b|remote.code.execution|\\bopen.redirect|OSVDB|vuln|\\bCVE\\b|\\bXSS\\b|\\bReDoS\\b|\\bNVD\\b|malicious|x-frame-options|attack|cross.site|exploit|directory.traversal|\\bRCE\\b|\\bdos\\b|\\bXSRF\\b|clickjack|session.fixation|hijack|advisory|insecure|security|\\bcross-origin\\b|unauthori[z|s]ed|infinite.loop|authenticat(e|ion)|brute force|bypass|constant.time|crack|credential|expos(e|ing)|hack|harden|injection|lockout|password|\\bPoC\\b|proof.of.concept|poison|privilege|\\b(in)?secur(e|ity)|(de)?serializ|spoof|timing|traversal|segv|null pointer exception|assertion failure|breakage)'
    result_df = pandas.DataFrame()
    csvname = os.path.basename(i).replace('.csv', '')
    regexnewfile = r"C:\Users\User\Desktop\Work\SMU\Capstone\Datasets\commits\regex" + "\\" + str(csvname) + ".csv"
    a = 1
    for (_, sha, msg, html_url, author, commit_date) in dataframe.itertuples():
        if re.search(pattern,
                     str(msg)):  # search matches anywhere in string instead of match which only matches beginning
            # print(a)
            result_df = result_df.append(
                {"Sha": sha, "Message": msg, "html.url": html_url, "Author": author, "Date": commit_date},
                ignore_index=True, sort=False)
            a = a + 1
    print(result_df)
    if not result_df.empty:
        result_df.to_csv(regexnewfile, mode='w')  # write df back out to csv
