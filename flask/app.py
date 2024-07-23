from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

def is_valid_search_term(search_term):
    # Ensure the input is alphanumeric and between 3 and 16 characters long
    if not re.match(r'^[a-zA-Z0-9_]{3,16}$', search_term):
        return False

    # Disallow simple XSS patterns (basic check)
    if re.search(r'<[^>]*>', search_term):
        return False

    # Simplified check for common SQL injection patterns
    sql_patterns = [
        r'(--|;|/\*|\*/| OR | AND )'
    ]
    for pattern in sql_patterns:
        if re.search(pattern, search_term, re.IGNORECASE):
            return False

    return True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_term = request.form['search']
        if is_valid_search_term(search_term):
            return render_template_string(RESULT_PAGE_TEMPLATE, search_term=search_term)
        else:
            return render_template_string(HOME_PAGE_TEMPLATE, error='Invalid input. Please enter a valid search term.')
    return render_template_string(HOME_PAGE_TEMPLATE)

HOME_PAGE_TEMPLATE = '''
<!doctype html>
<title>Search App</title>
<h1>Enter your search term</h1>
<form method=post>
    <input type=text name=search>
    <input type=submit value=Submit>
</form>
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
'''

RESULT_PAGE_TEMPLATE = '''
<!doctype html>
<title>Search Result</title>
<h1>Search Result</h1>
<p>Your search term: {{ search_term }}</p>
<a href="/">Go back to home page</a>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
