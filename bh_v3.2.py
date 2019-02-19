def install(sname):
    fname = ['engin.py','Bh_ipf.txt','custom.py','ipf_check.py','Basin_hopping.py','template.txt','bhv3_readme.txt']
    a=["##############################################################################################                                                                   \n"+              
       "#Basin Hopping version 3.0                                                                                                                                       \n"+
       "#Writen by Moaraj for Python 2.7                                                                                                                           \n"+
       "#Made for the  Hopkins Research Group                                                                                                                                  \n"+
       "#Special thanks to Pjcarr and JRJfeath for all the bugs they found thanks guys ...                                                                                                                                            \n"+
       "#1535+ lines 0_0!                                                                                                                                                 \n"+
       "##############################################################################################                                                                   \n"+
       "#Import Modules                                                                                                                                                  \n"+
       "import os                                                                                                                                                        \n"+
       "import re                                                                                                                                                        \n"+
       "import copy                                                                                                                                                      \n"+
       "import random                                                                                                                                                    \n"+
       "import subprocess, datetime, os, time, signal                                                                                                                    \n"+
       "from random import randint                                                                                                                                       \n"+
       "from time import sleep                                                                                                                                           \n"+
       "from threading import Thread                                                                                                                                     \n"+
       "from math import sqrt,pi,sin,cos,exp                                                                                                                             \n"+
       "from custom import *                                                                                                                                             \n"+
       "##############################################################################################                                                                   \n"+
       "def Basin_hop(ipfname,locat): #Runs the BH routine                                                                                                               \n"+
       "    global bhstart                                                                                                                                               \n"+
       "    bhstart = datetime.datetime.now()                                                                                                                            \n"+
       "    options = ipf_open(ipfname)                                                                                                                                  \n"+
       "    if options ==0:                                                                                                                                              \n"+
       "        return 0 #kill if ipf_open had an error                                                                                                                  \n"+
       "    bh_files=[options[3]] #place to store all bh_files                                                                                                           \n"+
       "    bh_cf=['',options[3],0] #place to store current bh files, ie test and 1b4 \n"+
       "    j = 0 #step number counter                                                                                                                                   \n"+
       "    nrg = [] #energy list                                                                                                                                        \n"+
       "    if options[2] == 'true': #options 2 = restart                                                                                                                \n"+
       "        j,bh_cf,nrg,bh_files = restart_bh(options)\n"+
       "        pass_ = check_gjf(bh_cf[1],options) #check the int gjf and grab con,header nrg term ect \n"+
       "        bh_cf[0],options = extract_geom(bh_cf[1],options)                                                                                                     \n"+
       "        if pass_ == 0:                                                                                                                                       \n"+
       "            savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                              \n"+
       "            print>>savef, '\\n\\nFirst .gjf file failed to be contained in specified radius adjust box size\\n\\n'                                               \n"+
       "            savef.close()\n"+
       "            return 0 \n"+
       "        j+=1                                                                                                                                                     \n"+
       "    else:\n"+
       "        opf = open(options[6],'w')                                                                                                                           \n"+
       "        opf.close()\n"+
       "    kt = 1 #kill timer                                                                                                                                           \n"+
       "    save = [] #save data                                                                                                                                         \n"+
       "    steps = 0 #steps since save                                                                                                                                  \n"+
       "    for i in range(options[0]-j): #for every step                                                                                                                \n"+
       "        steps = steps + 1                                                                                                                                        \n"+
       "        t=0 #count for back steps                                                                                                                                \n"+
       "        if i == 0 and options[2] != 'true': #on the first instance                                                                                               \n"+
       "            pass_ = check_gjf(options[3],options) #check the int gjf and grab con,header nrg term ect                                                            \n"+
       "            if pass_ == 0:                                                                                                                                       \n"+
       "                savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                              \n"+
       "                print>>savef, '\\n\\nFirst .gjf file failed to be contained in specified radius adjust box size\\n\\n'                                               \n"+
       "                savef.close()\n"+
       "                return 0                                                                                                                                         \n"+
       "            options[22]+=1 #another step                                                                                                                         \n"+
       "            a=run_g09(['g09',options[3]],20*60) #run the int file with 20 min wall time                                                                            \n"+
       "            new_fname,options = extract_geom(options[3],options)#distort int gjf, lable isomer2  [:len(int_file[0])-4]+'.log')                                   \n"+
       "            openint = open(options[3][:len(options[3])-4]+'.log','r') #extract the nrg from in file                                                              \n"+
       "            text = openint.read()                                                                                                                                \n"+
       "            text=''.join(text.split()) #remove all white space and lines                                                                                         \n"+
       "            try:                                                                                                                                                 \n"+
       "                hf_nrg=re.findall(r'HF=(.*?)%s'%(options[9]),text,re.DOTALL)                                                                                     \n"+
       "                nrg.append(float(hf_nrg[len(hf_nrg)-1]))                                                                                                         \n"+
       "            except:                                                                                                                                              \n"+
       "                savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                              \n"+
       "                print>>savef, '\\n\\nOriginal file has no energy check %s for errors\\nCheck for the correct energy term default is \\\\\\\\\\n\\n'%(options[3]) \n"+
       "                savef.close()\n"+
       "            openint.close()                                                                                                                                      \n"+
       "            bh_cf[0] = new_fname                                                                                                                                 \n"+
       "            bh_cf[2] = float(hf_nrg[len(hf_nrg)-1]) #global minimum nrg                                                                                          \n"+
       "        elif i < options[0]:                                                                                                                                     \n"+
       "            time_g09(bh_cf[0],options[12]) #run the test file                                                                                                    \n"+
       "            pass_ = 0 # int the check criterias                                                                                                                  \n"+
       "            c = 0 #count the # of g09 calcs this step                                                                                                            \n"+
       "            if options[24] != 'disable':                                                                                                                         \n"+
       "                now = datetime.datetime.now()                                                                                                                    \n"+
       "                nt = (now-bhstart).seconds+(now-bhstart).days*float(24*60*60)                                                                                    \n"+
       "                if nt>kt*options[24][2]: #pass check time                                                                                                        \n"+
       "                    if (i+j) < kt*options[24][0]: #not far enough in steps                                                                                       \n"+
       "                        savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                      \n"+
       "                        print>>savef,'BH job failed to complete requested steps in requested time, job terminated at',datetime.datetime.now()                    \n"+
       "                        savef.close()\n"+
       "                        return 0                                                                                                                                 \n"+
       "                    else:                                                                                                                                        \n"+
       "                        kt+=1                                                                                                                                    \n"+
       "            while pass_ != 1: #one is the pass criteria                                                                                                          \n"+
       "                c +=1                                                                                                                                            \n"+
       "                pass_= nrg_check(bh_cf,nrg,options) #compair vs boltzman                                                                                         \n"+
       "                if pass_ != 1:                                                                                                                                   \n"+
       "                    if c<options[17]: #failed calc                                                                                                               \n"+
       "                        new_fname,options = change_geom(bh_cf[1],options) #redo the distortion                                                                   \n"+
       "                        time_g09(new_fname,options[12]) #rerun the calc                                                                                          \n"+
       "                        if options[24] != 'disable':                                                                                                             \n"+
       "                            now = datetime.datetime.now()                                                                                                        \n"+
       "                            nt = (now-bhstart).seconds+(now-bhstart).days*float(24*60*60)                                                                        \n"+
       "                            if nt>kt*options[24][2]: #pass check time                                                                                            \n"+
       "                                if (i+j) < kt*options[24][0]: #not far enough in steps                                                                           \n"+
       "                                    savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                              \n"+
       "                                    print>>savef,'BH job failed to complete requested steps in requested time, job terminated at',datetime.datetime.now()        \n"+
       "                                    savef.close()\n"+
       "                                    return 0                                                                                                                     \n"+
       "                                else:                                                                                                                            \n"+
       "                                    kt+=1                                                                                                                        \n"+
       "                    else: #failed to many times                                                                                                                  \n"+
       "                        c=0                                                                                                                                      \n"+
       "                        bh_cf[1]=bh_files[len(bh_files)-2-t] #go back 1 plus t                                                                                   \n"+
       "                        t+=1                                                                                                                                     \n"+
       "                        new_fname,options = extract_geom(bh_cf[1],options) #redo the distortion                                                                  \n"+
       "                        time_g09(new_fname,options[12]) #rerun the calc                                                                                          \n"+
       "            f1,options = change_geom(bh_cf[0],options) #produce new distortion                                                                                   \n"+
       "            f2 = bh_cf[0]                                                                                                                                        \n"+
       "            f3 = bh_cf[2]                                                                                                                                        \n"+
       "            bh_cf = [f1,f2,f3] # reset for next step                                                                                                             \n"+
       "            bh_files.append(f2) #save the file to the list                                                                                                       \n"+
       "        #print to save file i current nrg gm nrg and file name last one to pass                                                                                  \n"+
       "        save.append([i+j,nrg[i],bh_cf[2],bh_cf[1]])                                                                                                              \n"+
       "        if steps == options[19]: #save on step                                                                                                                   \n"+
       "            opf = open(options[6],'a')                                                                                                                           \n"+
       "            savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                              \n"+
       "            print>>savef,'Wrote to save file, %d gaussian calls completed so far, %d method runs at '%(options[22],options[25]),datetime.datetime.now()        \n"+
       "            savef.close()\n"+
       "            for s in range(len(save)):                                                                                                                           \n"+
       "                print>>opf, '%d %.8f %.8f %s' %(save[s][0],save[s][1],                                                                                           \n"+
       "                                                save[s][2],save[s][3])                                                                                           \n"+
       "            opf.close()                                                                                                                                          \n"+
       "            steps = 0                                                                                                                                            \n"+
       "            save = []                                                                                                                                            \n"+
       "    opf2 = open(options[5],'w') #write data and unique data                                                                                                      \n"+
       "    opf3 = open(options[5][:len(options[5])-4]+'_Unique.txt','w')                                                                                                \n"+
       "    for i in range(len(nrg)):                                                                                                                                    \n"+
       "        print>>opf2,nrg[i],',',bh_files[i][len('/scratch/%s/'):]                                                                                           \n"%(sname)+
       "    if options[15] == 1: #lol                                                                                                                                    \n"+
       "        print>>opf2,'\\nLike I would make turning off quotes an option\\n'                                                                                         \n"+
       "    quote = print_quote() #grab a quote                                                                                                                          \n"+
       "    print>>opf2,quote                                                                                                                                            \n"+
       "    opf2.close()                                                                                                                                                 \n"+
       "    dir(locat) #make folders                                                                                                                                     \n"+
       "    dir(locat+'/Unique')                                                                                                                                         \n"+
       "    dir(locat+'/Doubles')                                                                                                                                        \n"+
       "    if options[23] != 'Off':                                                                                                                                     \n"+
       "        dir(locat+'/gjfs')                                                                                                                                       \n"+
       "        nheader,nfooter = extract_ngjf(options)                                                                                                                  \n"+
       "    rem(bh_cf[0]) #rm last gjf was not run in g09                                                                                                                \n"+
       "    nrg,nrg2,bh_f2,bh_files2 = nrg_analysis(nrg,bh_cf,bh_files,options) #check nrg vs delta e                                                                    \n"+
       "    rcm_list,geom_tot = log_extract(nrg,bh_files) #get there geoms                                                                                               \n"+
       "    nrg2 = rcm_analysis(nrg2,bh_f2,rcm_list,geom_tot,options)#compair vs some geom criteria                                                                      \n"+
       "    if len(nrg2) !=0: #make sure it found some unique                                                                                                            \n"+
       "        for i in range(len(nrg2)):                                                                                                                               \n"+
       "            if nrg2[i] !=4:                                                                                                                                      \n"+
       "                print>>opf3,nrg2[i],',',bh_f2[i][len('/scratch/%s/'):]                                                                                     \n"%(sname)+
       "        for i in range(len(nrg2)):                                                                                                                               \n"+
       "            if nrg2[i] != 4:                                                                                                                                     \n"+
       "                if options[23] != 'Off':                                                                                                                         \n"+
       "                    try:                                                                                                                                         \n"+
       "                        ngjf = mkgjfs(geom_tot[i],bh_f2[i],nheader,nfooter)                                                                                      \n"+
       "                        move_f(ngjf,locat+'/gjfs')                                                                                                               \n"+
       "                    except:                                                                                                                                      \n"+
       "                        pass                                                                                                                                     \n"+
       "                move_f(bh_f2[i],locat+'/Unique')                                                                                                                 \n"+
       "                move_f(bh_f2[i][:len(bh_f2[i])-4]+'.log',locat+'/Unique')                                                                                        \n"+
       "            else:                                                                                                                                                \n"+
       "                bh_files2.append(bh_f2[i])                                                                                                                       \n"+
       "    if options[15] == 1:                                                                                                                                         \n"+
       "        print>>opf3,'\\nLike I would make turning off quotes an option\\n'                                                                                         \n"+
       "    print>>opf3,quote                                                                                                                                            \n"+
       "    opf3.close()                                                                                                                                                 \n"+
       "    for i in range(len(bh_files2)): #move to doubles                                                                                                             \n"+
       "            move_f(bh_files2[i],locat+'/Doubles')                                                                                                                \n"+
       "            move_f(bh_files2[i][:len(bh_files2[i])-4]+'.log',locat+'/Doubles')                                                                                   \n"+
       #"    move_f('/scratch/%s/bh/Doubles/6Cl2mq_1w_1.gjf','/scratch/%s')                                                                                   \n"%(sname,sname)+
       "    now = datetime.datetime.now()                                                                                                                                \n"+
       "    savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                              \n"+
       "    print>>savef,'\\nBH routine finsihed with %d g09 calcs'%(options[22])                                                                                           \n"+
       "    print>>savef,'BH Job Completed succesfully in',(now-bhstart)                                                                                                 \n"+
       "    savef.close()\n"+
       "##############################################################################################                                                                   \n"+
       "def ipf_open(ipfname):#Generate options and read the IPF                                                                                                         \n"+
       "    ipf_open = open(ipfname,'r') #everything that we look for                                                                                                    \n"+
       "    ipf = ipf_open.read() #open and find                                                                                                                         \n"+
       "    int_file = re.findall(r'int_file:(.*?)-end',ipf,re.DOTALL)                                                                                                   \n"+
       "    steps = re.findall(r'steps =(.*?)-end',ipf,re.DOTALL)                                                                                                        \n"+
       "    jwt = re.findall(r'job wall time =(.*?)-end',ipf,re.DOTALL)                                                                                                  \n"+
       "    logc = re.findall(r'check logs =(.*?)-end',ipf,re.DOTALL)                                                                                                  \n"+
       "    func = re.findall(r'method =(.*?)-end',ipf,re.DOTALL)                                                                                                        \n"+
       "    restart = re.findall(r'restart =(.*?)-end',ipf,re.DOTALL)                                                                                                    \n"+
       "    kill = re.findall(r'kill =(.*?)-end',ipf,re.DOTALL)                                                                                                          \n"+
       "    toq = re.findall(r'turn of quotes =(.*?)-end',ipf,re.DOTALL)                                                                                                 \n"+
       "    box_size = re.findall(r'box size =(.*?)-end',ipf,re.DOTALL)                                                                                                  \n"+
       "    mkgjf = re.findall(r'make gjf =(.*?)-end',ipf,re.DOTALL)                                                                                                     \n"+
       "    save_file = re.findall(r'save as:(.*?)-end',ipf,re.DOTALL)                                                                                                   \n"+
       "    chp_file = re.findall(r'sav_file:(.*?)-end',ipf,re.DOTALL)                                                                                                   \n"+
       "    con = re.findall(r'connectivity:(.*?)-end',ipf,re.DOTALL)                                                                                                    \n"+
       "    temp = re.findall(r'temp =(.*?)-end',ipf,re.DOTALL)                                                                                                          \n"+
       "    nrg_term = re.findall(r'nrg term =(.*?)-end',ipf,re.DOTALL)                                                                                                  \n"+
       "    header = re.findall(r'header =(.*?)-end',ipf,re.DOTALL)                                                                                                      \n"+
       "    custom = re.findall(r'custom check =(.*?)-end',ipf,re.DOTALL)                                                                                                \n"+
       "    de = re.findall(r'nrg var =(.*?)-end',ipf,re.DOTALL)                                                                                                         \n"+
       "    dg = re.findall(r'geom var =(.*?)-end',ipf,re.DOTALL)                                                                                                        \n"+
       "    btrace = re.findall(r'back step =(.*?)-end',ipf,re.DOTALL)                                                                                                   \n"+
       "    cdist = re.findall(r'shortest bond =(.*?)-end',ipf,re.DOTALL)                                                                                                \n"+
       "    bhtrys = re.findall(r'number of tries =(.*?)-end',ipf,re.DOTALL)                                                                                             \n"+
       "    ss = re.findall(r'save on step =(.*?)-end',ipf,re.DOTALL)                                                                                                    \n"+
       "    ipf_open.close() #check for syntax                                                                                                                           \n"+
       "    savef = open(int_file[0][:len(int_file[0])-4]+'calc_summary.txt','a')                                                                                        \n"+
       "    if len(int_file) == 0:                                                                                                                                       \n"+
       "        print>>savef, '\\n\\nInvalid syntax with inital file'                                                                                                      \n"+
       "    if len(steps) == 0:                                                                                                                                          \n"+
       "        print>>savef, '\\n\\nInvalid syntax with steps ='                                                                                                          \n"+
       "    if len(jwt) == 0:                                                                                                                                            \n"+
       "        jwt = 0                                                                                                                                                  \n"+
       "    else:                                                                                                                                                        \n"+
       "        try:                                                                                                                                                     \n"+
       "            jwt = float(jwt[0])                                                                                                                                  \n"+
       "        except:                                                                                                                                                  \n"+
       "            jwt = 0                                                                                                                                              \n"+
       "            print>>savef, '\\n\\nInvalid input for job wall time feature disabled'                                                                                 \n"+
       "    if len(ss) == 0:                                                                                                                                             \n"+
       "        ss = 100                                                                                                                                                 \n"+
       "    else:                                                                                                                                                        \n"+
       "        try:                                                                                                                                                     \n"+
       "            ss = int(ss[0])                                                                                                                                      \n"+
       "        except:                                                                                                                                                  \n"+
       "            ss = 100                                                                                                                                             \n"+
       "            print>>savef, '\\n\\nInvalid input for save on step using default (100)'                                                                               \n"+
       "    if len(bhtrys) == 0:                                                                                                                                         \n"+
       "        bhtrys = 10000                                                                                                                                           \n"+
       "    else:                                                                                                                                                        \n"+
       "        try:                                                                                                                                                     \n"+
       "            bhtrys = int(bhtrys[0])                                                                                                                              \n"+
       "        except:                                                                                                                                                  \n"+
       "            bhtrys = 10000                                                                                                                                       \n"+
       "            print>>savef, '\\n\\nInvalid input for number of tries using default settings (10000)'                                                                 \n"+
       "    if len(btrace) == 0:                                                                                                                                         \n"+
       "        btrace = 60                                                                                                                                              \n"+
       "    else:                                                                                                                                                        \n"+
       "        try:                                                                                                                                                     \n"+
       "            btrace = int(btrace[0])                                                                                                                              \n"+
       "        except:                                                                                                                                                  \n"+
       "            btrace = 60                                                                                                                                          \n"+
       "            print>>savef, '\\n\\nInvalid input for back step using default setting (20)'                                                                           \n"+
       "    if len(cdist) == 0:                                                                                                                                          \n"+
       "        cdist = 0.7                                                                                                                                              \n"+
       "    else:                                                                                                                                                        \n"+
       "        try:                                                                                                                                                     \n"+
       "            cdist = float(cdist[0])                                                                                                                              \n"+
       "        except:                                                                                                                                                  \n"+
       "            cdist = 0.7                                                                                                                                          \n"+
       "            print>>savef, '\\n\\nInvalid input for shortest bond using default setting (0.7A)'                                                                     \n"+
       "    if len(func) == 0:                                                                                                                                           \n"+
       "        print>>savef, '\\n\\nNo method found ='                                                                                                                    \n"+
       "        return 0                                                                                                                                                 \n"+
       "    if len(box_size) == 0:                                                                                                                                       \n"+
       "        print>>savef, '\\n\\nInvalid syntax with box size'                                                                                                         \n"+
       "        return 0                                                                                                                                                 \n"+
       "    if len(save_file) == 0:                                                                                                                                      \n"+
       "        print>>savef, '\\n\\nInvalid syntax with data file'                                                                                                        \n"+
       "        return 0                                                                                                                                                 \n"+
       "    if len(chp_file) == 0:                                                                                                                                       \n"+
       "        print>>savef, '\\n\\nInvalid syntax with .sav file'                                                                                                        \n"+
       "        return 0                                                                                                                                                 \n"+
       "    if len(mkgjf) == 0:                                                                                                                                          \n"+
       "        mkgjf = 'Off'                                                                                                                                            \n"+
       "    else:                                                                                                                                                        \n"+
       "        mkgjf=mkgjf[0].replace(' ','')                                                                                                                           \n"+
       "    if len(con) == 0:                                                                                                                                            \n"+
       "        con='default'                                                                                                                                            \n"+
       "    else:                                                                                                                                                        \n"+
       "        con = con[0]                                                                                                                                             \n"+
       "    if len(temp) == 0:                                                                                                                                           \n"+
       "        print>>savef, '\\n\\nInvalid syntax with temperature'                                                                                                      \n"+
       "        return 0                                                                                                                                                 \n"+
       "    if len(nrg_term) == 0:                                                                                                                                       \n"+
       "        nrg_term = '\\\\\\\\'                                                                                                                                        \n"+
       "    else:                                                                                                                                                        \n"+
       "        nrg_term = nrg_term[0].replace(' ','')                                                                                                                   \n"+
       "    if len(header) == 0:                                                                                                                                         \n"+
       "        header = 'default'                                                                                                                                       \n"+
       "    else:                                                                                                                                                        \n"+
       "        header = header[0]                                                                                                                                       \n"+
       "    if len(de) == 0:                                                                                                                                             \n"+
       "        print>>savef, '\\n\\nInvalid syntax with energy variance'                                                                                                  \n"+
       "        return 0                                                                                                                                                 \n"+
       "    if len(dg) == 0:                                                                                                                                             \n"+
       "        print>>savef, '\\n\\nInvalid syntax with geometry varriance'                                                                                               \n"+
       "        return 0                                                                                                                                                 \n"+
       "    if len(toq) == 0:                                                                                                                                            \n"+
       "        toq = 0                                                                                                                                                  \n"+
       "    else:                                                                                                                                                        \n"+
       "        if toq[0].replace(' ','') == 'yes':                                                                                                                      \n"+
       "            toq =1                                                                                                                                               \n"+
       "        else:                                                                                                                                                    \n"+
       "            toq = 0                                                                                                                                              \n"+
       "    try:                                                                                                                                                         \n"+
       "        steps = int(steps[0])                                                                                                                                    \n"+
       "    except:                                                                                                                                                      \n"+
       "        print>>savef, 'Steps must be an integer'                                                                                                                 \n"+
       "        return 0                                                                                                                                                 \n"+
       "    if len(kill) == 0:                                                                                                                                           \n"+
       "        kill = 'disable'                                                                                                                                         \n"+
       "    else:                                                                                                                                                        \n"+
       "        try:                                                                                                                                                     \n"+
       "            kill=kill[0].split()                                                                                                                                 \n"+
       "            time = 0.0                                                                                                                                           \n"+
       "            kill[0]=kill[0].replace('-',' ')                                                                                                                     \n"+
       "            kill[0]=kill[0].split()                                                                                                                              \n"+
       "            get2 =float(kill[0][0])                                                                                                                              \n"+
       "            by = float(kill[0][1])                                                                                                                               \n"+
       "            for i in range(len(kill)-1):                                                                                                                         \n"+
       "                kill[i+1]=kill[i+1].replace('-',' ')                                                                                                             \n"+
       "                kill[i+1]=kill[i+1].split()                                                                                                                      \n"+
       "                if kill[i+1][1] == 'days':                                                                                                                       \n"+
       "                    time+= float(kill[i+1][0])*24*60*60                                                                                                          \n"+
       "                if kill[i+1][1] == 'hours':                                                                                                                      \n"+
       "                    time+= float(kill[i+1][0])*60*60                                                                                                             \n"+
       "                if kill[i+1][1] == 'min':                                                                                                                        \n"+
       "                    time+= float(kill[i+1][0])*60                                                                                                                \n"+
       "                if kill[i+1][1] == 'sec':                                                                                                                        \n"+
       "                    time+= float(kill[i+1][0])                                                                                                                   \n"+
       "            rtime = time*float(by)/100.0                                                                                                                         \n"+
       "            rsteps = int(steps*float(get2)/100.0)                                                                                                                \n"+
       "            kill = [rsteps,time,rtime]                                                                                                                           \n"+
       "        except:                                                                                                                                                  \n"+
       "            kill = 'disable'                                                                                                                                     \n"+
       "            print>>savef, '\\n\\nInvalid input for kill, feature disabled'                                                                                         \n"+
       "    try:                                                                                                                                                         \n"+
       "        box_size = float(box_size[0])                                                                                                                            \n"+
       "    except:                                                                                                                                                      \n"+
       "        print>>savef, 'Box size must be a number'                                                                                                                \n"+
       "        return 0                                                                                                                                                 \n"+
       "    try:                                                                                                                                                         \n"+
       "        dg = float(dg[0])                                                                                                                                        \n"+
       "    except:                                                                                                                                                      \n"+
       "        print>>savef, 'Geometry Variance must be a number'                                                                                                       \n"+
       "        return 0                                                                                                                                                 \n"+
       "    try:                                                                                                                                                         \n"+
       "        de = float(de[0])                                                                                                                                        \n"+
       "    except:                                                                                                                                                      \n"+
       "        print>>savef, 'Energy Variance must be a number'                                                                                                         \n"+
       "        return 0                                                                                                                                                 \n"+
       "    int_file = int_file[0].replace(' ','')                                                                                                                       \n"+
       "    chp_file = chp_file[0].replace(' ','')                                                                                                                       \n"+
       "    save_file = save_file[0]                                                                                                                                     \n"+
       "    try:                                                                                                                                                         \n"+
       "        temp = float(temp[0])                                                                                                                                    \n"+
       "    except:                                                                                                                                                      \n"+
       "        print>>savef, 'Temperature must be a number'                                                                                                             \n"+
       "        return 0                                                                                                                                                 \n"+
       "    func = func[0].split() #set up method for random move                                                                                                        \n"+
       "    if func[0] == 'dihedral_rot':                                                                                                                                \n"+
       "        try:                                                                                                                                                     \n"+
       "            for i in range(len(func)-2):                                                                                                                         \n"+
       "                func[i+2] = func[i+2].replace(',',' ')                                                                                                           \n"+
       "                func[i+2] = func[i+2].replace(')',' ')                                                                                                           \n"+
       "                func[i+2] = func[i+2].replace('(',' ')                                                                                                           \n"+
       "                func[i+2] = func[i+2].replace('-',' ')                                                                                                           \n"+
       "                func[i+2] = func[i+2].split()                                                                                                                    \n"+
       "                for j in range(len(func[i+2])):                                                                                                                  \n"+
       "                    func[i+2][j] = int(func[i+2][j])-1                                                                                                           \n"+
       "        except:                                                                                                                                                  \n"+
       "            print>>savef, '\\n\\nInvalid syntax for dihedral_rot'                                                                                                  \n"+
       "            return 0                                                                                                                                             \n"+
       "    elif func[0] == 'gen_move':                                                                                                                                  \n"+
       "        try:                                                                                                                                                     \n"+
       "            rot = []                                                                                                                                             \n"+
       "            di = []                                                                                                                                              \n"+
       "            for i in range(len(func)-4):                                                                                                                         \n"+
       "                if func[i+4][len(func[i+4])-1:] == 'r':                                                                                                          \n"+
       "                    func[i+4] = func[i+4].replace('r','')                                                                                                        \n"+
       "                    func[i+4] = func[i+4].replace(',',' ')                                                                                                       \n"+
       "                    func[i+4] = func[i+4].replace(')',' ')                                                                                                       \n"+
       "                    func[i+4] = func[i+4].replace('(',' ')                                                                                                       \n"+
       "                    func[i+4] = func[i+4].split()                                                                                                                \n"+
       "                    for j in range(len(func[i+4])):                                                                                                              \n"+
       "                        func[i+4][j] = int(func[i+4][j]) - 1                                                                                                     \n"+
       "                    rot.append(func[i+4])                                                                                                                        \n"+
       "                elif '-' in func[i+4]:                                                                                                                           \n"+
       "                    func[i+4] = func[i+4].replace(',',' ')                                                                                                       \n"+
       "                    func[i+4] = func[i+4].replace(')',' ')                                                                                                       \n"+
       "                    func[i+4] = func[i+4].replace('(',' ')                                                                                                       \n"+
       "                    func[i+4] = func[i+4].replace('-',' ')                                                                                                       \n"+
       "                    func[i+4] = func[i+4].split()                                                                                                                \n"+
       "                    for j in range(len(func[i+4])):                                                                                                              \n"+
       "                        func[i+4][j] = int(func[i+4][j])-1                                                                                                       \n"+
       "                    di.append(func[i+4])                                                                                                                         \n"+
       "                else:                                                                                                                                            \n"+
       "                    print>>savef,'invalid syntax for gen_move'                                                                                                   \n"+
       "                    return 0                                                                                                                                     \n"+
       "            name = func[0]                                                                                                                                       \n"+
       "            di_theta = float(func[1])                                                                                                                            \n"+
       "            theta = float(func[2])                                                                                                                               \n"+
       "            tran = float(func[3])                                                                                                                                \n"+
       "            func = [name,di_theta,theta,tran,rot,di]                                                                                                             \n"+
       "        except:                                                                                                                                                  \n"+
       "            print>>savef, '\\n\\nInvalid syntax for gen_move'                                                                                                      \n"+
       "            return 0                                                                                                                                             \n"+
       "    elif func[0] == 'gen_rot':                                                                                                                                   \n"+
       "        try:                                                                                                                                                     \n"+
       "            rot = []                                                                                                                                             \n"+
       "            for i in range(len(func)-3):                                                                                                                         \n"+
       "                func[i+3] = func[i+3].replace(',',' ')                                                                                                           \n"+
       "                func[i+3] = func[i+3].replace(')',' ')                                                                                                           \n"+
       "                func[i+3] = func[i+3].replace('(',' ')                                                                                                           \n"+
       "                func[i+3] = func[i+3].split()                                                                                                                    \n"+
       "                for j in range(len(func[i+3])):                                                                                                                  \n"+
       "                    func[i+3][j] = int(func[i+3][j])-1                                                                                                           \n"+
       "                rot.append(func[i+3])                                                                                                                            \n"+
       "            n = func[0]                                                                                                                                          \n"+
       "            theta = float(func[1])                                                                                                                               \n"+
       "            tran = float(func[2])                                                                                                                                \n"+
       "            func = [n,theta,tran,rot]                                                                                                                            \n"+
       "        except:                                                                                                                                                  \n"+
       "            print>>savef, '\\n\\nInvalid syntax for gen_rot'                                                                                                       \n"+
       "            return 0                                                                                                                                             \n"+
       "    elif func[0] == 'rand_rot':                                                                                                                                  \n"+
       "        try:                                                                                                                                                     \n"+
       "            if len(func)<6:                                                                                                                                      \n"+
       "                a = int(func[2])                                                                                                                                 \n"+
       "                b = int(func[1])                                                                                                                                 \n"+
       "                c = float(func[3])                                                                                                                               \n"+
       "                d = float(func[4])                                                                                                                               \n"+
       "                n = func[0]                                                                                                                                      \n"+
       "                func = [n,a,b,c,d]                                                                                                                               \n"+
       "            else:                                                                                                                                                \n"+
       "                print>>savef, '\\nTo many parameters found in method'                                                                                             \n"+
       "                return 0                                                                                                                                         \n"+
       "        except:                                                                                                                                                  \n"+
       "            print>>savef, 'Invald syntax for method'                                                                                                             \n"+
       "            return 0                                                                                                                                             \n"+
       "    elif func[0] == 'rand_trans':                                                                                                                                \n"+
       "        try:                                                                                                                                                     \n"+
       "            if len(func)<5:                                                                                                                                      \n"+
       "                a = int(func[2])                                                                                                                                 \n"+
       "                b = int(func[1])                                                                                                                                 \n"+
       "                c = float(func[3])                                                                                                                               \n"+
       "                n = func[0]                                                                                                                                      \n"+
       "                func = [n,a,b,c]                                                                                                                                 \n"+
       "            else:                                                                                                                                                \n"+
       "                print>>savef, '\\nTo many parameters found in method'                                                                                             \n"+
       "                return 0                                                                                                                                         \n"+
       "        except:                                                                                                                                                  \n"+
       "            print>>savef, 'Invald syntax for method'                                                                                                             \n"+
       "            return 0                                                                                                                                             \n"+
       "    elif func[0] == 'ulti_move':                                                                                                                                 \n"+
       "        try:                                                                                                                                                     \n"+
       "            tran = []                                                                                                                                            \n"+
       "            rot = []                                                                                                                                             \n"+
       "            di = []                                                                                                                                              \n"+
       "            for i in range(len(func)-1):                                                                                                                         \n"+
       "                if func[i+1][len(func[i+1])-1:] == 'r':                                                                                                          \n"+
       "                    func[i+1] = func[i+1].replace('r','')                                                                                                        \n"+
       "                    func[i+1] = func[i+1].replace(',',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].replace(')',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].replace('(',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].split()                                                                                                                \n"+
       "                    for j in range(len(func[i+1])):                                                                                                              \n"+
       "                        if j >1:                                                                                                                                 \n"+
       "                            func[i+1][j] = int(func[i+1][j]) - 1                                                                                                 \n"+
       "                        else:                                                                                                                                    \n"+
       "                            func[i+1][j] = float(func[i+1][j])                                                                                                   \n"+
       "                    rot.append(func[i+1])                                                                                                                        \n"+
       "                elif '-' in func[i+1]:                                                                                                                           \n"+
       "                    func[i+1] = func[i+1].replace(',',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].replace(')',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].replace('(',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].replace('-',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].split()                                                                                                                \n"+
       "                    for j in range(len(func[i+1])):                                                                                                              \n"+
       "                        if j<len(func[i+1])-1:                                                                                                                   \n"+
       "                            func[i+1][j] = int(func[i+1][j])-1                                                                                                   \n"+
       "                        else:                                                                                                                                    \n"+
       "                            func[i+1][j] = float(func[i+1][j])                                                                                                   \n"+
       "                    di.append(func[i+1])                                                                                                                         \n"+
       "                elif func[i+1][len(func[i+1])-1:] == 't':                                                                                                        \n"+
       "                    func[i+1] = func[i+1].replace('t','')                                                                                                        \n"+
       "                    func[i+1] = func[i+1].replace(',',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].replace(')',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].replace('(',' ')                                                                                                       \n"+
       "                    func[i+1] = func[i+1].split()                                                                                                                \n"+
       "                    for j in range(len(func[i+1])):                                                                                                              \n"+
       "                        if j >0:                                                                                                                                 \n"+
       "                            func[i+1][j] = int(func[i+1][j]) - 1                                                                                                 \n"+
       "                        else:                                                                                                                                    \n"+
       "                            func[i+1][j] = float(func[i+1][j])                                                                                                   \n"+
       "                    tran.append(func[i+1])                                                                                                                       \n"+
       "                else:                                                                                                                                            \n"+
       "                    print>>savef,'invalid syntax for ulti_move'                                                                                                  \n"+
       "                    return 0                                                                                                                                     \n"+
       "            name = func[0]                                                                                                                                       \n"+
       "            func = [name,di,rot,tran]                                                                                                                            \n"+
       "        except:                                                                                                                                                  \n"+
       "            print>>savef, '\\n\\nInvalid syntax for gen_move'                                                                                                      \n"+
       "            return 0                                                                                                                                             \n"+
       "    if len(restart) == 0:                                                                                                                                        \n"+
       "        restart = 'false'                                                                                                                                        \n"+
       "    else:                                                                                                                                                        \n"+
       "        if restart[0].replace(' ','')=='yes':                                                                                                                    \n"+
       "            restart = 'true'                                                                                                                                     \n"+
       "        elif restart[0].replace(' ','')=='no':                                                                                                                   \n"+
       "            restart = 'false'                                                                                                                                    \n"+
       "        else:                                                                                                                                                    \n"+
       "            restart = 'false'                                                                                                                                    \n"+
       "            print>>savef, '\\n\\nInvalid restart syntax using default setting: false'                                                                              \n"+
       "    if len(logc) == 0:                                                                                                                                        \n"+
       "        logc = 'false'                                                                                                                                        \n"+
       "    else:                                                                                                                                                        \n"+
       "        if logc[0].replace(' ','')=='yes':                                                                                                                    \n"+
       "            logc = 'true'                                                                                                                                     \n"+
       "        elif logc[0].replace(' ','')=='no':                                                                                                                   \n"+
       "            logc = 'false'                                                                                                                                    \n"+
       "        else:                                                                                                                                                    \n"+
       "            logc = 'false'                                                                                                                                    \n"+
       "            print>>savef, '\\n\\nInvalid check logs syntax using default setting: false' \n"+      
       "    if len(custom) == 0:                                                                                                                                         \n"+
       "        custom = 0                                                                                                                                               \n"+
       "    else:                                                                                                                                                        \n"+
       "        if custom[0].replace(' ','') =='yes':                                                                                                                    \n"+
       "            custom = 1                                                                                                                                           \n"+
       "        else:                                                                                                                                                    \n"+
       "            custom = 0                                                                                                                                           \n"+
       "    ipf_open.close()                                                                                                                                             \n"+
       "    geom =[]                                                                                                                                                     \n"+
       "    charg_spin=[]                                                                                                                                                \n"+
       "    options = [steps,func,restart,int_file,box_size,save_file,chp_file,con, #compile options list                                                                \n"+
       "               temp,nrg_term,header,custom,jwt,de,dg,toq,cdist,btrace,bhtrys,ss,geom,charg_spin,0,mkgjf,kill,0,logc]                                                    \n"+
       "    print>>savef,'\\n***************************************\\nInitiating BH Routine at ',bhstart                                                                  \n"+
       "    print>>savef,'\\nBH options are read as follows'                                                                                                              \n"+
       "    print>>savef,'Number of steps',options[0]                                                                                                                    \n"+
       "    print>>savef,'Temperature',options[8]                                                                                                                        \n"+
       "    print>>savef,'Method used',options[1]                                                                                                                        \n"+
       "    print>>savef,'Box Size',options[4]                                                                                                                           \n"+
       "    print>>savef,'Initial file',options[3]                                                                                                                       \n"+
       "    print>>savef,'Data File',options[5]                                                                                                                          \n"+
       "    print>>savef,'Save File',options[6]                                                                                                                          \n"+
       "    print>>savef,'Restart',options[2]                                                                                                                            \n"+
       "    print>>savef,'Connectivity',options[7]                                                                                                                       \n"+
       "    print>>savef,'Header',options[10]                                                                                                                            \n"+
       "    print>>savef,'Custom Check',options[11]                                                                                                                      \n"+
       "    print>>savef,'Energy Term',options[9]                                                                                                                        \n"+
       "    print>>savef,'Job wall time',options[12]                                                                                                                     \n"+
       "    print>>savef,'Energy Variance',options[13]                                                                                                                   \n"+
       "    print>>savef,'Geometry Variance',options[14]                                                                                                                 \n"+
       "    print>>savef,'Turn off Quotes',options[15]                                                                                                                   \n"+
       "    print>>savef,'Shortest acceptable bond length',options[16]                                                                                                   \n"+
       "    print>>savef,'Back step after this many tries',options[17]                                                                                                   \n"+
       "    print>>savef,'Number of method tries',options[18]                                                                                                            \n"+
       "    print>>savef,'Save on step',options[19] #things for calc_summary                                                                                             \n"+
       "    print>>savef,'Make gjf from unique',options[23]                                                                                                              \n"+
       "    print>>savef,'Kill filles if progression is not far enough. ',options[24]                                                                                    \n"+
       "    savef.close()\n"+
       "    savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                              \n"+
       "    return options                                                                                                                                               \n"+
       "##############################################################################################                                                                   \n"+
       "def restart_bh(options): #The restart function                                                                                                                   \n"+
       "    openfile = open(options[6],'r')                                                                                                                              \n"+
       "    text = openfile.read() #grab data                                                                                                                            \n"+
       "    lines = text.split('\\n')                                                                                                                                     \n"+
       "    nrg = []                                                                                                                                                     \n"+
       "    bh_cf = []                                                                                                                                                   \n"+
       "    bh_files = []                                                                                                                                                \n"+
       "    for i in range(len(lines)):                                                                                                                                  \n"+
       "        line = lines[i].split()                                                                                                                                  \n"+
       "        if len(line) == 4:                                                                                                                                       \n"+
       "            nrg.append(float(line[1]))                                                                                                                           \n"+
       "            bh_files.append(line[3].replace(' ',''))                                                                                                             \n"+
       "        if i == len(lines)-1:                                                                                                                                    \n"+
       "            if len(line) ==4:                                                                                                                                    \n"+
       "                j = int(line[0].replace(' ','')) #i                                                                                                              \n"+
       "                gm = float(line[2])                                                                                                                              \n"+
       "                fname = line[3].replace(' ','')                                                                                                                  \n"+
       "            else:                                                                                                                                                \n"+
       "                line = lines[len(nrg)-1].split()                                                                                                                 \n"+
       "                j = int(line[0].replace(' ','')) #i                                                                                                              \n"+
       "                gm = float(line[2].replace(' ',''))                                                                                                              \n"+
       "                fname = line[3].replace(' ','')                                                                                                                  \n"+
       "    bh_cf = ['null',fname,gm]                                                                                                                                    \n"+
       "    return j,bh_cf,nrg,bh_files                                                                                                                                  \n"+
       "##############################################################################################                \n"+                                                   
       "def nrg_check(bh_cf,nrg,options): #montecarlo part                                                            \n"+                                                   
       "    options[22]+=1                                                                                            \n"+                                                   
       "    try:                                                                                                      \n"+                                                   
       "        tf_open = open(bh_cf[0][:len(bh_cf[0])-4]+'.log','r') #open the file to check                         \n"+                                                   
       "        text = tf_open.read()                                                                                 \n"+                                                   
       "        text=''.join(text.split()) #remove all white space lines ect                                          \n"+                                                   
       "        hf_output_tf=re.findall(r'HF=(.*?)%s'%(options[9]),text,re.DOTALL)                                    \n"+                                                   
       "        tf_open.close() #always close the file bc python int_grabage_comp is garbage                          \n"+
       "        if options[26] == 'true':                                                                             \n"+
       "            pass_ = log_geom(bh_cf[0][:len(bh_cf[0])-4]+'.log',options)                                       \n"+
       "            if pass_ == 0:                                                                                    \n"+
       "                hf_output_tf=[]                                                                               \n"+
       "            else:                                                                                             \n"+
       "               pass_ == 0                                                                                     \n"+
       "    except:                                                                                                   \n"+                                                   
       "        hf_output_tf=[]                                                                                       \n"+                                                   
       "                                                                                                              \n"+                                                   
       "    if len(hf_output_tf) == 0: #_calculation failed toss                                                      \n"+                                                    
       "        return 0                                                                                              \n"+                                                   
       "    else:                                                                                                     \n"+                                                   
       "        pass_ = 0                                                                                             \n"+                                                   
       "        nrg_dif = float(hf_output_tf[len(hf_output_tf)-1])-bh_cf[2]                                           \n"+                                                   
       "        if nrg_dif <0: # implies that test was lower in nrg than one other                                    \n"+                                                   
       "            pass_ = 1                                                                                         \n"+                                                   
       "            bh_cf[2] = float(hf_output_tf[len(hf_output_tf)-1])                                               \n"+                                                   
       "            nrg.append(float(hf_output_tf[len(hf_output_tf)-1]))                                              \n"+                                                   
       "            return 1 #passed                                                                                  \n"+                                                   
       "        else: #check global minimum (bh_cf[2])...                                                             \n"+                                                   
       "            if exp(-nrg_dif/(0.00000316681*options[8])) > random.random():  #0.0023448964553751833            \n"+                                                                 
       "                nrg.append(float(hf_output_tf[len(hf_output_tf)-1]))                                          \n"+                                                   
       "                return 1 # still passed                                                                       \n"+                                                   
       "            else:                                                                                             \n"+                                                   
       "                return 0 #failed                                                                              \n"+
       "##############################################################################################                                                                   \n"+
       "def extract_ngjf(options): #readeds the template file                                                                                                            \n"+
       "    fname=open(options[23],'r')                                                                                                                                  \n"+
       "    text=fname.read()                                                                                                                                            \n"+
       "    fname.close()                                                                                                                                                \n"+
       "    header = ''                                                                                                                                                  \n"+
       "    footer = ''                                                                                                                                                  \n"+
       "    lines=text.split('\\n')                                                                                                                                       \n"+
       "    switch = 0                                                                                                                                                   \n"+
       "    skip =0                                                                                                                                                      \n"+
       "    for i in range(len(lines)):                                                                                                                                  \n"+
       "        if 'Geom' in lines[i]:                                                                               \n"+
       "            switch = 1                                                                                                                                           \n"+
       "            skip = 1                                                                                                                                             \n"+
       "        if switch != 1:                                                                                                                                          \n"+
       "            header +=lines[i]+'\\n'                                                                                                                               \n"+
       "        else:                                                                                                                                                    \n"+
       "            if skip != 1:                                                                                                                                        \n"+
       "                footer +=lines[i] + '\\n'                                                                                                                         \n"+
       "            else:                                                                                                                                                \n"+
       "                skip =0                                                                                                                                          \n"+
       "    header = header[:len(header)-1]                                                                                                                              \n"+
       "    return header,footer                                                                                                                                         \n"+
       "##############################################################################################                                                                   \n"+
       "def mkgjfs(geom,fname,nheader,nfooter):#makes gjf with geom and such                                                                                             \n"+
       "    newname = fname[:len(fname)-4]+'_DFT.gjf'                                                                                                                    \n"+
       "    opf = open(newname,'w')                                                                                                                                      \n"+
       "    print>>opf,nheader.replace('_name_',newname[len('/scratch/%s/'):len(newname)-4])              \n"%(sname)+
       "    for i in range(len(geom)):                                                                                                                                   \n"+
       "        print>>opf,'%s        %.6f    %.6f     %.6f'%(geom[i][0],geom[i][1],geom[i][2],geom[i][3])                                                               \n"+
       "    print>>opf,nfooter                                                                                                                                           \n"+
       "    opf.close()                                                                                                                                                  \n"+
       "    return newname                                                                                                                                               \n"+
       "##############################################################################################                                                                   \n"+
       "def check_gjf(filename,options): #Check int gjf to make sure in box and grab some data                                                                           \n"+
       "    if filename[len(filename)-4:] == '.gjf':                                                                                                                     \n"+
       "        #Extract geometries from a gjf                                                                                                                           \n"+
       "        geom=[] #empty list to keep geoms                                                                                                                        \n"+
       "        footer = [] #place ot keep the connectivity                                                                                                              \n"+
       "        charg_spin=[] # charge and spin                                                                                                                          \n"+
       "        openfile = open(filename,'r') #Open file                                                                                                                 \n"+
       "        text=openfile.read() # Make file readable                                                                                                                \n"+
       "        geomtext = text.split('\\n') # split the text by lines                                                                                                    \n"+
       "        openfile.close() # close the file                                                                                                                        \n"+
       "        con =''                                                                                                                                                  \n"+
       "        header=''                                                                                                                                                \n"+
       "        savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                              \n"+
       "        for i in range(len(geomtext)): #read the lines                                                                                                           \n"+
       "            line=geomtext[i].split() #split the line                                                                                                             \n"+
       "            is_line = 0 #switch                                                                                                                                  \n"+
       "            is_footer = 0                                                                                                                                        \n"+
       "            if i < 5:                                                                                                                                            \n"+
       "                if i == 1:                                                                                                                                       \n"+
       "                    for j in range(len(line)):                                                                                                                   \n"+
       "                        header +=line[j]                                                                                                                         \n"+
       "                        header +=' '                                                                                                                             \n"+
       "                pass #skip the title block                                                                                                                       \n"+
       "            elif i == 5:                                                                                                                                         \n"+
       "                charg_spin.append(geomtext[i]) #save the charge, spin                                                                                            \n"+
       "            elif len(line) == 4: #looking for Rh, x,y,z                                                                                                          \n"+
       "                try:                                                                                                                                             \n"+
       "                    line[1] = float(line[1]) # try and make into numbers                                                                                         \n"+
       "                    line[2] = float(line[2])                                                                                                                     \n"+
       "                    line[3] = float(line[3])                                                                                                                     \n"+
       "                    try:                                                                                                                                         \n"+
       "                        a=int(line[0])                                                                                                                           \n"+
       "                    except:                                                                                                                                      \n"+
       "                        is_line = 1                                                                                                                              \n"+
       "                except:                                                                                                                                          \n"+
       "                    pass # if it fails then its not a geometry                                                                                                   \n"+
       "            else:                                                                                                                                                \n"+
       "                footer.append(line)                                                                                                                              \n"+
       "            if is_line == 1: #if it is a good line then add to geoms                                                                                             \n"+
       "                geom.append(line)                                                                                                                                \n"+
       "        for j in range(len(footer)):                                                                                                                             \n"+
       "            for k in range(len(footer[j])):                                                                                                                      \n"+
       "                con += footer[j][k]                                                                                                                              \n"+
       "                con += ' '                                                                                                                                       \n"+
       "            con +='\\n'                                                                                                                                           \n"+
       "        if options[7] =='default':                                                                                                                               \n"+
       "            options[7] = con                                                                                                                                     \n"+
       "            print>>savef,'\\nConnectivity read from gjf file as\\n'                                                                                                \n"+
       "            print>>savef,con                                                                                                                                     \n"+
       "        if options[10] == 'default':                                                                                                                             \n"+
       "            options[10] = header                                                                                                                                 \n"+
       "            print>>savef,'\\nHeader read from gjf file as\\n'                                                                                                      \n"+
       "            print>>savef,header                                                                                                                                  \n"+
       "        savef.close()\n"+
       "        pass_ = check(geom,options)                                                                                                                              \n"+
       "        return pass_                                                                                                                                             \n"+
       "##############################################################################################                    \n"+                                               
       "def log_geom(fname,options): #grab geoms from a log file                                                          \n"+                                                                                                                                                                                            
       "    try:                                                                                                          \n"+                                       
       "        geom = [] #place to put the geometry                                                                      \n"+                                       
       "        openfile=open(fname[:len(fname)-4]+'.log','r')                                                            \n"+                           
       "        text=openfile.read()                                                                                      \n"+                                       
       "        geostring=re.findall(r'Standard orientation:(.*?)Rotational',text,re.DOTALL)                              \n"+                                       
       "        openfile.close()                                                                                          \n"+                                       
       "        good_geo=geostring[len(geostring)-1] #take the last geometry                                              \n"+                                       
       "        lines=good_geo.split('\\n') #split it based on lines                                                       \n"+                                       
       "        for i in range(len(lines)):                                                                               \n"+                                       
       "            if i > 4 and i < (len(lines)-2): #where the geometry is                                               \n"+                                       
       "                atom = lines[i].split()                                                                           \n"+                                       
       "                geom.append([int(atom[1]),float(atom[3]),float(atom[4]),float(atom[5])])                          \n"+                                                           
       "        pass_ = check(geom,options)                                                                               \n"+
       "    except:                                                                                                       \n"+
       "        pass_ = 0                                                                                                 \n"+                                     
       "    return pass_                                                                                                  \n"+
       "##############################################################################################                                                                   \n"+
       "def change_geom(filename,options): #change the geom of the last gjf saved in options                                                                             \n"+
       "    if filename[len(filename)-4:] == '.gjf':                                                                                                                     \n"+
       "        # Do things to current geometries                                                                                                                        \n"+
       "        geom = options[20]                                                                                                                                       \n"+
       "        charg_spin=[options[21]]                                                                                                                                 \n"+
       "        pass_ = 0                                                                                                                                                \n"+
       "        geom2 = copy.deepcopy(geom)                                                                                                                              \n"+
       "        geom = copy.deepcopy(geom2)                                                                                                                              \n"+
       "        cnt = 0                                                                                                                                                  \n"+
       "        while pass_ == 0:                                                                                                                                        \n"+
       "            options[25] += 1\n"+
       "            pass_,geom3 = random_move(geom,options)                                                                                                              \n"+
       "            cnt += 1                                                                                                                                             \n"+
       "            geom = copy.deepcopy(geom2)                                                                                                                          \n"+
       "            if cnt == options[18]:                                                                                                                               \n"+
       "                savef = open(options[3][:len(options[3])-4]+'calc_summary.txt','a')                                                                              \n"+
       "                pass_ = 1                                                                                                                                        \n"+
       "                print>>savef,'Gave up on rotating the geometry on method call %d'%(options[25])\n"+
       "                savef.close()\n"+
       "        geom = copy.deepcopy(geom3)                                                                                                                              \n"+
       "        for i in range(len(geom)):                                                                                                                               \n"+
       "            geom[i][0] = geom2[i][0]                                                                                                                             \n"+
       "        # Produce new file name                                                                                                                                  \n"+
       "        new_name = filename[:len(filename)-4] #drop the .gjf                                                                                                     \n"+
       "        new_name = new_name.replace('_',' ') #remove _'s                                                                                                         \n"+
       "        new_name = new_name.split() #split it                                                                                                                    \n"+
       "        iso_number = int(new_name[len(new_name)-1]) +1                                                                                                           \n"+
       "        new_fname = ''                                                                                                                                           \n"+
       "        for i in range(len(new_name)):                                                                                                                           \n"+
       "            if i < (len(new_name)-1):                                                                                                                            \n"+
       "                new_fname+=new_name[i] + '_'                                                                                                                     \n"+
       "            else:                                                                                                                                                \n"+
       "                new_fname+='%d' %(iso_number)                                                                                                                    \n"+
       "        new_fname +='.gjf' #add the gjf ext                                                                                                                      \n"+
       "        #produce the gjf file now isomer_x+1                                                                                                                     \n"+
       "        fname = new_fname.split('/') #name a name for the gjf file                                                                                               \n"+
       "        opf=open(new_fname,'w') #open the new file name as opf (Out Put File)                                                                                    \n"+
       "        #print the gjf file                                                                                                                                      \n"+
       "        print>>opf,'%nosave'                                                                                                                                     \n"+
       "        print>>opf,'%s' %(options[10])                                                                                                                           \n"+
       "        print>>opf,''                                                                                                                                            \n"+
       "        print>>opf,'%s Basin Hop' %(fname[len(fname)-1]                                                                                                          \n"+
       "                                    [:len(fname[len(fname)-1])-4]                                                                                                \n"+
       "                                    .replace('_',' ')) # drop the gjf                                                                                            \n"+
       "        print>>opf,''                                                                                                                                            \n"+
       "        print>>opf,charg_spin[0]                                                                                                                                 \n"+
       "        for i in range(len(geom)): #n1                                                                                                                           \n"+
       "            print>>opf,'%s      %.6f  %.6f  %.6f'%(geom[i][0],geom[i][1],                                                                                        \n"+
       "                                             geom[i][2],geom[i][3])                                                                                              \n"+
       "        print>>opf,options[7]                                                                                                                                    \n"+
       "        print>>opf,'\\n\\n'                                                                                                                                        \n"+
       "        options[20] = geom\n"+
       "        opf.close()                                                                                                                                              \n"+
       "        return new_fname,options                                                                                                                                 \n"+
       "##############################################################################################                                                                   \n"+
       "def extract_geom(filename,options): #Extract a geometry from a gjf if you do not have one already                                                                \n"+
       "    if filename[len(filename)-4:] == '.gjf':                                                                                                                     \n"+
       "        #Extract geometries from a gjf                                                                                                                           \n"+
       "        geom=[] #empty list to keep geoms                                                                                                                        \n"+
       "        footer = [] #place ot keep the connectivity                                                                                                              \n"+
       "        charg_spin=[] # charge and spin                                                                                                                          \n"+
       "        openfile = open(filename,'r') #Open file                                                                                                                 \n"+
       "        text=openfile.read() # Make file readable                                                                                                                \n"+
       "        geomtext = text.split('\\n') # split the text by lines                                                                                                    \n"+
       "        openfile.close() # close the file                                                                                                                        \n"+
       "        for i in range(len(geomtext)): #read the lines                                                                                                           \n"+
       "            line=geomtext[i].split() #split the line                                                                                                             \n"+
       "            is_line = 0 #switch                                                                                                                                  \n"+
       "            is_footer = 0                                                                                                                                        \n"+
       "            if i < 5:                                                                                                                                            \n"+
       "                pass #skip the title block                                                                                                                       \n"+
       "            elif i == 5:                                                                                                                                         \n"+
       "                charg_spin.append(geomtext[i]) #save the charge, spin                                                                                            \n"+
       "            elif len(line) == 4: #looking for Rh, x,y,z                                                                                                          \n"+
       "                try:                                                                                                                                             \n"+
       "                    line[1] = float(line[1]) # try and make into numbers                                                                                         \n"+
       "                    line[2] = float(line[2])                                                                                                                     \n"+
       "                    line[3] = float(line[3])                                                                                                                     \n"+
       "                    try:                                                                                                                                         \n"+
       "                        a=int(line[0])                                                                                                                           \n"+
       "                    except:                                                                                                                                      \n"+
       "                        is_line = 1                                                                                                                              \n"+
       "                except:                                                                                                                                          \n"+
       "                    pass # if it fails then its not a geometry                                                                                                   \n"+
       "            else:                                                                                                                                                \n"+
       "                try:                                                                                                                                             \n"+
       "                    for i in range(len(line)):                                                                                                                   \n"+
       "                        a=int(line[i])                                                                                                                           \n"+
       "                        is_footer = 1                                                                                                                            \n"+
       "                except:                                                                                                                                          \n"+
       "                    pass                                                                                                                                         \n"+
       "            if is_footer == 1:                                                                                                                                   \n"+
       "                footer.append(line)                                                                                                                              \n"+
       "                                                                                                                                                                 \n"+
       "            if is_line == 1: #if it is a good line then add to geoms                                                                                             \n"+
       "                geom.append(line)                                                                                                                                \n"+
       "                                                                                                                                                                 \n"+
       "        for i in range(len(geom)):                                                                                                                               \n"+
       "            geom[i][0] = geom[i][0].replace(' ','')                                                                                                              \n"+
       "        # Do things to current geometries                                                                                                                        \n"+
       "        pass_ = 0                                                                                                                                                \n"+
       "        geom2 = copy.deepcopy(geom)                                                                                                                              \n"+
       "        geom = copy.deepcopy(geom2)                                                                                                                              \n"+
       "        cnt = 0                                                                                                                                                  \n"+
       "        while pass_ == 0:                                                                                                                                        \n"+
       "            options[25]+=1\n"+
       "            pass_,geom3 = random_move(geom,options)                                                                                                              \n"+
       "            cnt += 1                                                                                                                                             \n"+
       "            geom = copy.deepcopy(geom2)                                                                                                                          \n"+
       "            if cnt == options[18]:                                                                                                                               \n"+
       "                pass_ = 1                                                                                                                                        \n"+
       "        geom = copy.deepcopy(geom3)                                                                                                                              \n"+
       "        for i in range(len(geom)):                                                                                                                               \n"+
       "            geom[i][0] = geom2[i][0]                                                                                                                             \n"+
       "        # Produce new file name                                                                                                                                  \n"+
       "        new_name = filename[:len(filename)-4] #drop the .gjf                                                                                                     \n"+
       "        new_name = new_name.replace('_',' ') #remove _'s                                                                                                         \n"+
       "        new_name = new_name.split() #split it                                                                                                                    \n"+
       "        iso_number = int(new_name[len(new_name)-1]) +1                                                                                                           \n"+
       "        new_fname = ''                                                                                                                                           \n"+
       "        for i in range(len(new_name)):                                                                                                                           \n"+
       "            if i < (len(new_name)-1):                                                                                                                            \n"+
       "                new_fname+=new_name[i] + '_'                                                                                                                     \n"+
       "            else:                                                                                                                                                \n"+
       "                new_fname+='%d' %(iso_number)                                                                                                                    \n"+
       "        new_fname +='.gjf' #add the gjf ext                                                                                                                      \n"+
       "        #produce the gjf file now isomer_x+1                                                                                                                     \n"+
       "        fname = new_fname.split('/') #name a name for the gjf file                                                                                               \n"+
       "        opf=open(new_fname,'w') #open the new file name as opf (Out Put File)                                                                                    \n"+
       "        #print the gjf file                                                                                                                                      \n"+
       "        print>>opf,'%nosave'                                                                                                                                     \n"+
       "        print>>opf,'%s' %(options[10])                                                                                                                           \n"+
       "        print>>opf,''                                                                                                                                            \n"+
       "        print>>opf,'%s Basin Hop' %(fname[len(fname)-1]                                                                                                          \n"+
       "                                    [:len(fname[len(fname)-1])-4]                                                                                                \n"+
       "                                    .replace('_',' ')) # drop the gjf                                                                                            \n"+
       "        print>>opf,''                                                                                                                                            \n"+
       "        print>>opf,charg_spin[0]                                                                                                                                 \n"+
       "        for i in range(len(geom)): #n1                                                                                                                           \n"+
       "            print>>opf,'%s      %.6f  %.6f  %.6f'%(geom[i][0],geom[i][1],                                                                                        \n"+
       "                                             geom[i][2],geom[i][3])                                                                                              \n"+
       "        print>>opf,options[7]                                                                                                                                    \n"+
       "        print>>opf,'\\n\\n'                                                                                                                                        \n"+
       "        opf.close()                                                                                                                                              \n"+
       "        options[20]=geom                                                                                                                                         \n"+
       "        options[21]=charg_spin[0]                                                                                                                                \n"+
       "        return new_fname,options                                                                                                                                 \n"+
       "##############################################################################################                                                                   \n"+
       "def random_move(geom,options): #send off to right method                                                                                                         \n"+
       "    #picks which method                                                                                                                                          \n"+
       "    if options[1][0] == 'rand_trans':                                                                                                                            \n"+
       "        pass_,geom2 = random_trans(geom,options)                                                                                                                 \n"+
       "    elif options[1][0] ==  'rand_rot':                                                                                                                           \n"+
       "        pass_,geom2 = random_rot(geom,options)                                                                                                                   \n"+
       "    elif options[1][0] == 'dihedral_rot':                                                                                                                        \n"+
       "        pass_,geom2 = dihedral_rot(geom,options)                                                                                                                 \n"+
       "    elif options[1][0] == 'gen_move':                                                                                                                            \n"+
       "        pass_,geom2 = gen_move(geom,options)                                                                                                                     \n"+
       "    elif options[1][0] == 'gen_rot':                                                                                                                             \n"+
       "        pass_,geom2 = gen_rot(geom,options)                                                                                                                      \n"+
       "    elif options[1][0] == 'ulti_move':                                                                                                                           \n"+
       "        pass_,geom2 = ulti_move(geom,options)                                                                                                                    \n"+
       "    if options[11] == 1:                                                                                                                                         \n"+
       "        pass_ = custom(geom2)                                                                                                                                    \n"+
       "    return pass_,geom2                                                                                                                                           \n"+
       "##############################################################################################                                                                   \n"+
       "def dihedral_rot(geom,options): #borhing math                                                                                                                    \n"+
       "    n_times = len(options[1])-2 #number of axis to rotate                                                                                                        \n"+
       "    theta = float(options[1][1])*pi/float(180.0)                                                                                                                 \n"+
       "    rotations = []                                                                                                                                               \n"+
       "    for i in range(len(options[1])-2):                                                                                                                           \n"+
       "        rotations.append(options[1][i+2])                                                                                                                        \n"+
       "    for i in range(n_times):                                                                                                                                     \n"+
       "        axis_atoms = [geom[rotations[i][0]],geom[rotations[i][1]]]                                                                                               \n"+
       "        axis = [axis_atoms[0][1]-axis_atoms[1][1],                                                                                                               \n"+
       "                axis_atoms[0][2]-axis_atoms[1][2],                                                                                                               \n"+
       "                axis_atoms[0][3]-axis_atoms[1][3]]                                                                                                               \n"+
       "        a = axis_atoms[0][1]                                                                                                                                     \n"+
       "        b = axis_atoms[0][2]                                                                                                                                     \n"+
       "        c = axis_atoms[0][3]                                                                                                                                     \n"+
       "        u = axis[0]                                                                                                                                              \n"+
       "        v = axis[1]                                                                                                                                              \n"+
       "        w = axis[2]                                                                                                                                              \n"+
       "        L = u*u +v*v + w*w                                                                                                                                       \n"+
       "        effect_atoms = []                                                                                                                                        \n"+
       "        theta_ = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        for j in range(len(rotations[i])-2):                                                                                                                     \n"+
       "            effect_atoms.append(geom[rotations[i][j+2]])                                                                                                         \n"+
       "        for k in range(len(effect_atoms)): # gen the new geoms                                                                                                   \n"+
       "            x = effect_atoms[k][1]                                                                                                                               \n"+
       "            y = effect_atoms[k][2]                                                                                                                               \n"+
       "            z = effect_atoms[k][3]                                                                                                                               \n"+
       "            x_ = ((a*(v*v+w*w)-u*(b*v+c*w-u*x-v*y-w*z))*                                                                                                         \n"+
       "                  (1-cos(theta_))+L*x*cos(theta_)+sqrt(L)*                                                                                                       \n"+
       "                  (-c*v+b*w-w*y+v*z)*sin(theta_))/float(L)                                                                                                       \n"+
       "            y_ = ((b*(u*u+w*w)-v*(a*u+c*w-u*x-v*y-w*z))*                                                                                                         \n"+
       "                  (1-cos(theta_))+L*y*cos(theta_)+sqrt(L)*                                                                                                       \n"+
       "                  (c*u-a*w+w*x-u*z)*sin(theta_))/float(L)                                                                                                        \n"+
       "            z_ = ((c*(v*v+u*u)-w*(a*u+b*v-u*x-v*y-w*z))*                                                                                                         \n"+
       "                  (1-cos(theta_))+L*z*cos(theta_)+sqrt(L)*                                                                                                       \n"+
       "                  (-b*u+a*v-v*x+u*y)*sin(theta_))/float(L)                                                                                                       \n"+
       "            effect_atoms[k][1] = x_                                                                                                                              \n"+
       "            effect_atoms[k][2] = y_                                                                                                                              \n"+
       "            effect_atoms[k][3] = z_                                                                                                                              \n"+
       "        for l in range(len(rotations[i])-2): # add back to geoms                                                                                                 \n"+
       "            geom[rotations[i][l+2]] = effect_atoms[l]                                                                                                            \n"+
       "    pass_ = check(geom,options)                                                                                                                                  \n"+
       "    return pass_,geom                                                                                                                                            \n"+
       "##############################################################################################                                                                   \n"+
       "def ulti_move(geom,options):                                                                                                                                     \n"+
       "    di_rot = options[1][1]                                                                                                                                       \n"+
       "    rot = options[1][2]                                                                                                                                          \n"+
       "    trans = options[1][3]                                                                                                                                        \n"+
       "    #di_rots first                                                                                                                                               \n"+
       "    for i in range(len(di_rot)):                                                                                                                                 \n"+
       "        axis_atoms = [geom[di_rot[i][0]],geom[di_rot[i][1]]]                                                                                                     \n"+
       "        axis = [axis_atoms[0][1]-axis_atoms[1][1],                                                                                                               \n"+
       "                axis_atoms[0][2]-axis_atoms[1][2],                                                                                                               \n"+
       "                axis_atoms[0][3]-axis_atoms[1][3]]                                                                                                               \n"+
       "        a = axis_atoms[0][1]                                                                                                                                     \n"+
       "        b = axis_atoms[0][2]                                                                                                                                     \n"+
       "        c = axis_atoms[0][3]                                                                                                                                     \n"+
       "        u = axis[0]                                                                                                                                              \n"+
       "        v = axis[1]                                                                                                                                              \n"+
       "        w = axis[2]                                                                                                                                              \n"+
       "        L = u*u +v*v + w*w                                                                                                                                       \n"+
       "        effect_atoms = []                                                                                                                                        \n"+
       "        theta_ = di_rot[i][len(di_rot[i])-1]*(random.random()*2-1)                                                                                               \n"+
       "        for j in range(len(di_rot[i])-3):                                                                                                                        \n"+
       "            effect_atoms.append(geom[di_rot[i][j+2]])                                                                                                            \n"+
       "        for k in range(len(effect_atoms)): # gen the new geoms                                                                                                   \n"+
       "            x = effect_atoms[k][1]                                                                                                                               \n"+
       "            y = effect_atoms[k][2]                                                                                                                               \n"+
       "            z = effect_atoms[k][3]                                                                                                                               \n"+
       "            x_ = ((a*(v*v+w*w)-u*(b*v+c*w-u*x-v*y-w*z))*                                                                                                         \n"+
       "                  (1-cos(theta_))+L*x*cos(theta_)+sqrt(L)*                                                                                                       \n"+
       "                  (-c*v+b*w-w*y+v*z)*sin(theta_))/float(L)                                                                                                       \n"+
       "            y_ = ((b*(u*u+w*w)-v*(a*u+c*w-u*x-v*y-w*z))*                                                                                                         \n"+
       "                  (1-cos(theta_))+L*y*cos(theta_)+sqrt(L)*                                                                                                       \n"+
       "                  (c*u-a*w+w*x-u*z)*sin(theta_))/float(L)                                                                                                        \n"+
       "            z_ = ((c*(v*v+u*u)-w*(a*u+b*v-u*x-v*y-w*z))*                                                                                                         \n"+
       "                  (1-cos(theta_))+L*z*cos(theta_)+sqrt(L)*                                                                                                       \n"+
       "                  (-b*u+a*v-v*x+u*y)*sin(theta_))/float(L)                                                                                                       \n"+
       "            effect_atoms[k][1] = x_                                                                                                                              \n"+
       "            effect_atoms[k][2] = y_                                                                                                                              \n"+
       "            effect_atoms[k][3] = z_                                                                                                                              \n"+
       "        for l in range(len(di_rot[i])-3): # add back to geoms                                                                                                    \n"+
       "            geom[di_rot[i][l+2]] = effect_atoms[l]                                                                                                               \n"+
       "    #then rots                                                                                                                                                   \n"+
       "    for i in range(len(rot)):                                                                                                                                    \n"+
       "        new_atoms = []                                                                                                                                           \n"+
       "        thetax = rot[i][0]*(random.random()*2-1)                                                                                                                 \n"+
       "        thetay = rot[i][0]*(random.random()*2-1)                                                                                                                 \n"+
       "        thetaz = rot[i][0]*(random.random()*2-1)                                                                                                                 \n"+
       "        transx = rot[i][1]*(random.random()*2-1)                                                                                                                 \n"+
       "        transy = rot[i][1]*(random.random()*2-1)                                                                                                                 \n"+
       "        transz = rot[i][1]*(random.random()*2-1)                                                                                                                 \n"+
       "        for j in range(len(rot[i])-2):                                                                                                                           \n"+
       "            new_atoms.append(geom[rot[i][j+2]])                                                                                                                  \n"+
       "        rcm = r_cm(new_atoms)                                                                                                                                    \n"+
       "        for k in range(len(new_atoms)):                                                                                                                          \n"+
       "            for l in range(3):                                                                                                                                   \n"+
       "                new_atoms[k][l+1] = new_atoms[k][l+1]-rcm[l]                                                                                                     \n"+
       "        for m in range(len(new_atoms)):                                                                                                                          \n"+
       "            x = new_atoms[m][1]                                                                                                                                  \n"+
       "            y = new_atoms[m][2]                                                                                                                                  \n"+
       "            z = new_atoms[m][3]                                                                                                                                  \n"+
       "            #rot x                                                                                                                                               \n"+
       "            y_ = y*cos(thetax)-z*sin(thetax)                                                                                                                     \n"+
       "            z_ = z*cos(thetax)+y*sin(thetax)                                                                                                                     \n"+
       "            #rot y                                                                                                                                               \n"+
       "            x_ = x*cos(thetay)+z_*sin(thetay)                                                                                                                    \n"+
       "            z__ = z_*cos(thetay)-x*sin(thetay)                                                                                                                   \n"+
       "            #rot z                                                                                                                                               \n"+
       "            x__ = x_*cos(thetaz)-y_*sin(thetaz)                                                                                                                  \n"+
       "            y__ = y_*cos(thetaz)+x_*sin(thetaz)                                                                                                                  \n"+
       "            new_atoms[m][1] = x__                                                                                                                                \n"+
       "            new_atoms[m][2] = y__                                                                                                                                \n"+
       "            new_atoms[m][3] = z__                                                                                                                                \n"+
       "        for n in range(len(new_atoms)):                                                                                                                          \n"+
       "            for l in range(3):                                                                                                                                   \n"+
       "                new_atoms[n][l+1] = new_atoms[n][l+1]+rcm[l]                                                                                                     \n"+
       "        for p in range(len(new_atoms)):                                                                                                                          \n"+
       "            new_atoms[p][1] = new_atoms[p][1]+transx                                                                                                             \n"+
       "            new_atoms[p][2] = new_atoms[p][2]+transy                                                                                                             \n"+
       "            new_atoms[p][3] = new_atoms[p][3]+transz                                                                                                             \n"+
       "        for q in range(len(rot[i])-2):                                                                                                                           \n"+
       "            geom[rot[i][q+2]] = new_atoms[q]                                                                                                                     \n"+
       "    #then trans                                                                                                                                                  \n"+
       "    for i in range(len(trans)):                                                                                                                                  \n"+
       "        tranx = trans[i][0]*(random.random()*2-1)                                                                                                                \n"+
       "        trany = trans[i][0]*(random.random()*2-1)                                                                                                                \n"+
       "        tranz = trans[i][0]*(random.random()*2-1)                                                                                                                \n"+
       "        for j in range(len(trans[i])-1):                                                                                                                         \n"+
       "            geom[trans[i][j+1]][1]+tranx                                                                                                                         \n"+
       "            geom[trans[i][j+1]][2]+trany                                                                                                                         \n"+
       "            geom[trans[i][j+1]][3]+tranz                                                                                                                         \n"+
       "    pass_ = check(geom,options)                                                                                                                                  \n"+
       "    return pass_,geom                                                                                                                                            \n"+
       "##############################################################################################                                                                   \n"+
       "def gen_move(geom,options):                                                                                                                                      \n"+
       "    di_theta = options[1][1]                                                                                                                                     \n"+
       "    theta = options[1][2]                                                                                                                                        \n"+
       "    trans = options[1][3]                                                                                                                                        \n"+
       "    rot = options[1][4]                                                                                                                                          \n"+
       "    di_rot = options[1][5]                                                                                                                                       \n"+
       "                                                                                                                                                                 \n"+
       "    #di_rots first                                                                                                                                               \n"+
       "    for i in range(len(di_rot)):                                                                                                                                 \n"+
       "        axis_atoms = [geom[di_rot[i][0]],geom[di_rot[i][1]]]                                                                                                     \n"+
       "        axis = [axis_atoms[0][1]-axis_atoms[1][1],                                                                                                               \n"+
       "                axis_atoms[0][2]-axis_atoms[1][2],                                                                                                               \n"+
       "                axis_atoms[0][3]-axis_atoms[1][3]]                                                                                                               \n"+
       "        a = axis_atoms[0][1]                                                                                                                                     \n"+
       "        b = axis_atoms[0][2]                                                                                                                                     \n"+
       "        c = axis_atoms[0][3]                                                                                                                                     \n"+
       "        u = axis[0]                                                                                                                                              \n"+
       "        v = axis[1]                                                                                                                                              \n"+
       "        w = axis[2]                                                                                                                                              \n"+
       "        L = u*u +v*v + w*w                                                                                                                                       \n"+
       "        effect_atoms = []                                                                                                                                        \n"+
       "        theta_ = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        for j in range(len(di_rot[i])-2):                                                                                                                        \n"+
       "            effect_atoms.append(geom[di_rot[i][j+2]])                                                                                                            \n"+
       "        for k in range(len(effect_atoms)): # gen the new geoms                                                                                                   \n"+
       "            x = effect_atoms[k][1]                                                                                                                               \n"+
       "            y = effect_atoms[k][2]                                                                                                                               \n"+
       "            z = effect_atoms[k][3]                                                                                                                               \n"+
       "            x_ = ((a*(v*v+w*w)-u*(b*v+c*w-u*x-v*y-w*z))*                                                                                                         \n"+
       "                  (1-cos(theta_))+L*x*cos(theta_)+sqrt(L)*                                                                                                       \n"+
       "                  (-c*v+b*w-w*y+v*z)*sin(theta_))/float(L)                                                                                                       \n"+
       "            y_ = ((b*(u*u+w*w)-v*(a*u+c*w-u*x-v*y-w*z))*                                                                                                         \n"+
       "                  (1-cos(theta_))+L*y*cos(theta_)+sqrt(L)*                                                                                                       \n"+
       "                  (c*u-a*w+w*x-u*z)*sin(theta_))/float(L)                                                                                                        \n"+
       "            z_ = ((c*(v*v+u*u)-w*(a*u+b*v-u*x-v*y-w*z))*                                                                                                         \n"+
       "                  (1-cos(theta_))+L*z*cos(theta_)+sqrt(L)*                                                                                                       \n"+
       "                  (-b*u+a*v-v*x+u*y)*sin(theta_))/float(L)                                                                                                       \n"+
       "            effect_atoms[k][1] = x_                                                                                                                              \n"+
       "            effect_atoms[k][2] = y_                                                                                                                              \n"+
       "            effect_atoms[k][3] = z_                                                                                                                              \n"+
       "        for l in range(len(di_rot[i])-2): # add back to geoms                                                                                                    \n"+
       "            geom[di_rot[i][l+2]] = effect_atoms[l]                                                                                                               \n"+
       "    #then rots                                                                                                                                                   \n"+
       "    for i in range(len(rot)):                                                                                                                                    \n"+
       "        new_atoms = []                                                                                                                                           \n"+
       "        thetax = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        thetay = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        thetaz = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        transx = trans*(random.random()*2-1)                                                                                                                     \n"+
       "        transy = trans*(random.random()*2-1)                                                                                                                     \n"+
       "        transz = trans*(random.random()*2-1)                                                                                                                     \n"+
       "        for j in range(len(rot[i])):                                                                                                                             \n"+
       "            new_atoms.append(geom[rot[i][j]])                                                                                                                    \n"+
       "        rcm = r_cm(new_atoms)                                                                                                                                    \n"+
       "        for k in range(len(new_atoms)):                                                                                                                          \n"+
       "            for l in range(3):                                                                                                                                   \n"+
       "                new_atoms[k][l+1] = new_atoms[k][l+1]-rcm[l]                                                                                                     \n"+
       "        for m in range(len(new_atoms)):                                                                                                                          \n"+
       "            x = new_atoms[m][1]                                                                                                                                  \n"+
       "            y = new_atoms[m][2]                                                                                                                                  \n"+
       "            z = new_atoms[m][3]                                                                                                                                  \n"+
       "            #rot x                                                                                                                                               \n"+
       "            y_ = y*cos(thetax)-z*sin(thetax)                                                                                                                     \n"+
       "            z_ = z*cos(thetax)+y*sin(thetax)                                                                                                                     \n"+
       "            #rot y                                                                                                                                               \n"+
       "            x_ = x*cos(thetay)+z_*sin(thetay)                                                                                                                    \n"+
       "            z__ = z_*cos(thetay)-x*sin(thetay)                                                                                                                   \n"+
       "            #rot z                                                                                                                                               \n"+
       "            x__ = x_*cos(thetaz)-y_*sin(thetaz)                                                                                                                  \n"+
       "            y__ = y_*cos(thetaz)+x_*sin(thetaz)                                                                                                                  \n"+
       "            new_atoms[m][1] = x__                                                                                                                                \n"+
       "            new_atoms[m][2] = y__                                                                                                                                \n"+
       "            new_atoms[m][3] = z__                                                                                                                                \n"+
       "        for n in range(len(new_atoms)):                                                                                                                          \n"+
       "            for l in range(3):                                                                                                                                   \n"+
       "                new_atoms[n][l+1] = new_atoms[n][l+1]+rcm[l]                                                                                                     \n"+
       "        for p in range(len(new_atoms)):                                                                                                                          \n"+
       "            new_atoms[p][1] = new_atoms[p][1]+transx                                                                                                             \n"+
       "            new_atoms[p][2] = new_atoms[p][2]+transy                                                                                                             \n"+
       "            new_atoms[p][3] = new_atoms[p][3]+transz                                                                                                             \n"+
       "        for q in range(len(rot[i])):                                                                                                                             \n"+
       "            geom[rot[i][q]] = new_atoms[q]                                                                                                                       \n"+
       "    pass_ = check(geom,options)                                                                                                                                  \n"+
       "    return pass_,geom                                                                                                                                            \n"+
       "##############################################################################################                                                                   \n"+
       "def gen_rot(geom,options):                                                                                                                                       \n"+
       "    theta = options[1][1]                                                                                                                                        \n"+
       "    trans = options[1][2]                                                                                                                                        \n"+
       "    rot = options[1][3]                                                                                                                                          \n"+
       "    for i in range(len(rot)):                                                                                                                                    \n"+
       "        new_atoms = []                                                                                                                                           \n"+
       "        thetax = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        thetay = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        thetaz = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        transx = trans*(random.random()*2-1)                                                                                                                     \n"+
       "        transy = trans*(random.random()*2-1)                                                                                                                     \n"+
       "        transz = trans*(random.random()*2-1)                                                                                                                     \n"+
       "        for j in range(len(rot[i])):                                                                                                                             \n"+
       "            new_atoms.append(geom[rot[i][j]])                                                                                                                    \n"+
       "        rcm = r_cm(new_atoms)                                                                                                                                    \n"+
       "        for k in range(len(new_atoms)):                                                                                                                          \n"+
       "            for l in range(3):                                                                                                                                   \n"+
       "                new_atoms[k][l+1] = new_atoms[k][l+1]-rcm[l]                                                                                                     \n"+
       "        for m in range(len(new_atoms)):                                                                                                                          \n"+
       "            x = new_atoms[m][1]                                                                                                                                  \n"+
       "            y = new_atoms[m][2]                                                                                                                                  \n"+
       "            z = new_atoms[m][3]                                                                                                                                  \n"+
       "            #rot x                                                                                                                                               \n"+
       "            y_ = y*cos(thetax)-z*sin(thetax)                                                                                                                     \n"+
       "            z_ = z*cos(thetax)+y*sin(thetax)                                                                                                                     \n"+
       "            #rot y                                                                                                                                               \n"+
       "            x_ = x*cos(thetay)+z_*sin(thetay)                                                                                                                    \n"+
       "            z__ = z_*cos(thetay)-x*sin(thetay)                                                                                                                   \n"+
       "            #rot z                                                                                                                                               \n"+
       "            x__ = x_*cos(thetaz)-y_*sin(thetaz)                                                                                                                  \n"+
       "            y__ = y_*cos(thetaz)+x_*sin(thetaz)                                                                                                                  \n"+
       "            new_atoms[m][1] = x__                                                                                                                                \n"+
       "            new_atoms[m][2] = y__                                                                                                                                \n"+
       "            new_atoms[m][3] = z__                                                                                                                                \n"+
       "        for n in range(len(new_atoms)):                                                                                                                          \n"+
       "            for l in range(3):                                                                                                                                   \n"+
       "                new_atoms[n][l+1] = new_atoms[n][l+1]+rcm[l]                                                                                                     \n"+
       "        for p in range(len(new_atoms)):                                                                                                                          \n"+
       "            new_atoms[p][1] = new_atoms[p][1]+transx                                                                                                             \n"+
       "            new_atoms[p][2] = new_atoms[p][2]+transy                                                                                                             \n"+
       "            new_atoms[p][3] = new_atoms[p][3]+transz                                                                                                             \n"+
       "        for q in range(len(rot[i])):                                                                                                                             \n"+
       "            geom[rot[i][q]] = new_atoms[q]                                                                                                                       \n"+
       "    pass_ = check(geom,options)                                                                                                                                  \n"+
       "    return pass_,geom                                                                                                                                            \n"+
       "##############################################################################################                                                                   \n"+
       "def random_rot(new_geom,options):                                                                                                                                \n"+
       "    n_times = options[1][1]                                                                                                                                      \n"+
       "    n_atoms = options[1][2]                                                                                                                                      \n"+
       "    theta = options[1][3]*pi/float(180.0)                                                                                                                        \n"+
       "    trans = options[1][4]                                                                                                                                        \n"+
       "    for i in range(n_times):                                                                                                                                     \n"+
       "        new_atoms = []                                                                                                                                           \n"+
       "        thetax = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        thetay = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        thetaz = theta*(random.random()*2-1)                                                                                                                     \n"+
       "        transx = trans*(random.random()*2-1)                                                                                                                     \n"+
       "        transy = trans*(random.random()*2-1)                                                                                                                     \n"+
       "        transz = trans*(random.random()*2-1)                                                                                                                     \n"+
       "        for j in range(n_atoms):                                                                                                                                 \n"+
       "            new_atoms.append(new_geom[len(new_geom)-1-j -i*n_atoms])                                                                                             \n"+
       "        rcm = r_cm(new_atoms)                                                                                                                                    \n"+
       "        for k in range(len(new_atoms)):                                                                                                                          \n"+
       "            for l in range(3):                                                                                                                                   \n"+
       "                new_atoms[k][l+1] = new_atoms[k][l+1]-rcm[l]                                                                                                     \n"+
       "        for m in range(len(new_atoms)):                                                                                                                          \n"+
       "            x = new_atoms[m][1]                                                                                                                                  \n"+
       "            y = new_atoms[m][2]                                                                                                                                  \n"+
       "            z = new_atoms[m][3]                                                                                                                                  \n"+
       "            #rot x                                                                                                                                               \n"+
       "            y_ = y*cos(thetax)-z*sin(thetax)                                                                                                                     \n"+
       "            z_ = z*cos(thetax)+y*sin(thetax)                                                                                                                     \n"+
       "            #rot y                                                                                                                                               \n"+
       "            x_ = x*cos(thetay)+z_*sin(thetay)                                                                                                                    \n"+
       "            z__ = z_*cos(thetay)-x*sin(thetay)                                                                                                                   \n"+
       "            #rot z                                                                                                                                               \n"+
       "            x__ = x_*cos(thetaz)-y_*sin(thetaz)                                                                                                                  \n"+
       "            y__ = y_*cos(thetaz)+x_*sin(thetaz)                                                                                                                  \n"+
       "            new_atoms[m][1] = x__                                                                                                                                \n"+
       "            new_atoms[m][2] = y__                                                                                                                                \n"+
       "            new_atoms[m][3] = z__                                                                                                                                \n"+
       "        for n in range(len(new_atoms)):                                                                                                                          \n"+
       "            for l in range(3):                                                                                                                                   \n"+
       "                new_atoms[n][l+1] = new_atoms[n][l+1]+rcm[l]                                                                                                     \n"+
       "        for p in range(len(new_atoms)):                                                                                                                          \n"+
       "            new_atoms[p][1] = new_atoms[p][1]+transx                                                                                                             \n"+
       "            new_atoms[p][2] = new_atoms[p][2]+transy                                                                                                             \n"+
       "            new_atoms[p][3] = new_atoms[p][3]+transz                                                                                                             \n"+
       "        for o in range(n_atoms):                                                                                                                                 \n"+
       "            new_geom[len(new_geom)-1-o -i*n_atoms] = new_atoms[o]                                                                                                \n"+
       "    pass_ = check(new_geom,options)                                                                                                                              \n"+
       "    return pass_,new_geom                                                                                                                                        \n"+
       "##############################################################################################                                                                   \n"+
       "def random_trans(geom,options):                                                                                                                                  \n"+
       "    n_times = options[1][2]                                                                                                                                      \n"+
       "    n_atoms = options[1][1]                                                                                                                                      \n"+
       "    trans = options[1][3]                                                                                                                                        \n"+
       "    for j in range(n_times):                                                                                                                                     \n"+
       "        new_atoms = []                                                                                                                                           \n"+
       "        #randomly generate new cord addition                                                                                                                     \n"+
       "        randcord=[(random.random()*2-1)*.2,                                                                                                                      \n"+
       "                  (random.random()*2-1)*.2,                                                                                                                      \n"+
       "                  (random.random()*2-1)*.2]                                                                                                                      \n"+
       "        for i in range(n_atoms):                                                                                                                                 \n"+
       "            new_atoms.append(geom[len(geom)-1-i -j*n_atoms])                                                                                                     \n"+
       "                                                                                                                                                                 \n"+
       "        #add the random cord to last n atoms                                                                                                                     \n"+
       "        for i in range(n_atoms):                                                                                                                                 \n"+
       "            new_atoms[i][1] += randcord[0]                                                                                                                       \n"+
       "            new_atoms[i][2] += randcord[1]                                                                                                                       \n"+
       "            new_atoms[i][3] += randcord[2]                                                                                                                       \n"+
       "        for i in range(n_atoms):                                                                                                                                 \n"+
       "            geom[len(geom)-1-i -j*n_atoms] = new_atoms[i]                                                                                                        \n"+
       "    pass_ = check(geom,options)                                                                                                                                  \n"+
       "    return pass_,geom                                                                                                                                            \n"+
       "##############################################################################################                                                                   \n"+
       "def check(geom,options):                                                                                                                                         \n"+
       "    #check to see if move was accepable                                                                                                                          \n"+
       "    dist = []                                                                                                                                                    \n"+
       "    pass_ = 1                                                                                                                                                    \n"+
       "    for i in range(len(geom)):                                                                                                                                   \n"+
       "        for j in range(len(geom)):                                                                                                                               \n"+
       "            if i != j and j>i: #will be zero lol                                                                                                                 \n"+
       "                dist_len=sqrt((geom[i][1]-geom[j][1])**2+                                                                                                        \n"+
       "                              (geom[i][2]-geom[j][2])**2+                                                                                                        \n"+
       "                              (geom[i][3]-geom[j][3])**2)                                                                                                        \n"+
       "                dist.append(dist_len)                                                                                                                            \n"+
       "    #defin a sphere if any atoms out of sphere then fail                                                                                                         \n"+
       "    for i in range(len(geom)):                                                                                                                                   \n"+
       "        r2 = geom[i][1]**2 + geom[i][2]**2 + geom[i][3]**2                                                                                                       \n"+
       "        if r2 > options[4]**2:                                                                                                                                   \n"+
       "            pass_ = 0                                                                                                                                            \n"+
       "    #check bond lengths                                                                                                                                          \n"+
       "    for i in range(len(dist)):                                                                                                                                   \n"+
       "        if dist[i] <= options[16]: #if any bond lengths are less than .x A                                                                                       \n"+
       "            pass_ = 0                                                                                                                                            \n"+
       "    return pass_                                                                                                                                                 \n"+
       "##############################################################################################                                                                   \n"+
       "def nrg_analysis(nrg,bh_cf,bh_files,options):                                                                                                                    \n"+
       "     min_ = bh_cf[2]                                                                                                                                             \n"+
       "     bh_files2 = []                                                                                                                                              \n"+
       "     max_ = max(nrg)                                                                                                                                             \n"+
       "     bin_ = options[13]                                                                                                                                          \n"+
       "     nrg2 = []                                                                                                                                                   \n"+
       "     bh_f2 = []                                                                                                                                                  \n"+
       "     steps = int((max_-min_)/bin_)+2                                                                                                                             \n"+
       "     for i in range(steps): #check nrg                                                                                                                           \n"+
       "         has_one = 0                                                                                                                                             \n"+
       "         c_low = 100                                                                                                                                             \n"+
       "         index = 0                                                                                                                                               \n"+
       "         for j in range(len(nrg)):                                                                                                                               \n"+
       "             if nrg[j] != 4:                                                                                                                                     \n"+
       "                 if nrg[j]<=(min_+(1+i)*bin_):                                                                                                                   \n"+
       "                     if nrg[j] >= (min_ +(i)*bin_):                                                                                                              \n"+
       "                         if has_one !=0:                                                                                                                         \n"+
       "                             has_one = 1                                                                                                                         \n"+
       "                             c_low = nrg[j]                                                                                                                      \n"+
       "                             index = j                                                                                                                           \n"+
       "                         else:                                                                                                                                   \n"+
       "                             if nrg[j] >= c_low:                                                                                                                 \n"+
       "                                 nrg[j] = 4                                                                                                                      \n"+
       "                             else:                                                                                                                               \n"+
       "                                 c_low = nrg[j]                                                                                                                  \n"+
       "                                 nrg[index] = 4                                                                                                                  \n"+
       "                                 index = j                                                                                                                       \n"+
       "     for i in range(len(nrg)):                                                                                                                                   \n"+
       "         if nrg[i] != 4:                                                                                                                                         \n"+
       "             nrg2.append(nrg[i])                                                                                                                                 \n"+
       "             bh_f2.append(bh_files[i])                                                                                                                           \n"+
       "         else:                                                                                                                                                   \n"+
       "             bh_files2.append(bh_files[i])                                                                                                                       \n"+
       "     return nrg,nrg2,bh_f2,bh_files2                                                                                                                             \n"+
       "##############################################################################################                                                                   \n"+
       "def log_extract(nrg,bh_files): #grab geoms from a log file                                                                                                       \n"+
       "    rcm_list = []                                                                                                                                                \n"+
       "    geom_tot = []                                                                                                                                                \n"+
       "    for i in range(len(bh_files)):                                                                                                                               \n"+
       "        if nrg[i] != 4:                                                                                                                                          \n"+
       "            try:                                                                                                                                                 \n"+
       "                geom = [] #place to put the geometry                                                                                                             \n"+
       "                openfile=open(bh_files[i][:len(bh_files[i])-4]+'.log','r')                                                                                       \n"+
       "                text=openfile.read()                                                                                                                             \n"+
       "                geostring=re.findall(r'Standard orientation:(.*?)Rotational',text,re.DOTALL)                                                                     \n"+
       "                openfile.close()                                                                                                                                 \n"+
       "                good_geo=geostring[len(geostring)-1] #take the last geometry                                                                                     \n"+
       "                lines=good_geo.split('\\n') #split it based on lines                                                                                              \n"+
       "                for i in range(len(lines)):                                                                                                                      \n"+
       "                    if i > 4 and i < (len(lines)-2): #where the geometry is                                                                                      \n"+
       "                        atom = lines[i].split()                                                                                                                  \n"+
       "                        geom.append([int(atom[1]),float(atom[3]),float(atom[4]),                                                                                 \n"+
       "                                    float(atom[5])]) #add the lines to geom                                                                                      \n"+
       "                geom = geom_con_ntl(geom)                                                                                                                        \n"+
       "                rcm = r_cm(geom)                                                                                                                                 \n"+
       "                rcm_R_list = []                                                                                                                                  \n"+
       "                for i in range(len(geom)):                                                                                                                       \n"+
       "                    R = ((geom[i][1]-rcm[0])**2+(geom[i][2]-rcm[1])**2                                                                                           \n"+
       "                         +(geom[i][3]-rcm[2])**2)                                                                                                                \n"+
       "                    rcm_R_list.append(R)                                                                                                                         \n"+
       "                geom_tot.append(geom)                                                                                                                            \n"+
       "                rcm_list.append(rcm_R_list)                                                                                                                      \n"+
       "            except:                                                                                                                                              \n"+
       "                nrg[i] =4                                                                                                                                        \n"+
       "    return rcm_list,geom_tot                                                                                                                                     \n"+
       "##############################################################################################                                                                   \n"+
       "def rcm_analysis(nrg2,bh_f2,rcm_list,geom_tot,options):#cross check geoms with center of mass                                                                    \n"+
       "     var_ = options[14]                                                                                                                                          \n"+
       "     atom_types = []                                                                                                                                             \n"+
       "     data = []                                                                                                                                                   \n"+
       "     if geom_tot ==[]:                                                                                                                                           \n"+
       "         print>>savef, '\\n\\nNo unique files found decrease nrg var, all files moved to doubles'                                                                  \n"+
       "         return nrg2                                                                                                                                             \n"+
       "     for i in range(len(geom_tot[0])):#just first atom                                                                                                           \n"+
       "         if geom_tot[0][i][0] in atom_types:                                                                                                                     \n"+
       "             pass                                                                                                                                                \n"+
       "         else:                                                                                                                                                   \n"+
       "             atom_types.append(geom_tot[0][i][0])                                                                                                                \n"+
       "     for j in range(len(geom_tot)):                                                                                                                              \n"+
       "         atom_data = []                                                                                                                                          \n"+
       "         for i in range(len(atom_types)):                                                                                                                        \n"+
       "             geom_dat = []                                                                                                                                       \n"+
       "             for k in range(len(geom_tot[j])):                                                                                                                   \n"+
       "                 if geom_tot[j][k][0] == atom_types[i]:                                                                                                          \n"+
       "                     geom_dat.append(rcm_list[j][k])                                                                                                             \n"+
       "             atom_data.append(geom_dat)                                                                                                                          \n"+
       "         data.append(atom_data)                                                                                                                                  \n"+
       "     for i in range(len(data)):#file i                                                                                                                           \n"+
       "         for j in range(len(data)):#file j                                                                                                                       \n"+
       "             pass_ =0                                                                                                                                            \n"+
       "             for k in range(len(data[i])):#every atom                                                                                                            \n"+
       "                 if j>i:                                                                                                                                         \n"+
       "                     data[i][k].sort() #rcm values                                                                                                               \n"+
       "                     data[j][k].sort()                                                                                                                           \n"+
       "                     for l in range(len(data[i][k])):                                                                                                            \n"+
       "                         dev = data[i][k][l] - data[j][k][l]                                                                                                     \n"+
       "                         if abs(dev)>var_:                                                                                                                       \n"+
       "                             pass_ = 1 # file i is not file j                                                                                                    \n"+
       "             if pass_ ==0 and j>i: #file are the same                                                                                                            \n"+
       "                 if nrg2[i] > nrg2[j]:                                                                                                                           \n"+
       "                     nrg2[i] =4                                                                                                                                  \n"+
       "                 else:                                                                                                                                           \n"+
       "                     nrg2[j] = 4                                                                                                                                 \n"+
       "     return nrg2                                                                                                                                                 \n"+
       "##############################################################################################                                                                   \n"+
       "def r_cm(geom):#grab the rcm                                                                                                                                     \n"+
       "    #find the center of mass                                                                                                                                     \n"+
       "    rx = 0                                                                                                                                                       \n"+
       "    ry = 0                                                                                                                                                       \n"+
       "    rz = 0                                                                                                                                                       \n"+
       "    m = 0                                                                                                                                                        \n"+
       "    geom = geom_con_ltn(geom)                                                                                                                                    \n"+
       "    geom = geom_con_ntm(geom)                                                                                                                                    \n"+
       "    for i in range(len(geom)):                                                                                                                                   \n"+
       "        rx+=geom[i][1]*geom[i][0]                                                                                                                                \n"+
       "        ry+=geom[i][2]*geom[i][0]                                                                                                                                \n"+
       "        rz+=geom[i][3]*geom[i][0]                                                                                                                                \n"+
       "        m+=geom[i][0]                                                                                                                                            \n"+
       "    geom = geom_con_mtn(geom)                                                                                                                                    \n"+
       "    geom = geom_con_ntl(geom)                                                                                                                                    \n"+
       "    rx = rx/float(m)                                                                                                                                             \n"+
       "    ry = ry/float(m)                                                                                                                                             \n"+
       "    rz = rz/float(m)                                                                                                                                             \n"+
       "    rcm = [rx,ry,rz]                                                                                                                                             \n"+
       "    return rcm                                                                                                                                                   \n"+
       "##############################################################################################                                                                   \n"+
       "def geom_con_ntl(geom): #converters                                                                                                                              \n"+
       "    atoms=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg',                                                                                                \n"+
       "           'Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','v','Cr','Mn',                                                                                         \n"+
       "           'Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr',                                                                                     \n"+
       "           'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb',                                                                                      \n"+
       "           'Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd',                                                                                      \n"+
       "           'Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir',                                                                                      \n"+
       "           'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac',                                                                                          \n"+
       "           'Th','Pa','U']                                                                                                                                        \n"+
       "    for i in range(len(geom)):                                                                                                                                   \n"+
       "        a=int(geom[i][0])-1                                                                                                                                      \n"+
       "        geom[i][0]=atoms[a]                                                                                                                                      \n"+
       "    return geom                                                                                                                                                  \n"+
       "##############################################################################################                                                                   \n"+
       "def geom_con_ltn(geom):                                                                                                                                          \n"+
       "    atoms=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg',                                                                                                \n"+
       "           'Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','v','Cr','Mn',                                                                                         \n"+
       "           'Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr',                                                                                     \n"+
       "           'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb',                                                                                      \n"+
       "           'Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd',                                                                                      \n"+
       "           'Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir',                                                                                      \n"+
       "           'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac',                                                                                          \n"+
       "           'Th','Pa','U']                                                                                                                                        \n"+
       "    for i in range(len(geom)):                                                                                                                                   \n"+
       "        is_atom = 0                                                                                                                                              \n"+
       "        for j in range(len(atoms)):                                                                                                                              \n"+
       "            if is_atom == 0:                                                                                                                                     \n"+
       "                if geom[i][0][:2].replace('-','') == atoms[j]:                                                                                                   \n"+
       "                    geom[i][0] = float(j + 1)                                                                                                                    \n"+
       "                    is_atom = 1                                                                                                                                  \n"+
       "    return geom                                                                                                                                                  \n"+
       "##############################################################################################                                                                   \n"+
       "def geom_con_ntm(geom):                                                                                                                                          \n"+
       "    atoms_mass = [1,4,7,9,11,12,14,16,19,20,23,24,27,28,31,32,                                                                                                   \n"+
       "                  35,40,39,40,45,48,51,52,55,56,59,58,63,64,69,                                                                                                  \n"+
       "                  74,75,80,79,84,85,88,89,90,93,98,98,102,103,106,                                                                                               \n"+
       "                  107,114,115,120,121,130,127,132,133,138,139,140,                                                                                               \n"+
       "                  141,142,145,152,153,158,159,164,165,166,169,174,175,                                                                                           \n"+
       "                  180,181,184,187,192,193,195,197,202,205,208,209,209,                                                                                           \n"+
       "                  210,222,223,226,227,232,231,238]                                                                                                               \n"+
       "    for i in range(len(geom)):                                                                                                                                   \n"+
       "        index  = int(geom[i][0])                                                                                                                                 \n"+
       "        geom[i][0] = atoms_mass[index-1]                                                                                                                         \n"+
       "    return geom                                                                                                                                                  \n"+
       " ##############################################################################################                                                                  \n"+
       "def geom_con_mtn(geom):                                                                                                                                          \n"+
       "    atoms_mass = [1,4,7,9,11,12,14,16,19,20,23,24,27,28,31,32,                                                                                                   \n"+
       "                  35,40,39,40,45,48,51,52,55,56,59,58,63,64,69,                                                                                                  \n"+
       "                  74,75,80,79,84,85,88,89,90,93,98,98,102,103,106,                                                                                               \n"+
       "                  107,114,115,120,121,130,127,132,133,138,139,140,                                                                                               \n"+
       "                  141,142,145,152,153,158,159,164,165,166,169,174,175,                                                                                           \n"+
       "                  180,181,184,187,192,193,195,197,202,205,208,209,209,                                                                                           \n"+
       "                  210,222,223,226,227,232,231,238]                                                                                                               \n"+
       "    for i in range(len(geom)):                                                                                                                                   \n"+
       "        for j in range(len(atoms_mass)):                                                                                                                         \n"+
       "            if int(geom[i][0]) == atoms_mass[j]:                                                                                                                 \n"+
       "                geom[i][0] = int(j+1)                                                                                                                            \n"+
       "    return geom                                                                                                                                                  \n"+
       "##############################################################################################                                                                   \n"+
       "def rem(fn):#remove a file                                                                                                                                       \n"+
       "    try:                                                                                                                                                         \n"+
       "        os.system('rm '+fn)                                                                                                                                      \n"+
       "    except:                                                                                                                                                      \n"+
       "        pass                                                                                                                                                     \n"+
       "##############################################################################################                                                                   \n"+
       "def run_g09(command, timeout): #call g09 and calc                                                                                                                \n"+
       "    start = datetime.datetime.now()                                                                                                                              \n"+
       "    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)                                                                          \n"+
       "    while process.poll() is None:                                                                                                                                \n"+
       "      time.sleep(0.1)                                                                                                                                            \n"+
       "      now = datetime.datetime.now()                                                                                                                              \n"+
       "      if (now-start).microseconds/float(1000000)+(now-start).seconds+(now-start).days*float(24*60*60)>=timeout:                                                  \n"+
       "        try:                                                                                                                                                     \n"+
       "            os.kill(process.pid+1, signal.SIGKILL)                                                                                                               \n"+
       "            os.waitpid(-1, os.WNOHANG)                                                                                                                           \n"+
       "        except:                                                                                                                                                  \n"+
       "            try:                                                                                                                                                 \n"+
       "                os.kill(process.pid, signal.SIGKILL)                                                                                                             \n"+
       "                os.waitpid(-1, os.WNOHANG)                                                                                                                       \n"+
       "            except:                                                                                                                                              \n"+
       "                pass                                                                                                                                             \n"+
       "        return None                                                                                                                                              \n"+
       "    return process.stdout.read()                                                                                                                                 \n"+
       "##############################################################################################                                                                   \n"+
       "def time_g09(filename,st):#if u shut of rjob wall time                                                                                                           \n"+
       "    if st != 0:                                                                                                                                                  \n"+
       "        a=run_g09(['g09',filename],st)                                                                                                                             \n"+
       "    else:                                                                                                                                                        \n"+
       "        os.system('g09 '+filename)                                                                                                                               \n"+
       "##############################################################################################                                                                   \n"+
       "def move_f(fname,locat):                                                                                                                                         \n"+
       "    try:                                                                                                                                                         \n"+
       "        os.system('mv ' +fname+ ' '+locat)                                                                                                                       \n"+
       "    except:                                                                                                                                                      \n"+
       "        pass                                                                                                                                                     \n"+
       "##############################################################################################                                                                   \n"+
       "def dir(locat):                                                                                                                                                  \n"+
       "    try:                                                                                                                                                         \n"+
       "        os.system('mkdir '+locat)                                                                                                                                \n"+
       "    except:                                                                                                                                                      \n"+
       "        pass                                                                                                                                                     \n"+
       "##############################################################################################                                                                   \n"+
       "def print_quote(): #super sweet and sexy science quotes                                                                                                          \n"+
       "    quotes=[ \n"+                                                                                                                                                
       "        '\\nMike sucks at Karate because his Sensee is a White guy,\\nCasual Rascims FTW', \n"+
       "        '\\nI am not very good at teaching stupid people, ie Moe', \n"+
       "        '\\nHave I fired you yet today?\\n - S. Hopkins\\n', \n"+
       "        '\\nH                                                        He\\n'+ \n"+
       "        'Li Be                                  B   C  N   O  F   Ne\\n'+ \n"+
       "        'Na Mg                                  Al  Si P   S  Cl  Ar\\n'+ \n"+
       "        'K  Ca    Sc Ti V  Cr Mn Fe Co Ni Cu Zn Ga  Ge As  Se Br  Kr\\n'+ \n"+
       "        'Rb Sr    Y  Zr Nb Mo Tc Ru Rh Pd Ag Cd In  Sn Sb  Te I   Xe\\n'+  \n"+
       "        'Cs Ba *  Lu Hf Ta W  Re Os Ir Pt Au Hg Tl  Pb Bi  Po At  Rn\\n'+ \n"+
       "        'Fr Ra *  Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Uut Fl Uup Lv Uus Uus\\n'+ \n"+
       "        '\\n'+ \n"+
       "        '      *  La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho  Er Tm  Yb\\n'+ \n"+
       "        '      *  Ac Th Pa U  Np Pu Am Cm Bk Cf Es  Fm Md  No\\n', \n"+
       "        '\\nHello, my name is Basin Hopkins\\n', \n"+
       "        '\\nShut up Moe, no one likes you\\n', \n"+
       "        '\\n\\\\              / \\n'+ \n"+
       "        ' \\\\            / \\n'+ \n"+
       "        '  \\\\          / \\n'+ \n"+
       "        '   \\\\        / \\n'+ \n"+
       "        '    \\\\      / \\n'+ \n"+
       "        '     \\\\    / \\n'+ \n"+
       "        '      \\\\  / \\n'+ \n"+
       "        '       \\\\/ \\n'+ \n"+
       "        '\\nV for Vandium!\\n', \n"+
       "        '\\n\\\\                            / \\n'+ \n"+
       "        ' \\\\            /\\\\            /\\n'+ \n"+
       "        '  \\\\          /  \\\\          /\\n'+ \n"+
       "        '   \\\\        /    \\\\        /\\n'+ \n"+
       "        '    \\\\      /      \\\\      /\\n'+ \n"+
       "        '     \\\\    /        \\\\    /\\n'+ \n"+
       "        '      \\\\  /          \\\\  /\\n'+ \n"+
       "        '       \\\\/            \\\\/\\n'+ \n"+
       "        '\\nT for Tugnsten!\\n', \n"+
       "        '           /~~\\\\\\n          |<><>|\\n          /_/\\\\_\\\\              %s, I am your Father!\\n'+\n"%(sname)+
       "        '          /\\___/\\\\\\n         // [ ]|\\\\\\\\  #/\\n        //| [_]| \\\\\\\\//\\n'+\n"+
       "        '        \\\\\\\\|    |\\n         \\\\#====|\\n         /|\\\\  /I\\\\\\n        / | || I \\\\\\n'+\n"+
       "        '       /  | || |  \\\\\\n      /   | || |   \\\\\\n     /    | || |    \\\\\\n',\n"+
       "        '\\nWhy do French people eat omelts with only one egg?\\n'+ \n"+
       "        'Because an egg is en uff!\\n', \n"+
       "        '\\nHonesty hurts, so I wont say anything\\n', \n"+
       "        '\\nIf you set the bar high enough, you can just walk under it.\\n', \n"+
       "        '\\nDuffman. Oooohh Yaaaa!!!\\n -Duffman\\n', \n"+
       "        '\\nDoh!\\n-H. Simpson\\n', \n"+
       "        '\\nIm Batman\\n -Batman\\n', \n"+
       "        '\\nMe fail inglish? Thats umpossible!\\n -R.W\\n', \n"+
       "        '\\nWhat do you call an alligator in a vest?\\nAn In-vest-igator\\n', \n"+
       "        '\\nNever trust an atom, they make up everything\\n -Mabel,she tried.\\n', \n"+
       "        '\\nFluorine\\nUranium\\nCarbon\\nPotassium\\nYttrium\\nOxygen\\nUranium\\n', \n"+
       "        '\\nAlcohol is the cause of and solution to all of lifes problems\\n', \n"+
       "        '\\nIf the facts do not fit the theory, change the facts!\\n', \n"+
       #"        '\\nYo Yo Yo, Whats Up Broffessor!!!\\n', \n"+
       "        '\\nComplaints? Call our customer suport and yell all you want at 1-226-338-2608.\\n', \n"+
       "        '\\nA word to the wise is not necessary \\n- it is the stupid ones that need advice\\n', \n"+
       "        '\\nWhere is Waldo?\\nGetting coffee!\\n', \n"+
       "        '\\nI cook with wine, some times I even add food to it.\\n', \n"+
       "        '\\nYou must be part of the fabric of space time because your'+ \n"+
       "        ' curves are attracting me ;)\\n', \n"+
       "        '\\nLittle Red Ridding Fume Hood\\n', \n"+
       "        '\\n6.02*10^23 Dalmations, another great movie\\n', \n"+
       "        '\\nThe names bond, Ionic Bond, taken not shared\\n', \n"+
       "        '\\nI only get confused when I think\\n', \n"+
       "        '\\nIf you see this quote go for coffee!\\n', \n"+
       "        '\\nLecoors light, ice cold\\n', \n"+
       "        '\\nError: Termination in Basin Hopping,\\nNo brain in operator'+ \n"+
       "        ' detected!\\nCut hair and try again!\\n', \n"+
       "        '\\nI hate dairy jokes, because they are so cheesy\\n'+ \n"+
       "        'I think I should use utter jokes, and stop milking this one.\\n', \n"+
       "        '\\Moaraj your programm doesnt work\\n-People who basin hop\\n' \n"+
       "        '\\nI thought I was an alcholic, but then I went drinking with'+ \n"+
       "        ' my Irish friends,\\nnow I know I am just a casual social drinker\\n', \n"+
       "        '\\nI am going to get chinese food with my friend Zang,\\n'+ \n"+
       "        'he just calls it food though...', \n"+
       "        '\\nI am so good at Kung Foo I can split an atom!\\n', \n"+
       "        '\\n\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\n waves are cool\\n', \n"+
       "        '\\nMabel needs to make a quote!\\n -Not Mabel\\n', \n"+
       "        '\\nI told a chemistry joke and I got no reaction\\n', \n"+
       "        '\\nI got my ion you!\\n', \n"+
       "        '\\nHey man do you have and sodium hypobromite?\\nNaBrO\\n', \n"+
       "        '\\nI blew up my chemistry experiment\\nOxidents happen\\n', \n"+
       "        '\\nUsing energy makes me m*a*d\\n', \n"+
       "        '\\nMake your own dam quote!\\n', \n"+
       "        '\\n  (\\\\_/)    (\\\\_/)    (\\\\_/)    (\\\\_/) \\n'\n"+
       "        ' (\\' . \\')  (\\' . \\')  (\\' . \\')  (\\' . \\')\\n'\n"+
       "        '(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')\\n' \n"+
       "        '\\n  (\\\\_/)    (\\\\_/)    (\\\\_/)    (\\\\_/) \\n'\n"+
       "        ' (\\' . \\')  (\\' . \\')  (\\' . \\')  (\\' . \\')\\n'\n"+
       "        '(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')\\n' \n"+
       "        '\\n  (\\\\_/)    (\\\\_/)    (\\\\_/)    (\\\\_/) \\n'\n"+
       "        ' (\\' . \\')  (\\' . \\')  (\\' . \\')  (\\' . \\')\\n'\n"+
       "        '(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')\\n' \n"+
       "        '\\n  (\\\\_/)    (\\\\_/)    (\\\\_/)    (\\\\_/) \\n'\n"+
       "        ' (\\' . \\')  (\\' . \\')  (\\' . \\')  (\\' . \\')\\n'\n"+
       "        '(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')\\n' \n"+
       "        '\\n  (\\\\_/)    (\\\\_/)    (\\\\_/)    (\\\\_/) \\n'\n"+
       "        ' (\\' . \\')  (\\' . \\')  (\\' . \\')  (\\' . \\')\\n'\n"+
       "        '(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')(\\'\\')-(\\'\\')\\n', \n"+
      # "        '\\nAll my friends are dead!\\n', \n"+
       "        '\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n-Someone with nothing to say\\n', \n"+
       "        '\\nChallenges are what make life interesting, and overcoming them '+ \n"+
       "        '\\nis what makes life meaningful\\n-dead white guy', \n"+
       "        '\\nObama is not the young socialist muslim he used to be\\n', \n"+
       "        '\\nThere is no stupid questions just Stupid people, like you!\\n', \n"+
       "        '\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe'+ \n"+
       "        '\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe'+ \n"+
       "        '\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe'+ \n"+
       "        '\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe\\nMoe', \n"+
       "        '\\nMoe Moe Moe Moe Moe\\nMoe Moe Moe Moe Moe Moe Moe\\nMoe Moe'+ \n"+
       "        ' Moe Moe Moe\\n\\n-A Moenificiant Haiku\\n', \n"+
       "        '\\nWhat does magikarp even do!?!!!!?!!!\\n', \n"+
       "        '\\nAtomic Theory is very Bohring\\n', \n"+
       "        '\\nWhat is the coolest element on the Periodic Table?\\nBromine Duh.\\n -G.F.\\n', \n"+
       "        '       |       |      \\n'+ \n"+
       "        '  \\\\/   |       |\\n'+ \n"+
       "        '  /\\\\   |       |\\n'+ \n"+
       "        '_______|_______|_______\\n'+ \n"+
       "        '   __  |  __   |       \\n'+ \n"+
       "        '  |  | | |  |  |  \\\\/      \\n'+ \n"+
       "        '  |__| | |__|  |  /\\\\       \\n'+ \n"+
       "        '_______|_______|_______\\n'+ \n"+
       "        '       |       |\\n'+ \n"+
       "        ' \\\\/    |       |\\n'+ \n"+
       "        ' /\\\\    |       |\\n'+ \n"+
       "        '       |       |\\n'+ \n"+
       "        '\\nLike you never screw around at work\\n' \n"+
       "        ] \n"+
       "    i = randint(0,len(quotes)-1) \n"+
       "    return quotes[i] \n"+
       "##############################################################################################\n",
	   
       "******************************************** \n"+
       "house keeping \n"+
       "----------------- \n"+
       "initial file(.gjf) and where to save the nrg data(.txt) and where to save restart info(.sav) \n"+
       "int_file:/scratch/%s/6Cl2mq_1w_1.gjf-end \n"%(sname)+
       "sav_file:/scratch/%s/bh.sav-end \n"%(sname)+
       "save as:/scratch/%s/data.txt-end \n"%(sname)+
       "------------------ \n"+
       "steps =5-end \n"+
       "box size = 10.0-end \n"+
       "temp = 300-end\n"+
       "--------------- \n"+
       "Analysis info\n"+
       "nrg var = 0.000001-end\n"+
       "geom var = 0.5-end\n"+
       " \n"+
       "--------------- \n"+
       "method? see below for possiblities \n"+
       "method = rand_rot 3 1 20 0.4-end \n"+
       " \n"+
       "***************************************** \n"+
       " \n"+
       "Possible Methods \n"+
       "rand_trans => random translation for last n atoms at m times with step = l  \n"+
       "	method_= rand_trans 3 2 0.2 -end \n"+
       "	 # rand_trans (group size) (number of groups) (translation step) atom groups must be at last atoms in geometry\n"+
       "rand_rot => random rotation about random axis \n"+
       "	method_ = rand_rot 3 2 20 0.4 -end \n"+
       "	# rand_rot (group size) (number of groups) (rotation angle) (translation step) atom groups must be at last atoms in geometry \n"+
       "dihedral_rot => randomly rotates across the dihedral angle, required user input \n"+
       "	method_= dihedral_rot 45 2-3(4,5,6) end \n"+
       "	# dihedral_rot (dihedral angle) (atoms the define axis ie 2-3)(atoms effected by the rotations) add as many groups as you like\n"+
       "gen_rot => randomly rotate about the cm any atoms in geom \n"+
       "	method_= gen_rot 45 0.7 (2,3,4) (4,5,6) end \n"+
       "	#gen_rot (rotation angle) (translation step) (groups of atoms) note translation step can be 0 but rand_rot is faster in this case \n"+
       "gen_move => combo of gen_rot and dihedral \n"+
       "	method_ = gen_move 45 20 0.7 (4,5,6)r (1,2,3)r 7-8(1,2,3,4,5,6) end \n"+
       "	#gen_move (dihedral angle) (rot angle) (translation step) (rotation group)r 1-2(dihedral group with atoms 1-2 as axis)\n"+
       "ulti_move => combo of gen_rot and dihedral and trans with each group having its own paramaters \n"+
       "	method_ = ultu_move (0.7)(7)t (45,0.7)(4,5,6)r (34,0.9)(1,2,3)r 7-8(1,2,3,4,5,6)(20) end \n"+
       "	#ulti_move (translation step)(atoms)t (rotation angle,translation step)(rotation group)r 1-2(dihedral group with atoms 1-2 as axis)(diheadral angle)\n"+
       " \n"+
       " \n"+
       "****************************************** \n"+
       "Additional options can be seen in the read me\n\n"+
       "\nTo check this file for errors type in the shell: python ipf_check.py, then follow the instructions\n"+
       " \n"+
       "Questions? Concerns? Quotes? Coffee? \n"+
       "send me an email at moaraj.hasan@gmail.com for further help, please include the ipf.txt file and the calc_summary.txt file. \n"+
       " \n",
       "def custom(geom): #return 0 if fail 1 if pass\n"+
       "    return 1 \n"+
       "def r_cm(geom): \n"+
       "    #find the center of mass \n"+
       "    rx = 0 \n"+
       "    ry = 0 \n"+
       "    rz = 0 \n"+
       "    m = 0 \n"+
       "    geom = geom_con_ltn(geom) \n"+
       "    geom = geom_con_ntm(geom) \n"+
       "     \n"+
       "    for i in range(len(geom)): \n"+
       "        rx+=geom[i][1]*geom[i][0] \n"+
       "        ry+=geom[i][2]*geom[i][0] \n"+
       "        rz+=geom[i][3]*geom[i][0] \n"+
       "        m+=geom[i][0] \n"+
       "     \n"+
       "    geom = geom_con_mtn(geom) \n"+
       "    geom = geom_con_ntl(geom) \n"+
       "    rx = rx/float(m) \n"+
       "    ry = ry/float(m) \n"+
       "    rz = rz/float(m) \n"+
       "    rcm = [rx,ry,rz] \n"+
       "    return rcm \n"+
       "     \n"+
       "     \n"+
       "         \n"+
       "def geom_con_ntl(geom): \n"+
       "    atoms=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg', \n"+
       "           'Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','v','Cr','Mn', \n"+
       "           'Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr', \n"+
       "           'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb', \n"+
       "           'Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd', \n"+
       "           'Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir', \n"+
       "           'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac', \n"+
       "           'Th','Pa','U'] \n"+
       "     \n"+
       "    for i in range(len(geom)): \n"+
       "        a=int(geom[i][0])-1 \n"+
       "        geom[i][0]=atoms[a] \n"+
       "         \n"+
       "    return geom \n"+
       " \n"+
       " \n"+
       "def geom_con_ltn(geom): \n"+
       "    atoms=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg', \n"+
       "           'Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','v','Cr','Mn', \n"+
       "           'Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr', \n"+
       "           'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb', \n"+
       "           'Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd', \n"+
       "           'Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir', \n"+
       "           'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac', \n"+
       "           'Th','Pa','U'] \n"+
       " \n"+
       "    for i in range(len(geom)): \n"+
       "        is_atom = 0 \n"+
       "        for j in range(len(atoms)): \n"+
       "            if is_atom == 0: \n"+
       "                if geom[i][0][:2].replace('-','') == atoms[j]: \n"+
       "                    geom[i][0] = float(j + 1) \n"+
       "                    is_atom = 1 \n"+
       "        #if is_atom == 0: \n"+
       "             \n"+
       " \n"+
       "    return geom \n"+
       " \n"+
       " \n"+
       "def geom_con_ntm(geom): \n"+
       "    atoms_mass = [1,4,7,9,11,12,14,16,19,20,23,24,27,28,31,32, \n"+
       "                  35,40,39,40,45,48,51,52,55,56,59,58,63,64,69, \n"+
       "                  74,75,80,79,84,85,88,89,90,93,98,98,102,103,106, \n"+
       "                  107,114,115,120,121,130,127,132,133,138,139,140, \n"+
       "                  141,142,145,152,153,158,159,164,165,166,169,174,175, \n"+
       "                  180,181,184,187,192,193,195,197,202,205,208,209,209, \n"+
       "                  210,222,223,226,227,232,231,238] \n"+
       " \n"+
       "    for i in range(len(geom)): \n"+
       "        index  = int(geom[i][0]) \n"+
       "        geom[i][0] = atoms_mass[index-1] \n"+
       "    return geom \n"+
       "def geom_con_mtn(geom): \n"+
       "    atoms_mass = [1,4,7,9,11,12,14,16,19,20,23,24,27,28,31,32, \n"+
       "                  35,40,39,40,45,48,51,52,55,56,59,58,63,64,69, \n"+
       "                  74,75,80,79,84,85,88,89,90,93,98,98,102,103,106, \n"+
       "                  107,114,115,120,121,130,127,132,133,138,139,140, \n"+
       "                  141,142,145,152,153,158,159,164,165,166,169,174,175, \n"+
       "                  180,181,184,187,192,193,195,197,202,205,208,209,209, \n"+
       "                  210,222,223,226,227,232,231,238] \n"+
       " \n"+
       "    for i in range(len(geom)): \n"+
       "        for j in range(len(atoms_mass)): \n"+
       "            if int(geom[i][0]) == atoms_mass[j]: \n"+
       "                geom[i][0] = int(j+1) \n"+
       " \n"+
       "    return geom \n"+
       " \n"+
       " \n",
       "from engin import ipf_open\n"+
       "def checker(ipf_name):\n"+
       "    options = ipf_open(ipf_name)\n"+
       "    if options == 0:\n"+
       "        return 0\n"+
       "    print 'Steps =',options[0],'   end of steps'\n"+
       "    print 'Box Size =',options[4],'end of Box Size'\n"+
       "    print 'Temperature =',options[8],'end of Temp'\n"+
       "    print 'Energy term =',options[9],'end of Energy term'\n"+
       "    print 'Restart =',options[2],'end of Restart'\n"+
       "    print 'Inital File =',options[3],'end of Inital File'\n"+
       "    print 'Data File =',options[5],'end of Data file'\n"+
       "    print 'Save File =',options[6],'end of Save file'\n"+
       "    print 'Method =',options[1][0],'end of Method'\n"+
       "    print 'Connectivity =',options[7],'end of Connectivity'\n"+
       "    print 'Key Words =',options[10],'end of Key words'\n"+
       "    print 'Custom Check =',options[11],'end of Custom Check'\n"+
       "    print 'Job wall time =',options[12],'end of Job wall time'\n"+
       "    print 'Energy Variance =',options[13],'end of Energy Variance'\n"+
       "    print 'Geometry Variance =',options[14],'end of Geometry Variance'\n"+
       "    print 'Turn off Quotes =',options[15],'end of Turn of quotes'\n"+
       "    print 'Shortest Bond lenght =',options[16],'end of Shortest Bond length'\n"+
       "    print 'Back Step =',options[17],'end of Back Step'\n"+
       "    print 'Movement Tries =',options[18],'end of Movement tries'\n"+
       "    print 'Save every =',options[19],' steps'\n"+
       "    print 'Make gjfs? =',options[23],'end of mkgjf'\n"+
       "    print 'kill? =',options[24],' end of kill'\n"+
       "ipfname = raw_input('Input File Name:')\n"+
       "checker(ipfname)\n",
       "from engin import *\n"+
       "def bh():\n"+
       "    Basin_hop('/scratch/%s/Bh_ipf.txt','bh')\n"%(sname)+
       "bh() \n",
       "%chk=/scratch/mjlecour/_name_.chk\n"+
       "%mem=2gb\n"+
       "%nprocs=8\n"+
       "# opt freq upbe1/pbe\n"+
       "\n"+
       "_name_ DFT OPT\n"+
       "\n"+
       "1 1\n"+
       "Geom\n"+
       "\n"+
       "Basis Set\n"+
       "and stuf lol\n"+
       "\n",
       "Readme includes all the aditional options for Bhv3.0\n"+
       "******************************************\n"+
       "extra options, example of how to turn them on\n"+
       "Add these lines anywhere in the ipf.txt file.\n"+
       "\n"+
       "turn off quotes = yes-end #yes you can turn off the quotes\n"+
       "\n"+
       "custom check =yes-end #use your own custom geom check\n"+
       "\n"+
       "restart = -yes-end #restart from .sav file\n"+
       "\n"+
       "back step = 20-end #number of times a step can fail before retrying step b4 it\n"+
       "\n"+
       "save on step = 100-end #adjust when you write to the .sav file, default is 100\n"+
       "\n"+
       "job wall time = 23 -end #give each step a wall time in seconds\n"+
       "\n"+
       "shortest bond = 0.7-end #closest 2 atoms can come together in the gjf\n"+
       "\n"+
       "nrg term = \\\\-end #is \\\\ by default\n"+
       "\n"+
       "connectivity:\n"+
       "data\n"+
       "-end #place to put the connectivity read from int gjf as default setting\n"+
       "\n"+
       "header = #keywords-end # read from gjf as default\n"+
       "\n"+
       "make gjf = template.txt-end #make dft gjfs out of unique files following the template.txt, \n"+
       "in make gjf, _name_ is replaced by the name of the file. Geom is replaced by the log file geometry.\n"+ 
       "\n"+
       "number of tries = 10000-end #times the method can try and make a good geom to be calculated by g09. \n"+
       "\n"+
       "kill = 6-10 0-days 0-hours 0-min 0-sec -end #if the job does not complete 6% of the steps in 10% of the\n"+
       "time then kill it. put in the wall time that you would give sharcnet. Only need one of -days,-hours,-min,-sec\n"+
       "\n"+
       "Good luck if you think of any more helpful options/quotes email me at moaraj.hasan@gmail.com\n"
       ]
    for i in range(len(fname)):
        opf = open(fname[i],'w')
        print>>opf,a[i]
sname = raw_input('Sharcnet User Name:')
install(sname)
