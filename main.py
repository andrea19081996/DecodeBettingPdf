import tabula
import csv
import os
import requests
from datetime import date
import re


# Method for download file pdf
def download_file(current_file):
    print('Sto per scaricare il file ' + current_file + '\n')
    url = 'https://locandine.lottomatica.it/WebPosterOdds/locandine/ARE/Scommesse/Quote/Calcio/' + current_file
    r = requests.get(url, allow_redirects=True)

    #save file
    open(current_file, 'wb').write(r.content)
    print('Scaricato il file ' + current_file + '\n')


def convert_pdf_to_csv(file_name, output_file_name):
    # output all the tables in the PDF to a csv
    print('Conversion of file from type pdf to csv')
    tabula.convert_into(file_name, output_file_name, output_format='csv', pages='all')

    print('End conversion')


'''
Metodo utilizzato per vedere se il nome di una squadra analizzato
fa parte delle squadre che hanno un numero nel proprio nome
'''
#Method for check if a team have a number in his name
def is_special_team(team):
    special_team = ['GRENOBLE FOOT 38', 'LAMIA 1964', 'CD BELCHITE 97', 'FC FELGUEIRAS 1932', 'CF CANELAS 2010',
                    'SCHALKE 04', 'HEIDENHEIM 1846', 'SV MEPPEN 1912', 'FOOTBALL BOURG-EN-BRESSE PERONNAS 01',
                    'SPORTFREUNDE LOTTE 1929']

    if team in special_team:
        return True
    else:
        return False

#Method for write the row in the final csv
def write_type_file(flag_type_file, result_writer, first_part, list_quote, row, man):
    if flag_type_file == 0:
        result_writer.writerow(
            [first_part[0], first_part[1], first_part[2], first_part[3], row[0], man, list_quote[0],
             list_quote[1], list_quote[2], list_quote[3],
             list_quote[4], list_quote[5],
             list_quote[6], list_quote[7], list_quote[8], list_quote[9], list_quote[10], list_quote[11],
             list_quote[12],
             list_quote[13], list_quote[14], list_quote[15], list_quote[16], list_quote[17],
             list_quote[18], list_quote[19],
             list_quote[20], list_quote[21], list_quote[22], list_quote[23], list_quote[24],
             list_quote[25], list_quote[26],
             list_quote[27]])
    elif flag_type_file == 1:
        result_writer.writerow(
            [first_part[0], first_part[1], first_part[2], first_part[3], row[0], man, list_quote[0],
             list_quote[1], list_quote[2], list_quote[3],
             list_quote[4], list_quote[5],
             list_quote[6], list_quote[7], list_quote[8], list_quote[9], list_quote[10], list_quote[11],
             list_quote[12],
             list_quote[13], list_quote[14], list_quote[15], list_quote[16], list_quote[17]])
    elif flag_type_file == 2:
        result_writer.writerow(
            [first_part[0], first_part[1], first_part[2], first_part[3], row[0], man, list_quote[0],
             list_quote[1], list_quote[2], list_quote[3], list_quote[4], list_quote[5], list_quote[6], list_quote[7],
             list_quote[8], list_quote[9], list_quote[10], list_quote[11], list_quote[12], list_quote[13],
             list_quote[14], list_quote[15], list_quote[16], list_quote[17], list_quote[18], list_quote[19],
             list_quote[20], list_quote[21], list_quote[22], list_quote[23], list_quote[24], list_quote[25],
             list_quote[26], list_quote[27], list_quote[28], list_quote[29], list_quote[30]])


def elab_file(result_writer, input_file, flag_type_file):
    days = ['LUNEDÌ', 'MARTEDÌ', 'MERCOLEDÌ', 'GIOVEDÌ', 'VENERDÌ', 'SABATO', 'DOMENICA']
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        setting_page = -1
        for row in csv_reader:

            #copy of row without empty field
            not_empty_row = []

            for elem in row:
                if elem != '':
                    not_empty_row.append(elem)

            if len(not_empty_row) == 1:
                setting_page = -1
                continue
            if len(not_empty_row) == 0:
                continue

            if not_empty_row[0] == 'ORA' or 'QUOTE' in not_empty_row[0] or 'Pubblicazione' in not_empty_row[0]:
                setting_page = -1
                continue

            if not_empty_row[0].split()[0] in days:
                day = not_empty_row[0]
                setting_page = 1
                line_count += 1
                continue

            if setting_page == 1:

                cont = 0
                search_man = False
                match_field = False

                for field in not_empty_row:
                    if cont == 0 or field == '':
                        cont += 1
                        continue

                    split_field = field.split(' ')

                    for elem_split_field in split_field:
                        #case when don't find MAN
                        if search_man == False:
                            search_man = re.search('[A-Z]{3}[0-9]*', elem_split_field)

                            if search_man:
                                man = elem_split_field
                                print('\nFIND MAN')
                                print(man + '\n')

                        #check if in current field there is match
                        if elem_split_field.isalpha() and ('-' in split_field) and match_field == False:
                            match_field = True
                            list_quote = extract_quote(not_empty_row[cont:])
                            break

                    cont += 1

                first_part = day.split(' ')

                write_type_file(flag_type_file, result_writer, first_part, list_quote, not_empty_row, man)

