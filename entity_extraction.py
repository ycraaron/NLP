from stop_words import get_stop_words
import re


def __search(message, stop_words):
    ls_result = []
    condition_specific_back = r"((((status of )|(status )|(meaning of ))+(?:(?P<dep>cat department)|(?P<dis>on display)|(?P<sea>on search)))" \
                              r"|((?:is )((?P<dep2>cat department)|(?P<dis2>on display)|(?P<sea2>on search))))"
    condition_specific_front = r"(?:(?:(?P<dep>cat department)|(?P<dis>on display)|(?P<sea>on search))" \
                      r"(?:( stand[s]{0,1} for)|(?: mean[s]{0,1})|(?: refer[s]{0,1} to)|(?: status)))"
    #condition_specific_back = r"(?:meaning of )+(?P<dis>on display)"
    search_result_specific_back = re.finditer(condition_specific_back, message, flags=re.IGNORECASE)
    # print(search_result_specific)
    if search_result_specific_back:
        word = None
        for result in search_result_specific_back:
            # print("Here")
            print(result)
            word = result.group('dep')
            if word:
                ls_result.append(word)
                word = None
            word = result.group('dis')
            if word:
                ls_result.append(word)
                word = None
            word = result.group('sea')
            if word:
                ls_result.append(word)
                word = None
            word = result.group('dep2')
            if word:
                ls_result.append(word)
                word = None
            word = result.group('dis2')
            if word:
                ls_result.append(word)
                word = None
            word = result.group('sea2')
            if word:
                ls_result.append(word)
                word = None

    search_result_specific_front = re.finditer(condition_specific_front, message, flags=re.IGNORECASE)
    # print(search_result_specific)
    if search_result_specific_front:
        word = None
        for result in search_result_specific_front:
            # print("Here")
            print(result)
            word = result.group('dep')
            if word:
                ls_result.append(word)
                word = None
            word = result.group('dis')
            if word:
                ls_result.append(word)
                word = None
            word = result.group('sea')
            if word:
                ls_result.append(word)
                word = None

    if len(ls_result) > 0:
        return ls_result

    condition_back = r"(?:(?:status of )|(?:status )|(?:meaning of ))+(?P<target1>\w+)|(?:is )(?P<target2>\w+( )*\?)"
    condition_front = r"(?:(?P<target>\w+)(?:( stand[s]{0,1} for)|(?: mean[s]{0,1})|(?: refer[s]{0,1} to)|(?: status)))"
    search_result_back = re.finditer(condition_back, message, flags=re.IGNORECASE)
    if search_result_back:
        for result in search_result_back:
            # print(result)
            if result.group('target1'):
                word = result.group('target1').strip()
                if word not in stop_words:
                    ls_result.append(word)
            elif result.group('target2'):
                word = result.group('target2').strip().replace('?', '')
                if word not in stop_words:
                    ls_result.append(word)

    search_result_front = re.finditer(condition_front, message, flags=re.IGNORECASE)
    if search_result_front:
        for result in search_result_front:
            # print(result)
            word = result.group('target').strip()
            if word not in stop_words:
                ls_result.append(word)

    return ls_result


def __filter(segment, splitter):
    #print("In filter")
    #print(segment)
    ls_result = []
    if splitter == "all":
        and_seg = segment.split("and")
        for and_word in and_seg:
            #print("andword", and_word)
            if ',' in and_word:
                #print(and_word)
                comma_seg = and_word.split(',')
                for comma_word in comma_seg:
                    ls_result.append(comma_word)
            else:
                ls_result.append(and_word)
    else:
        ls_result = segment.split(splitter)
    return ls_result


