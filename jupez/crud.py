from flask import Blueprint, current_app, request, render_template, redirect, url_for
from . import mongodb, storage

crud = Blueprint('crud', __name__)


def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info("Uploaded file %s as %s.", file.filename, public_url)

    return public_url


@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token.encode('utf-8')

    jupes, next_page_token = mongodb.list(cursor=token)

    return render_template("list.html", jupes=jupes, next_page_token=next_page_token)


@crud.route("/<id>")
def view(id):
    jupe = mongodb.read(id)
    return render_template("view.html", jupe=jupe)


@crud.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        image_url = upload_image_file(request.files.get('image'))
        if image_url:
            data['imageUrl'] = image_url

        jupe = mongodb.create(data)
        return redirect(url_for('.view', id=jupe['id']))

    return render_template('form.html', action='Add', jupe={})


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    jupe = mongodb.read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        image_url = upload_image_file(request.files.get('image'))
        if image_url:
            data['imageUrl'] = image_url

        jupe = mongodb.update(data, id)

        return redirect(url_for('.view', id=jupe['id']))

    return render_template("form.html", action="Edit", jupe=jupe)


@crud.route("/<id>/delete")
def delete(id):
    mongodb.delete(id)
    return redirect(url_for('.list'))