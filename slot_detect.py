from slots import RuleBaseSlot
from xlutils.copy import copy

import re
import xlrd
import xlwt


def validate(word, reg):
    return True

slot = RuleBaseSlot('hku')
slot_regex = slot.slots_regex

#print(slot_regex["LEXICA_UserTypeUndergradFinalYear"])

current_row = 0
sheet_num = 0
input_total = 0
output_total = 0

src = "/Users/Aaron/Intralogue/slot_filter.xlsx"
output_workbook = "/Users/Aaron/Intralogue/output.xls"

work_book = xlrd.open_workbook(src)
result_work_book = copy(work_book)


work_sheet = work_book.sheet_by_index(sheet_num)
result_work_sheet = result_work_book.get_sheet(sheet_num)


slot_type = "LEXICA_" + work_sheet.cell_value(0, 0)

i = 0
while True:
    slot_column_index = 2 * i
    result_column_index = 2 * i + 1
    cnt_row = work_sheet.nrows
    cnt_col = work_sheet.ncols
    # result_column = work_sheet.cell_value(0, result_column_index)

    # print(slot_category)
    # print(result_column)
    # print(result_column == "")

    # if slot_category == "" and result_column == "":
    # if slot_column_index > cnt_col:
    if work_sheet.cell_value(0, slot_column_index) == "END":
        i = 0
        sheet_num += 1
        print("Prepare move to sheet", sheet_num)
        work_sheet = work_book.sheet_by_index(sheet_num)
        result_work_sheet = result_work_book.get_sheet(sheet_num)
        slot_column_index = 2 * i
        result_column_index = 2 * i + 1
        cnt_row = work_sheet.nrows
        cnt_col = work_sheet.ncols
        if work_sheet.cell_value(0, 0) == "END":
            print("ALL END")
            break
        print("Move to next sheet")
        print("Row:", cnt_row, "Column:", cnt_col)

    slot_category = "LEXICA_" + work_sheet.cell_value(0, slot_column_index)
    reg = slot_regex[slot_category]
    # print(reg)
    j = 2
        # result_column_word = work_sheet.cell_value(j, slot_column_index)
        # print("word: ", result_column_word)
        # print("Rows: ", cnt_row, "Columns: ", cnt_col)
        # print("Numer of sheet", sheet_num)
    while j < cnt_row:
        word = work_sheet.cell_value(j, slot_column_index)
        # print(j, word)
        if word != "":
            result = re.search(reg[0], word, flags=re.IGNORECASE)
            # print(result)
            word = work_sheet.cell_value(j, slot_column_index)
            if result is None:
                result_work_sheet.write(j, result_column_index, 0)
            else:
                result_work_sheet.write(j, result_column_index, 1)
            # print("j: ", j, "word: ", word)
            j += 1
            # print("is word null?", j == u'')
        else:
            break
    i += 1

result_work_book.save(output_workbook)

# validate()

