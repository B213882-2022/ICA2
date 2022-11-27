#! /usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os, sys, time
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# make pandas able to display all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# set working directory
while True:  # ask users
    print('\nInvalid directory name will be regarded as a new folder name for current directory!')
    wd = input(
        '\nEnter a directory where you want to save your files:\
        \n(e.g. "new_folder" or "./new_folder" to create new folder under current directory)\
        \n(e.g. "/folder1/folder2" to use absolute directory)\
        \n(Press "Enter" to use [current directory] by default)\
        \n(Enter "exit" to quit programme)\n'
    ).strip()
    if len(wd) == 0:
        wd = os.getcwd()
        break
    elif len(wd) > 50:
        print('\nThat is too long! Try to limit it no more than 50 characters!')
    elif wd.lower() == 'exit' or wd.lower() == 'quit':
        print('\nGoodbye!')
        sys.exit()
    else:
        try:
            wd = os.path.abspath(wd)
            os.makedirs(wd, exist_ok=True)
            print('\nSetting your working directory to: ' + wd)
            os.chdir(wd)
            break
        except Exception as result:
            print('\nSomething goes wrong...\nHere is the error message: ' + str(result))
            while True:
                r = input('\nDo you want to try again? ([yes]/no) ').strip().lower()
                if r == 'yes' or len(r) == 0:
                    break
                elif r == 'no':
                    print('\nGoodbye!')
                    sys.exit()
                else:
                    print('\nOnly "yes" or "no" can be chosen!')

