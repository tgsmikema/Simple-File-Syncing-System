#!/usr/bin/env python3

# Once you have a ./sync command you can use this file to test it.
# The fact this test program is in Python has nothing to do with the language
# you use for your solution, because the command is called as though from the 
# command line.
# Comment out the bits at the bottom of the program you don't want to run.
# The order from 1 to 9 is mostly from easiest to hardest.

import os
import shutil
import time

def surround_test(message, test):
    print("*" * 40)
    print(message)
    test()
    print("*" * 40 + "\n")

def print_directory(directory, spaces):
    """Pretty print a directory, with indenting indicating subdirectories."""
    for file in os.listdir(directory):
        if file[0] != ".": # don't show files starting with '.'
            print(" " * spaces + "-" + file, end="")
            path = directory + "/" + file
            if os.path.isfile(path):
                modified_time = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(os.path.getmtime(path)))
                print(" " + str(os.path.getsize(path)) + " " + modified_time)
            else:
                print()
            if os.path.isdir(path):
                print_directory(path, spaces + 4)

def print_file(name):
    with open(name) as file:
        print(file.read())

def remove_all_files():
    shutil.rmtree("dir1", ignore_errors=True)
    shutil.rmtree("dir2", ignore_errors=True)

def remove_files(files):
    for file in files:
        os.remove(file)

def test_sync():
    os.system("./sync dir1 dir2")

def make_file(name, contents):
    with open(name, "w") as file:
        file.write("The contents of file, base/{}:\n".format(name) + contents)

def append_file(name, extra):
    with open(name, "a") as file:
        file.write(extra)

def setup_no_overlap():
    remove_all_files()
    # make the directories
    os.mkdir("dir1")
    os.mkdir("dir2")
    # make the initial files
    make_file("dir1/a.txt", "Not very exciting really.")
    make_file("dir1/b.txt", "Also, not very exciting.")
    make_file("dir2/c.txt", "Still not very exciting.")

def setup_with_overlap():
    setup_no_overlap()
    time.sleep(2) # to make sure the modified times are different
    make_file("dir2/a.txt", "This should replace the one in dir1.")

def setup_with_overlap_and_subdirectories():
    remove_all_files()
    # make all of the directories
    for name in ["dir1", "dir1/dir1_1", "dir1/dir1_1/dir1_1_1", "dir1/dir1_2", "dir2", "dir2/dir2_1"]:
        os.mkdir(name)
    # make the initial files
    make_file("dir1/file1_1.txt", "Not very exciting really.")
    make_file("dir1/file1_2.txt", "Also, not very exciting.")
    make_file("dir1/dir1_1/dir1_1_1/file1_1_1_1.txt", "But the pathname is exciting.")
    make_file("dir1/dir1_2/file1_2_1.txt", "")
    make_file("dir2/file2_1.txt", "Still not very exciting.")
    make_file("dir2/dir2_1/file2_1_1.txt", "Also, not very exciting.")
    time.sleep(2) # to make sure the modified times are different
    make_file("dir2/file1_1.txt", "This should replace the one in dir1.")

# The tests follow here

def p1():
    remove_all_files()
    test_sync()

def p2():
    remove_all_files()
    os.mkdir("dir1")
    test_sync()
    directories = [f for f in os.listdir(".") if os.path.isdir(f)]
    print("\n".join(directories))

def p3():
    remove_all_files()
    os.mkdir("dir1")
    make_file("dir1/file1_1.txt", "Not very exciting really.")
    test_sync()
    print_file("dir1/.sync")

def p4():
    remove_all_files()
    os.mkdir("dir1")
    make_file("dir1/file1_1.txt", "Not very exciting really.")
    test_sync()
    print_file("dir1/.sync")
    append_file("dir1/file1_1.txt", "\nNew data written.")
    test_sync()
    print_file("dir1/.sync")

def p5():
    setup_no_overlap()
    test_sync()
    print_directory('dir1', 0)
    print()
    print_directory('dir2', 0)

def p6():
    setup_with_overlap()
    test_sync()
    print_directory('dir1', 0)
    print()
    print_directory('dir2', 0)

def p7():
    p6()
    print("\n --- then after the change ---\n")
    # now make changes to dir2
    extra = "\nchanged in both."
    append_file("dir2/a.txt", extra)
    append_file("dir2/b.txt", extra)
    append_file("dir2/c.txt", extra)
    test_sync()
    print_directory('dir1', 0)
    print()
    print_directory('dir2', 0)

def p8():
    p5()
    print("\n --- only c.txt ---\n")
    remove_files(["dir1/b.txt", "dir2/a.txt"])
    test_sync()
    print_directory('dir1', 0)
    print()
    print_directory('dir2', 0)
    print("\n --- new b.txt ---\n")
    make_file("dir2/b.txt", "This doesn't hang around for long.")
    test_sync()
    os.remove("dir1/b.txt")
    test_sync()
    make_file("dir1/b.txt", "This one survives.")
    test_sync()
    print_directory('dir1', 0)
    print()
    print_directory('dir2', 0)

def p9():
    setup_with_overlap_and_subdirectories()
    test_sync()
    print_directory('dir1', 0)
    print()
    print_directory('dir2', 0)
    print("\n --- delete all files ---\n")
    remove_files(["dir1/file1_1.txt", "dir1/file1_2.txt", "dir1/dir1_1/dir1_1_1/file1_1_1_1.txt",
        "dir1/dir1_2/file1_2_1.txt", "dir2/file2_1.txt", "dir2/dir2_1/file2_1_1.txt"])
    test_sync()
    print_directory('dir1', 0)
    print()
    print_directory('dir2', 0)
    print("\n --- recreate two ---\n")
    make_file("dir1/dir1_1/dir1_1_1/file1_1_1_1.txt", "I'm back.")
    make_file("dir1/file1_1.txt", "I'm back.")
    test_sync()
    print_directory('dir1', 0)
    print()
    print_directory('dir2', 0)

# Run different parts of this test program by un/commenting the bits you do/don't want.
# surround_test("1. This should print an error (or usage) message:", p1)
# surround_test("2. This should show both dir1 and dir2 as directories:", p2)
# surround_test("3. This should show sync file contents:", p3)
# surround_test("4. This should show two different sync files:", p4)
# surround_test("5. This should show two matching directories:", p5)
# surround_test("""6. This should show two matching directories with the file 'a.txt' 75 bytes long and the modification time > 1 second later:""", p6)
surround_test("""7. This should show two pairs of matching directories with the second pair showing different sizes and modification times:""", p7)
# surround_test("""8. This should show the two directories. Then they should only contain c.txt. Then they should have a new version of b.txt:""", p8)
# surround_test("""9. This starts by showing the initial synchronized directories. file1_1.txt must be 81 bytes long:""", p9)