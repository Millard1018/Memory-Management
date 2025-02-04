from prettytable import PrettyTable #PrettyTable is a library used to organized data structures like list or arrays

def validateInt(validNum, range1, range2): # To avoid exception and validate user's input
    while True:
        try: # will try until it raise exception
            validNum = int(validNum)
            if not validNum >= range1 or not validNum <= range2: # Programmer used of valid ranges from num to num
                print(f"Must have atleast {range1} or less than {range2}")# out of range
                validNum = input("Please Enter the number again: ")# reentry
            else:
                return validNum
        except ValueError as e: # Exception raise a character is inputted
            print(f"Invalid Entry: {e}, must not have characters! ")
            validNum = input("Please Enter the number again: ")

def default(): # User did not choose any from the given allocation scheme
    print("\nYou have not choosen anything from the choices")
    print("Closing the program.\n")
    exit()

def fixed_partition_allocation_scheme(): # User is able to choose an allocation scheme that they want to commit
    print("'A'-First In First Out\n'B'-Best Fit\n'C'-Next Fit\n'D'-Worst Fit")
    functions = {
        'A': First_In_First_Out,
        'B':Best_Fit,
        'C':Next_Fit,
        'D':Worst_Fit
    } # dictionary which key is the user choice and value which is a function that will be executed
    partition_scheme = input("Enter the letter of your choice: ").upper()
    choice = functions.get(partition_scheme, None) # will execute a function from the option and will give the function as value unless None
    if choice: # User chooses an appropriate letter for a partition scheme
        jobs, par = user_input()
        return choice(jobs, par)
    else: # choice has value of None because user did not choose any letter from the option
        default()

def user_input()->list:
    partition: list = [] # Will contain the size of each partition
    jobs: list = [] # Will contain the size of each job 
    memory: int = input("Enter the amount of memory: ") # User can enter an appropriate amount of memory depending on the specific range
    memory = validateInt(memory, 10, 1000) # Range of appropriate memry size is from 10 to 1000
    num_partition: int = input("Enter how many partition in the memory: ")# User can enter how many partition the memory will be divided
    num_partition = validateInt(num_partition, 1, 100) # Range of appropriate memry size is from 1 to 100
    print("\nEnter the amount of memory for each Partition") # The first and succeding partion until before last 
    for i in range(1, num_partition+1):                      #User can enter the amount of memory for each partition
        if memory >= sum(partition) and i == num_partition: # The size of the last partition will depend on the remaining memory
            print(f"Partition #{i}: {memory-sum(partition)}")
            partition.append(memory-sum(partition))
            break
        par: int = input(f"Partition #{i}: ")
        par = validateInt(par, 1, 1000)
        if memory >= sum(partition)+par:
            partition.append(par)
        else:
            print("The size of partition exceed the size of memory") # If the user entered a value that will exceed the memory
            while memory < sum(partition)+par:                       # Reentry of the size of the particular partition
                par: int = input(f"Enter Partition #{i} again: ")
                par = validateInt(par, 1, 1000)
            partition.append(par)

    num_jobs: int = input("\nEnter how many jobs: ") # Jobs dont have the constraint of memory
    num_jobs = validateInt(num_jobs, 1, 100) # range of job from 1 to 100
    for i in range(1, num_jobs+1):
        job: int = input(f"Enter Job #{i}: ") # value for each job
        job = validateInt(job, 1, 1000)
        jobs.append(job)

    return jobs, partition

def First_In_First_Out(jobs: list, partition: list)->list:
    fragmentation: list = [] # list of all fragments in each partition unless partition is not used
    memory_utilization: list = [] # list of all memory utilized
    waiting: list = [] # list of jobs that is in waiting 
    fifo_list: list = [] # list containing the values that will be display
    allocated_partitions = [] # list of allocated partition that will be used to check to identify partition that was not used
    for i, job in enumerate(jobs): # The i will track the index and the 'job' is the elements of jobs
        allocated = False
        for j, part in enumerate(partition): # The j will track the index and the 'part' is the elements of partition
            if job <= part:
                frag = part - job # To identify the amount of fragmentation for each allocated partition
                fragmentation.append(frag)
                mem = (job/part)*100 # To identify the percentage of memory utilized for each allocated partition
                memory_utilization.append(mem)
                fifo_list.append([j, part, f"J{i+1}", job, frag, mem])# Will be used in display contains the particular partion, size fragmentation and memory utilized
                allocated_partitions.append(j) # Used to check to identify partition that was not used
                partition[j] = 0 # The particular partition will be set to 0 that will indicate that the partition is allocated
                allocated = True
                break
        if not allocated:
            waiting.append(i+1)

    return partition, allocated_partitions, fifo_list, fragmentation, waiting, memory_utilization

