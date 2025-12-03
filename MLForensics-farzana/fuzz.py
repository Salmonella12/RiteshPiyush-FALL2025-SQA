"""
fuzz.py
Fuzz 5 functions from mining/mining.py as required by the SQA project.

Functions fuzzed:
 1) giveTimeStamp()
 2) deleteRepo(dirName, type_)
 3) dumpContentIntoFile(strP, fileP)
 4) makeChunks(the_list, size_)
 5) days_between(d1_, d2_)
"""

import os
import random
import string
import shutil
import logging
from datetime import datetime, timedelta

# Import ONLY functions that actually exist in mining/mining.py
from mining.mining import (
    giveTimeStamp,
    deleteRepo,
    dumpContentIntoFile,
    makeChunks,
    days_between,
)

# Log file that you will later include as evidence in the repo/report
LOG_FILE = "fuzz_results.log"

logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# All temporary stuff for fuzzing is kept here (safe to delete)
BASE_TMP_DIR = os.path.join(os.path.dirname(__file__), "fuzz_tmp")


def random_string(min_len=0, max_len=200):
    length = random.randint(min_len, max_len)
    return "".join(random.choices(string.printable, k=length))


def random_datetime(start_year=1970, end_year=2030):
    """Return a random datetime between the given years."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta_days = (end - start).days
    day_offset = random.randint(0, delta_days)
    second_offset = random.randint(0, 86399)
    return start + timedelta(days=day_offset, seconds=second_offset)


def setup_tmp_dir():
    if os.path.exists(BASE_TMP_DIR):
        shutil.rmtree(BASE_TMP_DIR)
    os.makedirs(BASE_TMP_DIR, exist_ok=True)


def fuzz_giveTimeStamp(iterations=50):
    logging.info("=== Fuzzing giveTimeStamp() ===")
    for i in range(iterations):
        try:
            ts = giveTimeStamp()
            # Basic sanity check
            if not isinstance(ts, str):
                logging.error("Iteration %d: giveTimeStamp returned non-string: %r", i, ts)
            else:
                logging.info("Iteration %d: OK giveTimeStamp() -> %s", i, ts)
        except Exception as e:
            logging.exception("Iteration %d: EXCEPTION in giveTimeStamp(): %s", i, e)


def fuzz_dumpContentIntoFile(iterations=50):
    logging.info("=== Fuzzing dumpContentIntoFile(strP, fileP) ===")
    for i in range(iterations):
        try:
            content = random_string(0, 500)
            file_name = f"fuzz_file_{i}.txt"
            file_path = os.path.join(BASE_TMP_DIR, file_name)

            returned_size = dumpContentIntoFile(content, file_path)

            # Verify file exists and size matches length of content
            if not os.path.exists(file_path):
                logging.error("Iteration %d: File not created: %s", i, file_path)
            else:
                actual_size = os.stat(file_path).st_size
                logging.info(
                    "Iteration %d: dumpContentIntoFile -> returned=%s, actual=%s",
                    i,
                    returned_size,
                    actual_size,
                )
        except Exception as e:
            logging.exception(
                "Iteration %d: EXCEPTION in dumpContentIntoFile(): %s", i, e
            )


def fuzz_deleteRepo(iterations=50):
    logging.info("=== Fuzzing deleteRepo(dirName, type_) ===")
    for i in range(iterations):
        try:
            # For half the iterations, create a real directory; for the other half, use a non-existent one
            if i % 2 == 0:
                dir_name = os.path.join(BASE_TMP_DIR, f"dir_{i}")
                os.makedirs(dir_name, exist_ok=True)
                # create a nested file
                with open(os.path.join(dir_name, "dummy.txt"), "w") as f:
                    f.write("dummy")
            else:
                dir_name = os.path.join(BASE_TMP_DIR, f"nonexistent_{i}")

            type_str = random.choice(["FUZZ", "TEST", "", random_string(0, 10)])
            deleteRepo(dir_name, type_str)

            logging.info(
                "Iteration %d: deleteRepo(%r, %r) -> exists_after=%s",
                i,
                dir_name,
                type_str,
                os.path.exists(dir_name),
            )
        except Exception as e:
            logging.exception("Iteration %d: EXCEPTION in deleteRepo(): %s", i, e)


def fuzz_makeChunks(iterations=50):
    logging.info("=== Fuzzing makeChunks(the_list, size_) ===")
    for i in range(iterations):
        try:
            # Random list length and chunk size (avoid zero to prevent division problems)
            list_len = random.randint(0, 100)
            base_list = [random.randint(-1000, 1000) for _ in range(list_len)]
            chunk_size = random.randint(1, 20)

            chunks = list(makeChunks(base_list, chunk_size))
            flattened = [x for chunk in chunks for x in chunk]

            # Basic invariants
            if flattened != base_list:
                logging.error(
                    "Iteration %d: makeChunks lost or reordered elements. "
                    "original_len=%d, flattened_len=%d",
                    i,
                    len(base_list),
                    len(flattened),
                )
            else:
                logging.info(
                    "Iteration %d: OK makeChunks(len=%d, size=%d) -> %d chunks",
                    i,
                    len(base_list),
                    chunk_size,
                    len(chunks),
                )
        except Exception as e:
            logging.exception("Iteration %d: EXCEPTION in makeChunks(): %s", i, e)


def fuzz_days_between(iterations=50):
    logging.info("=== Fuzzing days_between(d1_, d2_) ===")
    for i in range(iterations):
        try:
            # Mostly valid datetimes
            if random.random() < 0.8:
                d1 = random_datetime()
                # random offset +/- 1000 days
                d2 = d1 + timedelta(days=random.randint(-1000, 1000))
            else:
                # Occasionally feed "weird" values to see robustness
                choices = [
                    random_string(0, 20),
                    None,
                    123,
                    datetime.now(),
                    datetime.now().isoformat(),
                ]
                d1 = random.choice(choices)
                d2 = random.choice(choices)

            result = days_between(d1, d2)

            # If it returns successfully, we at least expect a non-negative integer
            if not isinstance(result, int) or result < 0:
                logging.error(
                    "Iteration %d: days_between(%r, %r) -> suspicious result: %r",
                    i,
                    d1,
                    d2,
                    result,
                )
            else:
                logging.info(
                    "Iteration %d: OK days_between(%r, %r) -> %d",
                    i,
                    d1,
                    d2,
                    result,
                )
        except Exception as e:
            logging.exception(
                "Iteration %d: EXCEPTION in days_between(%r, %r): %s", i, d1, d2, e
            )


def main():
    setup_tmp_dir()
    logging.info("==== STARTING FUZZING RUN ====")

    fuzz_giveTimeStamp()
    fuzz_dumpContentIntoFile()
    fuzz_deleteRepo()
    fuzz_makeChunks()
    fuzz_days_between()

    logging.info("==== FUZZING RUN COMPLETE ====")

    # Optionally, remove the temporary directory at the end
    try:
        shutil.rmtree(BASE_TMP_DIR)
    except Exception:
        # If cleanup fails, it's not critical – directory is small.
        pass


if __name__ == "__main__":
    main()