# get sequences
while True:
    print('\nOnly support analysis with a single protein family from a single taxonomic group.')
    while True:  # Use exit sequences? or get from Enterz?
        selection = input('Do you need to get sequences from Entrez?\
                          \n [Yes], I do. (Enter "yes")\
                          \n No, I already have one. (Enter "no")\
                          \n I want to quit programme. (Enter "exit")\n').strip().lower()
        if selection == 'yes' or len(selection) == 0:
            select_code = 1
            break
        elif selection == 'no':
            select_code = 2
            # get file
            while True:
                print('\nYour current working directory is: ' + wd)
                fa_name = input(
                            'Enter your filename (Fasta) in the working directory\
                            \n(e.g. "file1.fa" or "folder1/file1.fa" or "./folder1/file1" to find file under current directory\
                            \n(e.g. "/folder1/folder2" to find file using absolute directory)\
                            \n(Enter "exit" to quit programme)\
                            \nMake sure it is a VALID FASTA-format file, otherwise the programme will fail: \n'
                            ).strip()
                fa_dir = os.path.abspath(fa_name)
                if len(fa_name) == 0:
                    print('\nTry entering a name please. Or you can enter "exit" to quit')
                elif len(fa_name) > 100:
                    print('\nToo long! Make a shorter input or change your file directory')
                elif fa_name.lower() == 'exit' or fa_name.lower() == 'quit':
                    print('\nGoodbye!')
                    sys.exit()
                elif os.path.exists(fa_dir) == False:
                    print('\nCan not find the file, check your input please!')
                elif subprocess.getoutput(r'cat %s | head' % (fa_dir)).startswith('>') == False:
                    print('\nIt is not a valid Fasta-format file, check your file again!')
                else:
                    break
            print('\nInput:\nTaxonomic Group: %s\nProtein Family Name: %s\nFile Directory: %s' % (taxo_name, family_name, fa_dir))
            break
        elif selection == 'exit' or selection == 'quit':
            print('\nGoodbye!')
            sys.exit()
        else:
            print('\nOnly "yes" or "no" or "exit/quit" can be chosen!')
    
    if select_code == 1:  # get sequences from Entrez
        # require target info from users
        print('\nOnly support one name for input. Multiple or invalid names may lead to failure in searching!')
        # get protein family name
        while True:
            family_name = input('\nEnter one protein family name: (e.g. Pyruvate dehydrogenase)\
                                 \n(Enter "exit" to quit programme)\n').strip()
            if len(family_name) == 0:
                print('\nTry entering a name please. Or you can enter "exit" to quit')
            elif len(family_name) > 50:
                print('\nI don\'t think there is such a long name for one protein family')
            elif family_name.isdigit():
                print('\nA name is needed, not a number!')
            elif family_name.lower() == 'exit' or family_name.lower() == 'quit':
                print('\nGoodbye!')
                sys.exit()
            else:
                break
        #get taxonomic group name/ID    
        while True:    
            taxo_name = input('\nEnter its taxonomic group name/ID: (e.g. ascomycete fungi/txid4890)\
                               \n(Enter "exit" to quit programme)\n').strip()
            if len(taxo_name) == 0:
                print('\nTry entering a name/ID please. Or you can enter "exit" to quit')
            elif len(taxo_name) > 50:
                print('\nI don\'t think there is such a long name/ID for one taxonomic group')
            elif taxo_name.lower() == 'exit' or taxo_name.lower() == 'quit':
                print('\nGoodbye!')
                sys.exit()
            else:
                if taxo_name.isdigit():
                    taxo_name = 'txid' + taxo_name
                    print('Your taxonomic group ID is: ' + taxo_name)
                break
        # get filename
        while True:
            fa_name = input('\nEnter a Fasta filename for the result:\
                             \n(e.g. "pyruvate_dehydrogenase.fa" or "./folder1/XX.fa")\
                             \n(Enter "exit" to quit programme)\n'
                         ).strip()
            fa_dir = os.path.abspath(fa_name)
            if len(fa_name) == 0:
                print('\nTry entering a name please. Or you can enter "exit" to quit')
            elif len(fa_name) > 50:
                print('\nI don\'t think it is necessary for such a long name...')
            elif fa_name.lower() == 'exit' or fa_name.lower() == 'quit':
                print('\nGoodbye!')
                sys.exit()
            elif subprocess.run(r'mkdir -p %s && touch %s' % (os.path.dirname(fa_dir), fa_dir), shell=True).returncode != 0:
                print('\nSomething goes wrong when creating file at: %s\
                       \nCheck your name / directory / permission for execution' % fa_dir)
            else:
                break

        print('\nInput:\nTaxonomic Group: %s\nProtein Family Name: %s\nFile Directory: %s' % (taxo_name, family_name, fa_dir))
        print('\nGetting protein sequence from NCBI Entrez database...\
               \n(some WARNINGs or ERRORs may happen due to Entrez, YOU DON\'T NEED TO DO ANYTHING!!)')
        fa_dir = wd + '/' + fa_name
        # get info from Entrez
        get_seq = 'esearch -db protein -query "%s[Organism] AND (%s[Protein Name] " | efetch -format fasta > %s' % (taxo_name, family_name, fa_dir)
        r = subprocess.run(get_seq, shell=True)
        if r.returncode == 0:
            if subprocess.getoutput(r'wc -l < %s' % (fa_dir)) == '0':
                while True:
                    r = input('\nIt seems nothing has come back...Would you like to try again? ([yes]/no)\n')
                    if r == 'yes' or len(r) == 0:
                        subprocess.run(r'rm -f %s' % (fa_dir), shell=True)
                        break
                    elif r == 'no':
                        print('\nGoodbye!')
                        subprocess.run(r'rm -f %s' % (fa_dir), shell=True)
                        sys.exit()
                    else:
                        print('\nOnly "yes" or "no" can be chosen!')
            else:
                print('\nSuccessful! Now all the sequences are in: ' + fa_dir)
                select_code = 2
        else:
            print('\nSomething goes wrong...' + '\nReturn code: ' + str(r.returncode))
            while True:
                r = input('\nDo you want to try again? ([yes]/no) ').strip().lower()
                if r == 'yes' or len(r) == 0:
                    break
                elif r == 'no':
                    print('\nGoodbye!')
                    subprocess.run(r'rm -f %s' % (fa_dir), shell=True)
                    sys.exit()
                else:
                    print('\nOnly "yes" or "no" can be chosen!')
    
    if select_code == 2:  # check sequences validity

        # deleting all '\n'  in fasta sequences
        temp_file = wd + '/temp_file'
        reformat = r"cat %s | tr -d '\n' | sed 's/>/\n>/g' | sed 's/]/]\n/g' | tail +2 > %s" % (fa_dir, temp_file)
        r = subprocess.run(reformat, shell=True)
        if r.returncode != 0:
            print('\nSomething goes wrong...' + '\nReturn code: ' + str(r.returncode))
            print('Wrong command: ' + r.args)
            sys.exit()
        
        # extract returned result
        descrip_command = 'grep ">" %s' % (temp_file)
        seq_descrip = subprocess.getoutput(descrip_command)
        protein_ids = re.findall(r'>([^\s]+)', seq_descrip)
        species = re.findall(r'\[(.*)\]', seq_descrip)

        # extract sequence
        seq_command = r'grep "^\w" %s' % (temp_file)
        seq_all = subprocess.getoutput(seq_command)
        seqs = seq_all.split('\n')

        # remove temp_file
        subprocess.run(r'rm -f %s' % (temp_file), shell=True)
        
        # use a dataframe (with sequence length in descending order) to store info
        seq_df = pd.DataFrame({'protein_id':protein_ids, 'species':species, 'sequence':seqs})
        s1 = seq_df['sequence'].apply(len)
        s1.name = 'seq_length'
        seq_df = pd.concat([seq_df,s1],axis=1).sort_values(by='seq_length', ascending=False)
        
        # count sequences with unknown amino acid 'X'
        def count_x(seqs):
            count = 0
            for i in seqs:
                if 'x' in i.lower():
                    count += 1
            return count
        x_number = count_x(list(seq_df['sequence']))
        
        # count species with multiple sequences
        if True in set(seq_df['species'].duplicated()):
            duplitcate_number = seq_df['species'].duplicated().value_counts()[True]
        else:
            duplitcate_number = 0
        
        # give brief summary
        print('\nSummary: ')
        print('Sequences Number: %d (%d of them are found containing unknown amino acid "X")' % (seq_df.shape[0], x_number))
        print('Species Number: %d (%d of them have multiple sequences)' % (len(set(seq_df['species'])), duplitcate_number))
        print('Brief information for sequences length:')
        print('\n'.join(str(seq_df['seq_length'].describe()).split('\n')[1:-1]))
        
        # check sequences number
        limit_code = 0
        if seq_df.shape[0] > 1000:  
            while True:
                r = input('\nWARNING: For subsequent processes, only at most 1000 sequences is available!\
                           \nYou can select one of the options:\
                           \n1. Exit programme and manually select 1000 sequences yourself\
                           \n2. Let system handle: (The longest 1000 sequences will be chosen)\
                           \n3. Re-fetch sequences or use existed Fasta file.\
                           \nEnter "1" or "2" or "3": ')
                if r == '1' or r == 'exit' or r == 'quit':
                    print('\nYou can go to %s to change your sequences now, goodbye!' % (fa_dir))
                    sys.exit()
                elif r == '2':
                    seq_df = seq_df.iloc[0:1000]
                    print('\nAntomatically select the longest 1000 sequences!')
                    print('\nSummary: ')
                    print('Sequences Number: %d (%d of them are found containing unknown amino acid "X")' % (seq_df.shape[0], x_number))
                    print('Species Number: %d (%d of them have multiple sequences)' % (len(set(seq_df['species'])), duplitcate_number))
                    print('Brief information for sequences length:')
                    print('\n'.join(str(seq_df['seq_length'].describe()).split('\n')[1:-1]))
                    break
                elif r == '3':
                    limit_code = 1
                    break
                elif len(r) == 0:
                    print('\nEnter something please...or type "quit" or "exit" to leave')
                else:
                    print('\nOnly "1" or "2" or "3" is available!')
        if limit_code == 1:
            continue
        
        # final check
        final_code = 0
        while True:
            r = input('\nDo you want to continue using the current sequences?\
                       \nyes: Continue!\
                       \nno: I want to input/fetch sequences again!\
                       \nexit: I want to quit programme!\
                       \n(Enter "yes" or "no" or "exit")\n').strip().lower()
            if r == 'yes':
                break
            elif r == 'no':
                final_code = 1
                break
            elif len(r) == 0:
                print('Enter something please...')
            elif r == 'exit' or r == 'quit':
                print('\nGoodbye!')
                subprocess.run(r'rm -f %s' % fa_dir, shell=True)
                sys.exit()
            else:
                print('\nChoose "yes" or "no" or "exit" please!')
        if final_code == 1:
            subprocess.run(r'rm -f %s' % fa_dir, shell = True)
            continue
        
        break