def Best_Fit(jobs: list, partition: list)->list:
    fragmentation: list = [] # list of all fragments in each partition unless partition is not used
    memory_utilization: list = [] # list of all memory utilized
    waiting: list = [] # list of jobs that is in waiting 
    bestFit: list = [] # list containing the values that will be display
    allocated_partitions = [] # list of allocated partition that will be used to check to identify partition that was not used
    for i, job in enumerate(jobs): # The i will track the index and the 'job' is the elements of jobs
        part = min((x for x in partition if x >= job), default=None) # Will find the minimum value that is greater than or equal than the job
        if part:
            frag = part - job # To identify the amount of fragmentation for each allocated partition
            mem = (job/part)*100
            memory_utilization.append(mem) # To identify the percentage of memory utilized for each allocated partition
            fragmentation.append(frag)
            index = partition.index(part)
            bestFit.append([index, part, f"J{i+1}", job, frag, mem])# Will be used in display contains the particular partion, size fragmentation and memory utilized
            allocated_partitions.append(index) # Used to check to identify partition that was not used
            partition[index] = 0
        else:
            waiting.append(i+1)

    return partition, allocated_partitions, bestFit, fragmentation, waiting, memory_utilization

def Next_Fit(jobs: list, partition: list)->list:
    fragmentation: list = [] # list of all fragments in each partition unless partition is not used
    memory_utilization: list = [] # list of all memory utilized
    waiting: list = [] # list of jobs that is in waiting 
    nextFit: list = [] # list containing the values that will be display
    allocated_partitions = [] # list of allocated partition that will be used to check to identify partition that was not used
    for i, job in enumerate(jobs):
        allocated = False
        for j in range (allocated_index, len(partition)):
            if job <= partition[j]:
                frag = partition[j] - job # To identify the amount of fragmentation for each allocated partition
                fragmentation.append(frag)
                mem = (job/partition[j])*100# To identify the percentage of memory utilized for each allocated partition
                memory_utilization.append(mem)
                nextFit.append([j, partition[j], f"J{i+1}", job, frag, mem])# Will be used in display contains the particular partion, size fragmentation and memory utilized
                allocated_partitions.append(j) # Used to check to identify partition that was not used
                partition[j] = 0
                allocated_index = j
                allocated = True
                break
        if not allocated:
            waiting.append(i+1)
        
    return partition, allocated_partitions, nextFit, fragmentation, waiting, memory_utilization

def Worst_Fit(jobs: list, partition: list)->list:
    fragmentation: list = [] # list of all fragments in each partition unless partition is not used
    memory_utilization: list = [] # list of all memory utilized
    waiting: list = [] # list of jobs that is in waiting 
    worstFit: list = [] # list containing the values that will be display
    allocated_partitions = [] # list of allocated partition that will be used to check to identify partition that was not used
    for i, job in enumerate(jobs): # The i will track the index and the 'job' is the elements of jobs
        part = max((x for x in partition if x >= job), default=None) # Will find the minimum value that is greater than or equal than the job
        if part:
            frag = part - job # To identify the amount of fragmentation for each allocated partition
            fragmentation.append(frag)
            mem = (job/part)*100 # To identify the percentage of memory utilized for each allocated partition
            memory_utilization.append(mem)
            index = partition.index(part)
            worstFit.append([index, part, f"J{i+1}", job, frag, mem])# Will be used in display contains the particular partion, size fragmentation and memory utilized
            allocated_partitions.append(index) # Used to check to identify partition that was not used
            partition[index] = 0
        else:
            waiting.append(i+1)

    return partition, allocated_partitions, worstFit, fragmentation, waiting, memory_utilization

def sort_allocation_scheme(partition:list, allocated_partitions: list, allocation_scheme: list):

    for p, part in enumerate(partition): # If there is a partition that has not be allocated
        if p not in allocated_partitions:
            allocation_scheme.append([p, part, None, None, 0, None])

    allocation_scheme = sorted(allocation_scheme, key=lambda x: x[0]) # Sorting of the fifo_list value using the partition number
    for x in allocation_scheme:
        x[0] = f"P{x[0]+1}"

    return allocation_scheme

def display(scheme: list, fragmentation: list, waiting:list, memory_utilization:list, partition:list):
    print("\n")
    table = PrettyTable() # to access PrettyTable
    table.field_names = ["Partition", "Partition Size", "Job", "Job Size", "Internal Fragmentation", "Memory Utilization"] # module of PrettyTable
    for row in scheme:                                                                                                     # Will seve as the header
        table.add_row(row) # Value per elemenent in scheme

    print(table) # Print the whole Table
    print("\n")

    if waiting: # If there is a job in waiting
        print(f"Waiting: ", end = "")
        for wait in waiting:
            print(f"J{wait}", end = " ")

    if fragmentation: #If there is fragmentation
        print(f"Average Internal Fragmentation: {sum(fragmentation)/len(fragmentation):.2f}")
    
    if memory_utilization: # If memory has been utilized
        print(f"Average Memory Utilization: {sum(memory_utilization)/len(partition):.2f}%")

def main()->None:
    partition, allocated_partitions, allocation_scheme, fragmentation, waiting, memory_utilization = fixed_partition_allocation_scheme()
    allocation_scheme = sort_allocation_scheme(partition, allocated_partitions, allocation_scheme)
    display(allocation_scheme, fragmentation, waiting, memory_utilization, partition)

if __name__ == '__main__': # main guard, to avoid unwanted execution
    main()