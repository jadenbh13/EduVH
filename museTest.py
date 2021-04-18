from muselsl import stream, list_muses

muses = list_muses()
#Discover available muse devices via bluetooth
if not muses:
    #If none found
    print('No Muses found')
    #Print message to user
else:
    try:
        stream(muses[0]['address'])
        #Begin streaming data for first device found
    except KeyboardInterrupt:
        #If user exits
        print('Stream has ended')
        #Print message then terminate
