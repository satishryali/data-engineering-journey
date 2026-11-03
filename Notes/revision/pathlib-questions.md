# pathlib practice

Try without the explanation note first. Say whether you used notes or hints, and share actual code/output.

1. Choose an existing notebook. Print its full address, containing folder, name, stem, suffix, and whether it is a file or folder. Explain where a relative path starts.
2. Build the address of an `analysis` folder beside that notebook. Predict whether building the address creates anything, then check.
3. In a disposable practice folder, create two nested folders. Run the creation again. Explain the effect of `parents` and `exist_ok`, and what changes if the target is an existing file.
4. Save `Hello` in a text file, print the return value from writing, and read it back. Explain the return value and whether a filename without an extension can be a file.
5. Find CSV files directly inside a folder and then in its subfolders. Explain how the searches differ.

Next bounded task: do question 1 and show the output. These are pending prompts, not completed reviews.

Follow-up recall from the path discussion:

6. Does creating a `Path` open a file? How is `pathlib` different from `Path`?
7. Why does a Windows path containing backslashes sometimes need a raw string? Write the same path using forward slashes.
8. Can you define and print a relative path without supplying an absolute path? Does `resolve()` search the computer for the file?
9. Compare `reports/daily` and `reports/daily/daily`. When can a file named `daily` coexist with a folder named `daily`, and when does `mkdir(exist_ok=True)` fail?
