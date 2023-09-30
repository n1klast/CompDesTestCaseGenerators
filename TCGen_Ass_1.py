import random
from pathlib import Path

#--------------------------------------------------------------------------------------------------------------------------------#
# Program Arguments #
difficultyy   = 1                  # 1 easy, 2 middle, 3 hard 
num_cases     = 5                  # Number of testcases
maximum_depth = [2, 3, 5]          # Maximum depth of exp for each difficulty, default: [2, 3, 5]
write_to_file = True               # Only want command line output? set False
tasks         = [True, True, True] # If you want to get these Tests set True else False
                                   # [optimized exp as string, optimized result correct, compiler correct]
#--------------------------------------------------------------------------------------------------------------------------------#


def custom_print(lst):
    formatted_list = []
    for tup in lst:
        formatted_tuple = "({}, {})".format(tup[0], tup[1])
        formatted_list.append(formatted_tuple)
    if write_to_file:
        f.write("let testctxt : ctxt = [{}]".format("; ".join(formatted_list)))
        f.write("\n\n")

    print("let testctxt : ctxt = [{}]".format("; ".join(formatted_list)))

def generate_expression(difficulty, max_depth, current_depth=1):
    if current_depth < 0:
        options = [1, 1]
        weight = (1, 1)
    elif current_depth >= max_depth:
        options = [1, 2]  # Limit to Const and Var for max depth
        weight = (1, 1)
    else:
        if difficulty == 1:
            options = [ 4, 7, 8, 9, 10]         # Simple optimizations
            weight  = ( 3, 3, 3, 3, 2)  
        elif difficulty == 2:
            options = [ 4, 5, 7, 8, 9, 10]
            weight  = ( 4,10, 4, 3, 3, 7)  
        else:
            options = [ 4, 5, 6, 7, 8, 9, 10]
            weight  = ( 5, 20, 19, 7, 7, 5, 5)

    choice = random.choices(options, weights = weight, k = 1)
    choice = choice [0]

    # Random negation
    negation_start = ""
    negation_end = ""
    if difficulty >= 2 and choice in [1, 2, 5, 6] or difficulty == 1 and choice == 1:
        if random.choice([0, 1]) == 1:
            negation_start = "Neg("
            negation_end = ")"

    if choice == 1:  # Const
        val = random.randint(1, 10)
        return f"{negation_start}Const {val}L{negation_end}", f"{val}"
    elif choice == 2:  # Var
        var_name = chr(97 + random.randint(0, 25))
        return f"{negation_start}Var \"{var_name}\"{negation_end}", var_name
    elif choice == 4:  # Mult with Const 0L
        expr2, val2 = generate_expression(difficulty, max_depth, current_depth + 1)
        if random.choice([0, 1]) == 1:
            return f"Mult(Const 0L, {expr2})", f"(0 * {val2})"
        else :
            return f"Mult({expr2}, Const 0L)", f"({val2} * 0)"
    elif choice == 5:  # Add
        expr1, val1 = generate_expression(difficulty, max_depth, current_depth + 1)
        expr2, val2 = generate_expression(difficulty, max_depth, current_depth + 1)
        return f"{negation_start}Add({expr1}, {expr2}){negation_end}", f"({val1} + {val2})"
    elif choice == 6:  # Mult
        expr1, val1 = generate_expression(difficulty, max_depth, current_depth + 1)
        expr2, val2 = generate_expression(difficulty, max_depth, current_depth + 1)
        return f"{negation_start}Mult({expr1}, {expr2}){negation_end}", f"({val1} * {val2})"
    elif choice == 7:  # Mult with Const 1L
        expr2, val2 = generate_expression(difficulty, max_depth, current_depth + 1)
        if random.choice([0, 1]) == 1:
            return f"Mult(Const 1L, {expr2})", f"(1 * {val2})"
        else :
            return f"Mult({expr2}, Const 1L)", f"({val2} * 1)"
    elif choice == 8:  # Add with Const 0L
        expr2, val2 = generate_expression(difficulty, max_depth, current_depth + 1)
        if random.choice([0, 1]) == 1:
            return f"Add(Const 0L, {expr2})", f"(0 + {val2})"
        else :
            return f"Add({expr2}, Const 0L)", f"({val2} + 0)"
        
    elif choice == 9:  # Nested adds
        expr1, val1 = generate_expression(1, max_depth, current_depth + 1)
        expr2, val2 = generate_expression(1, max_depth, current_depth + 1)
        return f"Add({expr1}, {expr2})", f"({val1} + {val2})"
    elif choice == 10:  # Multiplying constants
        expr1, val1 = generate_expression(1, 1, -1)
        expr2, val2 = generate_expression(1, 1, -1)
        return f"Mult({expr1}, {expr2})", f"({val1} * {val2})"
    #return "Const 0L", "0"
    


if difficultyy == 1:
    max_depth = maximum_depth[0]
elif difficultyy == 2:
    max_depth = maximum_depth[1]
else:
    max_depth = maximum_depth[2]

var_names = []
var_val =[]
for i in range (0, 26):
    var_names.append (f"\"{chr(97+i)}\"")
    var_val.append (f"{random.randint (0, 32)}L" )

varlist = zip(var_names, var_val)
if write_to_file:
    print('Output File Name:     ', os.path.dirname(__file__) + '\\testcases_out.txt')
    f= open(os.path.dirname(__file__) + '\\testcases_out.txt', 'w',  encoding = 'utf-8')
custom_print (varlist)

#Test Case printing
if write_to_file:
    f.write('Test (\"Testcases++\", [\\n \n')
print ("Test (\"Testcases++\", [")

for i in range (1, num_cases):
    expression, val = generate_expression (difficultyy, max_depth, 1)
    if tasks[0]:
        print (f"    (\"case{i}\", timeout_assert_const (fun () -> Printf.printf \" your optim.: %s  \\n\" (string_of (optimize ({expression})))));")
    if tasks[1]:
        print (f"    (\"case{i}.4.5\", assert_eq (interpret testctxt (optimize ({expression}))) (interpret testctxt ({expression})) );")
    if tasks[2]:
        print (f"    (\"case{i}.5\", assert_eq (interpret testctxt ({expression})) (run testctxt (compile ({expression}))) );")
    
    if write_to_file:
        if tasks[0]:
            f.write (f"    (\"case{i}\", timeout_assert_const (fun () -> Printf.printf \" your optim.: %s  \\n\" (string_of (optimize ({expression})))));\n")
        if tasks[1]:
            f.write (f"    (\"case{i}.4.5\", assert_eq (interpret testctxt (optimize ({expression}))) (interpret testctxt ({expression})) );\n")
        if tasks[2]:
            f.write (f"    (\"case{i}.5\", assert_eq (interpret testctxt ({expression})) (run testctxt (compile ({expression}))) );\n")
    


if write_to_file:
    f.write ("  ]);")
    f.close()
print ("  ]);")