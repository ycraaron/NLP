from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')
# nlp = StanfordCoreNLP('http://192.168.0.100:9000')


def stanford_tree(line, annotators='tokenize,ssplit,pos,ner,parse,depparse,coref'):
    output = nlp.annotate(line, properties={
        'annotators': annotators,
        'outputFormat': 'json'
    })
    try:
        return output
    except IndexError:
        pass


def __swap(nlp_tag):
    sentence_swap = []
    for sentence in nlp_tag['sentences']:
        sentence_swap = [token_item['originalText'] for token_item in sentence['tokens']]
        sen_with_pos = [token_item['pos'] + '_' + token_item['originalText'] for token_item in sentence['tokens']]
        ls_dependency = [{'type_dep': dependency['dep'], 'from':dependency['governorGloss'], 'index_from':dependency['governor']-1, 'to': dependency['dependentGloss'], 'index_to':dependency['dependent']-1} for dependency in sentence['basicDependencies']]
        for dependency in ls_dependency:
            if dependency['type_dep'] == 'nsubj':
                index_from = dependency['index_from']
                index_to = dependency['index_to']
                tag_pos_from = sen_with_pos[index_from].split('_')[0]
                tag_pos_to = sen_with_pos[index_to].split('_')[0]
                # deal with NN*, DT case
                if [tag_pos_from, tag_pos_to] == ["NN", "DT"] or [tag_pos_from, tag_pos_to] == ["NNS", "DT"] or [tag_pos_from, tag_pos_to] == ["NNP", "DT"] or [tag_pos_from, tag_pos_to] == ["NNPS", "DT"]:
                    is_compound = 0
                    # save the index of all compound word for add/delete use
                    ls_from_index_compound = []
                    # search compound NN
                    for com_dependency in ls_dependency:
                        # if compound is found and they share a same governor, the word is a part of the compound word
                        if com_dependency['type_dep'] == 'compound' and com_dependency['index_from'] == index_from:
                            if is_compound == 0:
                                is_compound = 1
                            ls_from_index_compound.append(com_dependency['index_to'])
                    # no compound word found, swap NN* and DT
                    if is_compound == 0:
                        sentence_swap[index_to] = sentence_swap[index_from]
                    # compound word found
                    else:
                        # first swap the root NN with DT
                        sentence_swap[index_to] = sentence_swap[index_from]
                        ls_word_to_move = []
                        # record the index of the words which need to be moved
                        ls_from_index_compound.reverse()
                        for index in ls_from_index_compound:
                            ls_word_to_move.append(sentence_swap[index])
                        # remove the words from the original list
                        # sentence_swap = [i for j, i in enumerate(sentence_swap) if j not in ls_from_index_compound]
                        # insert the removed words at the beginning
                        for word in ls_word_to_move:
                            sentence_swap.insert(0, word)

                # deal with DT1, DT2 -> NN* case
                # DT1, DT2->compound NN* case
                # simply swap the part "DT2->NN*" with DT1
                elif [tag_pos_from, tag_pos_to] == ["DT", "DT"]:
                    nmod_existed = 0
                    index_end = 0

                    # find the NN* through nmod dependency
                    for nmod_dependency in ls_dependency:
                        if nmod_dependency['type_dep'] == "nmod":
                            if nmod_existed == 0:
                                index_end = nmod_dependency['index_to']
                                nmod_existed = 1

                    if nmod_existed == 0:
                        sentence_swap[index_to] = sentence_swap[index_from]
                    elif nmod_existed == 1:
                        sentence_swap[index_to] = sentence_swap[index_from]

                        # Search compound NN
                        is_compound = 0
                        ls_from_index_compound = []
                        for com_dependency in ls_dependency:
                            # if compound is found and they share a same governor, the word is a part of the compound word
                            if com_dependency['type_dep'] == 'compound' and com_dependency['index_from'] == index_end:
                                if is_compound == 0:
                                    is_compound = 1
                                ls_from_index_compound.append(com_dependency['index_to'])
                                print(ls_from_index_compound)
                        # no compound word found, swap NN* and DT
                        if is_compound == 0:
                            sentence_swap[index_to] = sentence_swap[index_from]
                        # compound word found
                        else:
                            # first swap the root NN with DT
                            sentence_swap[index_to] = sentence_swap[index_end]
                            ls_word_to_move = []
                            # record the index of the words which need to be moved
                            ls_from_index_compound.reverse()
                            for index in ls_from_index_compound:
                                ls_word_to_move.append(sentence_swap[index])
                            # remove the words from the original list
                            # sentence_swap = [i for j, i in enumerate(sentence_swap) if j not in ls_from_index_compound]
                            # insert the removed words at the beginning
                            for word in ls_word_to_move:
                                sentence_swap.insert(0, word)

                        # # generate the index of the words which need to be moved
                        # ls_moved_index = [i for i in range(index_from+1, index_end+1)]
                        # ls_moved_index.reverse()
                        # # print(ls_moved_index)
                        # ls_word_to_move = []
                        # # record the words to be moved
                        # for index in ls_moved_index:
                        #     ls_word_to_move.append(sentence_swap[index])
                        # # remove the words from the message
                        # sentence_swap = [i for j, i in enumerate(sentence_swap) if j not in ls_moved_index]
                        # for word in ls_word_to_move:
                        #     sentence_swap.insert(1, word)

    return sentence_swap

message = "This is some of the library card that I would like to borrow"
result_tags = stanford_tree(message)
#print(result_tags)

print("Original message: ", message)
message_swap = " ".join(word for word in __swap(result_tags))
print("Swapped  message: ", message_swap)