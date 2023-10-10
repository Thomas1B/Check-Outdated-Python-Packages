'''
Python program to check if pip is outdated, as well as all installed python packages.
If pip or any modules are outdated, programs asks user if they would like to update them.

This program was mostly written using ChatGPT, as I wanted to see what it was capable of.
'''

import os
import subprocess


def check_pip_update():
    '''
    Function to check if 'pip' is up to date.

        If pip is outdated, updated is automaticaly installed.

        Parameters:
            None

        Returns:
            None
    '''

    print("\nChecking if pip is outdated...")

    # try block to make sure pip is installed.
    try:
        # checking if pip is outdated
        outdated_check = subprocess.run(
            ['pip', 'list', '--outdated'],
            capture_output=True, text=True
        )

        if "pip" in outdated_check.stdout.lower():
            print("The pip package is outdated.")
            user_text = 'Would you like to update pip? (y/n): '
            user = input(user_text)
            if user.lower() in ['y', 'yes']:
                # updating pip
                subprocess.run(
                    ['pip', 'install', '--upgrade', 'pip']
                )
            else:
                print("pip update skipped.")
        else:
            print("Your pip package is up to date!")

    except subprocess.CalledProcessError:
        exit("pip is not installed on your system!.\n")


def get_installed_pkgs() -> list[str]:
    '''
    Function to get all installed modules.

        Parameters:
            None

        Returns:
            list of modules names (alphabetical order).
    '''

    # try block to make sure pip is installed.
    try:
        # Run 'pip list' command to get a list of installed packages
        result = subprocess.run(
            ['pip', 'list'], stdout=subprocess.PIPE, text=True
        )

        # Split the output into lines and skip the header
        lines = result.stdout.strip().split('\n')[2:]

        # Extract package names
        modules = [line.split()[0] for line in lines]
        return modules

    except subprocess.CalledProcessError:
        print('Failed to get the list of installed modules!')
        exit('Pip may not be installed on your system...\n')


def get_pkgs_versions() -> list[str]:
    '''
    Function to get all installed modules versions.

        Parameters:
            None

        Returns:
            list of modules versions same order as get_installed_pkgs.
    '''

    # try block to make sure pip is installed.
    try:
        # Run 'pip list' command to get a list of installed packages
        result = subprocess.run(
            ['pip', 'list'], stdout=subprocess.PIPE, text=True)

        # Split the output into lines and skip the header
        lines = result.stdout.strip().split('\n')[2:]

        # Extract package versions
        versions = [line.split()[1] for line in lines]
        return versions

    except subprocess.CalledProcessError:
        print('Failed to get the list of module versions!')
        exit("Pip may not be installed on your system.\n")


def show_installed_pkgs():
    '''
    Function to ask user if they want to print installed modules.

        Parameters:
            None

        Returns:
            None
    '''

    # asking user if they want to show all installed packages
    user = input("Show installed packages? (y/n): ")
    if user.lower() in ['yes', 'y']:
        print('\nShowing installed packages...\n')
        print('Installed packages:')

        # getting installed modules
        installed_modules = get_installed_pkgs()

        if len(installed_modules) > 0:
            for i, module in enumerate(installed_modules, 1):
                print('{:>3} - {:s}'.format(i, module))

            if len(installed_modules) == 1:
                grammar = 'is'
            else:
                grammar = 'are'
            text = f'\nThere {grammar} {len(installed_modules)} packages installed.\n'
        else:
            text = "There are no packages installed!"
        print(text)
    else:
        print("Skipped.\n")


