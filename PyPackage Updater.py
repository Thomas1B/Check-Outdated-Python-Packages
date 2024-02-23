'''
Python program to check if pip is outdated, as well as all installed python packages.
If pip or any modules are outdated, programs asks user if they would like to update them.

This program was mostly written using ChatGPT, as I wanted to see what it was capable of.

to run auto update `python filename.py auto`
'''

import os
import subprocess
import sys


UPDATED = []


def check_pip_update(auto=False):
    '''
    Function to check if 'pip' is up to date.

        If pip is outdated, updated is automaticaly installed.

        Parameters:
            auto: update without asking user, (default False).

        Returns:
            None
    '''

    # local function
    def update_pip():
        global UPDATED
        UPDATED.append('pip')
        subprocess.run(
            [sys.executable, '-m', 'pip',
             'install', '--upgrade', 'pip']
        )

    print("\nChecking if pip is outdated...")

    # try block to make sure pip is installed.
    try:
        # checking if pip is outdated
        outdated_check = subprocess.run(
            ['pip', 'list', '--outdated'],
            capture_output=True, text=True
        )

        if "pip" in outdated_check.stdout.lower():
            print("-> The pip package is outdated.", end=' ')

            if auto:
                print('Auto updating')
                update_pip()
                return

            user_text = 'Would you like to update it? (y/n): '
            user = input(user_text)
            if user.lower() in ['y', 'yes']:
                update_pip()
            else:
                print("-> pip update skipped.")
        else:
            print("-> pip package is up to date")

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


def get_outdated_pkgs() -> list:
    '''
    Function to get a list of outdated packages.
    '''

    # Get a list of outdated modules
    outdated_modules = subprocess.check_output(
        ['pip', 'list', '--outdated'])
    outdated_modules = outdated_modules.decode().strip().split('\n')[2:]
    outdated_modules = [module.split()[0] for module in outdated_modules]


def check_outdated_pkgs(auto=False) -> None:
    '''
    Function to show outdated modules.

    Parameters:
        auto: update without asking user.

    Returns:
        None
    '''

    outdated_modules = []

    # try-block to make sure pip is installed.
    try:
        print("\nChecking for outdated packages...")
        # Get a list of outdated modules
        outdated_modules = get_outdated_pkgs()

        if outdated_modules:
            # print list of modules
            for i, module in enumerate(outdated_modules):
                print('{:>3} - {:s}'.format(i+1, module))
            print(f"\nThere are {len(outdated_modules)} packages outdated.")

            if auto:
                print('-> Auto updating')
                update_packages()
                return

            # asking user to update all packages
            user = input("Would you like to update all of them? (y/n): ")
            if user.lower() in ['y', 'yes']:
                update_packages()
            else:  # asking user if they want to update any packages.
                user = input("Would you like to update any package? (y/n): ")
                if user.lower() in ['y', 'yes']:
                    specific_modules = input(
                        "Enter the packages you want to update (separated by commas): "
                    )
                    if specific_modules:
                        for module in specific_modules.split(','):
                            update_packages(module)
                else:
                    print("-> Skipped.\n")
        else:
            print('All packages are up to date!\n')

    except subprocess.CalledProcessError:
        print("Error: Failed to check for outdated modules.")
        exit('Pip may not be installed on your system.\n')


def update_packages(modules=None):
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
            package_count = len(packages_to_update)
            global UPDATED
            for i, package in enumerate(packages_to_update, 1):
                UPDATED.append(package)
                print(f'Package {i}/{package_count}:')
                subprocess.run(['pip', 'install', '--upgrade', package])
                print()

            print("\nUpdating packages complete!\n")

    except subprocess.CalledProcessError:
        print(f"Error: Failed to update modules.")


def show_updated_pkgs() -> None:
    '''
    Function to show updated packages.
    '''

    if len(UPDATED) > 0:
        user = input('Show updated packages? (y/n): ')

        if user.lower() in ['y', 'yes']:
            length = len(UPDATED)
            for i, package in enumerate(UPDATED, 1):
                print(f'{i:>3}/{length}: {package}')

    else:
        print("-> No packages have been updated.")


if __name__ == '__main__':
    '''
    Main Program function
    '''

    try:
        print("Welcome to the Python Package Updater!")

        # checking if user started script with 'auto' argument.
        auto = False
        if len(sys.argv) > 1:
            if sys.argv[1].lower() == 'auto':
                auto = True

        check_pip_update(auto=auto)
        check_outdated_pkgs(auto=auto)

        if auto is False:
            show_installed_pkgs()
            show_updated_pkgs()

        while True:
            user = input("\nEnter 'q' to quit program: ")
            if user.lower() in ['q', 'quit']:
                print("Program Terminated.\n")
                break

    except KeyboardInterrupt:
        print("Program Terminated.")
