import os
import re


class FilesFolderClass:
    def __init__(self, target_path, type_filter_mode, file_type_targets=(), check_mode=False):
        paths_list = []
        for current_dir, subdirs, files in os.walk(target_path):
            for filename in files:
                relative_path = os.path.join(current_dir, filename)
                absolute_path = os.path.abspath(relative_path)
                paths_list.append(absolute_path)

        filtered_path_list = []
        # If we want to look at all file types
        if type_filter_mode == 'all':
            filtered_path_list = paths_list
        # If we only want to look at specific file types
        elif type_filter_mode == 'include':
            for file_path in paths_list:
                if file_path.endswith(file_type_targets):
                    filtered_path_list.append(file_path)
        # If we want to look at all file types except those specified
        elif type_filter_mode == 'exclude':
            for file_path in paths_list:
                if not file_path.endswith(file_type_targets):
                    filtered_path_list.append(file_path)

        # Creating a list of dictionaries containing the root, name and type of filtered paths
        filtered_dict_list = []
        for full_path in filtered_path_list:
            path_part_dict = {}
            root_and_file_name = list(os.path.split(full_path))
            name_and_type = list(os.path.splitext(root_and_file_name[1]))
            path_part_dict["root"] = root_and_file_name[0]
            path_part_dict["name"] = name_and_type[0]
            path_part_dict["type"] = name_and_type[1]
            filtered_dict_list.append(path_part_dict)

        # Setting the variables as object properties
        self.target_path = target_path
        self.paths_list = paths_list
        self.filtered_list = filtered_path_list
        self.filtered_dict_list = filtered_dict_list
        self.check_mode = check_mode

    # ||||||||||||||||||||||||||||||||||||||||||||||
    # Function which performs the rename action, and is called in the regex_rename function
    # Uses the dictionary structure created in the object initialisation
    # ||||||||||||||||||||||||||||||||||||||||||||||
    def rename_targets(self, nested_old_new_paths_list):
        # Set check_mode to True if you want to review changes as a text output before changing
        old_new_with_changes = []  # List where we store old vs new paths which are different
        total_count = len(nested_old_new_paths_list)
        for a_list in nested_old_new_paths_list:
            if a_list[0] != a_list[1]:  # Check if the old and new paths are different
                old_new_with_changes.append(a_list)  # If they are different add them to the list
        change_count = len(old_new_with_changes)
        print('%d files to change out of %d total files' % (change_count, total_count))
        print('')
        for old_new_pair in old_new_with_changes:
            print(old_new_pair[0] + ' | Changes to...')
            print(old_new_pair[1])
            print('')

        # Inputs accepted by the checking mode
        yes_inputs = ('Yes', 'yes', 'y', 'Y')
        no_inputs = ('No', 'no', 'n', 'N')
        valid_inputs = yes_inputs + no_inputs  # The full list of accepted inputs

        if change_count > 0:  # Only run code below if there are changes to make
            # Loops until a valid input is received
            while True:
                if not self.check_mode:
                    print("Check mode is off - proceeding without further input")
                    print('')
                    while_input = 'Yes'
                    break
                print('')
                print("Proceed? - Y/N")
                while_input = input()
                if while_input in [str(x) for x in valid_inputs]:
                    break
                else:
                    print('Input must be one of %s, try again:' % (str(valid_inputs)))
                    continue

            # Renames the files if the input is affirmative
            if while_input in yes_inputs:
                for old_new_pair in old_new_with_changes:
                    try:
                        os.rename(old_new_pair[0], old_new_pair[1])
                        print("SUCCESS")
                        print(old_new_pair[0])
                        print(">>> renamed as >>>")
                        print(old_new_pair[1])
                        print('')
                    except Exception as e:
                        print("FAILURE")
                        print(old_new_pair[0])
                        print(">>> NOT renamed as >>>")
                        print(old_new_pair[1])
                        print('')
                        print("Error was:" + str(e))
                        continue
            else:
                print('No changes made')
        else:
            print("No changes to make, try again")
            print("")

    # ||||||||||||||||||||||||||||||||||||||||||||||
    # Method which generates new file names recursively using a list of regex actions
    # It makes the changes using the rename_targets function above
    # ||||||||||||||||||||||||||||||||||||||||||||||

    def regex_rename(self, regex_target_list):
        # Pass a list containing tuples with regex / replacement pairs to the regex_sub_list variable
        nested_lists_new_old_paths = []

        for a_dict in self.filtered_dict_list:

            # Getting dict values as simple vars
            root = a_dict["root"]
            name = a_dict["name"]
            file_type = a_dict["type"]
            iterated_regex_changes = []

            # Running each of the regexes in order on the name field, each one acting upon the results of the last
            for index, a_regex_tuple in enumerate(regex_target_list):
                action_type = a_regex_tuple[0]
                regex_string = a_regex_tuple[1]
                replacement_string = a_regex_tuple[2]

                def generate_new_path(regex, string, target):
                    if action_type == 'replace':
                        return re.sub(regex, string, target)
                    if action_type == 'prefix':
                        return string + target
                    if action_type == 'suffix':
                        return target + string

                # Running the regex on the most recent iteration
                if index == 0:
                    new_name = generate_new_path(regex_string, replacement_string, name)
                    iterated_regex_changes.append(new_name)
                else:
                    iterated_new_name = generate_new_path(regex_string, replacement_string,
                                                          iterated_regex_changes[index - 1])
                    iterated_regex_changes.append(iterated_new_name)

            # Getting the last iteration appended to the list
            final_iteration = iterated_regex_changes.pop()

            # Appending the old and new paths for a single file to a list
            single_path_list = []

            old_path = os.path.join(root, (name + file_type))
            single_path_list.append(old_path)

            new_path = os.path.join(root, (final_iteration + file_type))
            single_path_list.append(new_path)

            nested_lists_new_old_paths.append(single_path_list)

        # Passing the nested list of old and new paths to the function which will rename the files
        self.rename_targets(nested_lists_new_old_paths)
