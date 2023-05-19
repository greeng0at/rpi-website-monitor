def difference(string1, string2):
      # Split both strings into list items
  string1 = string1.split()
  string2 = string2.split()

  A = set(string1) # Store all string1 list items in set A
  B = set(string2) # Store all string2 list items in set B
 
  str_diff = A.symmetric_difference(B)
  isEmpty = (len(str_diff) == 0)
 
  if isEmpty:
    print("No Difference. Both Strings Are Same")
  else:
    print("The Difference Between Two Strings: ")
    print(str_diff)
  
  print('The programs runs successfully.')

# Driver code to call a function
usr_str1 = 'Educative is good animal goon'
usr_str2 = 'Educative is bad animal goon botany'
output = difference(usr_str1, usr_str2)