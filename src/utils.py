def newlinestrip(arr):
    '''
    Takes a array-type argument with newline characters in values & strips them
    Args:
        arr : (list/tuple/set) array-type object to remove newline characters from
    Return:
        arr : (list/tuple/set) array-type object with all newline characters removed
    '''
    temp_arr = list()
    for val in arr:
        temp_arr.append(val.replace('\n', ''))
    return temp_arr

def remove_extension(filename):
    '''
    Takes a string argument and removes the extension (all characters after final '.')
    Args:
        filename : (string) name of file/filepath to remove extension from
    Return:
        filename : (string) file/filepath with extension removed
    '''
    filename = '.'.join(filename.split('.')[:-1])
    return filename