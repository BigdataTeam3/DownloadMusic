import tornado.ioloop
import tornado.web
import rethinkdb as r

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
	#conn = r.connect()
	#users = r.table('user').changes().run(conn)
	messages = ['one','two','three','four']
        self.render('first.html', messages = messages)

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", IndexHandler)
    ], autoreload=True)
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
