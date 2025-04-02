# ParsLang 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Add a license if you choose one -->

ParsLang is a simple, interpreted scripting language designed with educational purposes in mind. It features a straightforward syntax, basic data types, control flow structures, functions, and notably, **multilingual keyword support**, allowing keywords to be written in both English and Persian (Farsi).

The interpreter is built from the ground up using Python, demonstrating the core components of a language processor: Lexer, Parser, and Interpreter.

## ✨ Quick Start: Examples

Let's look at a classic example: calculating Fibonacci numbers.

**1. Using English Keywords (`fibo.txt`)**

```python
# Calculate the first few Fibonacci numbers
var a = 0
var b = 1

print(a)
print(b)

# Loop to generate the next numbers
for n = 1 to 10 then
    var temp = a + b
    a = b
    b = temp
    print(b)
end

print("Done!")
```

**2. Using Persian Keywords (`fibo-fa.txt` - equivalent logic)**

```python
# محاسبه چند عدد اول فیبوناچی
موگوم a = 0  # 'موگوم' is equivalent to 'var'
موگوم b = 1

bechup(a)  # 'bechup' is a custom alias for 'print'
bechup(b)

# حلقه برای تولید اعداد بعدی
واسه n = 1 تا 10 اووخ  # 'واسه' = for, 'تا' = to, 'اووخ' = then
    موگوم temp = a + b
    a = b
    b = temp
    bechup(b)
تمام  # 'تمام' = end

bechup("تمام شد!")
```

**Running the examples:**

You can run these scripts using the `parslang.py` interpreter or the pre-built executable:

```bash
# Using Python interpreter
python parslang.py fibo.txt
python parslang.py fibo-fa.txt

# Or using the executable (Windows example, adapt for Linux/macOS)
./parslang.exe fibo.txt
./parslang.exe fibo-fa.txt
```

## 🌟 Features

*   **Simple Syntax:** Designed to be easy to read and write.
*   **Variables:** Dynamically typed variables using `var` (or `let`, `موگوم`, `قرارده`).
*   **Data Types:** Supports Numbers (Integers and Floats), Strings, and Lists.
*   **Arithmetic Operations:** `+`, `-`, `*`, `/`, `%` (remainder), `^` (power).
*   **Comparison Operators:** `==`, `!=`, `<`, `>`, `<=`, `>=`.
*   **Logical Operators:** `and`, `or`, `not` (and Persian equivalents like `و`, `یا`, `نه`).
*   **Conditional Statements:** `if`/`elif`/`else` blocks (using `then` and `end`, or single-line expressions). Persian equivalents like `اگر`/`مگر`/`وگرنه` are supported.
*   **Loops:**
    *   `for` loops (`for i = start to end step value then ... end`). Persian: `برای`/`واسه`.
    *   `while` loops (`while condition then ... end`). Persian: `هنگامیکه`.
*   **Functions:** Define functions using `fun` (or `def`). Supports named and anonymous functions, argument passing, and return values (`return` or implicit return for arrow functions). Persian: `تابع`.
*   **Lists:** Create lists using `[...]`. Basic list manipulation is available via built-in functions.
*   **🌍 Multilingual Keywords:** Core language keywords have both English and Persian equivalents (see `components/CONSTANTS.py` for the full map).
*   **Identifier Support:** Variable and function names can include Persian letters.
*   **Built-in Functions:** Provides essential functions like `print`, `input`, type checking, list operations, etc.
*   **Error Handling:** Clear error messages with tracebacks and code highlighting pointing to the error location.
*   **Comments:** Single-line comments using `#`.

## 💡 Language Constructs Explained

### Variables

Declare variables using `var` (or aliases like `let`, `موگوم`). Assignment uses `=`. If no value is assigned, it defaults to `0`.

```python
var message = "Hello, ParsLang!"
var count = 10
var pi = 3.14
var x # Defaults to 0
```

### Conditional Statements (`if`/`elif`/`else`)

Supports multi-line blocks with `then` and `end`, or single-line expressions.

```python
var grade = 75

# Multi-line
if grade >= 90 then
    print("A")
elif grade >= 80 then
    print("B")
else
    print("C or lower")
end

# Single-line (result is the value of the expression)
var result = if grade > 50 then "Pass" else "Fail"
print(result)

# Using Persian keywords
اگر grade >= 90 اووخ
    bechup("عالی")
مگر grade >= 80 اووخ
    bechup("خوب")
وگرنه
    bechup("نیاز به تلاش بیشتر")
تمام
```

### Loops

**For Loop:** Iterates over a range of numbers.

