def reverse(arr,start,end):
    while start<end:
        arr[start],arr[end]=arr[end],arr[start]
        start+=1
        end-=1
def rotate_matrix_rows(mat,k):
     n=len(mat) if len(mat)>0 else -1
     m=len(mat[0])
     k%=m
     for i in range(n):
         reverse(mat[i],0,m-1)
         reverse(mat[i],0,k-1)
         reverse(mat[i],k,m-1)
         
     return mat


test=[[1,2,3,4,5]]

print(rotate_matrix_rows(test,7))

