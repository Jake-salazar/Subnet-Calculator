
#SALAZAR, JACOB ISRAEL NSCOM02 MACHINE PROJECT MILESTONE 2
import re #Use regular expression  for input validation

def getBroadcastIP(network_ip, mask):

    #get the number of 0 in the mask
    hostBits =  to32Bit(mask).count('0')

    #subtract the number of zeroes found to the network IP
    broadcast_ip_32bit = to32Bit(network_ip)[:-hostBits]



    #make the host bits all ones to make the broadcast IP
    broadcast_ip_32bit = broadcast_ip_32bit + f"{'1' * hostBits}"

    #return the broadcast 32 bits to IP addresss
    return toIP(broadcast_ip_32bit)



def getNetworkIP(network_ip, mask):

    one = "1"
    broadcast_ip_32bit = to32Bit(getBroadcastIP(network_ip, mask))

    broadcastIP = bin(int(broadcast_ip_32bit, 2) + int(one,2))

    network_ip =  broadcastIP.replace("0b","").rjust(32, "0")


    return toIP(str(network_ip))




def to32Bit(IP):
    bit_32 = ""

    IP = IP.split(".")
    for i in range (len(IP)):
        octet = bin(int(IP[i]))
        octet_string = str(octet.replace("0b", "").rjust(8, "0"))
        bit_32 = bit_32 + octet_string

    return bit_32


def getMask(prefix):

    hostBit = 32 - int(prefix)

    subnet_mask = ""
    mask = f"{'0'*hostBit}"
    x = mask.rjust(32,'1')
    x = x[:8] + "." + x[8:]
    x = x[:17] + "." + x[17:]
    x = x[:26] + "." + x[26:]
    x = x.split(".")

    for i in range(len(x)):
        subnet_mask = subnet_mask + f"{int(x[i], 2)}."
    return subnet_mask[:-1]


def toIP(x):
    IP = ""

    x = x[:8] + "." + x[8:]
    x = x[:17] + "." + x[17:]
    x = x[:26] + "." + x[26:]
    x = x.split(".")

    for i in range(len(x)):
        IP = IP + f"{int(x[i], 2)}."
    return IP[:-1]




def getFirstUsableIP(Network_Address):
    one = "1"

    Usable_IP = to32Bit(Network_Address)

    First_Usable = bin(int(Usable_IP, 2) + int(one, 2))

    Usable_IP = First_Usable.replace("0b", "").rjust(32, "0")

    return toIP(str(Usable_IP))

def getLastUsableIP(broadcast):
    one = "1"

    Usable_IP = to32Bit(broadcast)

    Last_Usable = bin(int(Usable_IP, 2) - int(one, 2))

    Usable_IP = Last_Usable.replace("0b", "").rjust(32, "0")

    return toIP(str(Usable_IP))


def calculateNetwork(Network,Array):

    clss = Network.split("/");
    IP = clss[0]
    Prefix = clss[1]


    current_networkAddress = IP
    for x in range(len(Array)):
         power = int((power2(Array[x][1])))
         Prefix = 32 - power #get the needed number of host per network
         Array[x].append(current_networkAddress)
         Array[x].append(getMask(Prefix))
         Array[x].append("/" + str(Prefix))
         Array[x].append(str(pow(2,power)-2))
         Array[x].append(getFirstUsableIP(current_networkAddress))

         broadcast = getBroadcastIP(current_networkAddress,getMask(Prefix))

         Array[x].append(getLastUsableIP(broadcast))
         Array[x].append(broadcast)
         Array[x].append(str(((pow(2,power)) - int(Array[x][1]))-2))
         current_networkAddress = getNetworkIP(current_networkAddress ,getMask(Prefix) )


    for i in range(len(Array)):
        Array[i].pop(1)


    return Array


def power2(n):
    res = 1
    count = 0

    while True:
        count = count +1
        res = res*2
        curr = res - 2
        if (curr >= int(n)):
            break
    return count





def display(data):

   header = "|  Network ID  |  Network Name  |  Network Address  |  Subnet Mask         |  Prefix Length  |  Number of Usable IPs  |  First Usable Host address  |  Last Usable Host address  |  Broadcast Address  |   Number of Unused Address  |"
   print(header)

   for i in range(len(data)):
       print("|","    ",str(i+1)," "*5,"|", "  ",data[i][0]," "*(9-len(data[i][0]))," |",
             "  ",data[i][1]," "*(12-len(data[i][1]))," |",
             "  ",data[i][2]," "*(11-len(data[i][2]))," |",
             "  ",data[i][3]," "*(10-len(data[i][3]))," |",
             "  ",data[i][4]," "*(17-len(data[i][4]))," |",
             "  ",data[i][5]," "*(23-len(data[i][5]))," |",
             "  ",data[i][6]," "*(21-len(data[i][6]))," |",
             "  ",data[i][7]," "*(14-len(data[i][7]))," |",
             "  ",data[i][8]," "*(22-len(data[i][8]))," |",)




