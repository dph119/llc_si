#!/usr/bin/python

DEBUG = 0
import sys

def parse_hitratios(fileName):
    # read in the file
    file_name = fileName.strip()

    if DEBUG: print 'Opening file', file_name, '\n'

    file_handle = open(file_name, 'r')

    ratioDict = {}

    # walk the file, parsing it
    for line in file_handle:

        line = line.strip()
        # 'mem_report__FFT__mem_config_0.txt-[ mm-0 ]'
        # This is a line identifying the memory module
        if line.endswith(']'):
            currentMemoryModule = line[line.find('[')+1:-1].strip()
            if DEBUG: print currentMemoryModule
            pass
        
        # 'mem_report__FFT__mem_config_0.txt:HitRatio = 0'
        # This line identifies the hit ratio of the previously
        # identified memory module
        if 'HitRatio' in line:
            # Get name of file. That is our key in the dict
            # e.g. extract "FFT__mem_config_0" from above string
            fileName = line[line.find('__')+2:line.find('.')]

            if DEBUG: print '\t\t'+fileName

            if fileName not in ratioDict.keys():
                if DEBUG: print 'creating dict entry...'
                #                        l1     l2     l3    mm
                ratioDict[fileName] = [ [0,0], [0,0], [0,0], [0,0] ]
                pass

            hitRatio = line[line.find('=')+1:].strip()

            if DEBUG: print '\tHitRatio = '+str(hitRatio)

            # benchmark/config -> [ [l1 sum, l1 count], [l2 sum, l2 count], [l3 sum, l3 count], [mm sum, mm count] ]
            memoryModule = currentMemoryModule[:2]
            if DEBUG: print memoryModule
            if memoryModule == 'l1' :
                if DEBUG: print 'is l1'
                ratioDict[fileName][0][0] = ratioDict[fileName][0][0] + float(hitRatio)
                ratioDict[fileName][0][1] = ratioDict[fileName][0][1] + 1
                pass
            elif memoryModule == 'l2' :
                if DEBUG: print 'is l2'
                ratioDict[fileName][1][0] = ratioDict[fileName][1][0] + float(hitRatio)
                ratioDict[fileName][1][1] = ratioDict[fileName][1][1] + 1
                pass
            elif memoryModule == 'l3' :
                if DEBUG: print 'is l3'
                ratioDict[fileName][2][0] = ratioDict[fileName][2][0] + float(hitRatio)
                ratioDict[fileName][2][1] = ratioDict[fileName][2][1] + 1
                pass
            elif memoryModule == 'mm' :
                if DEBUG: print 'is mm'
                ratioDict[fileName][3][0] = ratioDict[fileName][3][0] + float(hitRatio)
                ratioDict[fileName][3][1] = ratioDict[fileName][3][1] + 1
                pass
            else:
                print line
                print memoryModule
                assert(0) # Unidentified memory module
            
#            ratioDict[fileName]
                pass
            pass
        pass
    for key in ratioDict:
        counter = 0
#        print key[:key.find('__')]+','+key[key.find('__')+2:]
        if DEBUG: print ratioDict[key]
        for entry in ratioDict[key]:
            if counter == 0: currentMemoryModule = 'l1'
            elif counter == 1: currentMemoryModule = 'l2'
            elif counter == 2: currentMemoryModule = 'l3'
            elif counter == 3: currentMemoryModule = 'mm'
            else : assert(0) # counter > expected value of 3
            if DEBUG: print entry
            if entry[0] is not 0 and entry[0] is not 0:
                print key[:key.find('__')]+','+key[key.find('__')+2:]+','+currentMemoryModule+','+str(entry[0]/float(entry[1]))
                pass
            else:
                print key[:key.find('__')]+','+key[key.find('__')+2:]+','+currentMemoryModule+','+str(0)
                pass
            counter = counter + 1
        pass
pass

if __name__ == "__main__":
    # First arg is name of the file to parse
    parse_hitratios(sys.argv[1])
pass
