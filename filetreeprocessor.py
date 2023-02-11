import os
import re


class FilesFolderClass:
    def __init__(self,
                 target_path,
                 type_filter_mode,
                 file_type_targets=(),
                 check_mode=False,
                 folder_mode=False,
                 trim_mode=True,
                 multi_space_mode=True):
        paths_list = []
        nested_folders_list = []
        for current_dir, subdirs, files in os.walk(target_path):
            for filename in files:  # Appends all absolute paths of files
                relative_file_path = os.path.join(current_dir, filename)
                absolute_file_path = os.path.abspath(relative_file_path)
                paths_list.append(absolute_file_path)
            for folder in subdirs:  # Appends all folder paths
                folder_path = os.path.join(current_dir, folder)
                nested_folders_list.append([folder_path, folder])

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
        filtered_files_dict_list = []
        for full_path in filtered_path_list:
            path_part_dict = {}
            root_and_file_name = list(os.path.split(full_path))
            name_and_type = list(os.path.splitext(root_and_file_name[1]))
            path_part_dict["root"] = root_and_file_name[0]
            path_part_dict["name"] = name_and_type[0]
            path_part_dict["type"] = name_and_type[1]
            filtered_files_dict_list.append(path_part_dict)

        # Setting the variables as object properties
        self.target_path = target_path
        self.paths_list = paths_list
        self.nested_folders_list = nested_folders_list
        self.filtered_list = filtered_path_list
        self.filtered_dict_list = filtered_files_dict_list
        self.check_mode = check_mode
        self.folder_mode = folder_mode
        self.trim_mode = trim_mode
        self.multi_space_mode = multi_space_mode

    # ||||||||||||||||||||||||||||||||||||||||||||||
    # Basic functions to assist in cleaning up file and folder names
    # ||||||||||||||||||||||||||||||||||||||||||||||

    # Function replace double spaces with single spaces on strings, if feature is set to True for the object
    def multi_space_remover(self, string):
        if self.multi_space_mode:
            trimmed_string = ' '.join(string.split())
            return trimmed_string
        else:
            return string

    # Function to remove trailing and leading whitespace on strings, if feature is set to True for the object
    def trimmer(self, string):
        if self.trim_mode:
            trimmed_string = string.strip()
            return trimmed_string
        else:
            return string

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

        # Function to return the new path for each of the available options, used for both files and folders
        def return_regex_replacement(regex, string, target):
            if action_type == 'replace':  # Adds replacement for any regex matches
                return re.sub(regex, string, target)
            if action_type == 'prefix':  # Only adds prefix if regex matches
                if re.search(regex, target):
                    return string + target
                else:
                    return target
            if action_type == 'suffix':  # Only adds suffix if regex matches
                if re.search(regex, target):
                    return target + string
                else:
                    return target

        # Initialising lists containing paired lists with new and old paths for use in the rename_targets function
        new_old_file_paths = []
        new_old_folder_paths = []

        # |||||||||||||||
        # For files
        # ||||||||||||||||

        for a_dict in self.filtered_dict_list:
            # Getting dict values as simple vars
            root = a_dict["root"]
            name = a_dict["name"]
            file_type = a_dict["type"]
            iterated_file_regex_changes = []

            # Running each of the regexes in order on the name field, each one acting upon the results of the last
            for index, a_regex_tuple in enumerate(regex_target_list):
                action_type = a_regex_tuple[0]
                regex_string = a_regex_tuple[1]
                replacement_string = a_regex_tuple[2]

                # Running the regex on the most recent iteration
                if index == 0:
                    new_name_v1 = return_regex_replacement(regex_string, replacement_string, name)
                    new_name_v2 = self.multi_space_remover(new_name_v1)
                    new_name_final = self.trimmer(new_name_v2)
                    iterated_file_regex_changes.append(new_name_final)
                else:
                    iterated_new_name_v1 = return_regex_replacement(regex_string, replacement_string,
                                                                    iterated_file_regex_changes[index - 1])
                    iterated_new_name_v2 = self.multi_space_remover(iterated_new_name_v1)
                    iterated_new_name_final = self.trimmer(iterated_new_name_v2)
                    iterated_file_regex_changes.append(iterated_new_name_final)

            # Getting the last iteration appended to the list
            final_iteration = iterated_file_regex_changes.pop()

            # Appending the old and new paths for a single file to a list
            single_path_list = []

            old_path = os.path.join(root, (name + file_type))
            single_path_list.append(old_path)

            new_path = os.path.join(root, (final_iteration + file_type))
            single_path_list.append(new_path)

            new_old_file_paths.append(single_path_list)

        # |||||||||||||||
        # For folders
        # ||||||||||||||||

        for folder_pair in self.nested_folders_list:
            abs_folder_path = folder_pair[0]
            folder_name = folder_pair[1]
            iterated_folder_regex_changes = []

            # Running each of the regexes in order on the name field, each one acting upon the results of the last
            for index, a_regex_tuple in enumerate(regex_target_list):
                action_type = a_regex_tuple[0]
                regex_string = a_regex_tuple[1]
                replacement_string = a_regex_tuple[2]

                # Running the regex on the most recent iteration
                if index == 0:
                    new_folder_name_v1 = return_regex_replacement(regex_string, replacement_string, folder_name)
                    new_folder_name_v2 = self.multi_space_remover(new_folder_name_v1)
                    new_folder_name_final = self.trimmer(new_folder_name_v2)
                    iterated_folder_regex_changes.append(new_folder_name_final)
                else:
                    iterated_new_folder_name_v1 = return_regex_replacement(regex_string, replacement_string,
                                                                        iterated_folder_regex_changes[index - 1])
                    iterated_new_folder_name_v2 = self.multi_space_remover(iterated_new_folder_name_v1)
                    iterated_new_folder_name_final = self.trimmer(iterated_new_folder_name_v2)
                    iterated_folder_regex_changes.append(iterated_new_folder_name_final)

            # Getting the last iteration appended to the list
            final_folder_iteration = iterated_folder_regex_changes.pop()

            # Creating the replacement name
            after_last_slash = r'([^\\]+$)'  # regex for everything after the last slash
            changed_folder_path = re.sub(after_last_slash, final_folder_iteration, abs_folder_path)

            # Creating the pair list which will be passed to the full list for processing
            single_folder_path_list = [abs_folder_path, changed_folder_path]

            # Appending that to the big overall nested list
            new_old_folder_paths.append(single_folder_path_list)

        # Checking the status of folder mode, and if True, making the changes to both lists of old / new pairs
        if self.folder_mode:
            self.rename_targets(new_old_file_paths + new_old_folder_paths)  # Combines lists
        else:
            self.rename_targets(new_old_file_paths)
