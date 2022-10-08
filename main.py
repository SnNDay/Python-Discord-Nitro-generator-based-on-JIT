import aiomultiprocess   as amp
import numpy             as np

import asyncio
import aiohttp
import os

from cmpld import (
    genRandomAsciiSymbol,
    createEmptyNitroCodeArray,
    genNitroLink,
    checkNitroLinkValidation,
    print_border,
)



# Every function that can be speed up by copilation are in *compiled* or *cmpd* file
async def main():

    print("Preparations before running...")

    genRandomAsciiSymbol()                                            # Warming up these functions with numba's Just-In-Time compilation
    createEmptyNitroCodeArray()
    genNitroLink()
    link_container = np.empty(shape=os.cpu_count()*16, dtype="<U124") # Prepared array to change values faster

    input("Welcome to Nitro Generator v1.0! Press Enter to begin. You can stop the program by closing terminal")
    exec(print_border)

    async with amp.Pool(os.cpu_count()*16) as pool:                   # Async multiprocessing for using all CPU power
        while True:
            link_container.fill(genNitroLink())
            try: await pool.map(checkNitroLinkValidation, link_container)
            except aiohttp.ServerDisconnectedError: ...

if __name__ == "__main__": asyncio.run(main())