from pydoc import render_doc
from urllib import request
from flask import Flask, render_template, request, flash
import math
import random
from functools import reduce




app = Flask(__name__)
app.secret_key="super secret key"


@app.route("/", methods=['POST', 'GET'])
def main():



    return render_template("index.html")


@app.route('/prime-factorization/',  methods=['POST', 'GET'])
def primeFac():

    success = False

    def get_prime_factors(number):
            # create an empty list and later I will
            # run a for loop with range() function using the append() method to add elements to the list.
            prime_factors = []

            # First get the number of two's that divide number
            # i.e the number of 2's that are in the factors
            while number % 2 == 0:
                prime_factors.append(2)
                number = number / 2

            # After the above while loop, when number has been
            # divided by all the 2's - so the number must be odd at this point
            # Otherwise it would be perfectly divisible by 2 another time
            # so now that its odd I can skip 2 ( i = i + 2) for each increment
            for i in range(3, int(math.sqrt(number)) + 1, 2):
                while number % i == 0:
                    prime_factors.append(int(i))
                    number = number / i


            # Here is the crucial part.
            # First quick refreshment on the two key mathematical conjectures of Prime factorization of any non-Prime number
            # Which is - 1. If n is not a prime number AT-LEAST one Prime factor would be less than sqrt(n)
            # And - 2. If n is not a prime number - There can be AT-MOST 1 prime factor of n greater than sqrt(n).
            # Like 7 is a prime-factor for 14 which is greater than sqrt(14)
            # But if the above loop DOES NOT go beyond square root of the initial n.
            # Then how does that greater than sqrt(n) prime-factor
            # will be captured in my prime factorization function.
            # ANS to that is - in my first for-loop I am dividing n with the prime number if that prime is a factor of n.
            # Meaning, after this first for-loop gets executed completely, the adjusted initial n should become
            # either 1 or greater than 1
            # And if n has NOT become 1 after the previous for-loop, that means that
            # The remaining n is that prime factor which is greater that the square root of initial n.
            # And that's why in the next part of my algorithm, I need to check whether n becomes 1 or not,
            if number > 2:
                prime_factors.append(int(number))

            return prime_factors


    primeFactors = []
    if request.method == 'POST':

        try:
            success = True
            primeNumber = request.form.get('normalNumber')
            if int(primeNumber) <= 0:
                primeFactors = []
            else:
                primeFactors = get_prime_factors(int(primeNumber))
            flash("Successfully computed")

        except Exception as e:
            success = False
            error = e.args
            print('Your error message is: ', error)
            flash(error)

    return render_template("primeFactor.html", primeFactors = primeFactors, success = success)


@app.route('/totient-function/',  methods=['POST', 'GET'])
def totientFunc():

    success = False
    n =0
    # Euler's Totient Function
    # using Euler's product formula

    def phi(n) :

        result = n # Initialize result as n
        
        # Consider all prime factors
        # of n and for every prime
        # factor p, multiply result with (1 - 1 / p)
        p = 2
        while p * p<= n :

            # Check if p is a prime factor.
            if n % p == 0 :

                # If yes, then update n and result
                while n % p == 0 :
                    n = n // p
                result = result * (1.0 - (1.0 / float(p)))
            p = p + 1
		
		
        # If n has a prime factor
        # greater than sqrt(n)
        # (There can be at-most one
        # such prime factor)
        if n > 1 :
            result = result * (1.0 - (1.0 / float(n)))

        return int(result)
        
        
    if request.method == 'POST':

        try:
            success = True
            inputNumber = request.form.get('normalNumber')
            n = phi(int(inputNumber))
            flash("Succefully computed")

        except Exception as e:
            success = False
            error = e.args
            print('Your error message is: ', error)
            flash(error)

        

    # This code is contributed
    # by Nikita Tiwari.


    return render_template("totientFunction.html", phiOfN = n, success = success)



@app.route('/miller-rabin/',  methods=['POST', 'GET'])
def millerRabin():

    outputNumber = "Waiting..."
    success = False

    def is_Prime(n):
        """
        Miller-Rabin primality test.
    
        A return value of False means n is certainly not prime. A return value of
        True means n is very likely a prime.
        """
        if n!=int(n):
            return False
        n=int(n)
        #Miller-Rabin test for prime
        if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
            return False
    
        if n==2 or n==3 or n==5 or n==7:
            return True
        s = 0
        d = n-1
        while d%2==0:
            d>>=1
            s+=1
        assert(2**s * d == n-1)
    
        def trial_composite(a):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2**i * d, n) == n-1:
                    return False
            return True  
    
        for i in range(8):#number of trials 
            a = random.randrange(2, n)
            if trial_composite(a):
                return False
    
        return True 


    if request.method == 'POST':

        try:
            success = True
            inputNumber = request.form.get('testedNumber')
            outputNumber = is_Prime(int(inputNumber))

            if outputNumber == True:
                outputNumber = "Your number is very likely prime"

            elif outputNumber == False:
                outputNumber = "Your number is certainly not prime"
            flash("Successfully computed")

        except Exception as e:
            success = False
            error = e.args
            print('Your error message is: ', error)
            flash(error)


    return render_template("millerRabinAlgorithm.html", probableAnswer = outputNumber, success = success)



@app.route('/fast-exponentiation/',  methods=['POST', 'GET'])
def fastExpo():

    success = False
    outp = 0
    x = 1
    e = 1
    m = 1

    def fExp(x,e,m):
        X = x
        E = e
        Y = 1
        while E > 0:
            if E % 2 == 0:
                X = (X * X) % m
                E = E/2
            else:
                Y = (X * Y) % m
                E = E - 1
        return Y

    if request.method == 'POST':

        try:
            success = True
            x = int(request.form.get('x'))
            e = int(request.form.get('e'))
            m = int(request.form.get('m'))
            outp = fExp(x,e,m)
            flash("Successfully computed")


        except Exception as e:
            success = False
            error = e.args
            print('Your error message is: ', error)
            flash(error)

    return render_template("fastExponentiation.html", res = outp, success = success)

    

@app.route('/ch-rem-theorem/',  methods=['POST', 'GET'])
def chineseRemTheorem():

    rows=''
    m = [1]
    a = [1]
    success = False
    fin1 = []
    fin2 = []

    def mul_inv(a, b):
        b0 = b
        x0, x1 = 0, 1
        if b == 1: return 1
        while a > 1:
            q = a // b
            a, b = b, a%b
            x0, x1 = x1 - q * x0, x0
        if x1 < 0: x1 += b0
        return x1

    def chinese_remainder(m, a):
        sum = 0
        prod = reduce(lambda acc, b: acc*b, m)
        for n_i, a_i in zip(m, a):
            p = prod // int(n_i)
            sum += int(a_i) * mul_inv(p, int(n_i)) * p
        return sum % prod

    if request.method == 'POST':

        try:
            success = True
            m = (request.form.get('m'))
            a = (request.form.get('a'))


            for i in range(0, len(m)):
                fin1.append(int(m[i]))
                fin2.append(int(a[i]))
                rows = chinese_remainder(fin1,fin2)
            flash("Successfully computed")

        except Exception as e:
            success = False
            error = e.args
            print('Your error message is: ', error)
            flash(error)
            rows = ''

 
 
    

    return render_template("chineseRemTh.html", result = rows, success = success)







if __name__ == "__main__":
    app.run()