```python
# Multi-line
for i = 1 to 5 then
    print(i)
end

# With step
for j = 10 to 0 step -2 then
    print(j)
end

# Single-line (creates a list of results)
var squares = for x = 1 to 4 then x * x
print(squares) # Output: [1, 4, 9, 16]

# Using Persian keywords
واسه i = 1 تا 3 اووخ
    bechup(i)
تمام
```

**While Loop:** Executes as long as a condition is true.

```python
var counter = 0
# Multi-line
while counter < 3 then
    print(counter)
    counter = counter + 1
end

# Single-line (creates a list of results)
var vals = while counter < 5 then counter = counter + 1 # Note: depends on expression evaluated
# (Use with caution for single-line results, multi-line is clearer for state changes)

# Using Persian keywords
هنگامیکه counter < 6 اووخ
    bechup(counter)
    counter = counter + 1
تمام
```

### Functions (`fun`/`def`)

Define reusable blocks of code.

```python
# Multi-line function
fun greet(name)
    print("Hello, " + name)
end

greet("World")

# Function with return
fun add(x, y)
    return x + y
end

var sum = add(5, 3)
print(sum) # Output: 8

# Arrow function (single expression, implicit return)
fun multiply(a, b) -> a * b
print(multiply(4, 5)) # Output: 20

# Anonymous function assigned to a variable
var power = fun (base, exp) -> base ^ exp
print(power(2, 3)) # Output: 8

# Using Persian keywords
تابع سلام(اسم)
    bechup("سلام، " + اسم)
تمام

سلام("دنیا")
```

### Lists

Ordered collections of items.

```python
var my_list = [1, "two", 3.0, true]
print(my_list)

# List operations via built-ins
append(my_list, "new") # Add item
print(my_list)

var item = pop(my_list, 1) # Remove and return item at index 1
print(item)      # Output: "two"
print(my_list)

var another_list = [4, 5]
extend(my_list, another_list) # Append elements from another list
print(my_list)

print(len(my_list)) # Get length
```

## 🔧 Built-in Functions

ParsLang provides several built-in functions (available globally):

