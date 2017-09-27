from stop_words import get_stop_words
import re


def __search(message, stop_words):

    condition_back = r"(?:(?:status of)|(?:status)|(?:meaning of))+(?P<target1> \w+){1,2}|(?:is)(?P<target2> \w+( )*\?){1,2}"
    condition_front = r"(?:(?P<target>\w+ ){1,2}(?:(stand[s]{0,1} for)|(?:mean[s]{0,1})|(?:refer[s]{0,1} to)|(?:status)))"
    ls_result = []
    search_result_back = re.finditer(condition_back, message, flags=re.IGNORECASE)
    if search_result_back:
        for result in search_result_back:
            if result.group('target1'):
                word = result.group('target1')
                if word not in stop_words:
                    ls_result.append(word)
            elif result.group('target2'):
                #print("t2")
                word = result.group('target2').replace('?', '')
                if word not in stop_words:
                    ls_result.append(word)

    search_result_front = re.finditer(condition_front, message, flags=re.IGNORECASE)
    if search_result_front:
        for result in search_result_front:
            word = result.group('target')
            if word not in stop_words:
                ls_result.append(word)
    return ls_result

#
# message = "I saw a book on the website with status bindery, what does it mean?"
# msg = "What is bindery and status of bindery?"
# msg = "If a book has a status of bindery status or status of available status, what does it refers to?"

# for msg in ls_msgs:
#     ls_word = __search(msg, ls_stop_words)
#     print(ls_word)
#print(__search(msg))
