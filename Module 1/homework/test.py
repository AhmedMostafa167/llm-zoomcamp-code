import ingest
print(ingest.__file__)
lessons = ingest.load_lessons()
documents = ingest.format_lessons(lessons)
index = ingest>build_index(documents)

print(len(documents))