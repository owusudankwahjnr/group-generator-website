import random
import pandas as pd


class CreateGroupsFromCSV:

    # def __init__(self):
    #     self.use_num_of_groups: bool = False
    #     self.use_num_of_people_in_group: bool = True

    @staticmethod
    def convert_csv_or_xlsx_to_list(file_path: str):
        df = pd.read_excel(file_path)
        file_to_dict = df.to_dict()
        # print(file_to_dict)
        a_list = []
        for key in file_to_dict:

            for index in file_to_dict[key]:
                a_list.append(file_to_dict[key][index])
        print(a_list)
        return a_list

    @staticmethod
    def using_num_of_people_in_groups(csv_list: list, members_in_group: int):
        dict_for_groupings = {}
        remainder = len(csv_list) % members_in_group
        group_num = 1

        while len(csv_list) > 0:
            group_name = f"Group {group_num}"

            if remainder >= len(csv_list):
                dict_for_groupings[group_name] = [value for value in csv_list]
                len(dict_for_groupings[group_name])

            else:
                dict_for_groupings[group_name] = []
                for counter in range(members_in_group):
                    member = csv_list.pop(csv_list.index(random.choice(csv_list)))
                    dict_for_groupings[group_name].append(member)

            if len(dict_for_groupings[group_name]) < members_in_group:
                numbers_left = members_in_group - len(csv_list)
                for num in range(numbers_left):
                    dict_for_groupings[group_name].append("NaN")

                csv_list = []

            group_num += 1

        return dict_for_groupings

    @staticmethod
    def using_num_of_groups(csv_list: list, num_of_groups):
        dict_for_groupings = {}
        group_num = 1
        num_of_members_in_group = int(len(csv_list) / num_of_groups)
        members_remaining = len(csv_list) % num_of_groups

        while len(csv_list) > 0:
            group_name = f"Group {group_num}"

            if members_remaining == len(csv_list):
                for key in dict_for_groupings:
                    if len(csv_list) > 0:
                        member = csv_list.pop(csv_list.index(random.choice(csv_list)))
                        dict_for_groupings[key].append(member)
                csv_list = []
            else:
                dict_for_groupings[group_name] = []
                for num in range(num_of_members_in_group):
                    # print(num_of_members_in_group)
                    member = csv_list.pop(csv_list.index(random.choice(csv_list)))
                    dict_for_groupings[group_name].append(member)


            group_num += 1

        print(dict_for_groupings)
        return dict_for_groupings

    @staticmethod
    def convert_text_input_to_list(user_text_input: str):
        a_list = user_text_input.split(",")
        return a_list
