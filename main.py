import json
import re

filename = "swagger.json"

# Add collection names here
custom_collections = ["ItemsExample"]
directus_collections = ["Example"]

collections_to_leave = custom_collections + directus_collections

paths_to_leave = []
for collection in collections_to_leave:
    paths_to_leave.append(re.sub('([A-Z]{1})', r'/\1', collection).lower())

with open(filename) as json_data:
    data = json.load(json_data)
    tags = "tags"
    paths = "paths"
    schemas = "schemas"
    components = "components"

    tags_to_remove = []
    for tag in data[tags]:
        if tag['name'] not in collections_to_leave:
            tags_to_remove.append(tag)
    for tag_to_remove in tags_to_remove:
        data[tags].remove(tag_to_remove)

    for path in list(data[paths]):
        if path.lower().startswith(tuple(paths_to_leave)) is False:
            del data[paths][path]

    for schema in list(data[components][schemas]):
        if schema not in collections_to_leave:
            del data[components][schemas][schema]

with open("modified-" + filename, 'w') as f:
    json.dump(data, f, indent=4)