def subCalculator():



    IP = input("Input IP Address: ")


    if (checkIPvalid(IP, 2)):
        Mat = []
        m = int(input("Input number of networks: "))
        for i in range(m):
            name = input("Enter network name: ")
            numIP = input("Enter number of IP addresses ")
            arr = [name, int(numIP)]
            Mat.append(arr)
            Mat.sort(reverse=True, key=lambda x: x[1])

        Result = calculateNetwork(IP, Mat)
        display(Result)
    else:
        print("Invalid IP")
        input("Press ENTER to continue.......")





def checkType():
    IP = input("Input IP Address: ")
    clss = IP.split("/");



    if (checkIPvalid(IP,2)):
        prefix = int(clss[1])
        IPaddress = clss[0]
        binaryIPaddress = ip_to_binary(IPaddress)
        binarySubnet = prefixtoSubnetBinary(prefix)
        binaryHostbits = hostbitsBinary(32-prefix)
        result = getType(IP, binaryIPaddress, binarySubnet,binaryHostbits)
        print()
        print(result)
    else:
        print("Invalid IP")

    print()
    input("Press ENTER to continue...")

def checkAddress():

    answer = ""

    ip = input("Input IP Address: ")


    if (checkIPvalid(ip,1)):
        array = ip.split(".")
        IParray = list(map(int, array))


        if (IParray[0] >= 0 and IParray[0] <= 127 ):
            answer = "The IP address " + ip + " is a class A address whose network address is "
            answer = answer + str(IParray[0])+ ".0.0.0/8"

        elif(IParray[0] >= 128 and IParray[0]<=191):
            answer = "The IP address " + ip + " is a class B address whose network address is "
            answer = answer + str(IParray[0]) +"." + str(IParray[1])+ ".0.0/16"

        elif (IParray[0] >= 192 and IParray[0] <= 223):
            answer = "The IP address " + ip + " is a class C address whose network address is "
            answer = answer + str(IParray[0]) + "." + str(IParray[1]) + "." + str(IParray[2]) + "." + "0/24"
        elif (IParray[0] >= 224 and IParray[0]<= 239):
            answer = "The IP address " + ip + " is a class D address"
        elif (IParray[0] >= 240 and IParray[0] <= 255):
            answer = "The IP address " + ip + " is a class E address"
        else:
            answer = "cannot identify the class "
        print()
        print(answer)
    else:
        print("Invalid IP")
    print()
    input("Press ENTER to continue...")



def getType(IP,binaryAddress, binarySubnet,binaryHostBits):

    networkCompare = andOperationBitwise(binaryAddress, binarySubnet)
    broadcastCompare = orOperationBitwise(networkCompare, binaryHostBits)

    if (networkCompare == binaryAddress):
        return "The IP address " + IP + " is a Network address"
    elif (broadcastCompare == binaryAddress):
        return "The IP address " + IP + " is a Broadcast address"
    else:
        return "The IP address " + IP + " is a Host address"









def ip_to_binary(ip):
    octet_list_int = ip.split(".")
    octet_list_bin = [format(int(i), '08b') for i in octet_list_int]
    binary = ("").join(octet_list_bin)
    return binary

def andOperationBitwise(s1, s2):
    res = ""
    for i in range(32):
        # Convert s1[i] and s2[i] to int
        # and perform bitwise AND operation,
        # append to "res" string
        res = res + str(int(s1[i]) & int(s2[i]))

    return res








def hostbitsBinary(bits):
    str = ""

    x = range(bits)
    for i in x:
        str = str + "1"

    str = str.zfill(32)
    return str


def prefixtoSubnetBinary(prefix):

    str = ""

    x = range(prefix)
    for i in x:
        str = str + "1"

    str = str.ljust(32, '0');

    return str





def orOperationBitwise(s1, s2):
    res = ""
    for i in range(32):
        # Convert s1[i] and s2[i] to int
        # and perform bitwise AND operation,
        # append to "res" string
        res = res + str(int(s1[i]) | int(s2[i]))

    return res









def Menu():
    print("Hello there Network Engineer! ")
    print("In order to help you, please select any of the following options: ")
    print()
    print("1. Subnet calculator ")
    print("2. Check Address Class")
    print("3. Check Address Type")
    print("4. Exit")
    print("------------------------------------------------------------")





def checkIPvalid(value,type):
    zeroTo255 = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
    regex = zeroTo255 + "\\." + zeroTo255 + "\\." + zeroTo255 + "\\." + zeroTo255
    zeroTo32 = "([0-9]|[1-3][0-2])"

    if (type == 1):
        if (re.search(regex, value)):
            return True
        else:
            return False
    else:
        regex = regex + "\\/" + zeroTo32;
        if (re.search(regex, value)):
            return True
        else:
            return False


def main():
    while True:
        Menu()
        option = int(input("enter choice: "))
        if (option ==1):
            subCalculator()
            input("Press ENTER to continue")
        elif (option == 2):
            checkAddress()
        elif(option == 3):
            checkType()
        else:
            print("Good bye")
            break


if __name__ == '__main__':
    main()


