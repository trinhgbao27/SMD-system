from website import create_app


app = create_app()

app.config['WTF_CSRF_CHECK_DEFAULT'] = False  # tạm tắt CSRF check

if __name__ == '__main__':
    app.run(debug=True)