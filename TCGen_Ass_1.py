import random

difficultyy = 3             # 1 easy, 2 middle, 3 hard 
num_cases = 10               # number of testcases

tasks = [True, True, False]  #if you want to get these Tests set True else False
                            #[optimized exp as string, optimized result correct, compiler correct]

def custom_print(lst):
    formatted_list = []
    for tup in lst:
        formatted_tuple = "({}, {})".format(tup[0], tup[1])
        formatted_list.append(formatted_tuple)
    
    print("let testctxt : ctxt = [{}]".format("; ".join(formatted_list)))

def generate_expression(difficulty, max_depth, current_depth=1):
    if current_depth >= (0.7* max_depth) and difficulty == 3:
        difficulty = 2
    if current_depth >= max_depth:
        options = [1, 2]  # Limit to Const and Var for max depth
    else:
        if difficulty == 1:
            options = [ 7, 8, 9, 10]  # Simple optimizations
        elif difficulty == 2:
            options = [ 7, 8, 9, 10]
        else:
            options = [4, 5, 6, 7, 8, 9, 10]

    choice = random.choice(options)

    # Random negation for difficulty 3
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
        return f"Mult(Const 0L, {expr2})", f"(0 * {val2})"
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
            return f"Mult({expr2}, Const 1L)", f"({val2 * 1})"
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
        expr1, val1 = generate_expression(1, 1)
        expr2, val2 = generate_expression(1, 1)
        return f"Mult({expr1}, {expr2})", f"({val1} * {val2})"
    


if difficultyy == 1:
    max_depth = 2
elif difficultyy == 2:
    max_depth = 3
else:
    max_depth = 5

var_names = []
var_val =[]
for i in range (0, 25):
    var_names.append (f"\"{chr(97+i)}\"")
    var_val.append (f"{random.randint (0, 32)}L" )

varlist = zip(var_names, var_val)
custom_print (varlist)

print ("Test (\"Testcases++\", [")
    
  
for i in range (1, num_cases):
    expression, val = generate_expression (difficultyy, max_depth, 1)
    if tasks[0]:
        print (f"    (\"case{i}\", timeout_assert_const (fun () -> Printf.printf \" your optim.: %s  \\n\" (string_of (optimize ({expression})))));")
    if tasks[1]:
        print (f"    (\"case{i}.4.5\", assert_eq (interpret testctxt (optimize ({expression}))) (interpret testctxt ({expression})) );")
    if tasks[2]:
        print (f"    (\"case{i}.5\", assert_eq (interpret testctxt ({expression})) (run testctxt (compile ({expression}))) );")


print ("  ]);")