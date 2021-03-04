class Solution(object):
    def validPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        left = 0
        right = len(s) - 1
        lista = []
        lista = s
        value1 = False

        while left <= right:
            if lista[left] == lista[right]:
                left += 1
                right -= 1

            if lista[left] != lista[right]:
                left += 1
                if lista[left] == lista[right]:
                    return False

            if lista[left] == lista[right]:
                value1 = True
                return value1


print(Solution.validPalindrome('',"bddb"))