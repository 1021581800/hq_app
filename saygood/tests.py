class Solution:
    def findKthLargest(self, nums, k) :

        def partition(array, left,right):
            i = left-1
            for j in range(left,right):
                if array[j] <= array[right]:
                    i += 1
                    array[i], array[j] = array[j],array[i]
            array[i+1], array[right] = array[right],array[i+1]
            return i+1

        def quickSort(array,left,right,k):

            if left<=right:
                #如果
                pivot = partition(array,left,right)
                if pivot == len(array) - k:
                    return array[pivot]
                elif pivot < len(array) - k:
                    return quickSort(array,pivot+1,right,k)
                else:
                    return quickSort(array,left,pivot-1,k)
        #传入k
        return quickSort(nums,0,len(nums)-1,k)
Solution.findKthLargest('',[3,2,1,5],2)