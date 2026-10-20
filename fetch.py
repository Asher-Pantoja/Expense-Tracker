from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom

app = Flask(__name__)
app.secret_key = "flash message"
XML_FILE = 'userdata.xml'

def parse_xml(file):
    tree = ET.parse(file)
    return tree.getroot()

@app.route('/')
def index():
    try:
        root = parse_xml(XML_FILE)
        students = []
        expense_types = set()
        site_names = set()
        for user in root.findall('user'):
            student = [user.find(field).text for field in ['username', 'password', 'datetime', 'expense', 'site', 'product', 'quantity', 'price', 'totalprice']]

            date_string = user.find('datetime').text
            datetime_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            formatted_datetime = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
            student.append(formatted_datetime)

            students.append(student)
            expense_types.add(user.find('expense').text)
            site_names.add(user.find('site').text)

        selected_site = request.args.get('site_filter')
        selected_expense = request.args.get('expense_filter')
        search_query = request.args.get('search_query')
        selected_date = request.args.get('selected_date')
        
        if selected_expense:
            students = [student for student in students if student[3] == selected_expense]

        if selected_site:
            students = [student for student in students if student[4] == selected_site]

        if search_query:
            students = [student for student in students if search_query.lower() in student[5].lower()]  # Assuming product information is in index 5

        if selected_date:
            students = [student for student in students if selected_date in student[9]]

        order_by = request.args.get('order_by', default='asc')
        students.sort(key=lambda x: datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S'), reverse=(order_by == 'desc'))

        return render_template('webxml.html', students=students, expense_types=expense_types, site_names=site_names, expense_data=students)

    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('error.html')


def write_xml(root, file):
    tree = ET.ElementTree(root)
    tree.write(file, encoding='utf-8', xml_declaration=True)
    dom = xml.dom.minidom.parse(file)
    pretty_xml_data = dom.toprettyxml()
    lines = filter(lambda x: not x.isspace(), pretty_xml_data.split('\n'))
    pretty_xml_data = '\n'.join(lines)

    with open(file, 'w') as formatted_file:
        formatted_file.write(pretty_xml_data)


@app.route('/insert', methods=['POST'])
def insert():
    try:
        username = request.form['username']
        password = request.form['password']
        expense = request.form['expense']
        site = request.form['site']
        product = request.form['product']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        root = parse_xml(XML_FILE)
        new_user = ET.SubElement(root, 'user')
        ET.SubElement(new_user, 'username').text = username
        ET.SubElement(new_user, 'password').text = password
        ET.SubElement(new_user, 'expense').text = expense
        ET.SubElement(new_user, 'site').text = site
        ET.SubElement(new_user, 'product').text = product
        ET.SubElement(new_user, 'quantity').text = str(quantity)
        ET.SubElement(new_user, 'price').text = str(price)

        totalprice = quantity * price
        totalprice_text = "{:.2f}".format(totalprice)
        ET.SubElement(new_user, 'totalprice').text = totalprice_text

        write_xml(root, XML_FILE)
        flash('NOTE: User data inserted successfully', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"NOTE: An error occurred: {e}")
        flash('NOTE: Error occurred while inserting user data', 'error')
        return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    try:
        old_username = request.form['old_username']  
        new_username = request.form['new_username']  

        password = request.form['password']
        expense = request.form['expense']
        site = request.form['site']
        product = request.form['product']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        root = parse_xml(XML_FILE)
        for user in root.findall('user'):
            if user.find('username').text == old_username:
                user.find('username').text = new_username  
                user.find('password').text = password
                user.find('expense').text = expense
                user.find('site').text = site
                user.find('product').text = product
                user.find('quantity').text = str(quantity)
                user.find('price').text = str(price)

                totalprice = quantity * price
                totalprice_text = "{:.2f}".format(totalprice)
                user.find('totalprice').text = totalprice_text
                break

        write_xml(root, XML_FILE)
        flash('NOTE: User data updated successfully', 'success')
        return redirect(url_for('index'))
    except KeyError as e:
        flash(f'NOTE: Missing field in the form: {e}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('NOTE: Error occurred while updating user data', 'error')
        return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    try:
        username = request.form['username']
        print(f"Deleting user: {username}")

        tree = parse_xml(XML_FILE)
        root = parse_xml(XML_FILE)
        for user in root.findall('user'):
            if user.find('username').text == username:
                root.remove(user)
                break

        write_xml(root, XML_FILE)
        flash('NOTE: User data deleted successfully', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('NOTE: Error occurred while deleting user data', 'error')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
