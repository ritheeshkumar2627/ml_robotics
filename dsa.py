#second largest num in array
def secondlargest(arr):
    if len(arr) < 2:
        return -1
    
    largest=-1
    sec_largest=-1


    for num in arr:
        if num > largest:
            sec_largest=largest
            largest = num

        elif num> sec_largest and num < largest :
            sec_largest=num

    return sec_largest

array=([1,3,2,4,7,0])
print(secondlargest(array))

#moving zeroes in array to end
def move_zeros(arr):
    #create a positional pointer
    pos=0
    for num in arr:
        if num!=0:
            arr[pos]=num
            pos+=1
    while pos<len(arr):
        arr[pos]=0
        pos+=1

    return arr

set=([1,0,3,4,0,0,5,1,0])
print(move_zeros(set))

#sum of consecutive
def sumofconsecutive(n):
    for i in range(1,n):
        sum=0
        for j in range(i,n):
            sum+=j

            if sum==n and j>i :
                return True
            elif sum>n:
                break

    return False

print(sumofconsecutive(10))