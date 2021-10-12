
# Implementation FizzBuzz 
def fizz_buzz():
    for n in range(1, 101):
        fizz = n % 3 == 0
        buzz = n % 5 == 0

        if fizz and buzz:
            print('FizzBuzz')
        elif fizz:
            print('Fizz')
        elif buzz:
            print('Buzz')
        else:
            print(n)

if __name__ == '__main__':
    fizz_buzz()