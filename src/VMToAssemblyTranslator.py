# MPCS 52011 - Introduction to Computer Systems
# Eric Zacharia
# Project 8
import sys
import os


def remove_newlines_and_comments(lines):  # Removes comments and newlines, not whitespace
    '''
This function takes in a line and returns the line without leading whitespace, trailing whitespace, and comments.

Input: a string of VM code

Output: a string of VM code, stripped of undesired whitespace and comments
    '''
    stripped_lines = [line.strip() for line in lines]  # Strip whitespace before and after strings on each line
    # Only keep first string that splits before the '//', if the line doesn't begin with '//' and is not an empty string
    lines = [line.split('//')[0].strip() for line in stripped_lines if not is_comment_or_newline(line)]
    return lines


def is_comment_or_newline(line):  # Determines if the line is an empty string or begins as a comment
    '''
This function takes in a line and returns a Booleans value that categorizes the input line as a comment/newline or not.

Input: a string of VM code

Output: a Boolean value (True if comment or newline, False otherwise)
    '''
    line = line.strip()
    if not line:  # "if not line" = "if empty string" = "if newline only'
        return True
    if line.startswith('//'):
        return True
    return False


# Translates Virtual Machine code to Assembly code. Commands are separated by number of words on each VM line.
def translate_vm_to_asmbly(line, filename, counter):
    '''
This function takes in a string of vm code, a filename string without its extension, and a list of three values, such
that counter[0] counts Boolean commands, counter[1] counts number of calls, and counter[2] is for project 8.

Input: a string of vm code, a filename string, and a list of counters

Output: a list of assembly code string instructions
    '''
    # Strip whitespace before and after strings on each line, then split into list of strings
    filename = filename.split('\\')[-1]
    strings = line.strip().split()
    command = strings[0]  # VM Code command is first string in list of strings
    translation = [f'//{line}']
    if len(strings) == 1:  # If length of VM Code command is 1, then follow this translation pattern:
        if command == 'return':
            translation += ['@LCL', 'D=M', '@R14', 'M=D', '@5', 'A=D-A', 'D=M', '@R15', 'M=D', '@ARG', 'D=M', '@0',
                            'D=D+A', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D', '@ARG', 'D=M', '@SP',
                            'M=D+1', '@R14', 'AMD=M-1', 'D=M', '@THAT', 'M=D', '@R14', 'AMD=M-1', 'D=M', '@THIS', 'M=D',
                            '@R14', 'AMD=M-1', 'D=M', '@ARG', 'M=D', '@R14', 'AMD=M-1', 'D=M', '@LCL', 'M=D', '@R15',
                            'A=M', '0;JMP']
        else:
            operator_dict = {'add': '+', 'sub': '-', 'and': '&', 'or': '|', 'neg': '-', 'not': '!', 'eq': 'JNE',
                             'lt': 'JGE', 'gt': 'JLE'}
            if command in ['neg', 'not']:
                return ['@SP', 'A=M-1', f'M={operator_dict.get(command)}M']
            translation += ['@SP', 'AM=M-1', 'D=M', 'A=A-1']

            if command in ['add', 'sub', 'and', 'or']:
                translation.append(f'M=M{operator_dict.get(command)}D')
            else:  # if command in eq, gt, lt
                translation += ['D=M-D', f'@FALSE_{counter[0]}', f'D;{operator_dict.get(command)}', '@SP', 'A=M-1',
                                'M=-1', f'@CONTINUE_{counter[0]}', '0;JMP', f'(FALSE_{counter[0]})', '@SP', 'A=M-1',
                                'M=0', f'(CONTINUE_{counter[0]})']
                counter[0] += 1

    elif len(strings) == 2:  # If length of VM Code command is 2, then follow this translation pattern:
        if command == 'label':
            translation += [f'({counter[2]}{strings[1]})']
        elif command == 'goto':
            translation += [f'@{counter[2]}{strings[1]}', '0;JMP']
        else:  # 'if-goto':
            translation += ['@SP', 'M=M-1', 'A=M', 'D=M', f'@{counter[2]}{strings[1]}', 'D;JNE']

    else:  # If length of VM Code command is not 1 or 2, then follow this translation pattern:
        if command in ['push', 'pop']:
            address_dict = {'local': '@LCL', 'argument': '@ARG', 'this': '@THIS', 'that': '@THAT', 'static': 16,
                            'temp': 5, 'pointer': 3}
            if strings[1] == 'constant':
                translation += [f'@{strings[2]}']
            elif strings[1] == 'static':
                translation += [f'@{filename}.{strings[2]}']
            elif strings[1] in ['temp', 'pointer']:
                translation += [f'@R{address_dict.get(strings[1]) + int(strings[2])}']
            else:  # local, argument, this, that
                translation += [address_dict.get(strings[1]), 'D=M', f'@{strings[2]}', 'A=D+A']

            if strings[0] == 'push':
                if strings[1] == 'constant':
                    translation.append('D=A')
                else:
                    translation.append('D=M')
                translation += ['@SP', 'AM=M+1', 'A=A-1', 'M=D']
            else:
                translation += ['D=A', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
        elif command == 'call':
            translation += [f'@{filename}.RET_{counter[1]}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', '@LCL', 'D=M',
                            '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', '@ARG', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
                            '@THIS', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', '@THAT', 'D=M', '@SP', 'A=M', 'M=D',
                            '@SP', 'M=M+1', '@SP', 'D=M', '@LCL', 'M=D', f'@{int(strings[2]) + 5}', 'D=D-A', '@ARG',
                            'M=D', f'@{strings[1]}', '0;JMP', f'({filename}.RET_{counter[1]})']
            counter[1] += 1
        else:
            translation += [f'({strings[1]})']
            for i in range(int(strings[2])):
                translation += ['@0', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
            counter[2] = f'{strings[1]}$'
    return translation


def main():
    '''This function reads arguments passed on the command line that equate to the .vm file name with or without a path or
a folder path that contains any number of .vm files. '''
    input_f = sys.argv[1]  # Takes the input file name as an argument in command line
    if input_f[-3:] == '.vm':
        split_input_f = input_f.split('\\')
        split_input_f.pop()
        input_f = ''
        for folder in split_input_f:
            input_f += folder + '\\'
        input_f = input_f[:-1]
    fn_lst = []  # initialize a list of .vm files to translate
    for file in os.listdir(input_f):  # for each file in the input directory,
        if file[-3:] == '.vm':  # if it is a .vm file,
            fn_lst.append(f'{input_f}\{file}')  # then add file to the list of files that need to be translated.
    vm_file_paths_no_ext = []
    asm_file_path = input_f + '\\' + input_f.split('\\')[-1]

    for file_path in fn_lst:  # Translate all the .vm files in the list
        vm_file_paths_no_ext.append(file_path[:-3])
    translation = ['@256', 'D=A', '@SP', 'M=D', '@RETURN_BOOTSTRAP', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
                   '@LCL', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', '@ARG', 'D=M', '@SP', 'A=M', 'M=D', '@SP',
                   'M=M+1', '@THIS', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', '@THAT', 'D=M', '@SP', 'A=M',
                   'M=D', '@SP', 'M=M+1', '@SP', 'D=M', '@LCL', 'M=D', '@5', 'D=D-A', '@ARG', 'M=D',
                   f'@Sys.init', '0;JMP', '(RETURN_BOOTSTRAP)']

    for vm_file in vm_file_paths_no_ext:
        with open(f'{vm_file}.vm', 'r') as rf:
            virtual_machine_code = remove_newlines_and_comments(rf.readlines())
        counter = [0, 0, '']
        # For each line in the vm code, list each translation in the list of translations from each line of vm code.
        translation += [x for line in virtual_machine_code for x in translate_vm_to_asmbly(line, vm_file, counter)]

    with open(f'{asm_file_path}.asm', 'w') as wf:
        for item in translation:
            wf.write(item + '\n')  # Write one line at a time, and break with a newline


main()
