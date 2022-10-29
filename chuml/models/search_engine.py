from chuml.utils import db
from chuml.models.primitives import Integer, String
from chuml.models import node

class SearchEngine(node.Node):
	gen_attributes(locals(), {
		"key": String,
		"url": String,
		"search": String,
	})

	def render_view(self):
		return f"""search engine : <br />
			<b>{ self.key.render_view() }</b> -> { self.url.render_view() } <br />
			<b>{ self.key.render_view() } {'{'}query{'}'} -> { self.search.render_view() }
		"""