import json, os, subprocess, sys, ROOT, random, string, pandas
def CompileCpp(blockcode,library=False):
    '''Compiles C++ code via the gInterpreter.

    A python string (the actual code) can be passed or a file name 
    (the file will be opened and read). If a file is passed,
    the C++ code can be compiled
    as a library and if in the future the C++ script is older than the library,
    then the library will be loaded instead.

    @param blockcode (str): Either a block of C++ code or a file name to open.
    @param library (bool, optional): Compiles a library which can be later loaded
            to avoid compilation time. Defaults to False.
    '''


    if not library:
        if '\n' in blockcode or ';' in blockcode: # must be multiline string\
            ROOT.gInterpreter.Declare(blockcode)
        else: # must be file name to compile
            path = ''
            blockcode_str = open(path+blockcode,'r').read()
            ROOT.gInterpreter.Declare(blockcode_str)
    else:
        if '.so' not in blockcode:
            extension = blockcode.split('.')[-1]
            lib_path = blockcode.replace('.'+extension,'_'+extension)+'.so'
        else: 
            lib_path = blockcode
        
        loaded = False
        if os.path.exists(lib_path): # If library exists and is older than the cc file, just load
            mod_time_lib = os.path.getmtime(lib_path)
            mod_time_cc = os.path.getmtime(blockcode)
            if mod_time_lib > mod_time_cc:
                print ('Loading library...')
                ROOT.gSystem.Load(lib_path)
                loaded = True
        
        if not loaded: # Else compile a new lib
            ROOT.gSystem.AddIncludePath(" -I%s "%os.getcwd())
            print ('Compiling library...')
            ROOT.gROOT.ProcessLine(".L "+blockcode+"+")
