from featherduster import FeatherDuster
#from featherduster import NSA, debug

# junk demonstration functions.
#@NSA
def find_document(wert):
	return wert.split("==")

#@NSA
def find_chapter(wert):
	return wert.split(".")

#@NSA
def find_word(wert):
	return wert.split(" ")

#@NSA
def naive_docs_linter(wert):
	return True

#@NSA
def naive_doc_linter(wert):
	return True

#@NSA
def contains_syrup(wert):
	return wert.find("syrup") != -1

#@NSA
def ends_with_period(wert):
	return wert.endswith(".")

# declare the pipeline
documents = FeatherDuster()
documents.lint_with([naive_docs_linter])
document = documents.chunk_by(find_document)
document.lint_with([naive_doc_linter])
chapter = document.chunk_by(find_chapter)
chapter.lint_with([contains_syrup])

# a single pipeline can have more than one descendant
word = document.chunk_by(find_word)
word.lint_with([ends_with_period])

test = documents(["This is document 1. It has three sentences. It is ridiculously simple.==This is document 2. It is full of simple syrup."])

# could also support a nested/chain syntax, (but I suspect it would be worth taking a fresh swing at the API to optimize for that scenario):
# documents = FeatherDuster() \
# 	.lint_with(documents_linter_list) \
# 	.chunk_by(find_document) \
# 		.lint_with(document_linter_list) \
# 		.chunk_by(find_chapter) \
# 			.lint_with(chapter_linter_list)

# documents(...)
