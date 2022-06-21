

# params to control pass generation

tn = 0.08            # propability of a very hard password


# probabilities p1, p2, p3 add up to 1 (heuristically chosen)
p1 = 0.10            # random char propability
p2 = 0.40            # chance of a markov-order-1 char at this position (see code)
p3 = 0.50            # skip this position and dont change the char propability

q = 0.03             # bonus 3% noise words to list of passwords

#  parameters for a password creation
nL = 8               # password must have at least letters
nD = 1               # password must have at least digit
nS = 0               # password must have at least special (non-letter non-digit)

# END OF params to control pass generation


import random
import sys
import string
import os

#create an empty dict and fill it with passwords from the file that provide .
high_probability_passwords = """

"""
#filenames = []
#dicton = open(os.path.dirname(os.path.realpath(__file__)) + '\cpass.txt', "r")
#lines = dicton.readlines()
#for line in lines:
#    print(line)
#    filenames.extend( line.split() )
#print(len(filenames))
def read_password_files(filenames):
    """
    Return a list of passwords in all the password file(s), plus
    a proportional (according to parameter q) number of "noise" passwords.
    """
    diction = open(os.path.dirname(os.path.realpath(__file__)) + '\cpass.txt', "r")
    filenames = diction.readlines()
#    lines = dicton.readlines()
#    for line in lines:
#        filenames.extend( line.split() )
#    print(len(filenames))
    pw_list = [ ]
    if len(filenames)>0:
        lines = filenames
        for line in lines:
            pw_list.extend( line.split() )
    else:
        lines = high_probability_passwords.split()
        for line in lines:
            pw_list.extend( line.split() )
    # add noise passwords
    print(pw_list)
    pw_list.extend( noise_list(int(q*len(pw_list))) )
    print("read_password_files")
    print(pw_list)
    return pw_list

def noise_list(n):
    """
    Return a list of n ``noise'' passwords, to get better coverage of lengths and character
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    nchars = len(chars)
    L = [ ]
    for i in range(n):
        w = [ ]
        k = random.randrange(1,18)
        for j in range(k):
            w.append(chars[random.randrange(nchars)])
        w = ''.join(w)
        L.append(w)
    print("noise_list")
    print(L)
    return L

def tough_nut():
    """
    Return a ``tough nut'' password
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    nchars = len(chars)
    w = [ ]
    k = 40
    for j in range(k):
        w.append(chars[random.randrange(nchars)])
    w = ''.join(w)
    print("this is tough_nut")
    print(w)
    return w

def syntax(p):
    """
    Return True if password p contains at least nL letters, nD digits, and nS specials (others)
    """
    global nL, nD, nS
    L = 0
    D = 0
    S = 0
    for c in p:
        if c in string.ascii_letters:
            L += 1
        elif c in string.digits:
            D += 1
        else:
            S += 1
    if L >= nL and D >= nD and S >= nS:
        return False
    else:
        return True

def make_password(pw_list):
    """
    make a random password like those in given password list
    """
    if random.random() < tn:
        return tough_nut()
    # start by choosing a random password from the list
    # save its length as k; we'll generate a new password of length k
    k = len(random.choice(pw_list))
    # create list of all passwords of length k; we'll only use those in model
    L = [ pw for pw in pw_list if len(pw) == k ]
    print("SSSSSSSSSSSSSSSSSSSSSSSSSS")
    print(L)
    nL = len(L)
    # start answer with the first char of that random password
    # row = index of random password being used
    row = random.randrange(nL)
    ans = L[row][:1]                  # copy first char of L[row]
    j = 1                             # j = len(ans) invariant
    while j < k:                      # build up ans char by char
        p = random.random()           # randomly decide what to do next, based on p
        # here p1 = prob of action 1
        #      p2 = prob of action 2
        #      p3 = prob of action 3
        #      p1 + p2 + p3 = 1.00
        if p<p1:
            action = "action_1"
        elif p<p1+p2:
            action = "action_2"
        else:
            action = "action_3"
        if action == "action_1":
            # add same char that some random word of length k has in this position
            row = random.randrange(nL)
            ans = ans + L[row][j]
            j = j + 1
        elif action == "action_2":
            # take char in this position of random word with same previous char
            LL = [ i for i in range(nL) if L[i][j-1]==ans[-1] ]
            row = random.choice(LL)
            ans = ans + L[row][j]
            j = j + 1
        elif action == "action_3":
            # stick with same row, and copy another character
            ans = ans + L[row][j]
            j = j + 1
    if (nL > 0 or nD > 0 or nS > 0) and not syntax(ans):
        return make_password(pw_list)
    print("this is make_passwords")
    print(ans)
    return ans

def generate_passwords( n, pw_list ):
    """ print n passwords and return list of them """
    ans = [ ]
    for t in range( n ):
        pw = make_password(pw_list)
        while pw in ans:
            pw = make_password(pw_list)
        ans.append( pw )
    print("this is generate_passwords")
    print(ans)
    return ans

def gen(password, n, filenames):
    pw_list = read_password_files(filenames)
    new_passwords = generate_passwords(n,pw_list)
    random.shuffle(new_passwords)
    print("this is gen")
    print(new_passwords)
    return new_passwords