while True:  # select sequences
    # check how many sequences each species has?
    while True:  # ask from user
        r = input('\nDo you want check how many sequences each species has? yes/[no]/exit\n').strip().lower()
        if r == 'yes':
            print('\n'.join(str(seq_df['species'].value_counts()).split('\n')[1:-1]))
            break
        elif r == 'no':
            break
        elif len(r) == 0:
            print('"No" has been chosen')
            break
        elif r == 'exit' or r == 'quit':
            print('\nGoodbye!')
            sys.exit()
        else:
            print('\nOnly "yes" or "no" or "exit" is allowed')
            
    # check all info?
    while True:  # ask from user
        r = input('\nDo you want check all information in a table? yes/[no]/exit\n').strip().lower()
        if r == 'yes':
            print(pd.concat([seq_df[['protein_id','species','seq_length']],seq_df['sequence'].apply(lambda x: x[:10]+"...")],axis=1).sort_values(by='species').set_index('protein_id'))
            break
        elif r == 'no':
            break
        elif len(r) == 0:
            print('"No" has been chosen')
            break
        elif r == 'exit' or r == 'quit':
            print('\nGoodbye!')
            sys.exit()
        else:
            print('\nOnly "yes" or "no" or "exit" is allowed')
            
    # count sequences with unknown amino acid 'X'
    def count_x(seqs):
        count = 0
        for i in seqs:
            if 'x' in i.lower():
                count += 1
        return count
    x_number = count_x(list(seq_df['sequence']))
            
    # count species with multiple sequences
    if True in set(seq_df['species'].duplicated()):
        duplitcate_number = seq_df['species'].duplicated().value_counts()[True]
    else:
        duplitcate_number = 0

    drop_sth = 0
    # drop sequences with unknown amino acid "X" ?
    def no_x_in_seq(s):
        if 'x' in s.lower():
            return False
        else:
            return True
    if x_number != 0 :
        while True:
            print('\nSequence with unknown amino acid "X" are found!')
            drop = input('\nDo you want to drop sequences with unknown amino acid "X" ? yes/[no]/exit\n').strip().lower()
            if drop == 'yes':
                seq_df = seq_df.loc[seq_df['sequence'].apply(no_x_in_seq)]
                x_number = count_x(list(seq_df['sequence']))
                drop_sth = 1
                print('\nSequences with "X" dropped!')
                print('\nSummary: ')
                print('Sequences Number: %d (%d of them are found containing unknown amino acid "X")' % (seq_df.shape[0], x_number))
                print('Species Number: %d (%d of them have multiple sequences)' % (len(set(seq_df['species'])), duplitcate_number))
                print('Brief information for sequences length:')
                print('\n'.join(str(seq_df['seq_length'].describe()).split('\n')[1:-1]))
                break
            elif drop == 'no':
                break
            elif len(drop) == 0:
                print('"No" has been chosen')
                break
            elif drop == 'exit' or drop == 'quit':
                print('\nGoodbye!')
                sys.exit()
            else: 
                print('\nOnly "yes" or "no" or "exit"is allowed')
                        
    # drop duplicate?
    drop_duplicate = 0
    if duplitcate_number > 0: 
        while True:
            print('\nSpecies with multiple sequences are found!')
            drop = input('\nDo you want only the longest sequence of each species be chosen ? yes/[no]/exit\n').strip().lower()
            if drop == 'yes':
                seq_df = seq_df.loc[~seq_df['species'].duplicated()]
                duplitcate_number = 0
                drop_sth = 1
                print('\nAll species has only one sequence now!')
                print('\nSummary: ')
                print('Sequences Number: %d (%d of them are found containing unknown amino acid "X")' % (seq_df.shape[0], x_number))
                print('Species Number: %d (%d of them have multiple sequences)' % (len(set(seq_df['species'])), duplitcate_number))
                print('Brief information for sequences length:')
                print('\n'.join(str(seq_df['seq_length'].describe()).split('\n')[1:-1]))
                drop_duplicate = 1
                break
            elif drop == 'no':
                break
            elif len(drop) == 0:
                print('"No" has been chosen')
                break
            elif drop == 'exit' or drop == 'quit':
                print('\nGoodbye!')
                sys.exit()
            else: 
                print('\nOnly "yes" or "no" or "exit" is allowed')
                
    # limit sequences length? 
    limit_length = 0
    while True:  # ask from user
        r = input('\nDo you want to limit the length range of sequences? yes/[no]/exit\n').strip().lower()
        if r == 'yes':
            limit_length = 1
            break
        elif r == 'no':
            break
        elif len(r) == 0:
            print('\n"No" has been chosen')
            break
        elif r == 'exit' or r == 'quit':
            print('\nGoodbye!')
            sys.exit()
        else:
            print('\nOnly "yes" or "no" or "exit" is allowed')
    if limit_length == 1:
        print('\nSummary: ')
        print('Sequences Number: %d (%d of them are found containing unknown amino acid "X")' % (seq_df.shape[0], x_number))
        print('Species Number: %d (%d of them have multiple sequences)' % (len(set(seq_df['species'])), duplitcate_number))
        print('Brief information for sequences length:')
        print('\n'.join(str(seq_df['seq_length'].describe()).split('\n')[1:-1]))
        while True:  # input max
            r = input('\nPlease input the max-length: (Input one integer or enter "exit" or ["skip"])\n').strip().lower()
            if r.isdigit():
                max_len = int(r)
                seq_df = seq_df.loc[seq_df['seq_length'] <= max_len]
                break
            elif r == 'exit' or r == 'quit':
                print('\nGoodbye!')
                sys.exit()
            elif r == 'skip':
                break
            elif len(r) == 0:
                print('"Skip" has been chosen! ')
                break
            else:
                print('\nOnly integer (not float type number) or "exit" or "skip" can be input!')
        
        while True:  # input min
            r = input('\nPlease input the min-length: (Input one integer or enter "exit" or ["skip"])\n').strip().lower()
            if r.isdigit() and int(r) <= max_len:
                min_len = int(r)
                seq_df = seq_df.loc[seq_df['seq_length'] >= min_len]
                break
            elif r.isdigit() and int(r) > max_len:
                print('\nYou can not enter a number larger than max-length!')
            elif r == 'exit' or r == 'quit':
                print('\nGoodbye!')
                sys.exit()
            elif r == 'skip':
                break
            elif len(r) == 0:
                print('"Skip" has been chosen! ')
                break
            else:
                print('\nOnly integer (not float type number) or "exit" or "skip" can be input!')
                
    # check how many sequences each species has?
    if drop_duplicate != 1:
        if drop_sth == 1:
            while True:  # ask from user
                r = input('\nDo you want check how many sequences each species has again ? yes/[no]/exit\n').strip().lower()
                if r == 'yes':
                    print('\n'.join(str(seq_df['species'].value_counts()).split('\n')[1:-1]))
                    break
                elif r == 'no':
                    break
                elif len(r) == 0:
                    print('"No" has been chosen')
                    break
                elif r == 'exit' or r == 'quit':
                    print('\nGoodbye!')
                    sys.exit()
                else:
                    print('\nOnly "yes" or "no" or "exit" is allowed')

    # check all info?
    if drop_sth == 1:
        while True:  # ask from user
            r = input('\nDo you want check all information in a table again? yes/[no]/exit\n').strip().lower()
            if r == 'yes':
                print(pd.concat([seq_df[['protein_id','species','seq_length']],seq_df['sequence'].apply(lambda x: x[:10]+"...")],axis=1).sort_values(by='species').set_index('protein_id'))
                break
            elif r == 'no':
                break
            elif len(r) == 0:
                print('"No" has been chosen')
                break
            elif r == 'exit' or r == 'quit':
                print('\nGoodbye!')
                sys.exit()
            else:
                print('\nOnly "yes" or "no" or "exit" is allowed')        

    # manually exclude sequences?
    while True:  # ask from user
        exclude_ids = []
        r = input('\nDo you want to manually exclude sequences? yes/[no]/exit\n').strip().lower()
        if r == 'yes':
            while True:
                r = input('\nInput the protein ID you do not need: (Enter ["finish"] to finish)\
                        \n(Only support one protein ID for each input)\n').strip()
                if r.lower() == 'finish':
                    break
                if len(r) == 0:
                    break
                if r in list(seq_df['protein_id']):
                    exclude_ids.append(r)
                else:
                    print('\nThis ID can not be found!')
            break
        elif r == 'no':
            break
        elif len(r) == 0:
            print('"No" has been chosen')
            break
        elif r == 'exit' or r == 'quit':
            print('\nGoodbye!')
            sys.exit()
        else:
            print('\nOnly "yes" or "no" or "exit" is allowed')
    if exclude_ids:  # if got exclude_ids
        seq_df = seq_df.loc[~seq_df['protein_id'].isin(exclude_ids)]
        
    # check how many sequences each species has?
    if drop_duplicate != 1:
        if exclude_ids:
            while True:  # ask from user
                r = input('\nDo you want check how many sequences each species has again ? yes/[no]/exit\n').strip().lower()
                if r == 'yes':
                    print('\n'.join(str(seq_df['species'].value_counts()).split('\n')[1:-1]))
                    break
                elif r == 'no':
                    break
                elif len(r) == 0:
                    print('"No" has been chosen')
                    break
                elif r == 'exit' or r == 'quit':
                    print('\nGoodbye!')
                    sys.exit()
                else:
                    print('\nOnly "yes" or "no" or "exit" is allowed')

    # check all info?
    if exclude_ids:
        while True:  # ask from user
            r = input('\nDo you want check all information in a table again? yes/[no]/exit\n').strip().lower()
            if r == 'yes':
                print(pd.concat([seq_df[['protein_id','species','seq_length']],seq_df['sequence'].apply(lambda x: x[:10]+"...")],axis=1).sort_values(by='species').set_index('protein_id'))
                break
            elif r == 'no':
                break
            elif len(r) == 0:
                print('"No" has been chosen')
                break
            elif r == 'exit' or r == 'quit':
                print('\nGoodbye!')
                sys.exit()
            else:
                print('\nOnly "yes" or "no" or "exit" is allowed')        
        
    # final show summary
    print('\nHere is the FINAL summary!')
    print('Sequences Number: %d (%d of them are found containing unknown amino acid "X")' % (seq_df.shape[0], x_number))
    print('Species Number: %d (%d of them have multiple sequences)' % (len(set(seq_df['species'])), duplitcate_number))
    print('Brief information for sequences length:')
    print('\n'.join(str(seq_df['seq_length'].describe()).split('\n')[1:-1]))
    print('\nNow we will proceed to "Multiple Alignment" and "Consevation Plotting"!')

    # final check
    final_code = 0
    while True:
        r = input('\nDo you want to continue using the current sequences?\
                    \nyes: Continue!\
                    \nno: I want to select sequences again!\
                    \nexit: I want to quit programme!\
                    \n(Enter "yes" or "no" or "exit")\n').strip().lower()
        if r == 'yes':
            break
        elif r == 'no':
            final_code = 1
            break
        elif r == 'exit' or r == 'quit':
            print('\nGoodbye!')
            sys.exit()
        elif len(r) == 0:
            print('Enter something please...')
        else:
            print('Choose "yes" or "no" or "exit" please!')
    if final_code == 1:
        continue

    break

