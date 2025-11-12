def count_steps(s1,s2):
    if s2=="":
        return len(s1)
    count = 0
    i = 0    
    s1 = list(s1)
    s2 = list(s2)
    for j in range(len(s2)):
            if i==len(s1)-1 and j == len(s2)-1 and s1[i] == s2[j]:
                i +=1 
            elif i<len(s1) and s1[i] == s2[j]:
                if i == len(s1):
                    return count
                i += 1
            elif i<len(s1)-1 and j==len(s2)-1 and s1[i+1]==s2[j]:  
                count += 1
                s1.pop(i)
                i += 1
            elif i==len(s1)-1 and j<len(s2)-1 and s1[i]==s2[j+1]:  
                count += 1
                s1.insert(i,s2[j])
                i += 1    
            elif i<len(s1)-1 and j<len(s2)-1 and s1[i] == s2[j+1] and s1[i+1] != s2[j+1]:
                count += 1
                s1.insert(i,s2[j])
                i += 1
            elif i<len(s1)-1 and j<len(s2)-1 and s1[i] == s2[j+1] and s1[i+1] == s2[j+1]:
                count += 1
                s1[i] = s2[j]
                i += 1
            elif i<len(s1)-1 and j<len(s2)-1 and s1[i] != s2[j+1] and s1[i+1] != s2[j+1] and s1[i+1]==s2[j]:  
                count += 1
                s1.pop(i)
                i += 1
            elif i == len(s1):   
                count += len(s2) - j
                break
            else:
                count += 1
                s1[i] = s2[j]
                i += 1
    if len(s1) > len(s2):
            count += len(s1)-len(s2)
    return count        
            
x = input("enter the string s1 : ")
y = input("enter the string s2 : ")
print("steps to make s2 from s1 : ",count_steps(x,y))                                      