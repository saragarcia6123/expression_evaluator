from lib.calculator import Calculator

def main():

    print('WELCOME')

    calculator = Calculator()

    with open('test_cases.txt') as f:
        test_cases_raw = f.read()
    
    test_cases = test_cases_raw.split('\n')

    uin = '-1'

    while uin != '0':
        
        print('-'*20)
        print('0 - EXIT')
        print('1 - CALCULATOR')
        print('2 - HISTORY')
        print('3 - RUN TEST CASES')
        print('-'*20)
        uin = input('\nSELECT AN OPTION: ')

        if uin == '0':
            return

        if uin == '1':

            uin = input('\nENTER OPERATION: ').strip()

            result, sympy_result = calculator.calculate(uin)

            print("Result: ", result)
            print("Sympy Result: ", sympy_result)

        elif uin == '2':
            calculator.display_history()
        
        elif uin == '3':
            test_calculator = Calculator()
            for case in test_cases:
                test_calculator.calculate(case)
            test_calculator.display_history()
        else:
            print("INVALID OPERATION.")
        
        print("\nPRESS ENTER TO CONTINUE...")
        input()

if __name__ == "__main__":
    main()