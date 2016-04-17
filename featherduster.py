# I've been thinking about how we could build a module that creates a simple API for declaring transform+lint pipelines.

# potential pitfalls to avoid:
# - re-generating functions that can be re-used
# - holding weak references that undermine the low-memory generator approach

import types
import pdb

def NSA(f):
	"""Decorator for keeping an eye on things."""
	def wrap(*arg):
		print("calling", f, arg)
		ret = f(*arg)
		print("result", f, ret)
		return ret

	return wrap

def debug(f):
	"""Decorator for debugging things."""
	def wrap(*arg, **kwargs):
		return pdb.runcall(f, *arg, **kwargs)

	return wrap

class FeatherDuster(object):
	"""It slices, it dices, it lints..."""
	pipelines = data = lint = None

	def log(self, *arg):
		#return # uncomment to disable logspam
		print(self, *arg)

	def __init__(self):
		self.pipelines = []

	#@debug
	def chunk_by(self, chunker):
		"""
		Register new chunking function and return the next node in the pipeline.

		Args:
			chunker (callable): chunker(to_chunk) should return an iterator (preferably a generator) of chunks

		Returns:
			FeatherDuster instance to which each chunk will be published.
		"""

		self.log("chunk_by", chunker)
		child = self.__class__()

		#@NSA
		def chunk_stream(to_chunk):
			"""
			Generator to call child node with each chunk from chunker.

			Args:
				to_chunk: List or string; could probably standardize this somehow

			Yields:
				child.__call__(chunk)
			"""

			self.log("chunk_stream", to_chunk, self.__class__, child, child.__class__)
			for chunk in chunker(to_chunk):
				yield child(chunk)

		self.pipelines.append(chunk_stream)
		return child

	#@NSA
	def lint_with(self, linters):
		"""
		Set up linting function and return self for chaining.
		"""
		self.log("lint_with", linters)

		#@NSA
		def replace_lint(to_lint):
			"""Return result of passing chunk through each linter."""

			self.log("linting", to_lint, "with", self.__class__)
			return [linter(to_lint) for linter in linters]

		self.lint = replace_lint
		self.log("lint replaced", self.__class__, replace_lint)
		return self

	# new-style classes won't let us replace __call__ on a single object, so we need to just call something we can replace
	def __call__(self, payload):
		return self._you_used_to_call_me_on_my_lint_phone(payload)

	def _you_used_to_call_me_on_my_lint_phone(self, payload):
		"""
		Finalize the lint/chunk pipeline, then lint/chunk payload.

		Since user could add linters/chunkers in either order, we can't finalize the lint pipeline until call time. On first call, this method:
			- generates functions to implement the pipeline
			- replaces itself with one of these
			- runs the pipeline once and returns result
		"""
		self.log("__call__", payload)

		#@NSA
		def dust(chunks):
			"""Wrap a chunking function in a function that will run linters and the chunker."""
			self.log("dust", chunks)

			#@NSA
			def duster(unit):
				"""
				Lint the unit, then chunk it.

				Return isn't thought out yet.
				"""
				self.log("duster", self.lint, unit, "chunks", chunks)
				return [self.lint(unit), list(chunks(unit))]
			return duster

		# collapse existing pipeline definitions down into a re-usable list of functions
		if self.lint and not len(self.pipelines):
			# If there ARE linters and NO chunkers, we can just lint without building the pipeline
			return self.lint(payload)
		else:
			# wrap each chunker in the pipeline with a function that will run the linters
			self.pipelines = [dust(pipe) for pipe in self.pipelines]

		#@NSA
		def pipedream(data):
			"""Pipe *data* through each pipeline."""
			self.log("pipedream", data, self.pipelines)

			return [
				pipe(data) for pipe in self.pipelines
			]

		#@NSA
		def replacement(self, data):
			"""Feed each chunk of data into the pipelines."""
			self.log("replacement", data)
			# avoid breaking single string down into chars (for now, at least...)
			if isinstance(data, str):
				return pipedream(data)
			else:
				return [pipedream(x) for x in data]

		# replace with finalized pipeline
		self._you_used_to_call_me_on_my_lint_phone = types.MethodType(replacement, self)
		return replacement(self, payload)
