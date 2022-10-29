from chuml.models import node
from chuml.models.primitives import String

class Bookmark(node.Node):
	gen_attributes(locals(), {
		"name": String,
		"url": String,
	})

	def render_view(self):
		return f"<a href=\"{self.url}\">{self.name}</a>"

	def render_edit(self):
		return f"""
		<div>
			name: {self.name.render_edit()} <br/>
			url: {self.url.render_edit()} <br/>
		<div>
		"""