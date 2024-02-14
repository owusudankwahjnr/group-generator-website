from flask import Blueprint, Flask, render_template, request, redirect, url_for
from .create_group import CreateGroupsFromCSV
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField, IntegerField, TextAreaField
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'


class SiteForm(FlaskForm):
    file = FileField("file")
    group_by = SelectField("generate Group By", choices=["Number of groups", "Number of people in a group"])
    text_area = TextAreaField("Text")
    number = IntegerField("Number:")
    submit = SubmitField("Submit")
    re_generate = SubmitField("Re-Generate Groups")
    go_home = SubmitField("Home")


views = Blueprint("views", __name__)
group = CreateGroupsFromCSV()
general_group_list = []
temp_group_list = []
group_total = 5
by_number_of_groups = False
sub_groups: dict[str, list] = {"": ['']}
file_path: str = ""


@views.route("/", methods=["POST", "GET"])
def home():
    global general_group_list, group_total, by_number_of_groups, file_path
    form = SiteForm()
    if form.validate_on_submit():
        file = form.file.data
        # print(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))
        file_path = f'group_generator/static/files/{file.filename}'

        general_group_list = group.convert_csv_or_xlsx_to_list(file_path)

        the_form = request.form
        group_total = int(the_form.get('number'))
        by_number_of_groups = False
        if the_form.get("group_by") == "Number of groups":
            by_number_of_groups = True

        return redirect(url_for('views.generate_groups'))

    return render_template("main.html", form=form)


@views.route("/preview", methods=["POST", "GET"])
def generate_groups():
    global sub_groups, general_group_list, group, file_path
    general_group_list = group.convert_csv_or_xlsx_to_list(file_path)
    # print(file_path)
    if by_number_of_groups:
        sub_groups = group.using_num_of_groups(general_group_list, group_total)
    else:
        sub_groups = group.using_num_of_people_in_groups(general_group_list, group_total)

    # print(general_group_list, group_total)

    # if request.method == "POST":
    #     if request.form["re_generate"] == "Re-Generate Groups":
    #         temp_group_list = group.convert_csv_or_xlsx_to_list(file_path)
    #
    #         if by_number_of_groups:
    #             sub_groups = group.using_num_of_groups(temp_group_list, group_total)
    #         else:
    #             sub_groups = group.using_num_of_people_in_groups(temp_group_list, group_total)

    return render_template("preview.html", sub_groups=sub_groups)