*   `print(value)`: Prints the string representation of a value to the console.
*   `print_ret(value)`: Returns the string representation of a value (doesn't print).
*   `input()`: Reads a line of text input from the user, returns it as a String.
*   `input_int()`: Reads input, ensuring it's an Integer, and returns it as a Number. Reprompts if input is invalid.
*   `clear()`: Clears the console screen.
*   `is_number(value)`: Returns `true` if the value is a Number, `false` otherwise.
*   `is_string(value)`: Returns `true` if the value is a String, `false` otherwise.
*   `is_list(value)`: Returns `true` if the value is a List, `false` otherwise.
*   `is_function(value)`: Returns `true` if the value is a Function, `false` otherwise.
*   `append(list, value)`: Adds `value` to the end of `list`.
*   `pop(list, index)`: Removes and returns the element at `index` from `list`.
*   `extend(list1, list2)`: Appends all elements from `list2` to the end of `list1`.
*   `len(list)`: Returns the number of elements in `list` as a Number.
*   `run(filename)`: Executes the ParsLang script contained in the file specified by the `filename` string.

*(Note: Persian equivalents for these function names are planned but not yet implemented - see To-Do).*

## 💪 Resilience and Error Handling

ParsLang aims to provide helpful error messages:

*   **Lexical Errors:** Catches invalid characters (`IllegalCharError`).
*   **Syntax Errors:** Detects incorrect grammar or structure (`InvalidSyntaxError`, `ExpectedCharError`).
*   **Runtime Errors:** Handles errors during execution, like division by zero, undefined variables, type mismatches, or incorrect function arguments (`RuntimeError`).

Errors include:
*   The type of error.
*   A specific error message.
*   The filename and line number where the error occurred.
*   A traceback showing the function call stack.
*   The line(s) of code causing the error, with `^` characters pointing to the problematic segment.

## ⚙️ How to Use

**1. Interactive Shell**

Run the interactive shell to experiment with ParsLang commands directly:

```bash
python shell.py
```

You'll get a `Persian basic >` prompt. Type ParsLang code and press Enter. Type `exit` or `Ctrl+C` to quit.

**2. Running `.pars` Files**

Save your ParsLang code in a file with a `.pars` extension (e.g., `my_script.pars`). Then run it using `parslang.py`:

```bash
python parslang.py my_script.pars
```

**3. Using the Executables (No Python Installation Needed!)**

Pre-built executables (`shell.exe`, `parslang.exe` on Windows; `shell`, `parslang` on Linux/macOS) are provided in the repository (or you can build them yourself using PyInstaller). These allow you to run the shell or scripts without having Python installed on the system.

```bash
# Windows Example
./shell.exe
./parslang.exe my_script.pars

# Linux/macOS Example (ensure execute permission: chmod +x shell parslang)
./shell
./parslang my_script.pars
```

## 🏗️ Project Structure (Components Explained)

The interpreter is broken down into several key components:

*   `shell.py`: The interactive Read-Eval-Print Loop (REPL).
*   `parslang.py`: The script runner for `.pars` files.
*   `grammar.txt`: Defines the language's grammar rules (useful for understanding structure, though not directly used by this specific parser implementation which is recursive descent).
*   **`components/`**: Core interpreter modules.
    *   `CONSTANTS.py`: Defines keywords (English/Persian), character sets, etc.
    *   `POSITION.py`: Tracks file, line, and column numbers for error reporting.
    *   `TOKENS.py`: Defines token types (like `TT_INT`, `TT_PLUS`, `TT_IDENTIFIER`, `TT_KEYWORD`).
    *   `ERRORS.py`: Defines custom error classes (`IllegalCharError`, `InvalidSyntaxError`, `RuntimeError`).
    *   `LEXER.py`: Scans the source text and converts it into a stream of tokens (Tokenization).
    *   `NODES.py`: Defines the Abstract Syntax Tree (AST) node types (e.g., `NumberNode`, `BinOpNode`, `ifNode`).
    *   `PARSE_RESULT.py`: Helper class for the parser to manage results and errors.
    *   `PARSER.py`: Takes the token stream from the Lexer and builds an AST based on the language grammar.
    *   `RUNTIME_RESULT.py`: Helper class for the interpreter to manage results, errors, and control flow signals (return, break, continue).
    *   `CONTEXT.py`: Manages the execution context, including the symbol table and parent context (for scope).
    *   `SYMBOL_TABLE.py`: Stores variable and function names and their corresponding values within a scope.
    *   `INTERPRETER.py`: Traverses the AST generated by the Parser and executes the code (Evaluation).
    *   `VALUES/`: Defines the runtime value types.
        *   `VALUE.py`: Base class for all runtime values.
        *   `NUMBER.py`: Represents numeric values.
        *   `STRING.py`: Represents string values.
        *   `LIST.py`: Represents list values.
        *   `BASE_FUNCTION.py`: Base class for functions.
        *   (Implementation Note: `Function` is defined within `INTERPRETER.py`, `BuiltinFunction` within `BUILTIN_FUNCTIONS.py`).
    *   `BUILTIN_FUNCTIONS.py`: Defines and implements the built-in functions, and includes the main `run` function orchestrating the Lexer, Parser, and Interpreter.
*   **`utils/`**: Utility functions.
    *   `strings_with_arrows.py`: Generates the code snippet with arrows for error reporting.
    *   `mapPersian2EnglishAlphabet.py`: Maps Persian letters to their English phonetic equivalents (used internally for potential keyword matching logic, though the primary mapping is in `CONSTANTS.py`).
    *   `makeToken.py`: Helper function example for token creation (actual logic is in `LEXER.py`).
    *   `persianDigit2English.py`: Converts Persian digits (۰-۹) to English digits (0-9) during lexing.

## 📝 To-Do List

*   [ ] **Better Error Messages:** Provide more context-specific suggestions for syntax errors.
*   [ ] **Translate Built-in Functions:** Allow calling built-in functions using Persian names (e.g., `چاپ` for `print`).
*   [ ] **More Data Types:** Consider adding explicit Booleans (`true`/`false` currently map to Numbers 1/0) or Dictionaries/Maps.
*   [ ] **Standard List Indexing:** Implement `my_list[index]` syntax for accessing and potentially assigning list elements.
*   [ ] **More Built-in Functions:** Add functions for math operations, string manipulation, file I/O, etc.
*   [ ] **Unit Tests:** Develop a comprehensive test suite to ensure correctness and prevent regressions.
*   [ ] **Documentation:** Auto-generate documentation from code comments or write more detailed language specs.
*   [ ] **Modules/Imports:** Add a system for importing code from other ParsLang files.

## 🙏 Contributing

Contributions are welcome! If you'd like to help improve ParsLang:

1.  **Fork** the repository.
2.  Create a new **branch** for your feature or bug fix (`git checkout -b feature/your-feature-name`).
3.  Make your **changes**.
4.  **Commit** your changes (`git commit -am 'Add some feature'`).
5.  **Push** to the branch (`git push origin feature/your-feature-name`).
6.  Create a new **Pull Request**.

Please explain your changes clearly in the pull request description.

## 📧 Contact

Ahmad Reza Anaami - ahmadrezaanaami@gmail.com

Feel free to reach out with questions, suggestions, or feedback!

## 📜 License

[Specify Your License Here - e.g., MIT License]

