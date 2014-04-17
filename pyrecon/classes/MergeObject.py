class MergeObject:
	def __init__(self, *args, **kwargs):
		# Series to be merged
		self.series1 = None
		self.series2 = None

		# Series merge handlers
		self.series_attributes = None
		self.series_contours = None
		self.series_zcontours = None

		# Section merge handlers
		self.section_attributes = None
		self.section_images = None
		self.section_contours = None

		# Merge completion
		self.mergedSeries = None
		self.output_directory = None

		processArguments()

	def processArguments(self, *args, **kwargs):
		'''Process given arguments.'''
		return


	def run(self):
		'''Run mergeTool with the handler functions found in self'''
		return

	def save(self):
		'''Save the current <mergedSeries> to <output_directory>'''
		return

	def set(self, attribute, newAttribute):
		'''Set state of <attribute> to <newAttribute>'''
		return

	def get(self, attribute):
		'''Return current state of <attribute>'''
		return

