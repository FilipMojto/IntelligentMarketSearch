import concurrent.futures
import threading
from typing import List
import hashlib


class TextEditor:
    def __init__(self) -> None:
        pass

    @staticmethod
    def wrap_text(text: str, index: int = 3) -> str:
        result = ''
        for i, char in enumerate(text, start=1):
            result += char
            if i % index == 0:
                result += '\n'
        return result

    @staticmethod
    def join_text(text: str) -> str:
        result = ''

        for char in text:

            if char == '\n':
                continue

            result += char
        
        return result    


# class SignalHandler:
#     def __init__(self) -> None:
#         self.__groups: List[List[threading.Event]] = []

#     def add_group(self, group: List[threading.Event] = []):
#         self.__groups.append(group)

#     def remove_group(self, index: int):
#         self.__groups.pop(index)

#     def pop_first_complete(self) -> int:
#         for index, group in enumerate(self.__groups):
#             found_ = True

#             for inner_index, signal in enumerate(group):
#                 if not signal.is_set():
#                     print(f"Signal {inner_index} not set!")
#                     found_ = False
#                     break
            
#             if found_:
#                 self.__groups.pop(index)
#                 return index
#         else :
#             return -1


def hash_string(s, algorithm='sha256'):
    # Create a hash object using the specified algorithm
    hash_object = hashlib.new(algorithm)

    # Update the hash object with the bytes representation of the string
    hash_object.update(s.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    return hash_object.hexdigest()

# def fnv1a_hash(string):
#     """
#     FNV-1a hash function for string hashing.
#     """
#     # FNV-1a constants
#     FNV_PRIME = 16777619
#     offset_basis = 2166136261

#     # Initialize hash value to the offset basis
#     hash_value = offset_basis

#     # Hash each byte of the string
#     for byte in string.encode('utf-8'):
#         hash_value ^= byte
#         hash_value *= FNV_PRIME

#     return hash_value

class ThreadPool:

    def __init__(self, max_threads):
        self.__executor = concurrent.futures.ThreadPoolExecutor(max_threads)
        self.__thread_lock = threading.Lock()
        self.__futures: List[concurrent.futures.Future] = []

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.__executor.shutdown(wait=True)

    def schedule_task(self, task, *args, **kwargs):
        with self.__thread_lock:
            future = self.__executor.submit(task, *args, **kwargs)
            self.__futures.append(future)

        return future

    def wait_until_complete(self, task = None, timeout: int = 3, *args, **kwargs):

        with self.__thread_lock:
            #for future in concurrent.futures.as_completed(self.__futures):
            for future in self.__futures:
                print('CHECKING FUTURE!')
                if task:
                   while(True): 
                        try:
                            future.result(timeout=timeout)
                        except concurrent.futures.TimeoutError as e:
                            print("FINALLY EXECUTING!")
                            task(*args, **kwargs)
                            continue
                        break

                else:
                    print("NO TASK!")
                    future.result()

        self.__futures.clear()