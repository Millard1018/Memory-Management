from prettytable import PrettyTable
def validateInt(validNum, range1, range2):
    while True:
        try:
            validNum = int(validNum)
            if not validNum >= range1 or not validNum <= range2:
                print(f"Must have atleast {range1} or less than {range2}")
                validNum = input("Please Enter the number again: ")
            else:
                return validNum
        except ValueError:
            print("Invalid Entry must not have characters!")
            validNum = input("Please Enter the number again: ")

def default():
    print("\nYou have not choosen anything from the choices")
    print("Closing the program.\n")
    exit()

def fixed_partition_allocation_scheme():
    print("'A'-First In First Out\n'B'-Best Fit\n'C'-Next Fit\n'D'-Worst Fit")
    functions = {
        'A': First_In_First_Out,
        'B':Best_Fit,
        'C':Next_Fit,
        'D':Worst_Fit
    }
    partition_scheme = input("Enter the letter of your choice: ").upper()
    choice = functions.get(partition_scheme, None)
    if choice:
        jobs, par = user_input()
        return choice(jobs, par)
    else:
        default()

def user_input()->list:
    partition = []
    jobs = []
    memory: int = input("Enter the amount of memory: ")
    memory = validateInt(memory, 10, 1000)
    num_partition: int = input("Enter how many partition in the memory: ")
    num_partition = validateInt(num_partition, 1, 100)
    print("\nEnter the amount of memory for each Partition")
    for i in range(1, num_partition+1):
        if memory >= sum(partition) and i == num_partition:
            print(f"Partition #{i}: {memory-sum(partition)}")
            partition.append(memory-sum(partition))
            break
        par: int = input(f"Partition #{i}: ")
        par = validateInt(par, 1, 1000)
        if memory >= sum(partition)+par:
            partition.append(par)
        else:
            print("The size of partition exceed the size of memory")
            while memory < sum(partition)+par:
                par: int = input(f"Enter Partition #{i} again: ")
                par = validateInt(par, 1, 1000)
            partition.append(par)

    num_jobs: int = input("\nEnter how many jobs: ")
    num_jobs = validateInt(num_jobs, 1, 100)
    for i in range(1, num_jobs+1):
        job: int = input(f"Enter Job #{i}: ")
        job = validateInt(job, 1, 1000)
        jobs.append(job)

    return jobs, partition

def First_In_First_Out(jobs: list, partition: list)->list:
    fragmentation: list = []
    waiting: list = []
    fifo_list = []
    allocated_partitions = []
    for i, job in enumerate(jobs): # The i will track the index and the 'job' is the elements of jobs
        allocated = False
        for j, part in enumerate(partition): # The j will track the index and the 'part' is the elements of partition
            if job <= part:
                frag = part - job
                fragmentation.append(frag)
                fifo_list.append([j, part, f"J{i+1}", job, frag])
                allocated_partitions.append(j)
                partition[j] = 0
                allocated = True
                break
        if not allocated:
            waiting.append(i+1)

    for p, part in enumerate(partition): # If there is a partition that has not be allocated
        if p not in allocated_partitions:
            fifo_list.append([p, part, None, None, 0])

    fifo_list = sorted(fifo_list, key=lambda x: x[0]) # Sorting of the fifo_list value using the partition number
    for x in fifo_list:
        x[0] = f"P{x[0]+1}"

    return fifo_list, fragmentation, waiting

def Best_Fit(jobs: list, partition: list)->list:
    fragmentation: list = []
    waiting: list = []
    fifo_list = []
    allocated_partitions = []
    for i, job in enumerate(jobs): # The i will track the index and the 'job' is the elements of jobs
        part = min((x for x in partition if x >= job), default=None) # Will find the minimum value that is greater than or equal than the job
        if part:
            frag = part - job
            fragmentation.append(frag)
            index = partition.index(part)
            fifo_list.append([index, part, f"J{i+1}", job, frag])
            allocated_partitions.append(index)
            partition[index] = 0
        else:
            waiting.append(i+1)

    for p, part in enumerate(partition): # If there is a partition that has not be allocated
        if p not in allocated_partitions:
            fifo_list.append([p, part, None, None, 0])

    fifo_list = sorted(fifo_list, key=lambda x: x[0]) # Sorting of the fifo_list value using the partition number
    for x in fifo_list:
        x[0] = f"P{x[0]+1}"

    return fifo_list, fragmentation, waiting

def Next_Fit(jobs: list, partition: list)->list:
    fragmentation: list = []
    waiting: list = []
    fifo_list = []
    allocated_partitions: list = []
    allocated_index = 0
    for i, job in enumerate(jobs):
        allocated = False
        for j in range (allocated_index, len(partition)):
            if job <= partition[j]:
                frag = partition[j] - job
                fragmentation.append(frag)
                fifo_list.append([j, partition[j], f"J{i+1}", job, frag])
                allocated_partitions.append(j)
                partition[j] = 0
                allocated_index = j
                allocated = True
                break
        if not allocated:
            waiting.append(i+1)

    for p, part in enumerate(partition): # If there is a partition that has not be allocated
        if p not in allocated_partitions:
            fifo_list.append([p, part, None, None, 0])

    fifo_list = sorted(fifo_list, key=lambda x: x[0]) # Sorting of the fifo_list value using the partition number
    for x in fifo_list:
        x[0] = f"P{x[0]+1}"

    return fifo_list, fragmentation, waiting

def Worst_Fit(jobs: list, partition: list)->list:
    fragmentation: list = []
    waiting: list = []
    fifo_list = []
    allocated_partitions = []
    for i, job in enumerate(jobs): # The i will track the index and the 'job' is the elements of jobs
        part = max((x for x in partition if x >= job), default=None) # Will find the minimum value that is greater than or equal than the job
        if part:
            frag = part - job
            fragmentation.append(frag)
            index = partition.index(part)
            fifo_list.append([index, part, f"J{i+1}", job, frag])
            allocated_partitions.append(index)
            partition[index] = 0
        else:
            waiting.append(i+1)

    for p, part in enumerate(partition): # If there is a partition that has not be allocated
        if p not in allocated_partitions:
            fifo_list.append([p, part, None, None, 0])

    fifo_list = sorted(fifo_list, key=lambda x: x[0]) # Sorting of the fifo_list value using the partition number
    for x in fifo_list:
        x[0] = f"P{x[0]+1}"

    return fifo_list, fragmentation, waiting

def display(scheme: list, fragmentation: list, waiting:list):
    print("\n")
    table = PrettyTable()
    table.field_names = ["Partition", "Partition Size", "Job", "Job Size", "Internal Fragmentation"]
    for row in scheme:
        table.add_row(row)

    print(table)
    print("\n")

    if waiting:
        print(f"Waiting: ", end = "")
        for wait in waiting:
            print(f"J{wait}", end = " ")

    if fragmentation:
        print(f"\nAverage Internal Fragmentation: {sum(fragmentation)/len(fragmentation):.2f}")

def main()->None:
    scheme, fragmentation, waiting = fixed_partition_allocation_scheme()
    display(scheme, fragmentation, waiting)

if __name__ == '__main__':
    main()