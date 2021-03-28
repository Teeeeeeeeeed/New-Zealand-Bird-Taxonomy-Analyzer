import csv

def get_longest_common_name(all_common_names):
    name_list = all_common_names.split("|")
    longest = ""
    longest_count = 0
    for name in name_list:
        words = name.split()
        word_count = 0
        for word in words:
            word_count += len(word)
            
        if word_count > longest_count:
            longest = name
            longest_count = word_count
    if longest_count == 0:
        return None
    else:
        return longest

def get_classification_hierarchy(classification_ranks, classifications):
    classification_ranks = classification_ranks.split("|")
    classifications = classifications.split("|")
    if len(classification_ranks) != len(classifications):
        print("ERROR: Invalid input, classification ranks do not match classifications!")
        return []

    paired_classifications = []
    for num in range(0, len(classifications)):
        paired_classifications.append((classification_ranks[num], classifications[num]))
    return paired_classifications

def get_biostatus(biostatus_string):
    biostatus = ["Endemic", "Non-endemic", "Exotic", "Indigenous"]
    biostatus_string = biostatus_string.split("|")
    for entry in biostatus_string:
        if entry in biostatus:
            return entry
    return "N/A"

class Ave:
    def __init__(self, scientific_name, common_name, biostatus, classification_hierarchy):
        self.__scientific_name = scientific_name
        self.__common_name = common_name
        self.__biostatus = biostatus
        self.__classification_hierarchy = classification_hierarchy

    def get_scientific_name(self):
        return self.__scientific_name

    def get_common_name(self):
        return self.__common_name

    def get_biostatus(self):
        return self.__biostatus

    def get_classification_hierarchy(self):
        return self.__classification_hierarchy

    def __str__(self):
        return "{}, Status = {}".format(self.get_common_name(), self.get_biostatus())

    def __repr__(self):
        return "Ave<{}>".format(self.get_scientific_name())
    
#Less than comparison for object Ave
    def __lt__(self, other):
        if self.get_scientific_name() < other.get_scientific_name():
            return True
        else:
            return False

#Equal comparison
    def __eq__(self, other):
        if self.get_scientific_name() == other.get_scientific_name() and self.get_common_name() == other.get_common_name() and self.get_biostatus() == other.get_biostatus() and self.get_classification_hierarchy() == other.get_classification_hierarchy():
            return True
        else:
            return False

#finds the actual class given a rank
    def find_in_classification_hierarchy(self, classification_rank):
        for classes in self.__classification_hierarchy:
            if classes[0] == classification_rank:
                return classes[1]
        return None

#finds and returns the lowest class
    def lowest_classification_rank(self):
        return (self.get_classification_hierarchy())[0][0]

#Opens csv file and returns a list of Ave objects
class BirdDatasetReader:
    def __init__(self, filename):
        self.__csv_filename = filename
    
    def read_birds_dataset(self):
        try:
            csvfile = open(self.__csv_filename, mode = 'r')
            csv_dict_reader = csv.DictReader(csvfile)
            index = 1
            list_of_ave = []
            for row in csv_dict_reader:
                index += 1
                if len(row['VernacularNamesForScientific']) == 0:
                    ave = Ave(row['ScientificName'], row['ScientificName'],
                    get_biostatus(row['Biostatus']), get_classification_hierarchy(row['ClassificationRanks'], row['Classification']))
                    list_of_ave.append(ave)
                    
                else:
                    ave = Ave(row['ScientificName'] , get_longest_common_name(row['VernacularNamesForScientific']), get_biostatus(row['Biostatus']),
                    get_classification_hierarchy(row['ClassificationRanks'], row['Classification']))
                    list_of_ave.append(ave)
            csvfile.close()
            return list_of_ave
        except FileNotFoundError:
            print("ERROR: File '{}' not found!".format(self.__csv_filename))
            return []
        
def consistency_check(a_list_of_aves):
    index = 0
    pass_check = 1
    for aves in a_list_of_aves:
        index += 1
        aves_check = aves.find_in_classification_hierarchy(aves.lowest_classification_rank())
        if aves.get_scientific_name() == aves_check:
            pass
        else:
            print("Inconsistency found for bird #{} in the list! {} vs {}".format(index, aves.get_scientific_name(), aves_check))
            pass_check = 0
    if pass_check == 0:
        return False
    else:
        return True

def print_histogram_of_biostatuses(list_of_aves):
    type_of_entries = []
    for aves in list_of_aves:
        if aves.get_biostatus() not in type_of_entries:
            type_of_entries.append(aves.get_biostatus())
    print("Histogram of biostatus entries:")
    for entry in sorted(type_of_entries):
        count = 0
        for aves in list_of_aves:
            if entry == aves.get_biostatus():
                count += 1
        print("{:<12}: {}".format(entry, count))

def get_birds_with_specific_classification(list_of_aves, classification_rank, classification):
    aves_with_same_classification = []
    for aves in list_of_aves:
        for classes in aves.get_classification_hierarchy():
            if classes[0] == classification_rank and classes[1] == classification:
                aves_with_same_classification.append(aves)
    return aves_with_same_classification
    
def find_bird_by_scientific_name_binary_search(sorted_list_of_aves, scientific_name):
    count = 0
    max_index = len(sorted_list_of_aves)-1
    min_index = 0
    while (min_index <= max_index):
        count += 1
        mid_index = int((max_index+min_index)//2)
        if (sorted_list_of_aves[mid_index]).get_scientific_name() == scientific_name:
            return (sorted_list_of_aves[mid_index], count)
        elif sorted_list_of_aves[mid_index].get_scientific_name() < scientific_name:
            min_index = mid_index+1
        elif sorted_list_of_aves[mid_index].get_scientific_name() > scientific_name:
            max_index = mid_index-1
    return (None, 0)

import unittest

class TestBirdsMethods(unittest.TestCase):

    def test_0_read_csvfile(self):
        csv_filename = 'NZOR-BirdsTaxonomicExcerpt_15only.csv'
        reader = BirdDatasetReader(csv_filename)
        all_aves = reader.read_birds_dataset()
        self.assertEqual(repr(all_aves), "[Ave<Callaeas cinerea>, Ave<Hirundapus>, Ave<Leucocarbo colensoi>, Ave<Egretta alba>, Ave<Vanellus miles>, Ave<Thalasseus>, Ave<Anthus novaeseelandiae>, Ave<Callaeas>, Ave<Rallus pectoralis muelleri>, Ave<Procellaria>, Ave<Emeidae>, Ave<Puffinus puffinus puffinus>, Ave<Phalaropus fulicarius>, Ave<Porzana>, Ave<Anas>]")

    def test_1_find_all_birds(self):
        csv_filename = 'NZOR-BirdsTaxonomicExcerpt.csv'
        reader = BirdDatasetReader(csv_filename)
        all_aves = reader.read_birds_dataset()
        all_aves_sorted = sorted(all_aves)
        largest_number_of_search_steps = -1000
        smallest_number_of_search_steps = 1000
        index = 0
        for ave in all_aves:
            bird, nr_search_steps = find_bird_by_scientific_name_binary_search(all_aves_sorted, ave.get_scientific_name())
            index += 1
            if nr_search_steps > largest_number_of_search_steps:
                largest_number_of_search_steps = nr_search_steps
            if nr_search_steps < smallest_number_of_search_steps:
                smallest_number_of_search_steps = nr_search_steps
        self.assertEqual(largest_number_of_search_steps, 11)
        self.assertEqual(smallest_number_of_search_steps, 1)

if __name__ == "__main__":
    unittest.main(verbosity=0)