# save files
temp_dir = wd + '/temp_file'
target_ids = '|'.join(list(seq_df['protein_id']))
remove_seq = "cat %s | awk 'BEGIN{RS=\">\"; ORS=\"\";}{if($1~/%s/)print \">\"$0;}' > %s"%(fa_dir, target_ids, temp_dir)
r = subprocess.run(remove_seq, shell=True)
if r.returncode != 0:
    print('\nSomething goes wrong...' + '\nReturn code: ' + str(r.returncode))
    print('Wrong command: ' + r.args)
    sys.exit()

# ask for the name of alignment.fa file
while True:
    alig_name = input('\nEnter a filename for "Multiple Alignments" result (fasta format):\
                       \n(e.g. "alig.fa" or "./folder1/XX.fa")\
                       \n(Enter "exit" to quit programme)\n').strip()
    alig_dir = os.path.abspath(alig_name) 
    if len(alig_name) == 0:
        print('Try entering a name please. Or you can enter "exit" to quit')
    elif len(alig_name) > 50:
        print('I don\'t think it is necessary for such a long name...')
    elif alig_name.lower() == 'exit' or alig_name.lower() == 'quit':
        print('\nGoodbye!')
        sys.exit()
    elif subprocess.run(r'mkdir -p %s && touch %s' % (os.path.dirname(alig_dir), alig_dir), shell=True).returncode != 0:
        print('\nSomething goes wrong when creating file at: %s\
               \nCheck your name / directory / permission for execution' % alig_dir)
    else:
        break
        
