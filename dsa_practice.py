def missing_num(arr):
    if arr.pop()==len(arr):
        print("no missing number")

    else:
        n=len(arr)+1
        total=n*(n+1)/2
        return (total-sum(arr))

    

array=([1,2,4,5,6,7])
print(missing_num(array))