def check_outdated_pkgs():
    '''
    Function to show outdated modules.
    '''

    outdated_modules = []

    # try-block to make sure pip is installed.
    try:
        print("\nChecking for outdated packages...")
        # Get a list of outdated modules
        outdated_modules = subprocess.check_output(
            ['pip', 'list', '--outdated'])
        outdated_modules = outdated_modules.decode().strip().split('\n')[2:]
        outdated_modules = [module.split()[0] for module in outdated_modules]

        if outdated_modules:
            # print list of modules
            for i, module in enumerate(outdated_modules):
                print('{:>3} - {:s}'.format(i+1, module))
            print(f"\nThere are {len(outdated_modules)} packages outdated.\n")

            # asking user to update all packages
            user = input("Would you like to update all of them? (y/n): ")
            if user.lower() in ['y', 'yes']:
                updated_pkgs()
            else:  # asking user if they want to update any packages.
                user = input("Would you like to update any package? (y/n): ")
                if user.lower() in ['y', 'yes']:
                    specific_modules = input(
                        "Enter the packages you want to update (separated by commas): "
                    )
                    if specific_modules:
                        for module in specific_modules.split(','):
                            updated_pkgs(module)
                else:
                    print("Skipped.\n")
        else:
            print('All packages are up to date!\n')

    except subprocess.CalledProcessError:
        print("Error: Failed to check for outdated modules.")
        exit('Pip may not be installed on your system.\n')

    return outdated_modules


def updated_pkgs(modules=None):
    '''
        Function to packages.

            Parameter:
                modules (list/str): single module or list of modules to update

            Returns:
                None
    '''

    try:
        if modules:
            # Update specific modules
            subprocess.call(['pip', 'install', '--upgrade'] + modules)
        else:
            # Update all outdated modules
            print('\nUpdating all outdated packages...\n')
            result = subprocess.run(
                ['pip', 'list', '--outdated'], capture_output=True, text=True)
            outdated_packages = result.stdout.strip().split('\n')[2:]

            # Step 2: Extract package names
            packages_to_update = [package.split()[0]
                                  for package in outdated_packages]

            # Step 3: Upgrade packages
            for package in packages_to_update:
                subprocess.run(['pip', 'install', '--upgrade', package])

            print("\nUpdating all packages complete!\n")

    except subprocess.CalledProcessError:
        print(f"Error: Failed to update modules.")


def main():
    '''
    Main Program function
    '''

    check_pip_update()
    check_outdated_pkgs()
    show_installed_pkgs()

    # Not used yet
    # user = input("\nDo you want to uninstall any packages? (y/n): ")
    # if user.lower() == 'y':
    #     user = input("Uninstall all packages?: (y/n): ")
    #     if user.lower() == 'y':
    #         print("Uninstalling all packages... testing")
    #         # save_module_names_to_file("Python_Packages_List.txt")
    #     else:
    #         modules = input("Enter the packages you want to uninstall (separated by commas): ")
    #         if modules:
    #             uninstall_module(modules)
    #         else: print("Skipped!\n")
    # else: print('Skipped.\n')

# ******* not used yet *******


def save_module_names():
    '''
    Function to save installed modules to a .txt file for reference.
    '''

    downloads_path = os.path.expanduser("~" + os.sep + "Downloads")
    filename = f'{downloads_path}/Python Modules.txt'

    # modules = [dist.key for dist in pkg_resources.working_set]

    # Run 'pip list' command to get a list of installed packages
    result = subprocess.run(['pip', 'list'], stdout=subprocess.PIPE, text=True)

    # Split the output into lines and skip the header
    lines = result.stdout.strip().split('\n')[2:]

    # Extract package names and versions
    modules = [line.split()[0] for line in lines]

    with open(filename, 'w') as f:
        f.write('Python Packages:\n')
        for i, module in enumerate(modules):
            f.write('{:>3}, {:s}\n'.format(i+1, module))
    print(
        f'Module names saved to "{filename.split("/")[-1]}" in your downloads.')


def uninstall_module(modules):
    '''
    Function to uninstall a module

    Parameter:
        modules - str: name of module 
    '''
    for module in modules:
        try:
            subprocess.check_call(['pip', 'uninstall', '-y', module])
            print(f"Successfully uninstalled {module}.")
        except subprocess.CalledProcessError:
            print(f"Failed to uninstall {module}.")


def uninstall_all_pkgs():
    '''
    Function to uninstall all modules.

     calls save_module_name for future reference.
    '''

    modules = get_installed_pkgs()

    save_module_names()
    for module in modules:
        try:
            subprocess.check_call(['pip', 'uninstall', '-y', module])
            print(f"Successfully uninstalled {module}.")
        except subprocess.CalledProcessError:
            print(f"Failed to uninstall {module}.")


if __name__ == '__main__':
    main()
