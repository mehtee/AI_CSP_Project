from copy import deepcopy
import State
import Binairo
from utils import col_of_arr_with_index


def new_domain_after_check_circles_limit(variables_domain, variable_index):
    x, y = variable_index[0], variable_index[1]

    row = variables_domain[x][:]
    column = col_of_arr_with_index(variables_domain, y)
    var_domain_after_check = variables_domain[x][y]

    # Checking the row

    # if it is more than the half of the size of row/col
    row_bool = (row.count("W") > len(row) / 2) or (row.count("B") > len(row) / 2)
    col_bool = (column.count("W") > len(column) / 2) or (column.count("B") > len(column) / 2)
    if row_bool or col_bool:
        return False

    # if it is exactly the half in row
    if row.count("W") == len(row) / 2 and "W" in var_domain_after_check:
        var_domain_after_check.remove("W")

    if row.count("B") == len(row) / 2 and "B" in var_domain_after_check:
        var_domain_after_check.remove("B")

    # Checking the column
    # if it is exactly the half in col
    if column.count("W") == len(column) / 2 and "W" in var_domain_after_check:
        var_domain_after_check.remove("W")

    if column.count("B") == len(column) / 2 and "B" in var_domain_after_check:
        var_domain_after_check.remove("B")

    return var_domain_after_check


def var_domain_after_check_more_than_two_limit(arr, index, domain):
    var_domain_after_check = deepcopy(domain)

    # if Ba'd va Ba'd-tar is the same, then the current shouldn't be the same as that, changing domain of current
    if index <= len(arr) - 3 and arr[index + 1] == arr[index + 2] and (
            arr[index + 1] == "W" or arr[index + 1] == "B") and arr[index + 1] in var_domain_after_check:
        var_domain_after_check.remove(arr[index + 1])

    # if Ghabl va Ghabl-tar is the same, then the current shouldn't be the same as that, changing domain of current
    if index > 1 and arr[index - 1] == arr[index - 2] and (
            arr[index - 1] == "W" or arr[index - 1] == "B") and arr[index - 1] in var_domain_after_check:
        var_domain_after_check.remove(arr[index - 1])

    # if Ghabl va Ba'd is the same, then the current shouldn't be the same as that, changing domain of current
    if len(arr) - 2 >= index > 0 and arr[index - 1] == arr[index + 1] and (
            arr[index - 1] == "W" or arr[index - 1] == "B") and arr[index - 1] in var_domain_after_check:
        var_domain_after_check.remove(arr[index - 1])

    return var_domain_after_check


def domain_after_check_more_than_two_limit(variables_domain, variable_index):
    x, y = variable_index[0], variable_index[1]
    domain = variables_domain[x][y]

    # check in row
    row = variables_domain[x]
    new_domain = var_domain_after_check_more_than_two_limit(row, y, domain)

    # check in column
    column = col_of_arr_with_index(variables_domain, y)
    new_domain = var_domain_after_check_more_than_two_limit(column, x, new_domain)

    if len(new_domain) == 0:
        return False

    return new_domain


def check_for_new_domain(variables_domain, variable_index, state):
    variables_domain_copy = deepcopy(variables_domain)
    x, y = variable_index

    new_domain = new_domain_after_check_circles_limit(variables_domain_copy, variable_index)

    failure = False, []

    if new_domain == False:
        return failure
    variables_domain_copy[x][y] = new_domain

    # check rule 2
    flag = Binairo.is_unique(state)
    if not flag:
        return failure


    new_domain = domain_after_check_more_than_two_limit(variables_domain_copy, variable_index)
    if new_domain == False:
        return failure
    variables_domain_copy[x][y] = new_domain

    return True, variables_domain_copy

