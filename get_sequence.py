#! /usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os, sys
import re
import pandas as pd

# set working directory
while True:
    print('\nInvalid directory name will be regarded as a new folder name for current directory!')
    wd = input(
        'Enter a directory where you want to save your files: (e.g. "./foldername". Press "Enter" to use current directory; Enter "exit" to quit)\n'
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

while True:
    print('\nOnly support analysis with a single protein family from a single taxonomic group.')
    while True:
        selection = input('Do you need to get sequences from Entrez?\
                          \n [Yes], I did. (Enter "yes")\
                          \n No, I already have one. (Enter "no")\
                          \n I want to quit. (Enter "exit")\n').strip().lower()
        if selection == 'yes' or len(selection) == 0:
            select_code = 1
            break
        elif selection == 'no':
            select_code = 2
            # get protein family name
            while True:
                family_name = input('\nEnter your protein family name: (e.g. Pyruvate dehydrogenase; Enter "exit" to quit)\n').strip()
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
                taxo_name = input('\nEnter its taxonomic group name/ID: (e.g. ascomycete fungi/txid4890; Enter "exit" to quit)\n').strip()
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
                        print('\nYour taxonomic group ID is: ' + taxo_name)
                    break
            # get filename
            while True:
                print('\nYour current working directory is: ' + wd)
                fa_name = input('Enter your filename (Fasta) in the working directory\
                                \n(e.g. "filename.fa" or "folder_name/filename.fa"; Enter "exit" to quit)\
                                \nMake sure it is a valid Fasta-format file, otherwis the programme will fail: \n').strip()
                fa_dir = wd + '/' + fa_name
                if len(fa_name) == 0:
                    print('\nTry entering a name please. Or you can enter "exit" to quit')
                elif len(fa_name) > 100:
                    print('\nToo long! Make a shorter input or change your file directory')
                elif fa_name.lower() == 'exit' or fa_name.lower() == 'quit':
                    print('\nGoodbye!')
                    sys.exit()
                elif os.path.exists(fa_dir) == False:
                    print('\nCan not find the file, check your input please!')
                elif subprocess.getoutput(r'cat %s | grep ">" | head' % (fa_dir)).strip().startswith('>') == False:
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
    
    if select_code == 1:
        # require target info from users
        print('\nOnly support one name for input. Multiple or invalid names may lead to failure in searching!')
        # get protein family name
        while True:
            family_name = input('\nEnter one protein family name: (e.g. Pyruvate dehydrogenase; Enter "exit" to quit)\n').strip()
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
            taxo_name = input('\nEnter its taxonomic group name/ID: (e.g. ascomycete fungi/txid4890; Enter "exit" to quit)\n').strip()
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
            fa_name = input('\nEnter a Fasta filename for the result: (e.g. Pyruvate dehydrogenase.fa; Enter "exit" to quit)\n').strip()
            fa_dir = wd + '/' + fa_name
            if len(fa_name) == 0:
                print('\nTry entering a name please. Or you can enter "exit" to quit')
            elif len(fa_name) > 50:
                print('\nI don\'t think it is necessary for such a long name...')
            elif fa_name.lower() == 'exit' or fa_name.lower() == 'quit':
                print('\nGoodbye!')
                sys.exit()
            else:
                break

        print('\nInput:\nTaxonomic Group: %s\nProtein Family Name: %s\nFile Directory: %s' % (taxo_name, family_name, fa_dir))
        print('\nGetting protein sequence from NCBI Entrez database...\
               \n(some WARNINGs or ERRORs may happen due to Entrez, YOU DON\'T NEED TO DO ANYTHING!!)')
        fa_dir = wd + '/' + fa_name
        # get info from Entrez
        try:
            get_seq = 'esearch -db protein -query "%s[Organism] AND (%s[Protein Name] " | efetch -format fasta > %s' % (taxo_name, family_name, fa_dir)
            r = subprocess.run(get_seq,shell=True)
            if r.returncode == 0:
                if subprocess.getoutput(r'wc -l < %s' % (fa_dir)) == '0':
                    while True:
                        r = input('\nIt seems no return has come back...Would you like to try again? ([yes]/no)\n')
                        if r == 'yes' or len(r) == 0:
                            break
                        elif r == 'no':
                            print('\nGoodbye!')
                            subprocess.run(r'rm -f %s' % (fa_dir),shell=True)
                            sys.exit()
                        else:
                            print('\nOnly "yes" or "no" can be chosen!')
                else:
                    print('\nSuccessful! Now all the sequence are in: ' + fa_dir)
                    select_code = 2

            else:
                print('\nSomething goes wrong...' + '\nReturn code: ' + str(r.returncode))
                while True:
                    r = input('\nDo you want to try again? ([yes]/no) ').strip().lower()
                    if r == 'yes' or len(r) == 0:
                        break
                    elif r == 'no':
                        print('\nGoodbye!')
                        subprocess.run(r'rm -f %s' % (fa_dir),shell=True)
                        sys.exit()
                    else:
                        print('\nOnly "yes" or "no" can be chosen!')
        except Exception as result:
            print('Something goes wrong...\nHere is the error message: ' + str(result))
            while True:
                r = input('\nDo you want to try again? ([yes]/no) ').strip().lower()
                if r == 'yes' or len(r) == 0:
                    break
                elif r == 'no':
                    print('\nGoodbye!')
                    sys.exit()
                else:
                     print('\nOnly "yes" or "no" can be chosen!')
    
    if select_code == 2:
        # deleting all '\n'  in sequences
        temp_file = wd + 'temp_file'
        reformat = r"cat %s | tr -d '\n' | sed 's/>/\n>/g' | sed 's/]/]\n/g' | tail +2 > %s" % (fa_dir, temp_file)
        subprocess.run(reformat, shell=True)
        subprocess.run(r'cat %s > %s' % (temp_file, fa_dir), shell=True)
        subprocess.run(r'rm -f %s' % (temp_file), shell=True)
        
        # extract returned result
        descrip_command = 'grep ">" %s' % (fa_dir)
        seq_descrip = subprocess.getoutput(descrip_command)
        protein_ids = re.findall(r'>([^\s]+)', seq_descrip)
        species = re.findall(r'\[(.*)\]', seq_descrip)

        # extract sequence
        seq_command = r'grep "^\w" %s' % (fa_dir)
        seq_all = subprocess.getoutput(seq_command)
        seqs = seq_all.split('\n')
        
        # use a dataframe to store info
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
        x_number = count_x(seqs)
        
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
        
        # drop sequences with unknown amino acid "X" ?
        def no_x_in_seq(s):
            if 'x' in s.lower():
                return False
            else:
                return True
        if x_number != 0 :
            while True:
                drop = input('\nDo you want to drop sequences with unknown amino acid "X" ? yes/[no]\n').strip().lower()
                if drop == 'yes':
                    seq_df = seq_df.loc[seq_df['sequence'].apply(no_x_in_seq)]
                    x_number = count_x(list(seq_df['sequence']))
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
                    print('\n"No" has been chosen')
                    break
                else: 
                    print('\nOnly "yes" or "no" is allowed')
                    
        # drop duplicate?
        if duplitcate_number > 0: 
            while True:
                print('\nSpecies with multiple sequences are found!')
                drop = input('Do you want only the longest sequence of each species be chosen ? yes/[no]\n').strip().lower()
                if drop == 'yes':
                    seq_df = seq_df.loc[~seq_df['species'].duplicated()]
                    duplitcate_number = 0
                    print('\nAll species has only one sequence now!')
                    print('\nSummary: ')
                    print('Sequences Number: %d (%d of them are found containing unknown amino acid "X")' % (seq_df.shape[0], x_number))
                    print('Species Number: %d (%d of them have multiple sequences)' % (len(set(seq_df['species'])), duplitcate_number))
                    print('Brief information for sequences length:')
                    print('\n'.join(str(seq_df['seq_length'].describe()).split('\n')[1:-1]))
                    break
                elif drop == 'no':
                    break
                elif len(drop) == 0:
                    print('\n"No" has been chosen')
                    break
                else: 
                    print('\nOnly "yes" or "no" is allowed')
        
        # check sequences number
        limit_code = 0
        if seq_df.shape[0] > 100:  # 记得改回去1000
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
            r = input('\nDo you want to continue using the current sequences ? (Enter "yes" or "no" or "exit")\
                       \nyes: Continue!\
                       \nno: I want to input/fetch sequences again!\
                       \nexit: I want to leave!\
                       \n').strip().lower()
            if r == 'yes':
                break
            elif r == 'no':
                final_code = 1
                break
            elif r == 'exit' or 'quit':
                print('\nGoodbye!')
                sys.exit()
            else:
                print('\nChoose "yes" or "no" or "exit" please!')
        if final_code == 1:
            continue
        
        break