# ask for the name of distance matrix
while True:
    distmat_name = input('\nEnter a filename for "Percentage Distance Matrix" result:\
                          \n(e.g. "percent_distmat" or "./folder1/XX")\
                          \n(Enter "exit" to quit programme)\n').strip()
    distmat_dir = os.path.abspath(distmat_name)
    if len(distmat_name) == 0:
        print('Try entering a name please. Or you can enter "exit" to quit')
    elif len(distmat_name) > 50:
        print('I don\'t think it is necessary for such a long name...')
    elif distmat_name.lower() == 'exit' or distmat_name.lower() == 'quit':
        print('\nGoodbye!')
        sys.exit()
    elif subprocess.run(r'mkdir -p %s && touch %s' % (os.path.dirname(distmat_dir), distmat_dir), shell=True).returncode != 0:
        print('\nSomething goes wrong when creating file at: %s\
               \nCheck your name / directory / permission for execution' % distmat_dir)
    else:
        break
        
# multiple alignment through "clustalo"
print('\nAligning sequences...')
r = subprocess.run(r"clustalo --threads 128 --full --percent-id --distmat-out %s\
                     -i %s --force > %s"%(distmat_dir, temp_dir, alig_dir), shell=True)  
if r.returncode == 0:
    print('\nSuccessfully aligning the sequences, output can be found at: %s' % alig_dir)
    print('\nSuccessfully creating percentage distance matrix, output can be found at: %s' % distmat_dir)
