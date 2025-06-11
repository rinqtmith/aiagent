from functions.get_files_info import get_files_info


test = get_files_info("calculator", ".")
print(test)
test2 = get_files_info("calculator", "pkg")
print(test2)
test3 = get_files_info("calculator", "/bin")
print(test3)
test4 = get_files_info("calculator", "../")
print(test4)
