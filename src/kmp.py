def kmp(keyword, stringInput):
    # Keyword yang dicari harus lebih panjang dari stringInput tersisa
    keyword = keyword.lower()
    stringInput = stringInput.lower()
    if (len(stringInput) >= len(keyword)):
        j = 0
        while (j < len(keyword) and keyword[j] == stringInput[j]):
            j += 1
        if (j == len(keyword)):
            return True;
        else :
            # Prefix dan Suffix
            if (j > 1):
                k = 1
                obtained = False
                while (obtained == False and k <= j-1):
                    if (keyword[0 : j-k] == stringInput[j-k : j]):
                        obtained = True
                        break
                    k += 1
                
                if (obtained == True):
                    moveforward = j - len(keyword[0 : j-k])
                    return kmp(keyword,stringInput[moveforward:])

                # Tidak ada prefix sufix yang sepadan.
                else :
                    moveforward = 1
                    return kmp(keyword,stringInput[1:])
            # J <= 1
            else:
                moveforward = 1
                return kmp(keyword,stringInput[1:])
    else :

        return False