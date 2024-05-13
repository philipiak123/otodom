from flask import Flask, render_template_string
import csv

app = Flask(__name__)

@app.route('/')
def index():
    # Wczytaj dane z pliku CSV
    data = []
    with open('baza.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    
    # Szablon HTML
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dane z pliku CSV</title>
    </head>
    <body>
        <h1>Dane z pliku CSV</h1>
        <table border="1">
            <tr>
                <th>Column1</th>
                <th>Column2</th>
                <!-- Kontynuuj w zależności od liczby kolumn w pliku CSV -->
            </tr>
            {% for row in data %}
                <tr>
                    <td>{{ row['nazwa'] }}</td>
                    <td>{{ row['cena'] }}</td>
                    <!-- Kontynuuj w zależności od liczby kolumn w pliku CSV -->
                </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    # Renderuj szablon HTML z danymi z pliku CSV
    return render_template_string(template, data=data)

if __name__ == '__main__':
    app.run(debug=True)