else:
    print('\nSomething goes wrong...' + '\nReturn code: ' + str(r.returncode))
    print('Wrong command: ' + r.args)
    sys.exit()
    
# show percentage distance matrix
print('\nHere is the percentage distance matrix:\n')
distmat = subprocess.getoutput(r"cat %s" % distmat_dir).split('\n')[1:]
dist_matrix = {}
for i in distmat:
    name = i.split()[0]
    contents = i.split()[1:]
    dist_matrix[name] = contents
distmat_df = pd.DataFrame(dist_matrix, index=dist_matrix.keys())
distmat_df = distmat_df.applymap(float)
print(distmat_df.set_index('protein_id')) 

# ask for the size of window size parameter
while True:
    r = input('\nEnter a "Window Size" for "Conservation Plot" result: (Only one integer is allowed)\
                     \n(e.g. [4]; or enter "exit" to quit programme)\n').strip().lower()
    if r.isdigit():
        winsize = int(r)
        break
    elif r == 'exit' or r == 'quit':
        print('\nGoodbye!')
        sys.exit()
    elif len(r) == 0:
        print('"winsize = 4" has been chosen by default!')
        winsize = 4
        break
    else:
        print('\nOnly integer (not float type number) or "exit" can be input!')

# plot conservation through "plotcon"
print('\nPlotting...')
r = subprocess.run(r"plotcon %s -graph png -winsize %d -gdirectory %s"%(alig_dir, winsize, wd), shell=True)
if r.returncode == 0:
    print('\nSuccessful! The plot can be found at: %s' % wd + '/plotcon.1.png')