def __parse_result(r1, r2, ls_result, stop_words):
    ls_result = []
    # print(r1, r2)
    if r1:
        if r1 == r2:
            if "and " in r1 and ',' in r1:
                r1 = __filter(r1, "all")
                for word in r1:
                    if word not in stop_words:
                        ls_result.append(word)
            elif "and " in r1:
                r1 = __filter(r1, "and")
                # print(r1)
                for word in r1:
                    if word not in stop_words:
                        ls_result.append(word)
            elif ',' in r1:
                r1 = __filter(r1, ',')
                # print(r1)
                for word in r1:
                    if word not in stop_words:
                        ls_result.append(word)
            else:
                # print("else",r1)
                if r1 not in stop_words:
                    ls_result.append(r1)
        else:
            if "and " in r1 and ',' in r1:
                r1 = __filter(r1, "all")
                for word in r1:
                    if word not in stop_words:
                        ls_result.append(word)
            elif "and " in r1:
                r1 = __filter(r1, "and")
                # print(r1)
                for word in r1:
                    if word not in stop_words:
                        ls_result.append(word)
            elif ',' in r1:
                r1 = __filter(r1, ',')
                # print(r1)
                for word in r1:
                    if word not in stop_words:
                        ls_result.append(word)
            else:
                if r1 not in stop_words:
                    ls_result.append(r1)

            if r2:
                if "and " in r2 and ',' in r2:
                    r2= __filter(r2, "all")
                    for word in r2:
                        if word not in stop_words:
                            ls_result.append(word)
                elif "and " in r2:
                    r2 = __filter(r2, "and")
                    # print(r2)
                    for word in r2:
                        if word not in stop_words:
                            ls_result.append(word)
                elif ',' in r2:
                    r2 = __filter(r2, ',')
                    # print(r2)
                    for word in r2:
                        if word not in stop_words:
                            ls_result.append(word)
                else:
                    for word in r2:
                        if word not in stop_words:
                            ls_result.append(word)
    return ls_result


def __search_new(message, stop_words):
    condition1 = r"\b(?:(?:book|with )?status)(?: of)? (?P<target>(?:[a-z]+,? (?:[a-z ]+)?and (?:[a-z ]+))|(?P<target2>[a-z ]+))\b"
    condition2 = r"\b(?:do(?:es)?) (?P<target>(?:[a-z]+,? (?:[a-z ]+)?and (?:[a-z ]+))|(?P<target2>[a-z ]+))(?: (?:mean[s]{0,1}?|stand[s]{0,1}? for|refer[s]{0,1}? to))\b"
    condition3 = r"\b(?:what(?:`s| is)(?: the meaning of)? (?P<target>(?:[a-z]+,? (?:[a-z ]+)?and (?:[a-z ]+))|(?P<target2>[a-z ]+)))\b"
    # condition4 = r"\b(?P<target>(?:[a-z]+,? (?:[a-z ]+)?and (?:[a-z ]+))|(?P<target2>[a-z ]+))(?: (?:status))\b"

    result_cond1 = re.search(condition1, message, flags=re.IGNORECASE)
    result_cond2 = re.search(condition2, message, flags=re.IGNORECASE)
    result_cond3 = re.search(condition3, message, flags=re.IGNORECASE)
    # result_cond4 = re.search(condition4, message, flags=re.IGNORECASE)

    ls_result = []
    if result_cond1:
        # print(1)
        target1 = result_cond1.group('target')
        target2 = result_cond1.group('target2')
        for word in __parse_result(target1, target2, ls_result, stop_words):
            ls_result.append(word)
    # print(ls_result)
    if result_cond2:
        # print(2)
        target1 = result_cond2.group('target')
        target2 = result_cond2.group('target2')
        for word in __parse_result(target1, target2, ls_result, stop_words):
            ls_result.append(word)
    # print(ls_result)
    if result_cond3:
        # print(3)
        target1 = result_cond3.group('target')
        target2 = result_cond3.group('target2')
        for word in __parse_result(target1, target2, ls_result, stop_words):
            ls_result.append(word)
    #print(ls_result)
    # if result_cond4:
    #     # print(4)
    #     target1 = result_cond4.group('target')
    #     target2 = result_cond4.group('target2')
    #     for word in __parse_result(target1, target2, ls_result, stop_words):
    #         ls_result.append(word)
    # print(ls_result)

    return ls_result

ls_msgs = ["What does bindery means?", "What does cat department and available stands for?", "What is the meaning of bindery, available and withdraw?", "What does bindery refers to?",
           "What is bindery?", "I saw a book on the website with status transferred and available, what does it mean?", "If a book has a status of bindery, what does it refers to?",
           "book status withdraw", "bindery status", "what is cat department?"]

# ls_msgs = ["What is cat department?"]

ls_stop_words = get_stop_words('en')

for msg in ls_msgs:
    ls_word = __search_new(msg, ls_stop_words)
    print(ls_word)
