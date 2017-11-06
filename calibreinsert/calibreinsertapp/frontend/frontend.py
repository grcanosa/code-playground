import os
import flask
import flask_wtf
import flask_wtf.file
#from flask import Flask, render_template
import flask_uploads #import UploadSet, configure_uploads, IMAGES, patch_request_class
#from flask_wtf import FlaskForm
#from flask_wtf.file import FileField, FileRequired, FileAllowed
#from wtforms import SubmitField
import wtforms
import frontend.bookform as bookform
import bookanalyzer

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_BOOKS_DEST'] = "/tmp/"

books = flask_uploads.UploadSet('books', tuple(["epub"]))
flask_uploads.configure_uploads(app, books)
flask_uploads.patch_request_class(app)  # set maximum file size, default is 16MB


class UploadForm(flask_wtf.FlaskForm):
    book = flask_wtf.file.FileField(validators=[flask_wtf.file.FileAllowed(books, u'Only .epub files!'), flask_wtf.file.FileRequired(u'File was empty!')])
    submit = wtforms.SubmitField(u'Upload')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    file_url = None
    file_path= None
    if form.validate_on_submit():
        filename = books.save(form.book.data)
        file_url = books.url(filename)
        file_path = books.path(filename)
        mybook = bookanalyzer.BookAnalyzer()
        res = mybook.get_epub_info(file_path)
        print(res)
        f_book = bookform.BookForm()
        f_book.ftitle.data = res["title"]
        f_book.fauthor.data = res["creator"]
    return flask.render_template('upload.html', form=form,bookform = f_book, file_url=file_url,file_path=file_path)


if __name__ == '__main__':
    app.run()