else:
    print('\nSomething goes wrong...' + '\nReturn code: ' + str(r.returncode))
    print('Wrong command: ' + r.args)
    sys.exit()
    
# show plot
print('If no plot is shown, wait for a while and programme will continue...')
I = mpimg.imread(wd + '/plotcon.1.png')
plt.imshow(I)

# remove temp_dir
subprocess.run('rm -f %s'%temp_dir, shell=True)

# manually exclude sequences?
while True:  # ask from user
    exclude_ids = []
    r = input('\nDo you want to manually exclude sequences again? yes/[no]/exit\n').strip().lower()
    if r == 'yes':
        while True:
            r = input(
                '\nInput the protein ID you do not need: (Enter ["finish"] to finish)\
                \n(Only support one protein ID for each input)\n'
            ).strip()
            if r.lower() == 'finish':
                break
            if len(r) == 0:
                break
            if r in list(seq_df['protein_id']):
                exclude_ids.append(r)
            else:
                print('\nThis ID can not be found!')
        break
    elif r == 'no':
        break
    elif len(r) == 0:
        print('"No" has been chosen')
        break
    elif r == 'exit' or r == 'quit':
        print('\nGoodbye!')
        sys.exit()
    else:
        print('\nOnly "yes" or "no" or "exit" is allowed')
