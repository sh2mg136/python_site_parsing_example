import ParsePart1
import ParsePart2
import time

import YieldExample

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67"}

start = time.time()

# ParsePart1.start_process()

ParsePart2.start_process(2)

end = time.time()
print("\nOK")
print(f"Elapsed time: {round(end - start, 4)} sec\n")

YieldExample.run_me()

YieldExample.calc_cubes()




