def col_of_arr_with_index(arr, column_index):
    column = []
    for row in arr:
        column.append(row[column_index])

    return column