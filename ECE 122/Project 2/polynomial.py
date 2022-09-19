def display_menu():
    """ Display the list of polynomial available tools"""
    print("1-Insert; 2-Remove; 3-Info; 4-Evaluate; 5-Scaling; 6-Derive; 7-Integrate")
    print("8-Summation; 9-Subtract; 10-Multiply; 11-Divide")


def get_polynomial_easy(all_coef):
    """ Easy way out to use if you cannot implement get_polynomial as requested """
    return list(map(float,all_coef.split()))


def display_list(list_poly):
    """Displays the polynomial expression from the get_expression function"""
    i=0
    while i <= len(list_poly)-1:
        print("%s: %s"%(i+1,get_expression(list_poly[i])))
        i=i+1


def get_polynomial(list_str):
    """Turns string of coefficients into a list of coefficients"""
    i=0
    list=""
    final=[]
    if list_str[len(list_str)-1] !=" ":
        list_str=list_str+" "
    while i<= (len(list_str)-1):
        if list_str[i] == " " or i == len(list_str)-1:
            final=final+[float(list)]
            list=""
            i=i+1
        else:
            list=list + list_str[i]
            i=i+1
    return final


def degree(list3):
    """Outputs the degree of the polynomial given a list of coefficients"""
    i=0
    a=0
    while i <= len(list3)-1:
        if list3[i] == 0:
            i=i+1
            continue
        else:
            i=i+1
            a=a+1
    if a == len(list3) and len(list3) > 0:
        a=len(list3)-1
    return a


def get_expression(list1):
    """Turns list of float coefficients into a string polynomial expression """
    i=0
    final=""
    while i<= len(list1)-1:
        if list1[i] == 0: ## Skips 0 coefficients
            i=i+1
            continue
        if list1[i] >= 0:
            a = "+"
        if list1[i] < 0 or i == 0:
            a=""
        b=(len(list1)-(i+1)) ## determines the degree of the coefficient
        if b == 0:
            string=str(list1[i])
            final=final+a+string
            i=i+1
            continue
        if b == 1:
            final=final+a+"%sx"%(str(list1[i]))
            i=i+1
            continue
        string="%sx^%s"%(list1[i],b) ##converts coefficient into ax^b form
        final=final+a+string
        i=i+1
    if final == "":
        final = "0.0"
    return final


def evaluate(poly,float1):
    """Function that evaluates a polynomial at 11 hardcoded """
    i=0
    a=0
    while i <= len(poly)-1:
        a=a+poly[i]*(float1**(len(poly)-i-1))
        i=i+1
    return a


def scale(poly,float2):
    """Function that scales the coefficients of a polynomial by a scaling factor """
    i=0
    poly2 = []
    while i<= len(poly)-1:
        poly2=poly2+[poly[i]*float2]
        i=i+1
    return poly2


def derive(poly):
    """Function that finds the derivation of a polynomial"""
    i=0
    final=[]
    while i<= len(poly)-1:
        a=poly[i]*(len(poly)-i-1)
        if a == 0 or a == -0:
            i=i+1
            continue
        final=final+[a]
        i=i+1
    if len(final) == 0:
        final=[0.0]
    return final


def integrate(poly,lower,upper):
    """Function that finds the integral of a polynomial"""
    i=0
    poly2=0
    while i <= len(poly)-1:
        a=poly[i]/(len(poly)-i)
        b=(a*upper**(len(poly)-i))
        c=(a*lower**(len(poly)-i))
        poly2=poly2+(b-c)
        i=i+1
    return poly2


def add(poly1,poly2):
    """Function that adds together 2 polynomials"""
    i=-1
    final=[]
    while i >= -(len(poly1)) or i >= -(len(poly2)):
        if i<=-(len(poly1)+1):
            final=[poly2[i]]+final
            i=i-1
        elif i<=-(len(poly2)+1):
            final=[poly1[i]]+final
            i=i-1
        else:
            final=[poly1[i]+poly2[i]]+final
            i=i-1
    return final


def subtract (poly1,poly2):
    """Function that subtracts 2 polynomials"""
    p3=[]
    for i in range(len(poly2)): ## converts all coefficients from poly2 to the inverse sign
        p3=p3+[poly2[i]*-1]
    return add(poly1,p3)


def multiply (poly1,poly2):
    """Function that multiplies 2 polynomials using scale function"""
    new_poly2=[]
    i=0
    while i < len(poly1) and i < len(poly2): ## Utilizes scale function to multiply coefficients
        new_poly=scale(poly1,poly2[i])+([0.0]*(len(poly2)-(i+1)))
        new_poly2=add(new_poly,new_poly2) ## Scaled coefficients are then added to the new_poly2 list
        i=i+1
    return new_poly2
