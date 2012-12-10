'''
Generate the keyword list you concerned and copy them to the text file
@author : neal (njugui@gmail.com)
'''

import os
print "***Keywords to Text file: generate lines that contains your keywords**"

def parseKeywords(filepath, keyword_list):
    fileInput = open(filepath, 'r')
    fileOutput = open('keywords_output.txt', 'w')
    lines = fileInput.readlines() 
    for line in lines:
        for keyword in keyword_list:
            if keyword in line:
                fileOutput.write(line)
                break
            
if __name__ == '__main__':
    while True:
        filepath = raw_input('Please input the file path:\n')
        while not os.path.exists(filepath):
            filepath = raw_input('no %s ' % filepath + 'found! please input the file path again!!\n')
        keyword_list = []
        print 'Please input the keyword list, use [end] to end inputting: \n'
        keyword = ''
        while keyword != '[end]':
            print 'another keywords? or [end]'
            keyword = raw_input()
            keyword_list.append(keyword)
        parseKeywords(filepath, keyword_list);
        print 'Finish!!'
        os.system('keywords_output.txt')
