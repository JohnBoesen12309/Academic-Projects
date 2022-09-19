# Import modules
from Patient import Patient
import random
import polynomial as poly

# initialize global variable
random.seed(5)  # random seed used for reproducibility
LENGTH_DNA = 20


########################
##### Functions ########
########################

def display_menu():
    """ Display all the options, no input, no output """
    print("\n1-List; 2-Info; 3-Remove; 4-Insert; 5-Compare; 6-Compare all; 7-Analyze")


def random_base():
    """select the letter A,C,G,T at random, output (String) """
    bases = ["A", "C", "G", "T"]
    return random.choice(bases)


def random_strand():
    i = random_base()
    for x in range((LENGTH_DNA - 1)):
        i = i + random_base()
    return i


def initialize_patients():
    p1 = Patient("Andrea", 37, random_strand())
    p2 = Patient("Bob ", 28, random_strand())
    p3 = Patient("Brooke", 34, random_strand())
    p4 = Patient("Connor", 27, random_strand())
    p5 = Patient("James ", 25, random_strand())
    p6 = Patient("Jenna ", 44, random_strand())
    p7 = Patient("John  ", 45, random_strand())
    p8 = Patient("Julie ", 37, random_strand())
    p9 = Patient("Kate", 48, random_strand())
    p10 = Patient("Keith", 28, random_strand())
    p11 = Patient("Kelly", 25, random_strand())
    p12 = Patient("Luke", 33, random_strand())
    p13 = Patient("Mark", 34, random_strand())
    p14 = Patient("Pat", 26, random_strand())
    p15 = Patient("Taylor", 30, random_strand())
    p16 = Patient("Tony", 55, random_strand())
    a = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16]
    return a


def display(a, title):
    i = 0
    line = "--------------------------------------------"
    for x in title:
        if x == "Name":
            print("\t" + x, end="\t")
        else:
            print(x, end="\t")
        i = i + 1
        if i > 3:
            line = line + "-" * len(x) + "----"
    print("\n" + line)
    number = 0
    for p in a:
        while len(p.n) <= 3:
            p.n = p.n + " "
        number = number + 1
        if p.hc == None:
            print(number, p.n, p.a, p.d, sep="\t")
        elif len(p.hc) > 1:
            print(number, p.n, p.a, p.d+"    ", sep="\t", end="\t")
            i=3
            for x in p.hc:
                bool_str=str(x)
                ##while len(bool_str)<len(title[i]):
                    ##bool_str=bool_str+" "
                print(bool_str, end="\t")
            print("")
        else:
            print(number, p.n, p.a, p.d+"    ", p.hc[0], sep="\t")


def info(list):
    sum = 0
    a1 = 0
    a2 = 0
    a3 = 0
    a4 = 0
    a5 = 0
    a6 = 0
    b = None
    for p in list:
        if p.a < 20:
            a1 = a1 + 1
        elif 20 <= p.a < 30:
            a2 = a2 + 1
        elif 30 <= p.a < 40:
            a3 = a3 + 1
        elif 40 <= p.a < 50:
            a4 = a4 + 1
        elif 50 <= p.a < 60:
            a5 = a5 + 1
        else:
            a6 = a6 + 1
        sum = sum + p.a
        if p.hc != None:
            b = True
    percent = poly.scale([a1, a2, a3, a4, a5, a6], (100 / len(list)))
    avg = sum / len(list)
    print("#Patients " + str(len(list)))
    print("<20: " + str(percent[0]) + "%", "20's " + str(percent[1]) + "%", "30's " + str(percent[2]) + "%",
          "40's " + str(percent[3]) + "%", "50's " + str(percent[4]) + "%", ">=60 " + str(percent[5]) + "%", sep="\n")
    print("\n" + "Age Mean: " + str(avg))
    return b


def add_new_patient(list):
    new_p = Patient()
    new_p.n = input("Enter Name ")
    new_p.a = input("Enter Age ")
    while new_p.d is None or len(new_p.d) != LENGTH_DNA:
        new_p.d = input("Enter DNA strand ")
        if len(new_p.d) != LENGTH_DNA:
            print("Bad input! -length must be 20")
    list = list + [new_p]
    return list


def compare(obj1, obj2):
    i = 0
    final_str = ""
    a = 0
    while i < LENGTH_DNA:
        if obj1.d[i] == obj2.d[i]:
            final_str = final_str + obj1.d[i]
            a = a + 1
        else:
            final_str = final_str + "x"
        i = i + 1
    return final_str


def check_completness(str):
    a = 0
    for x in range(LENGTH_DNA):
        if str[x] == "x":
            a = a + 1
    return 100 * ((LENGTH_DNA - a) / LENGTH_DNA)


def compare_all(list):
    for p in list:
        for a in list:
            if check_completness(compare(p, a)) > 33 and a != p:
                print("%s vs %s  %s" % (p.n, a.n, check_completness(compare(p, a))) + "%")


def find_pattern(list, DNA):
    a = 0
    for p in list:
        for i in range(LENGTH_DNA):
            if p.d[i:i + len(DNA)] == DNA:
                has_condition = True
                a = a + 1
                break
            else:
                has_condition = False
        p.hc = p.hc + [has_condition]
    return 100 * (a / len(list))


### to complete


##########################
########## Main Function #  to uncomment step by step fo testing
##########################

def main():
    ##################### TEST FOR OPTION 1
    print("\n****TEST the random_strand function****")
    print(random_strand())

    ##################### TEST FOR OPTION 1
    print("\n****TEST the class Patient****")
    patient = Patient("Tom", 20, random_strand())
    print(patient.n, patient.a, patient.d)

    ##################### TEST FOR OPTION 1
    print("\n****TEST the display function****")
    patients = [patient, Patient()]
    patients[1].n = "Lucy"
    patients[1].a = 25
    patients[1].d = "TCTTGTAAACTCGGAAACTG"
    display(patients)

    ##################### TEST FOR OPTION 2
    print("\n****TEST the info function****")
    info(patients)

    ###################### TEST for OPTION 4
    # print("\n****TEST the add_new_patient function****")
    # patients=add_new_patient(patients)
    # display(patients)

    ###################### TEST for OPTION 5
    print("\n****TEST the compare function****")
    common_strand = compare(patients[0], patients[1])
    print(common_strand)

    ###################### TEST for OPTION 5
    print("\n****TEST the check_completness function****")
    print(check_completness(common_strand))


if __name__ == "__main__":
    main()
