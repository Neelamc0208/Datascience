"""
CryptoCurrency class is created to store attribute of crypto currency. We also add attribute cost which has ratio of profit value and quantity value
CryptoCurrencySelection class has implementation of fractional knapsack problem which uses heap sort for sorting based on max profit value.
MaxHeap class is implementation of sorting value in Descending order.


"""


class CryptoCurrency :
 
    """Crypto currency class created to store attribues """
 
    def __init__(self,code, quant_value, profit_value, index):
        self.code = code
        self.quant_value = quant_value
        self.profit_value = profit_value
        self.index = index
        self.cost = profit_value / quant_value
 
    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return f'ItemValue({self.cost})'
 
# Greedy Approach 
 
class CryptoCurrencySelection:
 
    """implementation of fractional knapsack problem which uses heap sort for sorting based on max profit value"""
    @staticmethod
    def getMaxValue(code,quantity,price, profit, capacity):
        """function to get maximum value """
        iVal = []
        for i in range(len(code)):
            iVal.append(CryptoCurrency(code[i], quantity[i]*price[i], quantity[i]*profit[i], i))
 
        # sorting items by value
        sort_value=MaxHeap(iVal)

        selected_val= []
        selected_ratio_item = []
        totalValue = 0
        while len(sort_value)>0:
            i = sort_value.pop()
            curWt = int(i.quant_value)
            curVal = int(i.profit_value)
            if capacity - curWt >= 0:
                capacity -= curWt
                totalValue += curVal
                
                selected_val.append(i.code)
            else:
                fraction = capacity / curWt
                selected_ratio_item.append([i.code,fraction])
                totalValue += curVal * fraction
                capacity = int(capacity - (curWt * fraction))
                break
        return (totalValue, selected_val, selected_ratio_item )


class MaxHeap:
    """
    Creation of Max heeap for sorting
    """

    def __init__(self, arr=[]):
        # Initializing the heap with no elements in it
        self._heap = []
         
        # If the array by the user is not empty, push all the elements
        if arr is not None:
            for root in arr:
                self.push(root)
 

    def push(self, value):
        # Appending the value given by user at the last
        self._heap.append(value)
        # Calling the bottom_up() to ensure heap is in order.
        # here we are passing our heap 
        _bottom_up(self._heap, len(self) - 1)
 

    def pop(self):
        if len(self._heap)!=0:
        # swapping the root value with the last value.
 
            _swap(self._heap, len(self) - 1, 0)
        # storing the popped value in the root variable
 
            root = self._heap.pop()
 
        #Calling the top_down function to ensure that the heap is still in order 
            _top_down(self._heap, 0)
             
        else:
            root="Heap is empty"
        return root
 

    def __len__(self):
        return len(self._heap)


    def peek(self):
        if len(self._heap)!=0:
            return(self._heap[0])
        else:
            return("heap is empty")

    def printh(self):
        for i in range(len(self._heap)):
            print(self._heap[i])
 
# Swaps value in heap between i and j index
def _swap(L, i, j):
    L[i], L[j] = L[j], L[i]
 
# This is a private function used for traversing up the tree and ensuring that heap is in order
def _bottom_up(heap, index):
    # Finding the root of the element
    root_index = (index - 1) // 2
     
    # If we are already at the root node return nothing
    if root_index < 0:
        return
 
    # If the current node is greater than the root node, swap them
    if heap[index] > heap[root_index]:
        _swap(heap, index,root_index)
    # Again call bottom_up to ensure the heap is in order
        _bottom_up(heap, root_index)
 
# This is a private function which ensures heap is in order after root is popped
def _top_down(heap, index):
    child_index = 2 * index + 1
    # If we are at the end of the heap, return nothing
    if child_index >= len(heap):
        return
 
    # For two children swap with the larger one
    if child_index + 1 < len(heap) and heap[child_index] < heap[child_index + 1]:
        child_index += 1
 
    # If the child node is smaller than the current node, swap them
    if heap[child_index] > heap[index]:
        _swap(heap, child_index, index)
        _top_down(heap, child_index)




def main():
    
    # open both input anf output text files

    file_name = "inputPS1.txt"
    try:
        infile = open(file_name, "r")

    except:
        print("File ", file_name, " is not present")
        print("Please ensure file ",file_name," is present in the folder") 

    outfile = open("outputPS1.txt", "w")
    
    # declare lists that will store code, sellPrice, quantity and profit
    code = []
    sellPrice = []
    profit = []
    quantity = []
    CoinCount = 0
    max_spend = 0
    outdata1 = []
    outdata2 = []
    
    # now, read input file line by line
    # each line includes code, capacity, and profit separated by delimiter " / "
    for line in infile:
        if ':' in line:
            i, count = line.strip().split(":")
            if i == "Type of Crypto coins":
                CoinCount = int(count)
            elif i == "Maximum spend":
                max_spend= int(count)
        elif '/' in line and line.count('/') ==3:
            
            # split values from the line
            i, b, v, k = line.strip().split(" / ")
            # add values to the corresponding lists
            code.append(i)
            quantity.append(int(b))
            sellPrice.append(int(v))
            profit.append(int(k))
            
        elif '/' in line and line.count('/') !=3 :
            outdata1.append("Incorrect format, line ignored:" + line )
            
    if CoinCount == 0 or max_spend == 0 or len(code) ==0 :
        if len(code) ==0:
            outdata1.append("\n input file is blank or format is not correct. Please check.")
        elif CoinCount == 0:
            outdata1.append("\nType of Crypto coins: information is missing\zero in input file. Please correct input file.")
        elif max_spend ==0:
            outdata1.append("\nMaximum spend: information is missing\zero in input file. Please correct input file.")
        else:
            outdata1.append("\ninput file format is not correct. Please use correct format.")
            
    else: 
        if int(len(code)) != CoinCount:
            outdata1.append("\nType of Crypto coins: " + str(CoinCount) + " in input file but actual values are : " + str(len(code))+ " which will be used in calculation.")
        capacity = max_spend
        maxValue,selected_val,selected_ratio_item = CryptoCurrencySelection.getMaxValue(code,quantity,sellPrice, profit, capacity)
        #print (maxValue,selected_val,selected_ratio_item )   
        # write all three returned values to the output file


        outdata1.append("\n\nTotal profit: " + str(round(maxValue,2)))

        outdata1.append("\nQuantity selection Ratio:\n")
        outdata2.append("\nTotal Quantity of each coin sold:\n")
        for i in range(len(code)):
            if code[i] in selected_val:
                outdata1.append(code[i] + " 1 \n")
                outdata2.append(code[i] + " " + str(quantity[i]) +"\n")
            elif code[i] in selected_ratio_item[0]:
                outdata1.append(code[i] + " " + str(round(selected_ratio_item[0][1],3)) + " \n")
                outdata2.append(code[i] + " " + str(round(selected_ratio_item[0][1] * quantity[i],3)) + " \n")
            else:
                outdata1.append(code[i] +  " 0 \n")
                outdata2.append(code[i] +  " 0 \n")
                
    outfile.write("".join(outdata1))
    outfile.write("".join(outdata2))    
    # close files
    infile.close()
    outfile.close()
    

# Driver Code
if __name__ == "__main__":
    main()

