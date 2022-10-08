import numba as nb
import numpy as np

import winsound
import aiohttp
import asyncio
import random
import types

# Preparations (ASCII-symbols + left and right link parts)
CHAR_ARRAY = np.array(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
                            's','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J',
                            'K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1',
                            '2','3','4','5','6','7','8','9'])
LEFT       = np.array(['h','t','t','p','s',':','/','/','d','i','s','c','o','r','d','a','p','p',
                            '.','c','o','m','/','a','p','i','/','v','9','/','e','n','t','i','t','l',
                            'e','m','e','n','t','s','/','g','i','f','t','-','c','o','d','e','s','/'])
RIGHT      = np.array(['?','w','i','t','h','_','a','p','p','l','i','c','a','t','i','o','n','=',
                            'f','a','l','s','e','&','w','i','t','h','_','s','u','b','s','c','r','i',
                            'p','t','i','o','n','_','p','l','a','n','=','t','r','u','e'])

# Generate random ascii symbol for createNitroLink function (numba requires that)
@nb.njit(fastmath=True, nogil=True)
def genRandomAsciiSymbol(): return CHAR_ARRAY[random.randint(0, 61)]

# Generate numpy array with length 19 and "<U1" data type (also for numba, I would never divide common link generation for 3 parts)
@nb.njit(fastmath=True, nogil=True)
def createEmptyNitroCodeArray(): return np.empty(shape=19, dtype="<U1")

# Generate random link with steroid speedup - 1 million links in 35 seconds (90s without njit)
@nb.njit(fastmath=True, nogil=True)
def genNitroLink():
    gen_code = createEmptyNitroCodeArray()
    for j in nb.prange(19): gen_code[j] = genRandomAsciiSymbol()
    return "".join(np.concatenate((LEFT, gen_code, RIGHT)))

# Check if url is valid, print the gift link in terminal and make sound notification
async def checkNitroLinkValidation(url: str):
    async with aiohttp.request("HEAD", url) as response:
        if response.status == 200: print(f"Valid gift: https://discord.gift/{url[54:73]}"); winsound.Beep(2000, 1000)


# Pre-compiling cyclic code (like sending request for example) to bytecode and speed up or program even MORE
print_border: types.CodeType = compile("print('-'*100)", "", "eval", 8192)
