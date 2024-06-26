from pear_admin import create_app
# from gevent import monkey

# monkey.patch_all(thread=False)
app = create_app()

if __name__ == "__main__":

    app.run()
