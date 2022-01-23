def get_storehouse():
    while True:
        print("Enter storehouse measurements:")
        height = input("height:")
        width = input("width:")
        depth = input("depth:")
        if height.isdigit() and width.isdigit() and depth.isdigit():
            height = int(height)
            width = int(width)
            depth = int(depth)
            if height >0 and width> 0 and depth > 0:
                return [height, width, depth]
            else:
                print("Please enter correct values\n")
        else:
            print("Please enter correct values\n")

def get_containers():
    containers = []
    while True:
        ans = input("Do you want to add new container?\n[y/n]\n")
        if ans == 'y':
            print("Enter the container measurements and number of containers with the given measurements:")
            height = input("height:")
            width = input("width:")
            depth = input("depth:")
            number = input("number:")
            if height.isdigit() and width.isdigit() and depth.isdigit() and number.isdigit():
                height = int(height)
                width = int(width)
                depth = int(depth)
                number = int(number)
                if height >0 and width> 0 and depth > 0 and number >0:
                    for i in range(number):
                        containers.append([height,width,depth])
                else:
                    print("Please enter correct values\n")
            else:
                print("Please enter correct values\n")
        elif ans == 'n':
            return containers
        else:
            print("Please enter correct answer\n")
        

def main():
    storehouse = get_storehouse()
    print(f"Storehouse measurements hxwxd = {storehouse[0]}x{storehouse[1]}x{storehouse[2]}\n")
    containers = get_containers()
    print("Given containers measurements hxwxd:")
    for i, container in enumerate(containers):
        print(f"{i+1}- {container[0]}x{container[1]}x{container[2]}") 

    print(storehouse)
    print(containers)
main()