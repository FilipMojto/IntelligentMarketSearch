
from config_paths import *
from AOSS.components.categorization import get_mapped_category


print(get_mapped_category(query_string_ID=41, mappings_file=CATEGORY_MAP_FILE['path'],
                    categories_file=CATEGORY_FILE['path']))

