#!/usr/bin/env python3


import ipcontrol 

#webbrowser.open_new("chrome-lhokfaekaimncdlobaiegdeckdpmemhm-Default.desktop")
#os.system(open "chrome-lhokfaekaimncdlobaiegdeckdpmemhm-Default.desktop")

def accessible():
    
    print("THE SERVER IS NOW RUNNING.")
    print("PLEASE DO NOT INTERUPT OR EXIT THE PROGRAM FROM SERVER WHILE THE CLIENT SIDE COMPUTER IS IN OPERATION.")

def notaccessible():
    
    print("THE SERVER IS NOW RUNNING.")
    print("THIS PORGRAM IS RUN OPERATION ONLY ON THE SERVER AND NOT ACCESS ABLE TO THE NETWORK.")

try:
    
    if ipcontrol.toconnect == 'y' or ipcontrol.toconnect == 'Y':
        
        try:
            
            import onezerotwofourbysevensixeight#, onethreesixsixbysevensixeight
            
            accessible()
            onezerotwofourbysevensixeight.albiemerapp.run(host = ipcontrol.myipaddress)
            
        except AttributeError:
            
            print("YOUR CONNECTION HAS A PROBLEM")
            print("PLEASE RECONFIGURED THE NETWORK TO MAKE THE PROGRAM WORK PROPERLY")
        
    elif ipcontrol.toconnect == 'n' or ipcontrol.toconnect == 'N':
        
        import onezerotwofourbysevensixeight#, onethreesixsixbysevensixeight
        
        notaccessible()
        onezerotwofourbysevensixeight.albiemerapp.run(host = ipcontrol.myipaddress)
        
    else:
        
        print("Invalid")

   
except:
    
    print("YOUR SERVER IS NOT CONNECTED TO THE NETWORK!")
    