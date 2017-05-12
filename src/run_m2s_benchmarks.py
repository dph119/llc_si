#!/usr/bin/python

import time
import datetime
import os

###################################
#
# Run the suite of AMD APP
# benchmarks, using pre-determined
# parameters that I care about.
#
###################################

# Contains the name of the benchmark, as well
# as the string of arguments to provide the benchmark.
benchmarkList = [
#    ['BinarySearch', '-q -x 1000000 -i 1000'], 
#    ['EigenValue', '-q '], 
#    ['MatrixTranspose', '-q '],
#    ['Reduction', '-q '], 
#    ['BinomialOption', '-q  '],  
#    ['FastWalshTransform', '-q  '],
#    ['MersenneTwister', '-q  '], 
#    ['ScanLargeArrays', '-q  '], 
#    ['BitonicSort', '-q  '],
    ['FFT', '-q -i 10000'], 
#    ['PrefixSum', '-q  '], 
#    ['SimpleConvolution', '-q  '],
#    ['BlackScholes', '-q  '], 
#    ['FloydWarshall', '-q  '], 
    ['QuasiRandomSequence', '-q -x 4096 -y 4096'],
#    ['SobelFilter', '-q  '], 
#    ['DCT', '-q  '], 
#    ['Histogram', '-q  '], 
#    ['RadixSort', '-q  '],
#    ['URNG', '-q  '], 
#    ['DwtHaar1D', '-q  '], 
    ['MatrixMultiplication', '-q -x 1024 -y 1024 -z 1024'], 
#    ['RecursiveGaussian', '-q  ']
    ]

# Dumb naming convention. Simply looking for config n
numConfigFiles = 19 # 1 control + 18 variants
memConfigPrefix = 'mem_config_'

benchmarkBaseDir = '/Users/Grad/dhullihen/m2s-bench-amdapp-2.5-si/'
logBaseDir = '/Users/Grad/dhullihen/m2s_sim_results/'
memConfigDir = '/Users/Grad/dhullihen/m2s_mem_configs/'

baseSiConfigFile = '/Users/Grad/dhullihen/si-config_ORIGINAL'

m2sCommand = 'm2s --si-sim detailed'

def runBenchmarksWithMemConfig(memConfigFile):
    # Create timestamp for report names
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d__%H_%M')

    returnPath = os.getcwd()

    # Now iterate through the benchmarks
    for benchmark in benchmarkList:
        print '=============================================\n'
        mem_config_name = memConfigFile[memConfigFile.rfind('/')+1:]
        si_report_name = logBaseDir+'si_report__'+benchmark[0]+'__'+mem_config_name+'.txt'
        mem_report_name = logBaseDir+'mem_report__'+benchmark[0]+'__'+mem_config_name+'.txt'

        # cd to the benchmark directory
        os.chdir(benchmarkBaseDir+benchmark[0])

        os.system('pwd')

        # run the benchmark
        fullCommand = m2sCommand + ' --si-config '+baseSiConfigFile+' --mem-config '+memConfigFile+' --si-report '+si_report_name+' --mem-report '+mem_report_name+' '+benchmark[0]+' --load '+benchmark[0]+'_Kernels.bin '+benchmark[1]
        
        print fullCommand+'\n'

        os.system(fullCommand)
        pass
    # cd back to starting directory
    os.chdir(returnPath)
pass

def runCrossProduct():
    memConfigFiles = []
    # Derive (extremely naive) name of files
    # Assumption is I number the config files [0, 1, ..., n]
    # Not very descriptive...
    for i in range(numConfigFiles):
        memConfigFiles.append(memConfigDir+memConfigPrefix+str(i))
        pass
    
    print memConfigFiles
        
    for config in memConfigFiles:
        runBenchmarksWithMemConfig(config)
        print '\n'
        pass
    
pass

if __name__ == "__main__":
    runCrossProduct()
pass