if exclude_ids:  # if got exclude_ids
    seq_df = seq_df.loc[~seq_df['protein_id'].isin(exclude_ids)]

# create a folder for patmatmotifs output
try:
    motifs_dir = wd + '/patmatmotifs_output'
    if os.path.exists(motifs_dir):
        new_name = input('Folder_name "patmatmotifs_output" already exits, enter a new folder name please!\n')
        motifs_dir = os.path.abspath(new_name)
    os.makedirs(motifs_dir)
except Exception as result:
    print('\nSomething goes wrong when creating a folder for motifs output.\nHere is the error message: ' + str(result))
    sys.exit()

# use "pullseq" to exract fasta sequence
# use "patmatmotifs" to scan sequence of interest with motifs from the PROSITE database
print('\nStart finding motifs based on PROSITE database...')
motifs = {}
for i in seq_df['protein_id']:
    temp_ids = wd + '/protein_ids'
    temp_seq = wd + '/protein_seqs'
    motif_dir = motifs_dir + '/' + i
    find_motifs = 'echo %s > %s && /localdisk/data/BPSM/ICA2/pullseq -i %s -n %s > %s &&\
                    patmatmotifs -sequence %s -outfile %s' % (i, temp_ids, fa_dir, temp_ids, temp_seq, temp_seq, motif_dir)
    r = subprocess.run(find_motifs, shell=True)
    if r.returncode != 0:
        print('\nSomething goes wrong with '+ i + '\nReturn code: ' + str(r.returncode))
        sys.exit()
    get_motifs = "cat %s | grep 'Motif ='" %(motif_dir)
    names = subprocess.getoutput(get_motifs).replace('Motif = ','').split()
    if names:
        motifs[i] = names
    else:
        motifs[i] = 'null'
print('Done! Here is the result:\ng')
print(pd.merge(seq_df[['protein_id','species']],pd.Series(motifs,name='motifs_name'), left_on='protein_id', right_index=True).sort_values('species').set_index('protein_id'))
print('All motifs for each selected protein ID can be found at: '+motifs_dir)

# remove temporary files
subprocess.run('rm -f %s'%temp_ids, shell=True)
subprocess.run('rm -f %s'%temp_seq, shell=True)