import os

total_jpeg = 137

def main():
    for _ in range(total_jpeg):
        os.rename("angiosperm_monocots conv " + str(_+1) + ".jpeg", "angiosperm_monocots_" + str(_+1) + ".jpeg")
    
    
main()