#Method for elab file of type Calcio_Orizzontale
def elab_calcio_orizzontale(input_file, result_file):
    with open(result_file, newline='', mode='w') as result:
        result_writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        result_writer.writerow(
            ['DAY', 'NUMBER_DAY', 'MONTH', 'YEAR', 'TIME', 'MAN', 'MATCH', '1', 'X', '2', 'G', 'NG', 'U-1.5', 'O-1.5',
             'U-2.5', 'O-2.5',
             'U-3.5', 'O-3.5', '1X', 'X2', '12', '1-1T', 'X-1T', '2-1T', 'H-SQ', 'H-1', 'H-X', 'H-2',
             '1+U-2.5', '1+O-2.5', 'X+U-2.5', 'X+O-2.5', '2+U-2.5', '2+O-2.5'])

        elab_file(result_writer, input_file, 0)

#Method for elab file of type Calcio_Verticale
def elab_calcio_verticale(input_file, result_file):
    with open(result_file, newline='', mode='w') as result:
        result_writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        result_writer.writerow(
            ['DAY', 'NUMBER_DAY', 'MONTH', 'YEAR', 'TIME', 'MAN', 'MATCH', '1', 'X', '2', 'G', 'NG', 'U-1.5', 'O-1.5',
             'U-2.5', 'O-2.5',
             'U-3.5', 'O-3.5', '1X', 'X2', '12', '1-1T', 'X-1T', '2-1T'])

        elab_file(result_writer, input_file, 1)

#Method for elab file of type Calcio_Under_Over
def elab_calcio_under_over(input_file, result_file):
    with open(result_file, newline='', mode='w') as result:
        result_writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        result_writer.writerow(
            ['DAY', 'NUMBER_DAY', 'MONTH', 'YEAR', 'TIME', 'MAN', 'MATCH', 'U-0.5', 'O-0.5', 'U-1.5', 'O-1.5', 'U-2.5',
             'O-2.5', 'U-3.5', 'O-3.5', 'U-4.5', 'O-4.5', 'U-5.5', 'O-5.5', 'U-6.5', 'O-6.5', 'U-7.5', 'O-7.5', 'U-8.5',
             'O-8.5', 'U-1.5-CASA', 'O-1.5-CASA', 'U-2.5-CASA', 'O-2.5-CASA', 'U-3.5-CASA', 'O-3.5-CASA',
             'U-1.5-OSPITE',
             'O-1.5-OSPITE', 'U-2.5-OSPITE', 'O-2.5-OSPITE', 'U-3.5-OSPITE', 'O-3.5-OSPITE'])

        elab_file(result_writer, input_file, 2)

#Method for find team on left part of match field
def find_first_team(first_part):
    for elem in first_part.split(' '):
        if not elem.isnumeric():
            index = first_part.split(' ').index(elem)
            return ' '.join(first_part.split(' ')[index:])

#Method for find quote in the match field
def find_number_quote_match(main_part, index_first_numeric, result):
    number = main_part.split(' ')[index_first_numeric:]
    result.extend(number)
    return result


def extract_quote(quote):
    count = 0
    special_team = False
    result = []

    for elem_quote in quote:
        if count == 0:

            #take right part of match field
            second_part = elem_quote[elem_quote.index('-') + 1:].lstrip()

            for elem_second_part in second_part.split(' '):

                if elem_second_part.replace(',', '').isnumeric() and special_team == False:

                    index_numeric = second_part.split(' ').index(elem_second_part)
                    team = ' '.join(second_part.split(' ')[:index_numeric + 1])
                    print('\n\nCURRENT TEAM\n' + team + '\n\n')
                    special_team = is_special_team(team)
                    #if find special team
                    if special_team:
                        match = find_first_team(elem_quote.split('-')[0].rstrip()) + ' - ' + team
                        result = [match]
                        special_team = True
                        result = find_number_quote_match(second_part, index_numeric + 1, result)
                        break

        else:
            #if current field is not empty, put every element in result
            if elem_quote != '':
                for inner_elem_quote in elem_quote.split(' '):
                    result.append(inner_elem_quote)

        #case don't find special team in the match field
        if special_team == False and count == 0:

            position = 0
            last_elem = -1

            match = ''
            for elem in elem_quote.split(' '):
                if not elem.replace(',', '').isnumeric():
                    match += elem + ' '
                    last_elem = position
                position += 1

            #save match in the first position of result
            result = [match.rstrip()]

            result = find_number_quote_match(elem_quote, last_elem + 1, result)

        count += 1

    return result


if __name__ == '__main__':
    #open file containing type of files to download
    file1 = open('./TXT/files.txt', 'r')
    Lines = file1.readlines()

    #take current date
    today = date.today()
    current_day = today.strftime("%d-%m")

    # Strips the newline character
    for line in Lines:
        file_name = line.replace('XXX', current_day).rstrip("\n")

        # download current file of the current day
        download_file(file_name)

        final_result = file_name.replace('.pdf', '.csv')
        middle_file_name = 'INTERMEDIO_' + final_result
        try:
            convert_pdf_to_csv(file_name, middle_file_name)
        except:
            file_error = open('./TXT/error.txt', 'a')
            file_error.write(current_day + ' Error conversion of file: ' + file_name + '\n')
            file_error.close
            print('Error conversion of file: -> go to next file')
            continue

        if 'Verticale' in file_name:
            elab_calcio_verticale(middle_file_name, final_result)
        elif 'Orizzontale' in file_name:
            elab_calcio_orizzontale(middle_file_name, final_result)
        elif 'Under-Over' in file_name:
            elab_calcio_under_over(middle_file_name, final_result)

        print('Create new file: ' + final_result + '\n')
        #delete intermediate file
        os.remove(middle_file_name)
