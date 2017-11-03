from pycorenlp import StanfordCoreNLP
from mysql_utils.db_manager import DBConn
import csv
nlp = StanfordCoreNLP('http://192.168.0.100:9000')
nlp = StanfordCoreNLP('http://localhost:9000')


def stanford_tree(line, annotators='pos,lemma'):
    output = nlp.annotate(line, properties={
        'annotators': annotators,
        'outputFormat': 'json'
    })
    try:
        return output
    except IndexError:
        pass


def load_data():
    db_conn = DBConn()
    ls_result = db_conn.fetch_data('SELECT user_input, lib_response FROM whatsapp_record_slot')
    ls_user_intput = []
    ls_lib_respon = []
    for record in ls_result:
        ls_user_intput.append(record['user_input'])
        ls_lib_respon.append(record['lib_response'])

    return ls_user_intput, ls_lib_respon


def deal_qa(msg):
    result = stanford_tree(msg)
    set_verb = set()
    for sentence in result['sentences']:
        for dic_token in sentence['tokens']:
            if 'VB' in dic_token['pos']:
                set_verb.add(dic_token['lemma'].lower())
    return ','.join(list(set_verb))


def entry():
    ls_msg, ls_respon = load_data()

    print(len(ls_msg), len(ls_respon))
    fid = open('verb_result.txt', 'w')
    # csv_writer = csv.writer(csv_file, dialect = ("excel"))
    i = 0  # current msg start
    while True:
        msg = ''
        respon = ''
        next_msg_start = 0
        end_tag = 0
        if ls_msg[i] != '':
            for j in range(i+1, len(ls_respon)):
                if ls_respon[j] != '':
                    print('respond id', j)
                    respon = ls_respon[j]
                    if j+1 == len(ls_respon):
                        end_tag = 1
                    for k in range(j+1, len(ls_respon)):
                        if ls_msg[k] != '':
                            if next_msg_start == 0:
                                next_msg_start = k
                            break
                        else:
                            if end_tag == 1:
                                break
                            respon += ls_respon[k]
                    break
                else:
                    continue
            if next_msg_start == 0: # end of conversation
                msg = ls_msg[i]
            for m in range(i, next_msg_start):
                msg += ls_msg[m]
        i = next_msg_start  # update next msg start
        print('msg', msg)
        print('response', respon)
        print('new msg id', next_msg_start)
        if end_tag == 1:
            break
        verb_msg = deal_qa(msg)
        verb_respon = deal_qa(respon)
        print(verb_msg)
        print(verb_respon)
        fid.write(verb_msg + '&&&' + verb_respon + '\n')

entry()
