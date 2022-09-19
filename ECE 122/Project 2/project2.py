'''------------------------------------------------------
                 Import Modules 
---------------------------------------------------------'''
import dna_tool as dna
'''------------------------------------------------------
                Main program starts here 
---------------------------------------------------------'''
def main():
    header=["Name","Age","DNA Sequence (20 length)"]
    list=dna.initialize_patients()
    while True:
        dna.display_menu()
        a=input("Command (Enter to exit):")
        if a == "" or a == " ":
            print("Thanks for using this tool ","Come back soon!",sep="\n")
            break
        if a == "1":
            dna.display(list,header)
        if a == "2":
            condition=dna.info(list)
            if condition== True:
                for i in range(3,len(header)):
                    print("%s: %s"%(condition_name,percent)+"%")
        if a == "3":
            num=int(input("Who do you want to remove (enter number): "))
            if not 1<= num <=len(list):
                continue
            del (list[num - 1])

        if a == "4":
            list=dna.add_new_patient(list)
        if a == "5":
            str1=int(input("First patient (enter number): "))-1
            str2=int(input("Second patient (enter number): "))-1
            print("Patients %s and %s common strand is "%(str1,str2)+dna.compare(list[str1],list[str2]))
            print("They are similar at "+str(dna.check_completness(dna.compare(list[str1],list[str2])))+"%")
        if a == "6":
            dna.compare_all(list)
        if a == "7":
            condition_name=input("What condition are you looking for: ")
            condition_strand=input("Enter sequence: ")
            header=header+[condition_name]
            percent=dna.find_pattern(list,condition_strand)
            print("Patients with %s condition: %s"%(condition_name,percent)+"%")
        else:
            continue
if __name__== "__main__":
    main()